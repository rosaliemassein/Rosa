from manim import *
import numpy as np

class ZeroShotClassification(Scene):
    def construct(self):
        # 1. Setup Image Placeholder and Image Vector 'v'
        # Using a Rectangle for the image to ensure the code runs without external assets
        image_rect = Rectangle(height=3, width=3, color=WHITE).to_edge(LEFT, buff=1)
        image_text = MathTex(r"\text{Image}").move_to(image_rect)
        image_group = VGroup(image_rect, image_text)

        v_label = MathTex(r"\mathbf{v}", color=RED).next_to(image_group, RIGHT, buff=0.5)
        # Representing vector as a small vertical array of values
        v_repr = MathTex(r"\begin{bmatrix} 0.8 \\ 0.1 \\ \vdots \\ 0.05 \end{bmatrix}").scale(0.8).next_to(v_label, RIGHT)
        v_group = VGroup(v_label, v_repr)

        # 2. Matrix 'X' with country descriptions using MathTex
        # This replaces the 'Matrix' class to avoid identifier issues
        matrix_x = MathTex(
            r"\mathbf{X} = \begin{bmatrix} \text{France} \\ \text{USA} \\ \vdots \\ \text{Nigeria} \end{bmatrix}"
        ).scale(0.9).to_edge(RIGHT, buff=1)

        # 3. Formula for Softmax Prediction
        formula = MathTex(
            r"h(\mathbf{v};\mathbf{X})=\frac{\exp(\mathbf{X}\mathbf{v})}{\sum_{j=1}^{N}\exp(\mathbf{X}_{j}^{T}\mathbf{v})}"
        ).scale(0.75).to_edge(UP, buff=0.5)

        # 4. Bar Chart for Softmax results (using Axes and Rectangles)
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 1, 0.5],
            x_length=4,
            y_length=2,
            axis_config={"include_tip": False}
        ).to_edge(DOWN, buff=0.7)
        
        x_labels = MathTex(r"\text{France \quad USA \quad \dots \quad Nigeria}").scale(0.6).next_to(axes, DOWN, buff=0.2)

        # Create bars manually
        bar_f = Rectangle(width=0.4, height=0.1, color=BLUE, fill_opacity=0.8).move_to(axes.c2p(0.5, 0), aligned_edge=DOWN)
        bar_u = Rectangle(width=0.4, height=0.1, color=BLUE, fill_opacity=0.8).move_to(axes.c2p(1.5, 0), aligned_edge=DOWN)
        bar_o = Rectangle(width=0.4, height=0.1, color=BLUE, fill_opacity=0.8).move_to(axes.c2p(2.5, 0), aligned_edge=DOWN)
        bar_n = Rectangle(width=0.4, height=0.1, color=BLUE, fill_opacity=0.8).move_to(axes.c2p(3.5, 0), aligned_edge=DOWN)
        bars = VGroup(bar_f, bar_u, bar_o, bar_n)

        # --- Animation Sequence ---
        
        # Display initial scene
        self.play(FadeIn(image_group))
        self.play(Write(v_group))
        self.wait(0.5)

        self.play(Write(matrix_x))
        self.play(Write(formula))
        self.wait(0.5)

        # Pulsing highlight simulation for dot product
        highlight_box = SurroundingRectangle(matrix_x, color=YELLOW)
        self.play(Create(highlight_box))
        self.play(FadeOut(highlight_box))
        self.wait(0.5)

        # Show probability distribution
        self.play(Create(axes), Write(x_labels))
        self.play(FadeIn(bars))
        self.wait(0.5)

        # Softmax update: France score shoots up
        target_height_f = axes.get_top()[1] - axes.get_bottom()[1] - 0.2
        self.play(
            bar_f.animate.stretch_to_fit_height(target_height_f, about_edge=DOWN).set_color(GREEN),
            bar_u.animate.stretch_to_fit_height(0.15, about_edge=DOWN),
            bar_o.animate.stretch_to_fit_height(0.1, about_edge=DOWN),
            bar_n.animate.stretch_to_fit_height(0.12, about_edge=DOWN),
            run_time=2
        )

        # Final result text
        result_text = MathTex(r"\text{Prediction: France}", color=GREEN).scale(0.8).next_to(formula, DOWN, buff=0.2)
        self.play(Write(result_text))
        
        self.wait(2)