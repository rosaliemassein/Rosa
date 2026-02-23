from manim import *

class ConceptOptimization(Scene):
    def construct(self):
        # 1. Objective Function / Formula
        formula = MathTex(
            r"\max \sum_{i,j} s_{i,j} x_{i,j} - \sum_{k} P_k \delta_k",
            color=WHITE
        ).to_edge(UP, buff=0.5)
        self.add(formula)

        # 2. Assignment Matrix (Binary grid)
        matrix_elements = VGroup()
        grid_size = 8
        for r in range(grid_size):
            for c in range(grid_size):
                # Hardcoded pattern of 0s and 1s
                val = "1" if (r + c) % 3 == 0 else "0"
                t = Text(val, font_size=18)
                # Position manually to avoid layout issues
                t.move_to([c * 0.5 - 4.2, r * -0.5 + 1.5, 0])
                matrix_elements.add(t)
        
        matrix_label = Text("Assignment Matrix", font_size=20).next_to(matrix_elements, UP, buff=0.3)
        matrix_border = Rectangle(width=4.4, height=4.4, color=BLUE).move_to(matrix_elements)
        matrix_group = VGroup(matrix_elements, matrix_label, matrix_border)
        self.add(matrix_group)

        # 3. Score Bar (Visualizing the objective function value)
        score_bg = Rectangle(height=4.0, width=0.7, color=WHITE, stroke_width=2).shift(RIGHT * 4)
        # Initial score height
        score_fill = Rectangle(height=2.2, width=0.7, color=GREEN, fill_opacity=0.8)
        score_fill.move_to(score_bg.get_bottom(), aligned_edge=DOWN)
        score_label = Text("Score", font_size=24).next_to(score_bg, UP, buff=0.3)
        self.add(score_bg, score_fill, score_label)

        # 4. Constraint Icons
        # Institutional Conflict (X)
        line1 = Line([-0.25, -0.25, 0], [0.25, 0.25, 0], color=RED)
        line2 = Line([-0.25, 0.25, 0], [0.25, -0.25, 0], color=RED)
        icon_x = VGroup(line1, line2)
        
        # Diversity (Scale representation)
        scale_top = Line([-0.4, 0, 0], [0.4, 0, 0], color=YELLOW)
        scale_base = Triangle(color=YELLOW).scale(0.15).set_fill(YELLOW, opacity=1).next_to(scale_top, DOWN, buff=0)
        icon_scale = VGroup(scale_top, scale_base)
        
        # Workload (Clock)
        clock_circle = Circle(radius=0.3, color=BLUE)
        clock_hand = Line([0, 0, 0], [0, 0.2, 0], color=BLUE)
        clock_hand2 = Line([0, 0, 0], [0.15, 0, 0], color=BLUE)
        icon_clock = VGroup(clock_circle, clock_hand, clock_hand2)

        icons_group = VGroup(icon_x, icon_scale, icon_clock).arrange(RIGHT, buff=1.2).to_edge(DOWN, buff=0.8)
        icon_labels = VGroup(
            Text("Conflict", font_size=16).next_to(icon_x, DOWN, buff=0.2),
            Text("Diversity", font_size=16).next_to(icon_scale, DOWN, buff=0.2),
            Text("Workload", font_size=16).next_to(icon_clock, DOWN, buff=0.2)
        )
        self.add(icons_group, icon_labels)

        # --- ANIMATIONS ---
        self.wait(1)

        # Step 1: Solving/Shifting (Changing values and score)
        # We manually change a couple of "0" to "1" and move score up
        cell_1 = matrix_elements[12]
        cell_2 = matrix_elements[27]
        new_val_1 = Text("1", font_size=18, color=YELLOW).move_to(cell_1)
        new_val_2 = Text("1", font_size=18, color=YELLOW).move_to(cell_2)

        self.play(
            Transform(cell_1, new_val_1),
            Transform(cell_2, new_val_2),
            score_fill.animate.set_height(3.2, stretch=True).move_to(score_bg.get_bottom(), aligned_edge=DOWN),
            run_time=1.5
        )
        self.wait(0.5)

        # Step 2: Constraint Violation (Red X and penalty)
        # Pick a cell that violates a rule
        violation_idx = 43
        violation_cell = matrix_elements[violation_idx]
        bad_val = Text("1", font_size=22, color=RED).move_to(violation_cell)
        
        # Highlight the row manually (Rectangle instead of BackgroundRectangle)
        row_num = violation_idx // grid_size
        row_start_index = row_num * grid_size
        row_end_index = row_start_index + grid_size
        row_mobjects = VGroup(*[matrix_elements[i] for i in range(row_start_index, row_end_index)])
        row_highlight = Rectangle(
            width=4.1, height=0.45, color=RED, fill_opacity=0.3, stroke_width=0
        ).move_to(row_mobjects)

        self.play(
            Transform(violation_cell, bad_val),
            FadeIn(row_highlight),
            Indicate(icon_x, color=RED, scale_factor=1.5),
            score_fill.animate.set_height(0.6, stretch=True).move_to(score_bg.get_bottom(), aligned_edge=DOWN).set_color(RED),
            run_time=2
        )
        self.wait(1)

        # Step 3: Resolve violation
        resolved_val = Text("0", font_size=18, color=WHITE).move_to(violation_cell)
        self.play(
            Transform(violation_cell, resolved_val),
            FadeOut(row_highlight),
            score_fill.animate.set_height(3.5, stretch=True).move_to(score_bg.get_bottom(), aligned_edge=DOWN).set_color(GREEN),
            run_time=1.5
        )
        self.wait(1)

        # Final Transition to Image (Safe attempt)
        try:
            image = ImageMobject("img-0.jpeg").scale(1.5)
            self.play(FadeIn(image), FadeOut(matrix_group), FadeOut(score_bg), FadeOut(score_fill), FadeOut(score_label))
        except:
            # Fallback if image not found
            final_rect = SurroundingRectangle(matrix_group, color=YELLOW, buff=0.5)
            self.play(Create(final_rect))

        self.wait(2)