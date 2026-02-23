from manim import *

class Concept04ConstrainedOptimization(Scene):
    def construct(self):
        # --- Data Definitions ---
        voice_text = "The system balances expertise matching against hard constraints."
        goal_text = "Goal: Balance expertise, diversity, and workload."
        formula_latex = r"\max \sum_{i,j} s_{i,j} x_{i,j} - \sum_{k} P_k \delta_k"
        
        # --- UI Elements ---
        title = Text("Constrained Optimization", font_size=32).to_edge(UP)
        goal_label = Text(goal_text, font_size=24, color=YELLOW).next_to(title, DOWN, buff=0.2)
        formula = MathTex(formula_latex, font_size=36).next_to(goal_label, DOWN, buff=0.3)
        
        self.add(title, goal_label, formula)

        # --- Manual Matrix Creation (Avoiding IntegerTable) ---
        matrix_data = [
            [1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [1, 0, 0, 0, 1],
            [0, 0, 1, 1, 0],
            [0, 1, 0, 0, 1]
        ]
        
        grid = VGroup()
        cells = [] # Flattened list of (Square, Text) groups
        
        for i in range(5):
            for j in range(5):
                sq = Square(side_length=0.6, stroke_width=2)
                val = Text(str(matrix_data[i][j]), font_size=20)
                cell = VGroup(sq, val)
                cell.move_to([j*0.6, -i*0.6, 0])
                grid.add(cell)
                cells.append(cell)
        
        grid.center().shift(LEFT * 3 + DOWN * 0.5)
        matrix_label = Text("Assignment Matrix", font_size=20).next_to(grid, UP)
        
        self.play(Create(grid), FadeIn(matrix_label))

        # --- Score Bar (Avoiding interpolate_color) ---
        score_tracker = ValueTracker(70)
        
        score_bg = Rectangle(height=3, width=0.6, color=GRAY, fill_opacity=0.2)
        score_fill = always_redraw(lambda: Rectangle(
            height=max(0.01, score_tracker.get_value() / 100 * 3),
            width=0.6,
            fill_opacity=1,
            fill_color=GREEN if score_tracker.get_value() > 50 else RED,
            stroke_width=0
        ).align_to(score_bg, DOWN))
        
        score_title = Text("Score", font_size=20).next_to(score_bg, UP)
        score_val = always_redraw(lambda: DecimalNumber(
            score_tracker.get_value(), num_decimal_places=0, font_size=20
        ).next_to(score_bg, DOWN))
        
        score_group = VGroup(score_bg, score_fill, score_title, score_val).shift(RIGHT * 5 + DOWN * 0.5)
        self.play(FadeIn(score_group))

        # --- Constraint Icons (Avoiding Cross) ---
        # Conflict Icon (Manual X)
        conflict_x = VGroup(
            Line(UL, DR, color=RED).scale(0.2),
            Line(UR, DL, color=RED).scale(0.2)
        )
        conflict_item = VGroup(conflict_x, Text("Conflict", font_size=18)).arrange(RIGHT)
        
        # Diversity Icon (Manual Scale)
        scale_tri = Triangle().scale(0.1).set_fill(WHITE, opacity=1)
        scale_top = Line(LEFT*0.2, RIGHT*0.2).next_to(scale_tri, UP, buff=0)
        diversity_item = VGroup(VGroup(scale_tri, scale_top), Text("Diversity", font_size=18)).arrange(RIGHT)
        
        # Workload Icon (Manual Clock)
        clock_circ = Circle(radius=0.15, color=WHITE)
        clock_h = Line(ORIGIN, UP*0.1).move_to(clock_circ.get_center(), aligned_edge=DOWN)
        workload_item = VGroup(VGroup(clock_circ, clock_h), Text("Workload", font_size=18)).arrange(RIGHT)
        
        constraints = VGroup(conflict_item, diversity_item, workload_item).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        constraints.next_to(grid, RIGHT, buff=1)
        
        self.play(FadeIn(constraints))

        # --- Animation: Matrix Shifts ---
        # Pick a cell to "flip" (Row 1, Col 2 -> index 1*5 + 2 = 7)
        target_cell = cells[7]
        self.play(
            target_cell[1].animate.become(Text("1", font_size=20).move_to(target_cell[1])),
            score_tracker.animate.set_value(85),
            run_time=1
        )
        self.wait(0.5)

        # --- Animation: Constraint Violation ---
        # Highlight a row in red
        violating_row_indices = range(15, 20) # Row 3
        row_rect = SurroundingRectangle(VGroup(*[cells[i] for i in violating_row_indices]), color=RED)
        
        # Trigger violation
        bad_cell = cells[17] # Row 3, Col 2
        self.play(
            bad_cell[1].animate.become(Text("1", font_size=20, color=RED).move_to(bad_cell[1])),
            score_tracker.animate.set_value(25),
            Create(row_rect),
            Indicate(workload_item, color=RED)
        )
        self.wait(1.5)

        # --- Restoration ---
        self.play(
            FadeOut(row_rect),
            bad_cell[1].animate.become(Text("0", font_size=20).move_to(bad_cell[1])),
            score_tracker.animate.set_value(78),
            run_time=1
        )

        self.wait(2)