from manim import *
import numpy as np

class LogisticRegressionFeatures(Scene):
    def construct(self):
        # Create Axes for the sigmoid curve
        axes = Axes(
            x_range=[-6, 6, 2],
            y_range=[0, 1.2, 0.5],
            x_length=6,
            y_length=4,
            axis_config={"include_tip": True}
        ).to_edge(RIGHT, buff=0.5)
        
        # Sigmoid curve function
        def sigmoid(x):
            return 1 / (1 + np.exp(-x))

        sigmoid_curve = axes.plot(sigmoid, color=BLUE)
        curve_label = MathTex(r"P(y=1)", font_size=24, color=BLUE).next_to(axes, UP)
        
        self.play(Create(axes), Create(sigmoid_curve), Write(curve_label))

        # Value trackers for the two features
        val_1d = ValueTracker(0)
        val_30d = ValueTracker(0)

        # UI for features (Sliding Bars)
        bar_height = 3
        bar_width = 0.5
        
        bg_1d = Rectangle(width=bar_width, height=bar_height, stroke_color=WHITE).shift(LEFT * 4.5)
        bg_30d = Rectangle(width=bar_width, height=bar_height, stroke_color=WHITE).shift(LEFT * 3.2)
        
        label_1d = Text("1-Day T-CSP", font_size=16).next_to(bg_1d, DOWN)
        label_30d = Text("30-Day T-CSP", font_size=16).next_to(bg_30d, DOWN)

        # Bar fills that respond to value trackers
        # Mapping tracker range [-3, 3] to bar height [0, bar_height]
        fill_1d = always_redraw(lambda: Rectangle(
            width=bar_width,
            height=np.clip(np.interp(val_1d.get_value(), [-3, 3], [0, bar_height]), 0.01, bar_height),
            fill_color=YELLOW,
            fill_opacity=0.7,
            stroke_width=0
        ).move_to(bg_1d.get_bottom(), aligned_edge=DOWN))

        fill_30d = always_redraw(lambda: Rectangle(
            width=bar_width,
            height=np.clip(np.interp(val_30d.get_value(), [-3, 3], [0, bar_height]), 0.01, bar_height),
            fill_color=ORANGE,
            fill_opacity=0.7,
            stroke_width=0
        ).move_to(bg_30d.get_bottom(), aligned_edge=DOWN))

        self.play(
            Create(bg_1d), Create(bg_30d),
            Write(label_1d), Write(label_30d)
        )
        self.add(fill_1d, fill_30d)

        # Dot on the curve representing current prediction
        # Formula: z = X_1d + X_30d (assuming weights = 1 for simplicity)
        dot = always_redraw(lambda: Dot(
            point=axes.c2p(val_1d.get_value() + val_30d.get_value(), sigmoid(val_1d.get_value() + val_30d.get_value())),
            color=GREEN
        ))
        
        self.play(Create(dot))

        # Animate sliding bars and moving dot
        self.play(val_1d.animate.set_value(2), run_time=1.5)
        self.wait(0.5)
        self.play(val_30d.animate.set_value(2), run_time=1.5)
        self.wait(0.5)
        self.play(val_1d.animate.set_value(-2.5), val_30d.animate.set_value(-1), run_time=2)
        self.wait(0.5)

        # Mathematical Formula
        formula = MathTex(
            "P(y=1) = \\frac{1}{1 + e^{-(\\beta_0 + \\beta_1 X_{1d} + \\beta_{30} X_{30d})}}",
            font_size=32
        ).to_edge(UP, buff=0.3)
        
        # Simplified vector version
        formula_vector = MathTex(
            "P(y=1) = \\frac{1}{1 + e^{-\\theta^T X}}",
            font_size=32
        ).to_edge(UP, buff=0.3)

        self.play(Write(formula))
        self.wait(1)
        
        # Transform the formula to show the abstraction
        # Using ReplacementTransform as a robust alternative to TransformMatchingTex
        self.play(ReplacementTransform(formula, formula_vector))
        self.wait(1)

        # Closing animation: slide bars to show mapping
        self.play(val_1d.animate.set_value(1.0), val_30d.animate.set_value(1.5), run_time=2)
        
        final_msg = Text("Memory features scale weights for prediction.", font_size=24).to_edge(DOWN)
        self.play(Write(final_msg))
        self.wait(2)