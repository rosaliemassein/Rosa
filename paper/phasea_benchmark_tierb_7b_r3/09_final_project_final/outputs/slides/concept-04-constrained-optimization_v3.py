from manim import *

class ConstrainedOptimization(Scene):
    def construct(self):
        # 1. Narration and Goal
        voice_text = Text("Assigning reviewers: A massive balancing act.", font_size=32).to_edge(UP)
        self.play(Write(voice_text))

        # 2. Formula Reference
        formula = MathTex(
            r"\max \sum_{i,j} s_{i,j} x_{i,j} - \sum_{k} P_k \delta_k",
            font_size=36
        ).next_to(voice_text, DOWN, buff=0.3)
        self.play(FadeIn(formula))

        # 3. Manual Assignment Matrix (Avoids IntegerMatrix)
        matrix_data = [
            [1, 0, 1, 0],
            [0, 1, 0, 0],
            [1, 0, 0, 1],
            [0, 1, 1, 0]
        ]
        
        cells = VGroup()
        for row in matrix_data:
            for val in row:
                cells.add(MathTex(str(val), font_size=36))
        
        cells.arrange_in_grid(rows=4, cols=4, buff=0.8)
        matrix_label = Text("Assignment Matrix", font_size=24).next_to(cells, UP, buff=0.5)
        
        # Brackets for the matrix
        bracket_l = MathTex(r"\begin{bmatrix} \phantom{\dots \dots \dots \dots} \\ \phantom{\dots \dots \dots \dots} \\ \phantom{\dots \dots \dots \dots} \\ \phantom{\dots \dots \dots \dots} \end{bmatrix}").scale(2.5).move_to(cells)
        
        matrix_group = VGroup(cells, matrix_label, bracket_l).to_edge(LEFT, buff=1).shift(DOWN * 0.5)

        # 4. Score Bar (Avoids ValueTracker and always_redraw)
        score_bg = Rectangle(height=3, width=0.5, color=WHITE).to_edge(RIGHT, buff=2).shift(DOWN * 0.5)
        score_fill = Rectangle(
            height=2.1, # 70% of 3
            width=0.5,
            fill_color=GREEN,
            fill_opacity=0.8,
            stroke_width=0
        ).align_to(score_bg, DOWN)
        
        score_label = Text("Score", font_size=24).next_to(score_bg, UP)
        score_val = MathTex("70", font_size=30).next_to(score_bg, RIGHT)
        
        score_group = VGroup(score_bg, score_fill, score_label, score_val)

        self.play(Create(matrix_group), Create(score_group))
        self.wait(1)

        # 5. Manual Constraint Icons (Avoids Cross)
        # Institutional Conflict (Red X)
        conflict_icon = VGroup(
            Line(UL, DR, color=RED).scale(0.3),
            Line(UR, DL, color=RED).scale(0.3)
        )
        # Gender Diversity (Scale)
        scale_icon = VGroup(
            Line(LEFT*0.3, RIGHT*0.3),
            Triangle(color=WHITE).scale(0.1).rotate(PI).shift(DOWN*0.1),
            Line(LEFT*0.3, LEFT*0.3+DOWN*0.3),
            Line(RIGHT*0.3, RIGHT*0.3+DOWN*0.3)
        ).set_color(GOLD)
        # Workload (Clock)
        clock_icon = VGroup(
            Circle(radius=0.3, color=BLUE),
            Line(ORIGIN, UP * 0.2, color=BLUE),
            Line(ORIGIN, RIGHT * 0.15, color=BLUE)
        )

        icons_group = VGroup(conflict_icon, scale_icon, clock_icon).arrange(RIGHT, buff=1).to_edge(DOWN, buff=0.5)
        icon_labels = VGroup(
            Text("Conflict", font_size=16).next_to(conflict_icon, DOWN),
            Text("Diversity", font_size=16).next_to(scale_icon, DOWN),
            Text("Workload", font_size=16).next_to(clock_icon, DOWN)
        )
        self.play(FadeIn(icons_group), FadeIn(icon_labels))

        # 6. Animate Matrix Changes and Score Updates Manually
        # Change row 0, col 1 from 0 to 1
        new_one = MathTex("1", font_size=36).move_to(cells[1])
        new_score_val = MathTex("75", font_size=30).move_to(score_val)
        
        self.play(
            Transform(cells[1], new_one),
            score_fill.animate.stretch_to_fit_height(2.25, about_edge=DOWN),
            Transform(score_val, new_score_val),
            run_time=0.8
        )
        self.wait(0.5)

        # 7. Constraint Violation (Highlight row 3 in red)
        violation_rect = SurroundingRectangle(VGroup(cells[12], cells[13], cells[14], cells[15]), color=RED)
        
        # Violate workload by adding another '1' in row 3
        violation_one = MathTex("1", font_size=36, color=RED).move_to(cells[15])
        penalty_score_val = MathTex("30", font_size=30).move_to(score_val)
        
        self.play(
            Transform(cells[15], violation_one),
            Create(violation_rect),
            clock_icon.animate.scale(1.3).set_color(RED),
            score_fill.animate.stretch_to_fit_height(0.9, about_edge=DOWN).set_color(RED),
            Transform(score_val, penalty_score_val),
            run_time=1
        )
        self.wait(1)

        # 8. Resolution
        fix_zero = MathTex("0", font_size=36).move_to(cells[15])
        final_score_val = MathTex("85", font_size=30).move_to(score_val)
        
        self.play(
            Transform(cells[15], fix_zero),
            FadeOut(violation_rect),
            clock_icon.animate.scale(1/1.3).set_color(BLUE),
            score_fill.animate.stretch_to_fit_height(2.55, about_edge=DOWN).set_color(GREEN),
            Transform(score_val, final_score_val),
            run_time=1
        )

        # 9. Conclusion
        conclusion = Text("Optimized Assignment Satisfied.", font_size=32).to_edge(UP)
        self.play(Transform(voice_text, conclusion), FadeOut(formula))
        self.wait(2)