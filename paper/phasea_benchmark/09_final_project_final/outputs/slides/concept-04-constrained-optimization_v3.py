from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Formula and Title
        formula = MathTex(
            r"\max \sum_{i,j} s_{i,j} x_{i,j} - \sum_{k} P_k \delta_k",
            font_size=36
        ).to_edge(UP, buff=0.5)
        
        # 2. Assignment Matrix (Manually constructed for maximum compatibility)
        rows_data = [
            ["1", "0", "0", "1", "0"],
            ["0", "1", "0", "0", "1"],
            ["1", "0", "1", "0", "0"],
            ["0", "1", "0", "1", "0"],
            ["1", "0", "0", "0", "1"]
        ]
        
        matrix = VGroup()
        for r in range(5):
            row_vg = VGroup()
            for c in range(5):
                sq = Square(side_length=0.7, color=WHITE, stroke_width=2)
                txt = Text(rows_data[r][c], font_size=20)
                cell = VGroup(sq, txt)
                row_vg.add(cell)
            row_vg.arrange(RIGHT, buff=0)
            matrix.add(row_vg)
        
        matrix.arrange(DOWN, buff=0).scale(0.8).shift(LEFT * 2.5)
        matrix_label = Text("Assignment Matrix", font_size=24).next_to(matrix, UP, buff=0.3)
        
        # 3. Score Bar (Using animate instead of updaters)
        score_bg = Rectangle(width=0.8, height=4, color=GRAY, stroke_width=2)
        score_fill = Rectangle(
            width=0.8, height=2.0, color=GREEN, fill_opacity=0.8, stroke_width=0
        ).align_to(score_bg, DOWN)
        score_label = Text("Expertise Score", font_size=20).next_to(score_bg, UP, buff=0.3)
        score_group = VGroup(score_bg, score_fill, score_label).shift(RIGHT * 3.5)
        
        # 4. Constraint Icons
        # Red X (Conflict)
        icon_x = VGroup(
            Line(UL, DR, color=RED, stroke_width=6),
            Line(UR, DL, color=RED, stroke_width=6)
        ).scale(0.2)
        
        # Scale (Diversity)
        icon_scale = VGroup(
            Triangle(color=BLUE).scale(0.1).rotate(PI),
            Line(LEFT, RIGHT, color=BLUE).scale(0.4).shift(UP * 0.15),
            Square(side_length=0.2, color=BLUE).shift(LEFT * 0.4),
            Square(side_length=0.2, color=BLUE).shift(RIGHT * 0.4)
        ).scale(0.8)
        
        # Clock (Workload)
        icon_clock = VGroup(
            Circle(radius=0.4, color=WHITE, stroke_width=3),
            Line(ORIGIN, UP * 0.25, color=WHITE, stroke_width=3),
            Line(ORIGIN, RIGHT * 0.15, color=WHITE, stroke_width=3)
        ).scale(0.6)
        
        icons_row = VGroup(icon_x, icon_scale, icon_clock).arrange(RIGHT, buff=1).to_edge(DOWN, buff=0.8)
        icon_labels = VGroup(
            Text("Conflict", font_size=16).next_to(icon_x, DOWN),
            Text("Diversity", font_size=16).next_to(icon_scale, DOWN),
            Text("Workload", font_size=16).next_to(icon_clock, DOWN)
        )
        
        # 5. Animation Sequence
        self.add(formula, matrix, matrix_label, score_group, icons_row, icon_labels)
        self.wait(1)
        
        # Action A: Shifting ones (Score goes up)
        # Change a '0' to a '1' in row 1, col 2
        cell_to_change = matrix[0][2]
        new_val_1 = Text("1", font_size=20, color=YELLOW).move_to(cell_to_change[1])
        
        self.play(
            Transform(cell_to_change[1], new_val_1),
            score_fill.animate.stretch_to_fit_height(3.2, about_edge=DOWN).set_color(GREEN),
            run_time=1.5
        )
        
        # Action B: Constraint Violation (Institutional Conflict)
        # Highlight Row 3 in red
        violation_row = matrix[2]
        row_highlight = SurroundingRectangle(violation_row, color=RED, fill_opacity=0.3, stroke_width=0)
        
        # Score drops significantly due to penalty term
        self.play(
            FadeIn(row_highlight),
            Indicate(icon_x, scale_factor=1.5),
            score_fill.animate.stretch_to_fit_height(0.6, about_edge=DOWN).set_color(RED),
            run_time=1.5
        )
        self.wait(1)
        
        # Action C: Balancing Constraints (Diversity and Workload)
        # Fix the violation and move to another state
        self.play(
            FadeOut(row_highlight),
            score_fill.animate.stretch_to_fit_height(2.8, about_edge=DOWN).set_color(GREEN),
            Indicate(icon_scale, color=BLUE),
            Indicate(icon_clock, color=WHITE),
            run_time=1.5
        )
        
        # Final subtle matrix shift
        cell_3 = matrix[4][1]
        new_val_3 = Text("1", font_size=20, color=YELLOW).move_to(cell_3[1])
        
        self.play(
            Transform(cell_3[1], new_val_3),
            score_fill.animate.stretch_to_fit_height(3.6, about_edge=DOWN),
            run_time=1.5
        )
        
        self.wait(2)