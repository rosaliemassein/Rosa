from manim import *
import numpy as np

class ConceptZeroShotClassification(Scene):
    def construct(self):
        # 1. Setup Image representation
        image_rect = Rectangle(height=2.5, width=3.5, color=WHITE).to_edge(LEFT, buff=0.5).shift(UP * 1.5)
        image_text = Text("Input Image", font_size=24).move_to(image_rect)
        image_group = VGroup(image_rect, image_text)

        # 2. Setup Vector v (using LaTeX for maximum compatibility)
        v_label = MathTex(r"\mathbf{v} = ").next_to(image_rect, RIGHT, buff=0.5)
        v_matrix = MathTex(
            r"\begin{bmatrix} 0.82 \\ -0.15 \\ \vdots \\ 0.44 \end{bmatrix}"
        ).next_to(v_label, RIGHT)
        v_group = VGroup(v_label, v_matrix)

        # 3. Setup Matrix X (Country Embeddings)
        x_label = MathTex(r"\mathbf{X} = ").shift(RIGHT * 2.5 + UP * 1.5)
        
        # Creating a visual representation of the matrix rows
        countries = ["France", "Japan", "Brazil", "Canada", "Egypt"]
        country_labels = VGroup(*[
            Text(name, font_size=20) for name in countries
        ]).arrange(DOWN, buff=0.3)
        
        dots = MathTex(r"\vdots").next_to(country_labels, DOWN, buff=0.2)
        last_country = Text("Vietnam", font_size=20).next_to(dots, DOWN, buff=0.2)
        
        matrix_rows = VGroup(country_labels, dots, last_country)
        # Draw brackets manually to avoid Matrix class issues
        left_bracket = MathTex(r"\left[").scale(4).next_to(matrix_rows, LEFT, buff=0.1)
        right_bracket = MathTex(r"\right]").scale(4).next_to(matrix_rows, RIGHT, buff=0.1)
        
        matrix_title = Text("140 Country Descriptions", font_size=18, color=GREEN).next_to(matrix_rows, UP, buff=0.5)
        matrix_group = VGroup(left_bracket, matrix_rows, right_bracket, x_label, matrix_title).next_to(v_group, RIGHT, buff=0.8)

        # 4. Formula (Softmax)
        formula = MathTex(
            r"h(\mathbf{v};\mathbf{X}) = \frac{\exp(\mathbf{X}\mathbf{v})}{\sum_{j=1}^{N}\exp(\mathbf{X}_{j}^{T}\mathbf{v})}"
        ).scale(0.8).to_edge(DOWN, buff=0.8)

        # 5. Manual Bar Chart
        chart_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1, 0.5],
            x_length=4,
            y_length=2,
            axis_config={"include_tip": False},
            tips=False
        ).to_edge(RIGHT, buff=1).shift(DOWN * 0.5)
        
        chart_labels = VGroup(*[
            Text(name[:3], font_size=16).next_to(chart_axes.c2p(i+0.5, 0), DOWN)
            for i, name in enumerate(countries)
        ])

        # Initial flat bars
        bars = VGroup(*[
            Rectangle(
                width=0.5, 
                height=0.1, 
                fill_opacity=0.8, 
                color=BLUE, 
                stroke_width=1
            ).move_to(chart_axes.c2p(i+0.5, 0), aligned_edge=DOWN)
            for i in range(5)
        ])

        # ANIMATION
        
        # 1. Image to Vector
        self.play(FadeIn(image_group))
        self.wait(0.5)
        self.play(Write(v_label), FadeIn(v_matrix))
        self.wait(1)

        # 2. Show Matrix X
        self.play(Write(x_label), Write(matrix_title))
        self.play(FadeIn(left_bracket), FadeIn(right_bracket), FadeIn(matrix_rows))
        self.wait(1)

        # 3. Pulsing Dot Product Highlight
        row_highlight = SurroundingRectangle(country_labels[0], color=YELLOW, buff=0.1)
        v_highlight = SurroundingRectangle(v_matrix, color=YELLOW, buff=0.1)
        
        self.play(Create(v_highlight), Create(row_highlight))
        self.play(row_highlight.animate.move_to(country_labels[1]), run_time=0.4)
        self.play(row_highlight.animate.move_to(country_labels[2]), run_time=0.4)
        self.play(FadeOut(row_highlight), FadeOut(v_highlight))

        # 4. Show Formula
        self.play(Write(formula))
        self.wait(1)

        # 5. Show Bar Chart and predict France
        self.play(Create(chart_axes), FadeIn(chart_labels))
        self.play(Create(bars))
        self.wait(0.5)
        
        # Animate Softmax Result (France index 0 shoots up)
        final_heights = [1.8, 0.2, 0.3, 0.15, 0.25] # Scaled to chart_axes y_length
        self.play(*[
            bars[i].animate.stretch_to_fit_height(final_heights[i]).move_to(chart_axes.c2p(i+0.5, 0), aligned_edge=DOWN)
            for i in range(5)
        ], run_time=2)
        
        # Highlight winner
        bars[0].set_color(YELLOW)
        winner_label = Text("Match: France", color=YELLOW, font_size=24).next_to(chart_axes, UP)
        self.play(Write(winner_label), bars[0].animate.set_fill(opacity=1))
        self.play(Indicate(winner_label))

        self.wait(2)