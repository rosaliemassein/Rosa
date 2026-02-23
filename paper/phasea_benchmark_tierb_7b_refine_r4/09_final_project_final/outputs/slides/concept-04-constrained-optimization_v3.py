from manim import *
import numpy as np

class ConstrainedOptimization(Scene):
    def construct(self):
        # 1. Setup Formula and Title
        formula = MathTex(
            r"\max \sum_{i,j} s_{i,j} x_{i,j} - \sum_{k} P_k \delta_k",
            color=WHITE
        ).scale(0.8).to_edge(UP, buff=0.5)
        
        title = Text("Assignment Matrix", font_size=24).next_to(formula, DOWN, buff=0.5).to_edge(LEFT, buff=1.5)
        
        # 2. Create Assignment Matrix (Binary)
        # We'll use a 5x5 grid of 0s and 1s
        matrix_data = [
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [1, 0, 0, 0, 1],
            [0, 1, 0, 1, 0],
            [0, 0, 0, 0, 1]
        ]
        
        matrix_mobs = VGroup()
        for i in range(5):
            row = VGroup()
            for j in range(5):
                val = Text(str(matrix_data[i][j]), font_size=30)
                val.shift(RIGHT * j * 0.8 + DOWN * i * 0.6)
                row.add(val)
            matrix_mobs.add(row)
        
        matrix_mobs.center().to_edge(LEFT, buff=1.5)
        title.next_to(matrix_mobs, UP, buff=0.3)

        # 3. Create Score Bar
        score_label = Text("Expertise Score", font_size=24)
        score_bg = Rectangle(height=4, width=0.6, color=GRAY, fill_opacity=0.2)
        score_fill = Rectangle(height=2.5, width=0.6, color=GREEN, fill_opacity=0.8, stroke_width=0)
        score_fill.align_to(score_bg, DOWN)
        
        score_group = VGroup(score_bg, score_fill, score_label).to_edge(RIGHT, buff=2)
        score_label.next_to(score_bg, UP)
        
        # 4. Constraint Icons
        icon_x = MathTex(r"\times", color=RED).scale(1.5) # Institutional Conflict
        icon_scale = MathTex(r"\Delta", color=BLUE).scale(1.2) # Diversity
        icon_clock = MathTex(r"\mathcal{T}", color=YELLOW).scale(1.2) # Workload
        
        icons = VGroup(icon_x, icon_scale, icon_clock).arrange(RIGHT, buff=0.8)
        icons.next_to(matrix_mobs, DOWN, buff=1)
        
        icon_labels = VGroup(
            Text("Conflict", font_size=16).next_to(icon_x, DOWN),
            Text("Diversity", font_size=16).next_to(icon_scale, DOWN),
            Text("Workload", font_size=16).next_to(icon_clock, DOWN)
        )

        # Initial Display
        self.play(Write(formula))
        self.play(Write(title), FadeIn(matrix_mobs))
        self.play(Create(score_bg), Create(score_fill), Write(score_label))
        self.play(FadeIn(icons), Write(icon_labels))
        self.wait(1)

        # 5. Animation Logic: Shifting ones and updating score
        def get_update_score_anim(new_height, color=GREEN):
            h = max(0.1, new_height)
            return score_fill.animate.stretch_to_fit_height(h, about_edge=DOWN).set_color(color)

        # Step A: Improvement
        new_val_1 = Text("1", font_size=30, color=GREEN).move_to(matrix_mobs[0][2].get_center())
        old_val_1 = matrix_mobs[0][1]
        
        self.play(
            old_val_1.animate.become(Text("0", font_size=30)),
            matrix_mobs[0][2].animate.become(new_val_1),
            get_update_score_anim(3.2)
        )
        self.wait(0.5)

        # Step B: Constraint Violation (Workload)
        violation_rect = SurroundingRectangle(matrix_mobs[3], color=RED)
        new_val_2 = Text("1", font_size=30, color=RED).move_to(matrix_mobs[3][4].get_center())
        
        self.play(
            Create(violation_rect),
            matrix_mobs[3][4].animate.become(new_val_2),
            icon_clock.animate.scale(1.5).set_color(RED),
            get_update_score_anim(1.0, color=RED),
            run_time=1
        )
        self.play(icon_clock.animate.scale(1/1.5).set_color(YELLOW))
        self.wait(1)

        # Step C: Resolution
        self.play(
            FadeOut(violation_rect),
            matrix_mobs[3][4].animate.become(Text("0", font_size=30)),
            get_update_score_anim(2.8, color=GREEN),
            run_time=1
        )

        # Step D: Conflict Violation (Institutional)
        conflict_rect = SurroundingRectangle(matrix_mobs[1][2], color=RED)
        self.play(
            Create(conflict_rect),
            matrix_mobs[1][2].animate.set_color(RED),
            icon_x.animate.scale(1.5),
            get_update_score_anim(1.5, color=RED)
        )
        self.wait(0.5)
        self.play(
            FadeOut(conflict_rect),
            icon_x.animate.scale(1/1.5),
            matrix_mobs[1][2].animate.set_color(WHITE),
            get_update_score_anim(2.8, color=GREEN)
        )

        # Final state
        self.wait(2)
        self.play(FadeOut(VGroup(formula, title, matrix_mobs, score_group, icons, icon_labels)))