from manim import *
import numpy as np

class ParameterVsDataBottleneck(Scene):
    def construct(self):
        # 1. Setup Axes for Side-by-Side plots
        # Using simple Axes and manual positioning to ensure compatibility
        ax_nn = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 5, 1],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": False}
        ).to_edge(LEFT, buff=0.5).shift(UP * 0.8)

        ax_lwr = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 5, 1],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": False}
        ).to_edge(RIGHT, buff=0.5).shift(UP * 0.8)

        # 2. Shared Data Points
        np.random.seed(42)
        x_vals = np.linspace(1, 9, 27)
        noise = np.random.normal(0, 0.4, 27)
        y_vals = 0.5 * x_vals + noise
        
        dots_left = VGroup(*[Dot(ax_nn.c2p(x, y), radius=0.04, color=WHITE) for x, y in zip(x_vals, y_vals)])
        dots_right = VGroup(*[Dot(ax_lwr.c2p(x, y), radius=0.04, color=WHITE) for x, y in zip(x_vals, y_vals)])

        # 3. Curves
        # Neural Network: Overfitting (High Variance)
        # Using a high-frequency sine wave to simulate "wiggling" through points
        nn_curve = ax_nn.plot(
            lambda x: 0.5 * x + 0.6 * np.sin(4 * x) * np.cos(1.5 * x),
            color=RED
        )
        nn_label = Text("Neural Network\n(High Variance)", font_size=20, color=RED).next_to(ax_nn, UP)

        # LWR: Smoother, local linear approximation
        lwr_curve = ax_lwr.plot(
            lambda x: 0.5 * x,
            color=GREEN
        )
        lwr_label = Text("LWR\n(Robust)", font_size=20, color=GREEN).next_to(ax_lwr, UP)

        # 4. MSE Formula
        formula = MathTex(
            r"MSE = \frac{||Y_{test} - Y_{pred}||_F^2}{3n}",
            font_size=30
        ).to_edge(UP, buff=0.1)

        # 5. Manual Bar Chart (Replacing BarChart to avoid undefined identifier error)
        # Scale for bars: y_range [0, 1.5] mapped to y_length 2.5
        chart_origin = DOWN * 2.5 + LEFT * 1.5
        
        # Neural Network Bar
        bar_nn = Rectangle(height=1.21 * 1.5, width=0.8, fill_opacity=0.8, fill_color=RED, stroke_color=RED)
        bar_nn.move_to(chart_origin + RIGHT * 0, aligned_edge=DOWN)
        
        # LWR Bar
        bar_lwr = Rectangle(height=0.85 * 1.5, width=0.8, fill_opacity=0.8, fill_color=GREEN, stroke_color=GREEN)
        bar_lwr.move_to(chart_origin + RIGHT * 2, aligned_edge=DOWN)
        
        # Bar Labels
        label_nn = Text("NN (1.21)", font_size=18).next_to(bar_nn, DOWN)
        label_lwr = Text("LWR (0.85)", font_size=18).next_to(bar_lwr, DOWN)
        chart_title = Text("Test MSE (Lower is Better)", font_size=20).next_to(bar_nn, UP, buff=1.5).shift(RIGHT)

        # 6. Animation
        self.play(
            Create(ax_nn), 
            Create(ax_lwr),
            Write(nn_label),
            Write(lwr_label),
            Write(formula)
        )
        self.wait(0.5)

        # Show data points
        self.play(Create(dots_left), Create(dots_right))
        self.wait(0.5)

        # Show learning/fitting curves
        self.play(Create(nn_curve), run_time=2)
        self.play(Create(lwr_curve), run_time=2)
        self.wait(1)

        # Show Bar Chart Comparison
        self.play(
            Create(bar_nn), 
            Create(bar_lwr), 
            Write(label_nn), 
            Write(label_lwr),
            Write(chart_title)
        )
        
        # Final Narration Text
        narration = Text(
            "NN memorizes noise due to high parameter-to-data ratio.",
            font_size=20, color=BLUE
        ).to_edge(DOWN, buff=0.1)
        self.play(FadeIn(narration))

        self.wait(3)