from manim import *

class Concept04ConstrainedOptimization(Scene):
    def construct(self):
        # 1. Setup the Title and Formula
        title = Text("Constrained Optimization", font_size=36).to_edge(UP)
        formula = MathTex(
            r"\max \sum_{i,j} s_{i,j} x_{i,j} - \sum_{k} P_k \delta_k",
            font_size=32
        ).next_to(title, DOWN)
        self.add(title, formula)

        # 2. Create the Assignment Matrix
        matrix_size = 6
        cells = VGroup()
        for i in range(matrix_size):
            row = VGroup()
            for j in range(matrix_size):
                square = Square(side_length=0.6, stroke_width=1, color=GRAY)
                label = Text("0", font_size=24).move_to(square.get_center())
                row.add(VGroup(square, label))
            row.arrange(RIGHT, buff=0)
            cells.add(row)
        cells.arrange(DOWN, buff=0).shift(LEFT * 2)
        
        matrix_label = Text("Assignment Matrix", font_size=24).next_to(cells, UP)
        self.add(cells, matrix_label)

        # 3. Create the Score Bar (No ValueTracker or always_redraw)
        score_box = Rectangle(width=0.8, height=4, color=WHITE).shift(RIGHT * 4)
        score_fill = Rectangle(
            width=0.8, 
            height=0.1, 
            fill_opacity=0.8, 
            fill_color=BLUE,
            stroke_width=0
        ).align_to(score_box, DOWN)
        
        score_label = Text("Expertise Score", font_size=24).next_to(score_box, UP)
        self.add(score_box, score_fill, score_label)

        # 4. Create Constraint Icons manually
        # Conflict Icon (X)
        conflict_icon = VGroup(
            Text("Conflict", font_size=20),
            VGroup(Line(UL, DR), Line(UR, DL)).scale(0.15).set_color(RED)
        ).arrange(RIGHT)
        
        # Diversity Icon (Triangle/Scale)
        diversity_icon = VGroup(
            Text("Diversity", font_size=20),
            Polygon(ORIGIN, LEFT*0.2+DOWN*0.3, RIGHT*0.2+DOWN*0.3, color=YELLOW).scale(0.6)
        ).arrange(RIGHT)
        
        # Workload Icon (Clock)
        workload_icon = VGroup(
            Text("Workload", font_size=20),
            VGroup(Circle(radius=0.15), Line(ORIGIN, UP*0.12), Line(ORIGIN, RIGHT*0.08)).set_color(BLUE)
        ).arrange(RIGHT)
        
        icons = VGroup(conflict_icon, diversity_icon, workload_icon).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        icons.next_to(score_box, LEFT, buff=1)
        self.add(icons)

        # 5. Helper function for updates
        def update_assignment(r, c, val_str, color, new_score_height):
            new_text = Text(val_str, font_size=24, color=color).move_to(cells[r][c][1].get_center())
            self.play(
                Transform(cells[r][c][1], new_text),
                score_fill.animate.stretch_to_fit_height(max(0.1, new_score_height), about_edge=DOWN),
                run_time=0.4
            )

        # 6. Animation Sequence
        self.wait(1)

        # Step 1: Assign reviewers (Score goes up)
        update_assignment(0, 1, "1", YELLOW, 1.0)
        update_assignment(2, 3, "1", YELLOW, 2.0)
        update_assignment(4, 5, "1", YELLOW, 3.0)
        self.wait(0.5)

        # Step 2: Violate Workload Constraint (Row 2 gets too many)
        update_assignment(2, 0, "1", YELLOW, 3.5)
        
        # Violation effect: Highlight row and drop score
        violation_rect = SurroundingRectangle(cells[2], color=RED, buff=0.05)
        self.play(
            Create(violation_rect), 
            workload_icon.animate.set_color(RED),
            score_fill.animate.stretch_to_fit_height(0.5, about_edge=DOWN),
            run_time=0.8
        )
        self.wait(1)
        
        # Step 3: Solver fixes it
        update_assignment(2, 0, "0", WHITE, 0.5)
        self.play(
            FadeOut(violation_rect), 
            workload_icon.animate.set_color(WHITE),
            score_fill.animate.stretch_to_fit_height(3.0, about_edge=DOWN),
            run_time=0.8
        )

        # Step 4: Conflict violation
        conflict_rect = SurroundingRectangle(cells[0][1], color=RED, buff=0.05)
        self.play(
            Create(conflict_rect), 
            conflict_icon.animate.set_color(RED),
            score_fill.animate.stretch_to_fit_height(1.0, about_edge=DOWN),
            run_time=0.8
        )
        self.wait(0.5)

        # Final move to optimize
        update_assignment(0, 1, "0", WHITE, 1.0)
        update_assignment(5, 2, "1", YELLOW, 3.8)
        self.play(
            FadeOut(conflict_rect), 
            conflict_icon.animate.set_color(WHITE),
            run_time=0.5
        )

        self.wait(2)