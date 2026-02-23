from manim import *
import numpy as np

class DualRewardShaping(Scene):
    def construct(self):
        # 1. Setup board and target zone
        board = Rectangle(width=10, height=6, color=WHITE)
        target_zone = Rectangle(width=3, height=6, color=GREEN, fill_opacity=0.2)
        target_zone.align_to(board, RIGHT)
        target_label = Text("Target Zone", font_size=20).next_to(target_zone, UP, buff=0.2)
        self.add(board, target_zone, target_label)

        # 2. Setup pegs (Team of pieces)
        pegs = VGroup()
        for _ in range(4):
            # Using random positions on the left side of the board
            x_pos = -4.5 + np.random.rand() * 2.0
            y_pos = -2.0 + np.random.rand() * 4.0
            p = Dot(point=[x_pos, y_pos, 0], color=BLUE)
            pegs.add(p)
        self.add(pegs)

        # 3. Centroid indicator with updaters
        centroid_dot = Dot(color=RED).scale(1.3)
        centroid_label = Text("Centroid", font_size=18, color=RED)
        
        def update_centroid_dot(mob):
            pos_list = []
            for p in pegs:
                pos_list.append(p.get_center())
            avg_pos = np.mean(pos_list, axis=0)
            mob.move_to(avg_pos)

        def update_centroid_label(mob):
            mob.next_to(centroid_dot, UP, buff=0.1)

        centroid_dot.add_updater(update_centroid_dot)
        centroid_label.add_updater(update_centroid_label)
        self.add(centroid_dot, centroid_label)

        # 4. Connection Line to Target (Standard Line used to ensure compatibility)
        target_line = Line(color=YELLOW)
        def update_target_line(mob):
            c_p = centroid_dot.get_center()
            t_x = target_zone.get_left()[0]
            # Line from centroid horizontal to target zone boundary
            mob.put_start_and_end_on(c_p, [t_x, c_p[1], 0])

        target_line.add_updater(update_target_line)
        self.add(target_line)

        # 5. Reward Counter display using Text updates
        reward_text = Text("Reward: 0.00", font_size=32).to_edge(UP)
        self.add(reward_text)

        def update_reward_text(mob):
            c_p = centroid_dot.get_center()
            t_p = target_zone.get_center()
            # Distance between centroid and target center
            dist = np.linalg.norm(c_p - t_p)
            
            # Count pegs that have crossed into the target zone
            count = 0
            for p in pegs:
                if p.get_center()[0] > target_zone.get_left()[0]:
                    count += 1
            
            # Reward Formula: R = w1 * (pegs_in)^2 + w2 * (dist)^-1
            w1 = 2.0
            w2 = 10.0
            # Small constant 0.1 added to distance to avoid division by zero
            val = w1 * (count ** 2) + w2 * (1.0 / (dist + 0.1))
            
            # Create new text for content change
            new_mob = Text("Reward: " + str(round(val, 2)), font_size=32).to_edge(UP)
            mob.become(new_mob)

        reward_text.add_updater(update_reward_text)

        # 6. Movement Animation
        for i in range(len(pegs)):
            peg = pegs[i]
            # Move individual pegs one by one into the target zone
            target_x = target_zone.get_left()[0] + 0.5 + i * 0.3
            target_y = -2.0 + np.random.rand() * 4.0
            
            self.play(
                peg.animate.move_to([target_x, target_y, 0]),
                run_time=1.5
            )
            
            # Squared bonus pop-up animation
            bonus_str = str(i + 1) + "^2"
            bonus_txt = Text(bonus_str, font_size=24, color=YELLOW).next_to(peg, UP)
            self.play(FadeIn(bonus_txt), run_time=0.4)
            self.play(FadeOut(bonus_txt), run_time=0.4)

        # 7. Formula display at the end
        formula = Text("R = w1(pegs_in)^2 + w2(dist)^-1", font_size=24).to_edge(DOWN, buff=0.5)
        self.play(Write(formula))
        self.wait(2)