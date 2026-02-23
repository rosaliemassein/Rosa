from manim import *
import numpy as np

class LogisticRegressionFeatures(Scene):
    def construct(self):
        # 1. Setup Axes and Sigmoid Curve (Right Side)
        axes = Axes(
            x_range=[-6, 6, 2],
            y_range=[0, 1.1, 0.5],
            x_length=6,
            y_length=4,
            axis_config={"include_tip": True},
            tips=False
        ).to_edge(RIGHT, buff=0.5)
        
        y_label = axes.get_y_axis_label("P(y=1)", edge=UP, direction=UP).scale(0.8)
        x_label = axes.get_x_axis_label("z", edge=RIGHT, direction=RIGHT).scale(0.8)
        
        def sigmoid_func(x):
            return 1 / (1 + np.exp(-x))
        
        sigmoid_curve = axes.plot(sigmoid_func, color=BLUE)
        
        # 2. Trackers for Features
        # X1 is 1-Day gap, X30 is 30-Day gap
        x1_tracker = ValueTracker(0)
        x30_tracker = ValueTracker(0)
        
        # Weights (fixed for visualization)
        beta0, beta1, beta30 = 0, 1.0, 1.0

        # 3. Sliders (Left Side)
        def create_slider(label_text, tracker, color, pos):
            # Track from -3 to 3
            line = Line(DOWN * 1.5, UP * 1.5, color=GRAY_C).move_to(pos)
            label = Text(label_text, font_size=18).next_to(line, UP)
            
            # Dot represents the current value on the slider
            knob = always_redraw(lambda: Dot(
                line.point_from_proportion(np.clip((tracker.get_value() + 3) / 6, 0, 1)),
                color=color
            ))
            
            # Value display
            val_tex = always_redraw(lambda: DecimalNumber(
                tracker.get_value(), num_decimal_places=1, font_size=16
            ).next_to(knob, RIGHT))
            
            return VGroup(line, label, knob, val_tex)

        slider1 = create_slider("1-Day T-CSP", x1_tracker, RED, LEFT * 5 + UP * 0.5)
        slider30 = create_slider("30-Day T-CSP", x30_tracker, GREEN, LEFT * 3 + UP * 0.5)

        # 4. The moving dot on the sigmoid curve
        # z = beta0 + beta1*x1 + beta30*x30
        dot_on_curve = always_redraw(lambda: Dot(
            axes.c2p(
                beta0 + beta1 * x1_tracker.get_value() + beta30 * x30_tracker.get_value(),
                sigmoid_func(beta0 + beta1 * x1_tracker.get_value() + beta30 * x30_tracker.get_value())
            ),
            color=YELLOW
        ))

        # Horizontal and Vertical projection lines for the dot
        h_line = always_redraw(lambda: axes.get_horizontal_line(dot_on_curve.get_center(), color=YELLOW, line_func=Line))
        v_line = always_redraw(lambda: axes.get_vertical_line(dot_on_curve.get_center(), color=YELLOW, line_func=Line))

        # 5. Formulas
        formula = MathTex(
            "P(y=1) = \\frac{1}{1 + e^{-(\\beta_0 + \\beta_1 X_{1d} + \\beta_{30} X_{30d})}}",
            font_size=36
        ).to_edge(DOWN, buff=0.8)

        # 6. Animation sequence
        self.add(axes, x_label, y_label, sigmoid_curve)
        self.add(slider1, slider30, dot_on_curve, h_line, v_line, formula)
        
        self.play(Write(formula))
        self.wait(1)

        # Animate change in 1-day feature
        self.play(x1_tracker.animate.set_value(2.5), run_time=2)
        self.wait(0.5)
        
        # Animate change in 30-day feature
        self.play(x30_tracker.animate.set_value(1.5), run_time=2)
        self.wait(1)
        
        # Animate both moving back (simulating a drop in gap)
        self.play(
            x1_tracker.animate.set_value(-2.0),
            x30_tracker.animate.set_value(-2.5),
            run_time=3
        )
        self.wait(2)