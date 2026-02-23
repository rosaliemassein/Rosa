import math
from manim import *

class DualRewardShaping(Scene):
    def construct(self):
        # Board and Target Zone setup
        board = Rectangle(width=10, height=6, color=WHITE)
        target = Rectangle(width=2, height=4, color=GREEN, fill_opacity=0.3).shift(RIGHT * 4)
        target_text = Text("Target Zone", font_size=24, color=GREEN).next_to(target, UP)
        
        # Blue pegs representing agents
        pegs = VGroup()
        for i in range(8):
            # Distribute pegs on the left side
            p = Dot(color=BLUE).move_to(LEFT * 4.5 + UP * (0.6 * i - 2.1))
            pegs.add(p)
        
        # Centroid point
        centroid = Dot(color=RED)
        centroid.move_to(pegs.get_center())
        
        # Reward-guiding line (Solid Line used as DashedLine is disallowed)
        line_to_target = Line(centroid.get_center(), target.get_center(), color=YELLOW)
        
        centroid_label = Text("Centroid", font_size=18, color=RED)
        
        # Named functions for updaters to avoid potential lambda identifier issues (like 'd' or 'l')
        def update_centroid_position(mob):
            mob.move_to(pegs.get_center())

        def update_label_position(mob):
            mob.next_to(centroid, UP, buff=0.1)

        def update_line_position(mob):
            mob.put_start_and_end_on(centroid.get_center(), target.get_center())

        # Registering updaters
        centroid.add_updater(update_centroid_position)
        centroid_label.add_updater(update_label_position)
        line_to_target.add_updater(update_line_position)
        
        # Reward Display text
        reward_display = Text("Reward: 0.00", font_size=32).to_edge(DOWN, buff=0.5)
        
        self.add(board, target, target_text, pegs, centroid, centroid_label, line_to_target, reward_display)
        self.wait(1)
        
        # Animation sequence: Move pegs to target one by one
        for i in range(8):
            # Determine destination inside target zone
            target_x = 3.5 + (i % 2) * 1.0
            target_y = (i // 2) * 0.8 - 1.2
            
            # Animate peg movement
            self.play(pegs[i].animate.move_to([target_x, target_y, 0]), run_time=0.8)
            
            # Calculate current reward parameters
            pegs_in_target = 0
            for p in pegs:
                # Peg is in target if its x-coordinate is within the zone (left edge is 3.0)
                if p.get_center()[0] > 3.0:
                    pegs_in_target += 1
            
            # Calculate distance from centroid to target center
            current_c = pegs.get_center()
            target_c = target.get_center()
            dist_val = math.sqrt((current_c[0] - target_c[0])**2 + (current_c[1] - target_c[1])**2)
            
            # Formula: Reward = w1 * (pegs_in)^2 + w2 * (1 / distance)
            # Weights chosen for visual clarity
            calculated_reward = (pegs_in_target ** 2) + (5.0 / (dist_val + 0.1))
            
            # Create updated reward text
            reward_str = "Reward: " + "{:.2f}".format(calculated_reward)
            new_reward_display = Text(reward_str, font_size=32).to_edge(DOWN, buff=0.5)
            
            # Square bonus pop-up to emphasize non-linear reward
            bonus_str = str(pegs_in_target) + "^2"
            bonus_text = Text(bonus_str, font_size=24, color=GREEN).next_to(pegs[i], UR, buff=0.1)
            
            # Perform the updates
            self.play(
                Transform(reward_display, new_reward_display),
                FadeIn(bonus_text, shift=UP * 0.2),
                run_time=0.4
            )
            self.play(FadeOut(bonus_text), run_time=0.2)
            
        self.wait(2)