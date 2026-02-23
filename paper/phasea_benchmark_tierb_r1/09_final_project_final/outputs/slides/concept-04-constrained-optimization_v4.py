from manim import *

class Concept04ConstrainedOptimization(Scene):
    def construct(self):
        # 1. Header and Formula
        title = Text("Constrained Optimization", font_size=32).to_edge(UP)
        formula = MathTex(
            r"\max \sum_{i,j} s_{i,j} x_{i,j} - \sum_{k} P_k \delta_k", 
            font_size=36
        ).next_to(title, DOWN, buff=0.3)
        
        # 2. Assignment Matrix (Custom Grid)
        rows, cols = 4, 5
        cell_size = 0.6
        matrix_group = VGroup()
        cells = VGroup()
        entries = VGroup()
        
        for r in range(rows):
            for c in range(cols):
                square = Square(side_length=cell_size, stroke_width=2)
                square.move_to([c * cell_size, -r * cell_size, 0])
                cells.add(square)
                # Initial binary values
                val = "1" if (r + c) % 3 == 0 else "0"
                txt = Text(val, font_size=20).move_to(square.get_center())
                entries.add(txt)
        
        matrix_group.add(cells, entries)
        matrix_group.center().shift(LEFT * 2.5 + DOWN * 0.5)
        matrix_label = Text("Assignment Matrix", font_size=20).next_to(matrix_group, UP)

        # 3. Score Bar (Manual Animation)
        bar_height_max = 3.0
        bar_bg = Rectangle(height=bar_height_max, width=0.6, color=WHITE, stroke_width=2)
        bar_bg.shift(RIGHT * 2.5 + DOWN * 0.5)
        
        # Initial score fill
        bar_fill = Rectangle(
            height=1.5, 
            width=0.6, 
            color=YELLOW, 
            fill_opacity=0.8, 
            stroke_width=0
        )
        bar_fill.move_to(bar_bg.get_bottom(), aligned_edge=DOWN)
        score_label = Text("Score", font_size=20).next_to(bar_bg, UP)

        # 4. Constraint Icons
        # Conflict (Red X)
        icon_x = VGroup(
            Line(UL, DR, color=RED),
            Line(UR, DL, color=RED)
        ).scale(0.2)
        
        # Diversity (Simplified Scale)
        icon_scale = VGroup(
            Triangle(color=WHITE).scale(0.1),
            Line(LEFT, RIGHT, color=WHITE).scale(0.3).shift(UP * 0.1)
        )
        
        # Workload (Clock)
        icon_clock = VGroup(
            Circle(radius=0.2, color=YELLOW),
            Line(ORIGIN, UP * 0.12, color=YELLOW),
            Line(ORIGIN, RIGHT * 0.1, color=YELLOW)
        )
        
        icons = VGroup(icon_x, icon_scale, icon_clock).arrange(DOWN, buff=0.6)
        icons.next_to(bar_bg, RIGHT, buff=0.7)
        
        icon_labels = VGroup(
            Text("Conflict", font_size=16, color=RED),
            Text("Diversity", font_size=16),
            Text("Workload", font_size=16, color=YELLOW)
        )
        for i in range(len(icons)):
            icon_labels[i].next_to(icons[i], RIGHT, buff=0.2)

        # --- ANIMATION SEQUENCE ---
        
        self.add(title, formula, matrix_group, matrix_label, bar_bg, bar_fill, score_label)
        self.play(FadeIn(icons), FadeIn(icon_labels))
        self.wait(1)

        # A. Shifting values improves score
        # Select cell (0,0), change 0 to 1
        new_entry_1 = Text("1", font_size=20, color=GREEN).move_to(entries[0].get_center())
        self.play(
            Transform(entries[0], new_entry_1),
            bar_fill.animate.stretch_to_fit_height(2.2, about_edge=DOWN),
            run_time=1
        )
        self.wait(0.5)

        # B. Constraint Violation (Workload)
        # Highlight second row
        row_highlight = SurroundingRectangle(cells[5:10], color=RED, buff=0.05)
        new_entry_violator = Text("1", font_size=20, color=RED).move_to(entries[7].get_center())
        
        self.play(
            Create(row_highlight),
            Transform(entries[7], new_entry_violator),
            icon_clock.animate.scale(1.3).set_color(RED),
            run_time=0.8
        )
        
        # Score drops due to penalty term in formula
        self.play(
            bar_fill.animate.stretch_to_fit_height(0.6, about_edge=DOWN),
            Indicate(formula[0][14:], color=RED), # Penalty part of formula
            run_time=1.5
        )
        self.wait(1)

        # C. Resolving Violation
        fixed_entry = Text("0", font_size=20).move_to(entries[7].get_center())
        self.play(
            FadeOut(row_highlight),
            Transform(entries[7], fixed_entry),
            icon_clock.animate.scale(1/1.3).set_color(YELLOW),
            bar_fill.animate.stretch_to_fit_height(2.6, about_edge=DOWN),
            run_time=1
        )

        # D. Conclusion
        conclusion = Text(
            "Balancing expertise against hard constraints.",
            font_size=24,
            color=BLUE
        ).to_edge(DOWN, buff=0.4)
        
        self.play(Write(conclusion))
        self.wait(3)