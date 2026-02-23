from manim import *
import numpy as np

class DualRewardShaping(Scene):
    def construct(self):
        # 1. Setup the Scene
        target_zone = Circle(radius=1.0, color=RED).shift(RIGHT * 4)
        target_label = Text("Target Zone", color=RED).scale(0.4).next_to(target_zone, UP)
        
        # 2. Create the Pegs
        pegs = VGroup(
            Dot(LEFT * 4 + UP * 1.2, color=BLUE),
            Dot(LEFT * 4, color=BLUE),
            Dot(LEFT * 4 + DOWN * 1.2, color=BLUE)
        )
        
        # 3. Initialize Centroid and Visuals
        centroid = Dot(color=YELLOW)
        # Initial position
        centroid.move_to(sum([p.get_center() for p in pegs]) / 3)
        
        centroid_text = Text("Centroid", color=YELLOW).scale(0.3)
        
        # Use simple Line instead of DashedLine to avoid compilation errors
        dist_line = Line(centroid.get_center(), target_zone.get_center(), color=WHITE)
        
        # Formula and Counter using MathTex
        reward_label = MathTex("R = 0.00").to_edge(UP)
        
        # 4. Define Updaters (Manual replacement for always_redraw)
        def update_centroid(m):
            avg_pos = sum([p.get_center() for p in pegs]) / 3
            m.move_to(avg_pos)
            
        def update_centroid_text(m):
            m.next_to(centroid, DOWN, buff=0.1)
            
        def update_line(m):
            m.put_start_and_end_on(centroid.get_center(), target_zone.get_center())
            
        def update_reward(m):
            # Calculate values for the reward formula
            p_centers = [p.get_center() for p in pegs]
            avg_pos = sum(p_centers) / 3
            dist = np.linalg.norm(avg_pos - target_zone.get_center())
            
            # Count pegs within the target zone
            pegs_in = 0
            for pos in p_centers:
                if np.linalg.norm(pos - target_zone.get_center()) < 1.05:
                    pegs_in += 1
            
            # Formula: R = w1 * pegs_in^2 + w2 * (1/dist)
            w1, w2 = 1.0, 5.0
            r_val = w1 * (pegs_in**2) + w2 * (1.0 / max(dist, 0.1))
            
            # Update the display
            new_tex = MathTex("R = " + "{:.2f}".format(r_val)).to_edge(UP)
            m.become(new_tex)

        # Add updaters to the objects
        centroid.add_updater(update_centroid)
        centroid_text.add_updater(update_centroid_text)
        dist_line.add_updater(update_line)
        reward_label.add_updater(update_reward)

        self.add(target_zone, target_label, pegs, centroid, centroid_text, dist_line, reward_label)
        self.wait(1)

        # 5. Animation Loop
        # Move pegs one by one to the target zone
        destinations = [
            target_zone.get_center() + UP * 0.4,
            target_zone.get_center(),
            target_zone.get_center() + DOWN * 0.4
        ]
        
        for i in range(len(pegs)):
            # Animate peg movement
            self.play(
                pegs[i].animate.move_to(destinations[i]),
                run_time=2
            )
            
            # Show the Squared Bonus popup
            bonus_val = (i + 1)**2
            bonus_text = MathTex(str(i+1) + "^2", color=GREEN).scale(0.8).next_to(pegs[i], UP)
            
            self.play(FadeIn(bonus_text, shift=UP * 0.2), run_time=0.4)
            self.play(FadeOut(bonus_text), run_time=0.4)
            self.wait(0.5)

        self.wait(2)