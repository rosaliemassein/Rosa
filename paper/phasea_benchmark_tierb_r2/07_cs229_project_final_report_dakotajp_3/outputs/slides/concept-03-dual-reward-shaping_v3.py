from manim import *
import numpy as np

class Concept03DualRewardShaping(Scene):
    def construct(self):
        # 1. Setup Board and Target Zone
        board = Rectangle(width=10, height=6, color=WHITE)
        target_zone = Rectangle(width=3, height=5, color=GREEN, fill_opacity=0.3).shift(3.5 * RIGHT)
        target_pos = target_zone.get_center()
        self.add(board, target_zone)

        # 2. Add Pegs
        pegs = VGroup(*[
            Dot(point=[np.random.uniform(-4, -1), np.random.uniform(-2, 2), 0], color=BLUE)
            for _ in range(6)
        ])
        self.add(pegs)

        # 3. Centroid and Line to Target
        centroid_dot = Dot(color=RED)
        centroid_dot.move_to(pegs.get_center())
        
        # Using Line instead of DashedLine to satisfy constraints
        line_to_target = Line(centroid_dot.get_center(), target_pos, color=YELLOW)
        
        self.add(centroid_dot, line_to_target)

        # 4. Reward Labels
        pegs_in_count = 0
        score_label = Text("Pegs In: 0", font_size=24).to_edge(UL, buff=0.5)
        dist_label = Text("Dist: 0.00", font_size=24).to_edge(UR, buff=0.5)
        self.add(score_label, dist_label)

        # 5. Updaters (using named functions instead of lambdas)
        def update_centroid(mob):
            mob.move_to(pegs.get_center())

        def update_line(mob):
            mob.put_start_and_end_on(centroid_dot.get_center(), target_pos)

        def update_dist(mob):
            # Calculate distance between centroid and target
            d = np.linalg.norm(pegs.get_center() - target_pos)
            txt = "Dist: " + "{:.2f}".format(d)
            # Re-creating Text as replacement for DecimalNumber
            new_mob = Text(txt, font_size=24).to_edge(UR, buff=0.5)
            mob.become(new_mob)

        centroid_dot.add_updater(update_centroid)
        line_to_target.add_updater(update_line)
        dist_label.add_updater(update_dist)

        # 6. Formula Text
        formula = Text("R = w1(In)^2 + w2(Dist)^-1", font_size=20).to_edge(UP, buff=0.2)
        self.add(formula)

        # 7. Animation Loop
        for i in range(len(pegs)):
            peg = pegs[i]
            # Random destination inside target zone
            dest = target_pos + [np.random.uniform(-1, 1), np.random.uniform(-2, 2), 0]
            
            # Move the peg
            self.play(peg.animate.move_to(dest), run_time=1)
            
            # Increment and update piece counter
            pegs_in_count += 1
            new_score = Text("Pegs In: " + str(pegs_in_count), font_size=24).to_edge(UL, buff=0.5)
            score_label.become(new_score)
            
            # Squared Bonus Visualization
            bonus_str = str(pegs_in_count) + " squared bonus"
            bonus_text = Text(bonus_str, color=GOLD, font_size=20).next_to(peg, UP)
            self.play(
                FadeIn(bonus_text),
                bonus_text.animate.shift(UP * 0.5).set_opacity(0),
                run_time=0.8
            )
            self.remove(bonus_text)

        self.wait(2)