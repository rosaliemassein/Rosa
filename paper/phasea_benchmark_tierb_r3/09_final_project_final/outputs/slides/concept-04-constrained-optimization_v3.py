from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Formula and Title
        formula = MathTex(
            r"\max \sum_{i,j} s_{i,j} x_{i,j} - \sum_{k} P_k \delta_k",
            font_size=36
        ).to_edge(UP, buff=0.3)
        
        matrix_label = Text("Assignment Matrix", font_size=24).next_to(formula, DOWN, buff=0.4)
        
        # 2. Assignment Matrix (Constructed manually to avoid IntegerMatrix)
        matrix_data = [
            [1, 0, 0, 1, 0],
            [0, 1, 0, 0, 1],
            [1, 0, 1, 0, 0],
            [0, 0, 1, 1, 0],
            [1, 1, 0, 0, 1]
        ]
        
        matrix_rows = VGroup()
        for r_data in matrix_data:
            row_vg = VGroup(*[Text(str(val), font_size=24) for val in r_data])
            row_vg.arrange(RIGHT, buff=0.6)
            matrix_rows.add(row_vg)
        matrix_rows.arrange(DOWN, buff=0.4).next_to(matrix_label, DOWN)
        
        brackets = MathTex(r"\left[ \right]").scale(7)
        brackets.stretch_to_fit_height(matrix_rows.get_height() + 0.4)
        brackets.stretch_to_fit_width(matrix_rows.get_width() + 0.6)
        brackets.move_to(matrix_rows)
        
        full_matrix = VGroup(matrix_rows, brackets)
        
        # 3. Score Bar (Manual animation instead of ValueTracker)
        score_label = Text("Score", font_size=24)
        score_bar_bg = Rectangle(height=3, width=0.5, color=WHITE)
        score_bar_fill = Rectangle(
            height=2.0, # Initial height
            width=0.5,
            fill_opacity=1,
            fill_color=GREEN,
            stroke_width=0
        )
        score_bar_fill.align_to(score_bar_bg, DOWN)
        
        score_group = VGroup(score_bar_bg, score_bar_fill, score_label)
        score_label.next_to(score_bar_bg, DOWN)
        score_group.to_edge(RIGHT, buff=1.5)

        # 4. Constraint Icons
        # Institutional Conflict (Red X)
        inst_icon = VGroup(
            Text("X", color=RED), 
            Text("Inst", font_size=18)
        ).arrange(DOWN, buff=0.1)
        
        # Diversity (Scale-like triangle)
        diversity_icon = VGroup(
            Triangle(color=YELLOW).scale(0.2), 
            Text("Diversity", font_size=18)
        ).arrange(DOWN, buff=0.1)
        
        # Workload (Clock-like circle)
        workload_icon = VGroup(
            Circle(radius=0.2, color=BLUE), 
            Text("Workload", font_size=18)
        ).arrange(DOWN, buff=0.1)
        
        icons = VGroup(inst_icon, diversity_icon, workload_icon).arrange(RIGHT, buff=1).to_edge(DOWN, buff=0.5)

        # --- ANIMATION SEQUENCE ---
        
        # Intro
        self.play(Write(formula))
        self.play(FadeIn(full_matrix), Write(matrix_label))
        self.play(FadeIn(score_bar_bg), FadeIn(score_bar_fill), Write(score_label))
        self.wait(1)

        # Animation: Shift some ones
        # Target: Row 0, Col 2 (index 2 in matrix_rows[0])
        cell_to_change = matrix_rows[0][2]
        new_val = Text("1", font_size=24, color=YELLOW).move_to(cell_to_change)
        
        self.play(
            Transform(cell_to_change, new_val),
            score_bar_fill.animate.stretch_to_fit_height(2.5, about_edge=DOWN).set_color(GREEN),
            run_time=1
        )
        
        # Introduce Constraint Icons
        self.play(FadeIn(icons))
        self.wait(1)

        # Violation Scenario
        # Row 2 (index 2) gets a violation (too many reviewers)
        violation_cell = matrix_rows[2][1]
        violation_val = Text("1", font_size=24, color=RED).move_to(violation_cell)
        
        violation_rect = SurroundingRectangle(matrix_rows[2], color=RED)
        
        self.play(
            Transform(violation_cell, violation_val),
            score_bar_fill.animate.stretch_to_fit_height(0.5, about_edge=DOWN).set_color(RED),
            Create(violation_rect),
            inst_icon.animate.scale(1.2).set_color(RED),
            run_time=1.5
        )
        
        # Show Penalty text
        penalty = Text("- Penalty", color=RED, font_size=24).next_to(score_bar_bg, LEFT)
        self.play(Write(penalty))
        self.play(FadeOut(penalty, shift=LEFT))
        
        self.wait(1)
        
        # Fix the violation
        fixed_val = Text("0", font_size=24, color=WHITE).move_to(violation_cell)
        self.play(
            Transform(violation_cell, fixed_val),
            FadeOut(violation_rect),
            score_bar_fill.animate.stretch_to_fit_height(2.2, about_edge=DOWN).set_color(GREEN),
            inst_icon.animate.scale(1/1.2).set_color(WHITE),
            run_time=1
        )

        self.wait(2)