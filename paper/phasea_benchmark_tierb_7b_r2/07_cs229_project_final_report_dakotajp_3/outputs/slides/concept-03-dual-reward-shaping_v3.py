from manim import *
import numpy as np

class DualRewardShaping(Scene):
    def construct(self):
        # 1. Setup Environment
        board = Rectangle(width=10, height=6, color=GREY).set_stroke(opacity=0.5)
        target_zone = Circle(radius=1.2, color=GREEN, fill_opacity=0.2).shift(RIGHT * 4)
        target_label = Text("Target", font_size=20, color=GREEN).next_to(target_zone, UP)
        
        # Create blue pegs
        pegs = VGroup(*[Dot(radius=0.15, color=BLUE) for _ in range(6)])
        pegs.arrange_in_grid(2, 3, buff=0.5).shift(LEFT * 4)
        
        # 2. Centroid and Visual Indicators
        centroid = Dot(color=RED)
        centroid.move_to(pegs.get_center())
        
        centroid_label = Text("Centroid", color=RED, font_size=18)
        centroid_label.next_to(centroid, UP, buff=0.1)
        
        # Line from Centroid to Target (using Line instead of DashedLine)
        dist_line = Line(centroid.get_center(), target_zone.get_center(), color=YELLOW)
        
        # 3. Reward Logic and Counter
        reward_counter = MathTex("R = 0.00").to_edge(UP)
        
        self.add(board, target_zone, target_label, pegs, centroid, centroid_label, dist_line, reward_counter)
        
        # 4. Define Updaters using functions instead of lambdas to avoid identifier errors
        def update_centroid_pos(mob):
            mob.move_to(pegs.get_center())
            
        def update_centroid_label(mob):
            mob.next_to(centroid, UP, buff=0.1)
            
        def update_dist_line(mob):
            start = centroid.get_center()
            end = target_zone.get_center()
            new_line = Line(start, end, color=YELLOW)
            mob.become(new_line)
            
        def update_reward_text(mob):
            # Calculate pegs in target zone
            target_pos = target_zone.get_center()
            pegs_in = 0
            for p in pegs:
                dist = np.linalg.norm(p.get_center() - target_pos)
                if dist < 1.2:
                    pegs_in += 1
            
            # Distance from centroid to target
            c_dist = np.linalg.norm(pegs.get_center() - target_pos)
            
            # Formula: R = (pegs_in)^2 + 5 * (dist)^-1
            w1, w2 = 1.0, 5.0
            val = w1 * (pegs_in**2) + w2 * (1.0 / max(c_dist, 0.1))
            
            # Update the text
            new_math = MathTex("R = " + "{:.2f}".format(val)).to_edge(UP)
            mob.become(new_math)

        # Attach updaters
        centroid.add_updater(update_centroid_pos)
        centroid_label.add_updater(update_centroid_label)
        dist_line.add_updater(update_dist_line)
        reward_counter.add_updater(update_reward_text)
        
        self.wait(1)

        # 5. Animation: Movement sequence
        # Move the entire group forward to show distance reward
        self.play(pegs.animate.shift(RIGHT * 3.5), run_time=3)
        self.wait(0.5)

        # Move individual pegs into the target zone to show piece-count reward
        for i in range(len(pegs)):
            # Distribute pegs inside the circle
            angle = (i / len(pegs)) * 2 * np.pi
            r_offset = 0.5
            target_pos = target_zone.get_center() + np.array([
                r_offset * np.cos(angle), 
                r_offset * np.sin(angle), 
                0
            ])
            
            # Squared Bonus pop-up
            bonus_val = i + 1
            bonus_text = MathTex(str(bonus_val) + "^2", color=GREEN).scale(0.8)
            bonus_text.next_to(pegs[i], UP, buff=0.1)
            
            self.play(
                pegs[i].animate.move_to(target_pos),
                FadeIn(bonus_text, shift=UP * 0.3),
                run_time=0.8
            )
            self.play(FadeOut(bonus_text), run_time=0.2)

        self.wait(2)