from manim import *
import numpy as np

class ZeroShotClassification(Scene):
    def construct(self):
        voice_text = "Once the model is trained, we can use it as a zero-shot classifier..."
        
        # 1. Setup Image Placeholder
        image_rect = Rectangle(height=3, width=4, color=GRAY).shift(LEFT * 4 + UP * 1.5)
        image_label = Text("Input Image", font_size=24).move_to(image_rect)
        image_group = VGroup(image_rect, image_label)
        
        # 2. Manual construction of Vector v (instead of using Matrix class)
        v_elements = VGroup(
            MathTex("0.1"), MathTex("0.8"), MathTex("0.3"), MathTex("\\vdots"), MathTex("0.5")
        ).arrange(DOWN, buff=0.2)
        v_bracket_l = MathTex("[").scale(2.5).next_to(v_elements, LEFT, buff=0.1)
        v_bracket_r = MathTex("]").scale(2.5).next_to(v_elements, RIGHT, buff=0.1)
        v_vector = VGroup(v_bracket_l, v_elements, v_bracket_r).scale(0.7).next_to(image_rect, RIGHT, buff=0.5)
        v_label = MathTex("\\mathbf{v}").next_to(v_vector, UP)

        self.play(FadeIn(image_group))
        self.play(Create(v_vector), Write(v_label))

        # 3. Manual construction of Matrix X (Country Names)
        countries = ["France", "Japan", "USA", "Brazil", "China"]
        x_elements = VGroup(*[Text(c, font_size=20) for c in countries])
        x_elements.add(MathTex("\\vdots", font_size=24))
        x_elements.add(Text("Norway", font_size=20))
        x_elements.arrange(DOWN, buff=0.25)
        
        x_bracket_l = MathTex("[").scale(4).next_to(x_elements, LEFT, buff=0.1)
        x_bracket_r = MathTex("]").scale(4).next_to(x_elements, RIGHT, buff=0.1)
        matrix_X = VGroup(x_bracket_l, x_elements, x_bracket_r).scale(0.8).next_to(v_vector, RIGHT, buff=1)
        X_label = MathTex("\\mathbf{X}").next_to(matrix_X, UP)
        
        self.play(Create(matrix_X), Write(X_label))

        # 4. Highlight Dot Product
        # Highlight first row of X and vector v
        highlight_row = SurroundingRectangle(x_elements[0], color=YELLOW, buff=0.1)
        highlight_v = SurroundingRectangle(v_elements, color=YELLOW, buff=0.1)
        
        dot_expr = MathTex("\\mathbf{X}\\mathbf{v}").to_edge(DOWN, buff=1.2)
        
        self.play(Write(dot_expr))
        for _ in range(2):
            self.play(Create(highlight_row), Create(highlight_v), run_time=0.4)
            self.play(FadeOut(highlight_row), FadeOut(highlight_v), run_time=0.4)

        # 5. Bar Chart for Softmax
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 1, 0.5],
            x_length=4,
            y_length=2.5,
            axis_config={"include_tip": False}
        ).to_edge(RIGHT, buff=0.5).shift(DOWN * 1.2)
        
        chart_labels = VGroup(*[
            Text(countries[i], font_size=14).next_to(axes.c2p(i+1, 0), DOWN)
            for i in range(len(countries))
        ])

        # Create bars as individual Rectangles
        bars = VGroup()
        for i in range(len(countries)):
            bar = Rectangle(
                width=0.4, 
                height=0.1, 
                fill_opacity=0.8, 
                fill_color=BLUE
            ).move_to(axes.c2p(i+1, 0), aligned_edge=DOWN)
            bars.add(bar)

        self.play(Create(axes), Write(chart_labels), Create(bars))

        # 6. Animation: Bars update and formula transforms
        target_heights = [0.8, 0.1, 0.15, 0.05, 0.1]
        bar_animations = []
        for i, bar in enumerate(bars):
            # Scale rectangle height relative to axes
            new_height = target_heights[i] * (axes.c2p(0, 1)[1] - axes.c2p(0, 0)[1])
            new_bar = Rectangle(
                width=0.4, 
                height=max(new_height, 0.01), 
                fill_opacity=0.8, 
                fill_color=RED if i == 0 else BLUE
            ).move_to(axes.c2p(i+1, 0), aligned_edge=DOWN)
            bar_animations.append(Transform(bar, new_bar))

        softmax_formula = MathTex(
            "h(\\mathbf{v};\\mathbf{X}) = \\frac{\\exp(\\mathbf{X}\\mathbf{v})}{\\sum_{j=1}^{N}\\exp(\\mathbf{X}_{j}^{T}\\mathbf{v})}"
        ).scale(0.75).move_to(dot_expr)

        self.play(
            *bar_animations,
            Transform(dot_expr, softmax_formula),
            run_time=2
        )

        # 7. Conclusion Label
        pred_text = Text("Prediction: France", font_size=24, color=RED).next_to(bars[0], UP, buff=0.5)
        self.play(Write(pred_text))
        
        self.wait(2)