from manim import *
import numpy as np

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Define strings and basic components from JSON
        formula_tex = r"\max \sum_{i,j} s_{i,j} x_{i,j} - \sum_{k} P_k \delta_k"
        
        # 2. Display Formula at the top
        formula = MathTex(formula_tex).to_edge(UP)
        self.play(Write(formula))
        self.wait(1)

        # 3. Create Assignment Matrix (5x5 grid of 0s and 1s)
        # Using DecimalNumber with 0 decimal places instead of Integer to avoid potential identifier errors
        matrix_mobs = VGroup()
        for i in range(5):
            row = VGroup()
            for j in range(5):
                val = DecimalNumber(0, num_decimal_places=0).scale(0.8)
                row.add(val)
            matrix_mobs.add(row)
        
        matrix_mobs.arrange_in_grid(rows=5, buff=0.5).shift(LEFT * 3)
        matrix_label = Text("Assignment Matrix", font_size=24).next_to(matrix_mobs, UP)
        
        # Add background grid for clarity
        grid = Rectangle(width=4, height=4, color=GRAY_A, stroke_width=1).move_to(matrix_mobs)
        
        self.play(Create(grid), Write(matrix_label), FadeIn(matrix_mobs))
        self.wait(0.5)

        # 4. Create Score Bar on the right
        score_val = ValueTracker(60)
        score_bar_bg = Rectangle(height=4, width=0.5, color=WHITE).shift(RIGHT * 3.5)
        
        # Redraw the fill based on the value tracker
        score_bar_fill = always_redraw(lambda: Rectangle(
            height=max(0.01, (score_val.get_value() / 100) * 4), 
            width=0.5,
            fill_opacity=1,
            fill_color=GREEN if score_val.get_value() > 40 else RED,
            stroke_width=0
        ).align_to(score_bar_bg, DOWN))
        
        score_label = Text("Score", font_size=24).next_to(score_bar_bg, UP)
        self.play(Create(score_bar_bg), Create(score_bar_fill), Write(score_label))

        # 5. Animate Matrix shifting and Score fluctuating
        def update_matrix_values():
            anims = []
            for row in matrix_mobs:
                for entry in row:
                    new_val = np.random.randint(0, 2)
                    anims.append(entry.animate.set_value(new_val))
            return anims

        for _ in range(2):
            self.play(
                *update_matrix_values(), 
                score_val.animate.set_value(np.random.randint(50, 95)), 
                run_time=1
            )

        # 6. Introduce Constraint Icons
        # Institutional Conflict: Red X
        conflict_icon = VGroup(Line(UL, DR), Line(UR, DL)).set_color(RED).scale(0.15)
        conflict_text = Text("Conflict", font_size=16, color=RED).next_to(conflict_icon, DOWN)
        conflict_group = VGroup(conflict_icon, conflict_text).shift(RIGHT * 1 + UP * 1.5)

        # Gender Diversity: Scale
        scale_base = Triangle().scale(0.1).set_fill(WHITE, opacity=1)
        scale_beam = Line(LEFT*0.3, RIGHT*0.3).next_to(scale_base, UP, buff=0)
        scale_icon = VGroup(scale_base, scale_beam)
        scale_text = Text("Diversity", font_size=16).next_to(scale_icon, DOWN)
        scale_group = VGroup(scale_icon, scale_text).next_to(conflict_group, DOWN, buff=0.8)

        # Workload: Clock
        clock_icon = VGroup(Circle(radius=0.2), Line(ORIGIN, 0.15*UP), Line(ORIGIN, 0.1*RIGHT))
        clock_text = Text("Workload", font_size=16).next_to(clock_icon, DOWN)
        clock_group = VGroup(clock_icon, clock_text).next_to(scale_group, DOWN, buff=0.8)

        self.play(FadeIn(conflict_group), FadeIn(scale_group), FadeIn(clock_group))

        # 7. Demonstrate a Constraint Violation
        # Highlight a row in red
        violation_row_rect = SurroundingRectangle(matrix_mobs[2], color=RED, buff=0.1)
        
        # Change values to trigger "violation" (e.g., too many 1s in a row)
        self.play(
            matrix_mobs[2][0].animate.set_value(1),
            matrix_mobs[2][1].animate.set_value(1),
            matrix_mobs[2][2].animate.set_value(1),
            matrix_mobs[2][3].animate.set_value(1),
            matrix_mobs[2][4].animate.set_value(1),
            run_time=0.5
        )
        
        # Drop score significantly and show red penalty term
        penalty_math = MathTex(r"-\sum P_k \delta_k", color=RED).next_to(formula, DOWN)
        
        self.play(
            Create(violation_row_rect),
            score_val.animate.set_value(15), 
            Write(penalty_math),
            conflict_icon.animate.scale(1.5),
            run_time=1.5
        )
        self.wait(2)

        # 8. Resolve violation
        self.play(
            FadeOut(violation_row_rect),
            FadeOut(penalty_math),
            score_val.animate.set_value(82),
            matrix_mobs[2][2].animate.set_value(0),
            matrix_mobs[2][4].animate.set_value(0),
            conflict_icon.animate.scale(1/1.5),
            run_time=1
        )
        
        self.wait(2)