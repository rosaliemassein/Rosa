import numpy as np
import math
from manim import *

class LogisticRegressionScene(Scene):
    def construct(self):
        # 1. Formula Display
        formula = MathTex(
            r"P(y=1) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 X_{1d} + \beta_{30} X_{30d})}}",
            font_size=32
        ).to_edge(UP, buff=0.5)
        self.add(formula)

        # 2. Manual Coordinate System (Custom Axes)
        # We avoid Axes and NumberPlane as per constraints
        origin_point = RIGHT * 2 + DOWN * 1.5
        x_axis = Line(origin_point + LEFT * 3, origin_point + RIGHT * 3, color=WHITE)
        y_axis = Line(origin_point, origin_point + UP * 3.5, color=WHITE)
        x_label = MathTex("z", font_size=20).next_to(x_axis, RIGHT)
        y_label = MathTex("P", font_size=20).next_to(y_axis, UP)
        self.add(x_axis, y_axis, x_label, y_label)

        # 3. Sigmoid Curve Construction
        # We manually create a curve using small Line segments
        def sigmoid(val):
            return 1 / (1 + math.exp(-val))
        
        curve = VGroup()
        curve_steps = 40
        x_vals = np.linspace(-3, 3, curve_steps)
        for i in range(curve_steps - 1):
            p1 = origin_point + RIGHT * x_vals[i] + UP * sigmoid(x_vals[i]) * 3
            p2 = origin_point + RIGHT * x_vals[i+1] + UP * sigmoid(x_vals[i+1]) * 3
            curve.add(Line(p1, p2, color=GREEN, stroke_width=4))
        self.add(curve)

        # 4. Input Bars (Memory Features)
        # Using Rectangles as the sliding bars
        bar_base_y = -3
        bar1 = Rectangle(width=0.8, height=0.2, fill_opacity=0.8, color=BLUE)
        bar1.move_to([-4.5, bar_base_y + 0.1, 0])
        
        bar2 = Rectangle(width=0.8, height=0.2, fill_opacity=0.8, color=RED)
        bar2.move_to([-3.0, bar_base_y + 0.1, 0])
        
        label1 = MathTex(r"1\text{-Day } T\text{-CSP}", font_size=18).next_to(bar1, DOWN)
        label2 = MathTex(r"30\text{-Day } T\text{-CSP}", font_size=18).next_to(bar2, DOWN)
        self.add(bar1, bar2, label1, label2)

        # 5. Prediction Dot with Updater
        # The dot moves along the sigmoid based on the height of the bars
        prediction_dot = Dot(color=YELLOW, radius=0.12)
        
        def update_prediction(mob):
            # Calculate a dummy 'z' value based on bar heights
            # Height 0.2 is our baseline
            h1 = bar1.get_height() - 0.2
            h2 = bar2.get_height() - 0.2
            # Weights beta1=1.0, beta2=1.0, beta0=-1.5
            z_val = (h1 + h2) * 1.2 - 1.5
            # Clamp z for the visual range of our graph
            z_clamped = max(min(z_val, 3), -3)
            prob = sigmoid(z_clamped)
            mob.move_to(origin_point + RIGHT * z_clamped + UP * prob * 3)

        prediction_dot.add_updater(update_prediction)
        self.add(prediction_dot)

        # 6. Animation Sequence
        self.play(FadeIn(curve), Write(formula))
        self.wait(0.5)

        # First slide: Increase inputs (Higher probability)
        self.play(
            bar1.animate.stretch_to_fit_height(2.5, about_edge=DOWN),
            bar2.animate.stretch_to_fit_height(1.8, about_edge=DOWN),
            run_time=3
        )
        self.wait(1)

        # Second slide: Decrease inputs (Lower probability)
        self.play(
            bar1.animate.stretch_to_fit_height(0.4, about_edge=DOWN),
            bar2.animate.stretch_to_fit_height(0.3, about_edge=DOWN),
            run_time=3
        )
        self.wait(1)

        # 7. Scaling the weights logic visualization
        # Transform concept: show how these features relate to probability
        prob_display = MathTex(r"P(y=1) \approx ", "0.12", font_size=36)
        prob_display.move_to(LEFT * 3.5 + UP * 1.5)
        
        # We manually update the text for the probability display
        def update_prob_text(mob):
            h1 = bar1.get_height() - 0.2
            h2 = bar2.get_height() - 0.2
            z_val = (h1 + h2) * 1.2 - 1.5
            p_val = sigmoid(z_val)
            new_text = MathTex(r"P(y=1) \approx ", f"{p_val:.2f}", font_size=36)
            new_text.move_to(LEFT * 3.5 + UP * 1.5)
            mob.become(new_text)

        prob_display.add_updater(update_prob_text)
        self.play(Write(prob_display))

        # Final movement to show responsiveness
        self.play(
            bar1.animate.stretch_to_fit_height(3.0, about_edge=DOWN),
            bar2.animate.stretch_to_fit_height(1.0, about_edge=DOWN),
            run_time=3
        )
        self.wait(2)

        # Clean up
        prediction_dot.remove_updater(update_prediction)
        prob_display.remove_updater(update_prob_text)
        self.wait(1)