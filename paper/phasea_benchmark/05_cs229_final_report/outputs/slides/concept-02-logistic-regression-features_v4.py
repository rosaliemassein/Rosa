from manim import *
import numpy as np

class LogisticRegressionFeatures(Scene):
    def construct(self):
        # 1. Background and Axes
        plane = NumberPlane(background_line_style={"stroke_opacity": 0.1})
        self.add(plane)

        axes = Axes(
            x_range=[-6, 6, 1],
            y_range=[0, 1.1, 0.5],
            x_length=6,
            y_length=4,
            axis_config={"include_tip": True}
        ).to_edge(RIGHT, buff=0.5)
        
        axes_labels = axes.get_axis_labels(x="z", y="P(y=1)")
        
        def sigmoid_func(x):
            return 1 / (1 + np.exp(-x))
        
        sigmoid_curve = axes.plot(sigmoid_func, color=BLUE)
        self.play(Create(axes), Create(axes_labels))
        self.play(Create(sigmoid_curve))

        # 2. Value Trackers for Features
        val_1d = ValueTracker(0)
        val_30d = ValueTracker(0)

        # 3. Create Sliders manually using always_redraw to avoid updater parameter issues
        def create_slider_group(tracker, label_text, color, pos):
            track = Line(pos + DOWN*1.5, pos + UP*1.5, color=GREY)
            label = Text(label_text, font_size=20).next_to(track, UP)
            
            # Knob uses always_redraw instead of add_updater(lambda m: ...)
            knob = always_redraw(lambda: 
                Dot(color=color).move_to(track.point_from_proportion(tracker.get_value()/5))
            )
            
            # Value display
            val_disp = always_redraw(lambda:
                DecimalNumber(tracker.get_value(), num_decimal_places=1)
                .scale(0.6)
                .next_to(knob, RIGHT)
            )
            
            return VGroup(track, label, knob, val_disp)

        slider_1d_group = create_slider_group(val_1d, "1-Day T-CSP", GREEN, LEFT * 5 + DOWN * 0.5)
        slider_30d_group = create_slider_group(val_30d, "30-Day T-CSP", RED, LEFT * 3 + DOWN * 0.5)

        self.play(FadeIn(slider_1d_group), FadeIn(slider_30d_group))

        # 4. Logistic Formula
        # Using specific coefficients for the demonstration
        beta0, beta1, beta30 = -2.0, 0.8, 0.4
        
        formula = MathTex(
            "P(y=1) = \\frac{1}{1 + e^{-(\\beta_0 + \\beta_1 X_{1d} + \\beta_{30} X_{30d})}}",
            font_size=36
        ).to_edge(UP)

        formula_with_coeffs = MathTex(
            f"P(y=1) = \\frac{{1}}{{1 + e^{{ -({beta0} + {beta1} X_{{1d}} + {beta30} X_{{30d}}) }}}}",
            font_size=36
        ).to_edge(UP)

        self.play(Write(formula))
        self.wait(1)
        # Using ReplacementTransform as a robust alternative to TransformMatchingTex
        self.play(ReplacementTransform(formula, formula_with_coeffs))
        self.wait(1)

        # 5. The Moving Dot on Sigmoid Curve
        def get_current_z():
            return beta0 + beta1 * val_1d.get_value() + beta30 * val_30d.get_value()

        moving_dot = always_redraw(lambda:
            Dot(axes.c2p(get_current_z(), sigmoid_func(get_current_z())), color=YELLOW)
        )
        
        prob_label = always_redraw(lambda:
            DecimalNumber(sigmoid_func(get_current_z()), num_decimal_places=2, color=YELLOW)
            .scale(0.7)
            .next_to(moving_dot, UR, buff=0.1)
        )

        self.play(FadeIn(moving_dot), FadeIn(prob_label))

        # 6. Interaction Animation
        # Scenario: Increasing the 1-day temperature gap
        self.play(val_1d.animate.set_value(4.5), run_time=3)
        self.wait(1)
        
        # Scenario: Increasing the 30-day "memory" gap
        self.play(val_30d.animate.set_value(4.0), run_time=3)
        self.wait(1)

        # Scenario: Returning to normal
        self.play(
            val_1d.animate.set_value(1.0),
            val_30d.animate.set_value(0.5),
            run_time=3
        )
        self.wait(2)

        # Final Summary Text
        summary = Text(
            "Features scale weights to determine probability",
            font_size=24, color=WHITE
        ).to_edge(DOWN, buff=0.3)
        self.play(Write(summary))
        self.wait(2)