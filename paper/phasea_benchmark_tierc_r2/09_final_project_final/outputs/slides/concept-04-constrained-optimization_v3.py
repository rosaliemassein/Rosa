from manim import *

class ConceptOptimization(Scene):
    def construct(self):
        # 1. Formula Header
        formula = MathTex(r"\max \sum_{i,j} s_{i,j} x_{i,j} - \sum_{k} P_k \delta_k")
        formula.to_edge(UP, buff=0.5)
        self.add(formula)

        # 2. Assignment Matrix Construction
        rows, cols = 6, 8
        matrix_mobs = VGroup()
        for r in range(rows):
            row_group = VGroup()
            for c in range(cols):
                # Start with mostly 0s, some random 1s
                val = "1" if (r + c) % 7 == 0 else "0"
                char = Text(val, font_size=24)
                char.move_to([c * 0.6 - 2.5, r * -0.5 + 1, 0])
                row_group.add(char)
            matrix_mobs.add(row_group)

        matrix_label = Text("Assignment Matrix", font_size=24).next_to(matrix_mobs, UP, buff=0.3)
        matrix_bg = SurroundingRectangle(matrix_mobs, color=GRAY, buff=0.2)
        matrix_all = VGroup(matrix_bg, matrix_mobs, matrix_label).shift(LEFT * 1)
        self.add(matrix_all)

        # 3. Score Bar (Vertical)
        score_tracker = ValueTracker(50) # Percentage 0-100
        score_bar_outline = Rectangle(height=3, width=0.6, color=WHITE).to_edge(RIGHT, buff=1.5)
        
        score_fill = always_redraw(lambda: Rectangle(
            height=max(0.01, score_tracker.get_value() / 100 * 3),
            width=0.6,
            fill_opacity=0.8,
            fill_color=GREEN if score_tracker.get_value() > 40 else RED,
            stroke_width=0
        ).move_to(score_bar_outline.get_bottom(), aligned_edge=DOWN))

        score_label = Text("Score", font_size=20).next_to(score_bar_outline, UP)
        self.add(score_bar_outline, score_fill, score_label)

        # 4. Constraint Icons (Manual construction for maximum compatibility)
        # Red X (Institutional conflict)
        icon_x = VGroup(
            Line(UL, DR),
            Line(UR, DL)
        ).scale(0.2).set_color(RED)
        
        # Diversity (Scale-like Triangle)
        icon_scale = VGroup(
            Line(LEFT, RIGHT), 
            Triangle().scale(0.2).rotate(PI).move_to(ORIGIN, DOWN)
        ).set_color(YELLOW).scale(0.8)
        
        # Workload (Clock)
        icon_clock = VGroup(
            Circle(radius=0.3), 
            Line(ORIGIN, 0.2*UP), 
            Line(ORIGIN, 0.15*RIGHT)
        ).set_color(BLUE).scale(0.7)

        icons_group = VGroup(icon_x, icon_scale, icon_clock).arrange(DOWN, buff=0.8).to_edge(LEFT, buff=0.5)
        icon_labels = VGroup(
            Text("Conflict", font_size=16),
            Text("Diversity", font_size=16),
            Text("Workload", font_size=16)
        )
        for i in range(3):
            icon_labels[i].next_to(icons_group[i], DOWN, buff=0.1)

        self.add(icons_group, icon_labels)

        # 5. Animation Sequence
        self.wait(1)

        # Step A: Normal optimization (shift 0s to 1s, score goes up)
        target_cell_1 = matrix_mobs[4][2]
        new_one_1 = Text("1", font_size=24, color=BLUE).move_to(target_cell_1)
        
        self.play(
            Transform(target_cell_1, new_one_1),
            score_tracker.animate.set_value(75),
            run_time=1
        )
        self.wait(0.5)

        # Step B: Violation occurs (Assigning too many to one reviewer)
        target_cell_2 = matrix_mobs[4][5]
        new_one_2 = Text("1", font_size=24, color=RED).move_to(target_cell_2)
        violation_rect = SurroundingRectangle(matrix_mobs[4], color=RED, buff=0.1)

        self.play(
            Transform(target_cell_2, new_one_2),
            Create(violation_rect),
            Indicate(icons_group[2]), # Workload icon
            score_tracker.animate.set_value(25), # Massive drop due to penalty term
            run_time=1.5
        )
        self.wait(1)

        # Step C: Solver fixes the violation
        fixed_zero = Text("0", font_size=24).move_to(target_cell_2)
        self.play(
            FadeOut(violation_rect),
            Transform(target_cell_2, fixed_zero),
            score_tracker.animate.set_value(65),
            run_time=1
        )

        # Step D: Final shift to higher expertise
        target_cell_3 = matrix_mobs[1][6]
        new_one_3 = Text("1", font_size=24, color=BLUE).move_to(target_cell_3)
        self.play(
            Transform(target_cell_3, new_one_3),
            score_tracker.animate.set_value(88),
            run_time=1
        )

        self.wait(2)