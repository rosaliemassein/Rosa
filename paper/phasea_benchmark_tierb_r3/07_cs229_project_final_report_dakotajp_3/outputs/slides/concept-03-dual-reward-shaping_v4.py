from manim import *
import numpy as np

class DualRewardShaping(Scene):
    def construct(self):
        # 1. Setup Board and Target Zone
        board = Rectangle(width=10, height=6, color=WHITE).set_opacity(0.2)
        target_zone = Circle(radius=1.5, color=GREEN, fill_opacity=0.3).shift(4 * RIGHT)
        target_label = Text("Target Zone", font_size=20, color=GREEN).next_to(target_zone, UP)
        
        # 2. Create Pegs in a cluster
        pegs = VGroup(*[
            Dot(
                point=[np.random.uniform(-4.5, -3.0), np.random.uniform(-2.0, 2.0), 0], 
                color=BLUE, 
                radius=0.15
            )
            for _ in range(5)
        ])
        
        # 3. Setup Centroid and Updaters
        centroid_dot = Dot(color=YELLOW, radius=0.1)
        def update_centroid(mob):
            points = [p.get_center() for p in pegs]
            mob.move_to(np.mean(points, axis=0))
        centroid_dot.add_updater(update_centroid)
        
        centroid_label = Text("Centroid", font_size=16, color=YELLOW)
        def update_centroid_label(mob):
            mob.next_to(centroid_dot, UP, buff=0.1)
        centroid_label.add_updater(update_centroid_label)

        # 4. Line to Target Zone
        # Using Line instead of DashedLine and manual updater instead of always_redraw for compatibility
        line_to_goal = Line(centroid_dot.get_center(), target_zone.get_center(), color=YELLOW, stroke_width=2)
        def update_line_to_goal(mob):
            new_line = Line(centroid_dot.get_center(), target_zone.get_center(), color=YELLOW, stroke_width=2)
            mob.become(new_line)
        line_to_goal.add_updater(update_line_to_goal)
        
        # 5. Reward Counter
        reward_text = Text("Reward: 0.0", font_size=28).to_edge(UP, buff=0.5)
        def update_reward_text(mob):
            # Calculate number of pegs inside the target circle
            pegs_in = 0
            for p in pegs:
                dist_to_target = np.linalg.norm(p.get_center() - target_zone.get_center())
                if dist_to_target < 1.5:
                    pegs_in += 1
            
            # Calculate distance from centroid to goal
            c_dist = np.linalg.norm(centroid_dot.get_center() - target_zone.get_center())
            
            # w1 * (pegs_in)^2 + w2 * (dist^-1)
            val = 10 * (pegs_in**2) + 5 * (1.0 / max(c_dist, 0.1))
            
            new_text = Text(f"Reward: {val:.1f}", font_size=28).to_edge(UP, buff=0.5)
            mob.become(new_text)
        
        reward_text.add_updater(update_reward_text)
        
        # Add all elements to the scene
        self.add(board, target_zone, target_label, pegs, centroid_dot, centroid_label, line_to_goal, reward_text)
        
        # 6. Animation Sequence
        for i in range(len(pegs)):
            # Move each peg to a random point within the target zone
            r = np.random.uniform(0, 1.2)
            angle = np.random.uniform(0, 2 * np.pi)
            destination = target_zone.get_center() + np.array([r * np.cos(angle), r * np.sin(angle), 0])
            
            self.play(pegs[i].animate.move_to(destination), run_time=1.2)
            
            # Show "Squared Bonus" pop-up for each peg finishing
            current_bonus = (i + 1)**2
            bonus_popup = Text(f"+{current_bonus} Bonus!", color=RED, font_size=24).next_to(pegs[i], UP)
            self.play(FadeIn(bonus_popup, shift=UP), run_time=0.4)
            self.play(FadeOut(bonus_popup), run_time=0.3)
            
        self.wait(2)