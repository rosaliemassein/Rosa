from manim import *
import numpy as np

class ParameterVsDataBottleneck(Scene):
    def construct(self):
        # 1. Formula Reference
        formula = MathTex(
            r"MSE = \frac{||Y_{test} - Y_{pred}||_F^2}{3n}",
            color=WHITE
        ).scale(0.8).to_edge(UP, buff=0.3)

        # 2. Side-by-Side Axes
        # Left: Neural Network
        ax_left = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": False, "include_ticks": False}
        ).shift(LEFT * 3.5 + UP * 0.5)

        # Right: LWR
        ax_right = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": False, "include_ticks": False}
        ).shift(RIGHT * 3.5 + UP * 0.5)

        title_left = Text("Neural Network", color=RED).scale(0.5).next_to(ax_left, UP)
        title_right = Text("LWR", color=BLUE).scale(0.5).next_to(ax_right, UP)
        high_variance = Text("High Variance", color=YELLOW).scale(0.4).next_to(title_left, DOWN, buff=0.1)

        # 3. Generate Data Points (27 points)
        np.random.seed(42)
        x_data = np.linspace(1, 9, 15) # Reduced for visual clarity
        y_base = 0.5 * x_data + 2
        y_noise = np.array([0.8, -0.9, 1.2, -0.5, 0.4, -1.1, 0.7, 0.2, -0.6, 1.0, -0.3, 0.5, -0.8, 0.2, -0.4])
        y_data = y_base + y_noise

        dots_left = VGroup(*[Dot(ax_left.c2p(x, y), radius=0.05, color=WHITE) for x, y in zip(x_data, y_data)])
        dots_right = VGroup(*[Dot(ax_right.c2p(x, y), radius=0.05, color=WHITE) for x, y in zip(x_data, y_data)])

        # 4. Curves
        # NN: Highly wiggling curve fitting noise
        nn_curve = ax_left.plot(
            lambda x: 0.5 * x + 2 + 1.2 * np.sin(2.5 * x) * np.cos(1.2 * x),
            color=RED
        )
        # LWR: Smoother trend
        lwr_curve = ax_right.plot(
            lambda x: 0.5 * x + 2,
            color=BLUE
        )

        # 5. Manual Bar Chart for MSE
        # Use a small coordinate system to host bars
        ax_mse = Axes(
            x_range=[0, 3, 1],
            y_range=[0, 1.5, 0.5],
            x_length=4,
            y_length=2,
            axis_config={"include_tip": False, "font_size": 20}
        ).shift(DOWN * 2.5)

        # NN Bar (1.21)
        # Height is relative to axes: 1.21 units on y_range [0, 1.5] mapped to y_length 2
        bar_nn_height = 1.21 * (2 / 1.5)
        bar_nn = Rectangle(
            width=0.8, height=bar_nn_height, 
            fill_opacity=0.8, fill_color=RED, stroke_color=RED
        ).move_to(ax_mse.c2p(1, 0), aligned_edge=DOWN)

        # LWR Bar (0.85)
        bar_lwr_height = 0.85 * (2 / 1.5)
        bar_lwr = Rectangle(
            width=0.8, height=bar_lwr_height, 
            fill_opacity=0.8, fill_color=BLUE, stroke_color=BLUE
        ).move_to(ax_mse.c2p(2, 0), aligned_edge=DOWN)

        label_mse_nn = Text("NN: 1.21", color=RED).scale(0.4).next_to(bar_nn, UP, buff=0.1)
        label_mse_lwr = Text("LWR: 0.85", color=BLUE).scale(0.4).next_to(bar_lwr, UP, buff=0.1)
        mse_footer = Text("Mean Squared Error (MSE)", color=WHITE).scale(0.4).next_to(ax_mse, DOWN, buff=0.2)

        # 6. Animation Sequence
        self.play(Write(formula))
        self.wait(0.5)

        # Draw plots
        self.play(
            Create(ax_left), Create(ax_right),
            Write(title_left), Write(title_right)
        )
        self.play(Create(dots_left), Create(dots_right))
        self.wait(0.5)

        # Draw curves
        self.play(Create(nn_curve), Write(high_variance), run_time=2)
        self.play(Create(lwr_curve), run_time=2)
        self.wait(1)

        # Draw Bar Chart
        self.play(Create(ax_mse), Write(mse_footer))
        self.play(
            Create(bar_nn), Create(bar_lwr),
            Write(label_mse_nn), Write(label_mse_lwr)
        )
        
        # Narration Overlay
        narration = Text(
            "Neural Network memorized noise due to small sample size.",
            slant="ITALIC", color=GRAY_A
        ).scale(0.4).to_edge(DOWN, buff=0.1)
        self.play(FadeIn(narration))

        self.wait(3)