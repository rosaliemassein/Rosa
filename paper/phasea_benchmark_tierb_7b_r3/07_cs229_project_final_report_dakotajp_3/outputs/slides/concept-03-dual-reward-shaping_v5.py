from manim import *
import numpy as np

class DualRewardShaping(Scene):
    def construct(self):
        # 1. Setup Board and Environment
        board = Rectangle(height=6, width=10, color=GREY).set_fill(BLACK, opacity=1)
        target_zone = Rectangle(height=4, width=2, color=GREEN).set_fill(GREEN, opacity=0.2)
        target_zone.move_to(RIGHT * 3.5)
        target_label = Text("Goal Zone", font_size=20, color=GREEN).next_to(target_zone, UP)
        self.add(board, target_zone, target_label)

        # 2. Place blue pegs in a cluster
        pegs = VGroup(*[Circle(radius=0.15, color=BLUE, fill_opacity=0.8) for _ in range(5)])
        pegs.arrange_in_grid(rows=2, cols=3, buff=0.4).move_to(LEFT * 3)
        self.play(Create(pegs))

        # 3. Initial Centroid and Connection Line
        # We compute the centroid manually to avoid restricted ValueTrackers/Updaters
        def get_centers(group):
            return [p.get_center() for p in group]
        
        curr_centers = get_centers(pegs)
        centroid_pos = np.mean(np.array(curr_centers), axis=0)
        centroid_dot = Dot(centroid_pos, color=RED)
        centroid_text = Text("Centroid", font_size=16, color=RED).next_to(centroid_dot, UP, buff=0.1)
        
        # Using a standard Line instead of DashedLine per restriction log
        line = Line(centroid_pos, target_zone.get_center(), color=YELLOW).set_opacity(0.5)
        self.play(FadeIn(centroid_dot), FadeIn(centroid_text), Create(line))

        # 4. Reference Formula and Reward Counter
        formula = MathTex(r"R = w_1(n_{in})^2 + w_2(dist)^{-1}", font_size=24).to_edge(UP)
        self.play(Write(formula))
        
        reward_val = 0
        reward_text = Text("Reward: 0", font_size=24).to_edge(DOWN, buff=0.5)
        self.add(reward_text)

        # 5. Animation Loop: Moving pegs one by one
        for i in range(len(pegs)):
            # Determine target position for current peg
            target_pos = target_zone.get_center() + np.array([
                np.random.uniform(-0.5, 0.5),
                np.random.uniform(-1.2, 1.2),
                0
            ])
            
            # Pre-calculate the next centroid state for simultaneous animation
            simulated_centers = get_centers(pegs)
            simulated_centers[i] = target_pos
            next_centroid_pos = np.mean(np.array(simulated_centers), axis=0)
            next_line = Line(next_centroid_pos, target_zone.get_center(), color=YELLOW).set_opacity(0.5)
            
            # Prepare updated reward text
            reward_val += (i + 1)**2
            new_reward_text = Text(f"Reward: {reward_val}", font_size=24).to_edge(DOWN, buff=0.5)
            
            # Prepare bonus pop-up
            bonus_label = Text(f"+{i+1}^2", color=GREEN, font_size=22).next_to(target_pos, UP, buff=0.1)
            
            # Execute all transitions together
            self.play(
                pegs[i].animate.move_to(target_pos),
                centroid_dot.animate.move_to(next_centroid_pos),
                centroid_text.animate.next_to(next_centroid_pos, UP, buff=0.1),
                Transform(line, next_line),
                Transform(reward_text, new_reward_text),
                FadeIn(bonus_label, shift=UP * 0.3),
                run_time=1.2
            )
            
            # Clean up bonus pop-up
            self.play(FadeOut(bonus_label), run_time=0.4)

        self.wait(2)