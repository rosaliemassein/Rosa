from manim import *
import numpy as np

class DualRewardShaping(Scene):
    def construct(self):
        # 1. Setup board and target zone
        board = Rectangle(width=10, height=6, color=WHITE)
        target_pos = np.array([3.5, 0, 0])
        target_zone = Circle(radius=1.2, color=RED, fill_opacity=0.2).move_to(target_pos)
        target_label = Text("Target Zone", font_size=20, color=RED).next_to(target_zone, UP)
        self.add(board, target_zone, target_label)

        # 2. Setup pegs on the board
        start_points = [
            [-3.5, 1.5, 0], [-4.0, 0.5, 0], [-3.0, 0, 0], 
            [-4.2, -1.0, 0], [-3.2, -1.5, 0]
        ]
        pegs = VGroup(*[Dot(p, color=BLUE, radius=0.15) for p in start_points])
        self.add(pegs)

        # 3. Create Centroid and connecting line with updaters
        centroid = Dot(color=GREEN)
        def update_centroid(c):
            # Calculate the average position of all pegs
            avg_pos = np.mean([p.get_center() for p in pegs], axis=0)
            c.move_to(avg_pos)
        
        centroid.add_updater(update_centroid)
        
        # Using a standard Line as DashedLine was flagged as restricted
        centroid_line = Line(color=YELLOW)
        def update_line(l):
            l.put_start_and_end_on(centroid.get_center(), target_pos)
        
        centroid_line.add_updater(update_line)
        
        self.add(centroid, centroid_line)

        # 4. Rewards UI and dynamic calculation
        reward_anchor = Dot(UP * 2.5 + LEFT * 4.5).set_opacity(0)
        reward_display = Text("Reward: 0.00", font_size=24)
        reward_display.move_to(reward_anchor.get_center(), aligned_edge=LEFT)
        
        def update_reward_text(obj):
            # Count pegs inside the radius of the target zone
            count = sum(1 for p in pegs if np.linalg.norm(p.get_center() - target_pos) < 1.2)
            # Calculate distance between centroid and target
            dist = np.linalg.norm(centroid.get_center() - target_pos)
            # Formula: R = w1 * (pegs_in)^2 + w2 * (dist)^-1
            # Using example weights w1=2, w2=0.5
            reward_val = 2 * (count**2) + 0.5 * (1.0 / max(dist, 0.1))
            
            new_text = Text(f"Reward: {reward_val:.2f}", font_size=24)
            new_text.move_to(reward_anchor.get_center(), aligned_edge=LEFT)
            obj.become(new_text)

        reward_display.add_updater(update_reward_text)
        self.add(reward_anchor, reward_display)

        # 5. Animation sequence: Moving pegs toward the target
        destinations = [
            [3.2, 0.4, 0],  # In
            [3.6, -0.4, 0], # In
            [0.5, 0.5, 0],  # Out
            [3.8, 0.1, 0],  # In
            [-1.0, -1.0, 0] # Out
        ]

        prev_count = 0
        for i in range(len(pegs)):
            # Animate movement
            self.play(pegs[i].animate.move_to(destinations[i]), run_time=1.2)
            
            # Check for bonus pop-up when a peg enters the zone
            current_count = sum(1 for p in pegs if np.linalg.norm(p.get_center() - target_pos) < 1.2)
            if current_count > prev_count:
                bonus_label = Text(f"Bonus: {current_count}^2", color=GREEN, font_size=24)
                bonus_label.next_to(pegs[i], UP)
                self.play(Write(bonus_label), run_time=0.4)
                self.play(FadeOut(bonus_label), run_time=0.4)
                prev_count = current_count
            
            self.wait(0.1)

        self.wait(2)