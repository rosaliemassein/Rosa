from manim import *
import numpy as np

class DualRewardShaping(Scene):
    def construct(self):
        # Define a linear rate function explicitly to avoid "linear" undefined error
        def my_linear_rate(t):
            return t
            
        # 1. Environment Setup
        # Create a board and a target zone
        board = Rectangle(height=4.5, width=7.0, color=WHITE).shift(UP * 0.5)
        target = Circle(radius=1.0, color=GREEN, fill_opacity=0.3).shift(RIGHT * 2.5 + UP * 0.5)
        target_text = Text("Target Zone", font_size=20, color=GREEN).next_to(target, UP)
        
        # Display the reward formula using Text for maximum compatibility
        formula_text = Text("R = w1 * (Pegs_In)^2 + w2 * (Dist^-1)", font_size=24).to_edge(UP, buff=0.2)
        
        # 2. Agent Pieces (Pegs)
        # Create a cluster of blue dots
        pegs_list = [
            Dot(color=BLUE).move_to(LEFT * 3 + UP * (0.8 * i - 0.8) + UP * 0.5)
            for i in range(3)
        ]
        pegs = VGroup(*pegs_list)
        
        # 3. Dynamic Visual Elements
        # Centroid Marker representing the average position of the team
        centroid_dot = Dot(color=YELLOW)
        def update_centroid_pos(centroid_obj):
            centroid_obj.move_to(pegs.get_center())
        centroid_dot.add_updater(update_centroid_pos)
        
        centroid_label = Text("Centroid", font_size=16, color=YELLOW)
        def update_label_pos(label_obj):
            label_obj.next_to(centroid_dot, DOWN, buff=0.1)
        centroid_label.add_updater(update_label_pos)
        
        # Line from Centroid to Target (visualizing gravity/pull)
        dist_line = Line(color=RED)
        def update_line_endpoints(line_obj):
            line_obj.put_start_and_end_on(pegs.get_center(), target.get_center())
        dist_line.add_updater(update_line_endpoints)
        
        # 4. Reward Tracking UI
        reward_label = Text("Total Reward:", font_size=24).to_edge(DOWN, buff=0.5).shift(LEFT * 0.6)
        reward_value_text = Text("0.0", font_size=24, color=YELLOW).next_to(reward_label, RIGHT)
        
        # Helper function to calculate reward based on current state
        def calculate_current_reward():
            # Term 1: Distance-based reward
            team_center = pegs.get_center()
            target_center = target.get_center()
            dist = np.linalg.norm(team_center - target_center)
            dist_reward = 10.0 / (dist + 0.1)
            
            # Term 2: Squared bonus for pieces in target
            in_count = 0
            for p in pegs_list:
                if np.linalg.norm(p.get_center() - target_center) < 1.0:
                    in_count += 1
            finish_reward = (in_count ** 2) * 5.0
            
            return dist_reward + finish_reward

        # Updater for the reward display
        def update_reward_display(val_obj):
            current_val = calculate_current_reward()
            # We recreate the text to update the value shown
            val_obj.become(
                Text(str(round(current_val, 1)), font_size=24, color=YELLOW).next_to(reward_label, RIGHT)
            )
        reward_value_text.add_updater(update_reward_display)

        # 5. Build the Scene
        self.add(board, target, target_text, formula_text, pegs, centroid_dot, centroid_label, dist_line, reward_label, reward_value_text)
        
        # 6. Animation: Moving the entire team forward
        # This increases the reward by decreasing the centroid distance
        self.play(pegs.animate.shift(RIGHT * 2.5), run_time=4, rate_func=my_linear_rate)
        self.wait(0.5)
        
        # 7. Animation: Pieces entering the zone individually
        # This highlights the non-linear "Squared Bonus"
        for i in range(len(pegs_list)):
            p = pegs_list[i]
            # Calculate a unique spot inside the target circle
            inner_dest = target.get_center() + np.array([(i-1)*0.25, (i-1)*0.25, 0])
            self.play(p.animate.move_to(inner_dest), run_time=1.2)
            
            # Show a pop-up bonus to emphasize the squared logic (1^2, 2^2, 3^2)
            bonus_amount = (i + 1)**2
            bonus_text = Text("+" + str(bonus_amount), font_size=22, color=YELLOW).next_to(p, UP)
            self.play(Write(bonus_text), run_time=0.3)
            self.play(bonus_text.animate.shift(UP * 0.4).set_opacity(0), run_time=0.5)
            self.remove(bonus_text)
            
        self.wait(2)

        # Cleanup updaters to prevent issues at scene end
        centroid_dot.remove_updater(update_centroid_pos)
        centroid_label.remove_updater(update_label_pos)
        dist_line.remove_updater(update_line_endpoints)
        reward_value_text.remove_updater(update_reward_display)