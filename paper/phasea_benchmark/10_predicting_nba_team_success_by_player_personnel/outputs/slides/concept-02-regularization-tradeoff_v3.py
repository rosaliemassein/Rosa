from manim import *
import numpy as np

class RegularizationTradeoff(Scene):
    def construct(self):
        # 1. Main Plot Setup (MSE vs Dimensions)
        axes = Axes(
            x_range=[0, 11, 1],
            y_range=[0, 12, 2],
            x_length=6,
            y_length=4,
            axis_config={"include_tip": True}
        ).to_edge(LEFT, buff=0.5).shift(DOWN * 0.5)

        x_label = Tex("Number of Players", font_size=24).next_to(axes.x_axis, DOWN)
        y_label = Tex("Mean Squared Error", font_size=24).rotate(90 * DEGREES).next_to(axes.y_axis, LEFT)
        axes_labels = VGroup(x_label, y_label)

        # KNN Curve: Overfitting visualization (dips then rises sharply)
        def knn_fn(t):
            return 0.4 * (t - 3.5)**2 + 1.5
        
        knn_curve = axes.plot(
            knn_fn,
            x_range=[1, 10],
            color=RED
        )
        knn_tag = Tex("KNN", color=RED, font_size=24).next_to(knn_curve.get_end(), UR, buff=0.1)

        # Lasso/Ridge Curve: Regularization visualization (steady decline)
        def lasso_fn(t):
            return 9 * np.exp(-0.2 * t) + 0.5
            
        lasso_curve = axes.plot(
            lasso_fn,
            x_range=[1, 10],
            color=GREEN
        )
        lasso_tag = Tex("Lasso / Ridge", color=GREEN, font_size=24).next_to(lasso_curve.get_end(), DR, buff=0.1)

        # 2. Title and Formula
        title = Text("Regularization Tradeoff", font_size=32).to_edge(UP, buff=0.3)
        lasso_formula = MathTex(
            r"J(\theta) = \|y - X\theta\|^2 + \lambda \|\theta\|_1",
            font_size=36
        ).next_to(title, DOWN, buff=0.3)

        # 3. Coefficient Shrinkage Visualization (Right Side)
        num_coeffs = 100 
        coeff_axes = Axes(
            x_range=[0, num_coeffs, 10],
            y_range=[0, 5, 1],
            x_length=5,
            y_length=3,
            tips=False,
            axis_config={"include_numbers": False}
        ).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.5)
        
        coeff_title = Tex("Coefficients $\\theta$", font_size=24).next_to(coeff_axes, UP)
        
        np.random.seed(42)
        initial_heights = np.random.uniform(0.1, 4.0, num_coeffs)
        
        lambda_val = ValueTracker(0)

        # Bars representing coefficients
        bars = VGroup()
        for i in range(num_coeffs):
            h_init = initial_heights[i]
            # Use line to represent the coefficient magnitude
            bar = Line(
                coeff_axes.c2p(i, 0),
                coeff_axes.c2p(i, h_init),
                color=GREEN,
                stroke_width=1.5
            )
            bar.initial_h = h_init
            bar.idx = i
            bars.add(bar)

        # Updater to simulate Lasso shrinkage: coeff = max(0, original - lambda)
        def update_coeff_bars(m):
            current_lambda = lambda_val.get_value()
            for b in m:
                new_h = max(0, b.initial_h - current_lambda)
                b.put_start_and_end_on(
                    coeff_axes.c2p(b.idx, 0),
                    coeff_axes.c2p(b.idx, new_h)
                )
                if new_h <= 0:
                    b.set_stroke(opacity=0)
                else:
                    b.set_stroke(opacity=0.7)

        bars.add_updater(update_coeff_bars)

        lambda_display = always_redraw(lambda: 
            MathTex(f"\\lambda = {lambda_val.get_value():.2f}", font_size=30, color=YELLOW)
            .next_to(coeff_axes, DOWN)
        )

        # 4. Rendering
        self.add(axes, axes_labels, title, lasso_formula)
        self.play(Create(knn_curve), Write(knn_tag))
        self.play(Create(lasso_curve), Write(lasso_tag))
        self.wait(0.5)

        self.play(
            Create(coeff_axes), 
            Write(coeff_title),
            Create(bars),
            Write(lambda_display)
        )
        
        # Animate lambda increasing to show coefficients vanishing (Lasso feature selection)
        self.play(
            lambda_val.animate.set_value(3.5),
            run_time=8,
            rate_func=lambda t: t # Linear transition
        )
        self.wait(2)