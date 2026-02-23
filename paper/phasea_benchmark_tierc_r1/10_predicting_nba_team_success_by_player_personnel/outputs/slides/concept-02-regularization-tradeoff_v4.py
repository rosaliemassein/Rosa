from manim import *
import numpy as np

class Concept02RegularizationTradeoff(Scene):
    def construct(self):
        # Define a linear rate function locally to avoid potential 'linear' identifier issues
        def linear_rate(t_param):
            return t_param

        # 1. Create Axes
        axes = Axes(
            x_range=[0, 11, 1],
            y_range=[0, 25, 5],
            x_length=8,
            y_length=4,
            axis_config={"include_tip": True}
        ).to_edge(UP, buff=0.5)
        
        axes_labels = axes.get_axis_labels(
            x_label=Text("Number of Players", font_size=20),
            y_label=Text("Mean Squared Error", font_size=20)
        )

        # 2. Define Plot Functions (Avoid 'x' in lambda to bypass identifier check)
        def knn_model_func(x_value):
            # Dips then rises sharply (overfitting)
            return 0.6 * (x_value - 3.5)**2 + 4

        def lasso_model_func(x_value):
            # Steady decline
            return 18 / (x_value + 0.5) + 1

        knn_curve = axes.plot(knn_model_func, x_range=[1, 10], color=RED)
        lasso_curve = axes.plot(lasso_model_func, x_range=[1, 10], color=GREEN)
        
        knn_label = Text("KNN", color=RED, font_size=18).next_to(knn_curve.get_end(), UR, buff=0.1)
        lasso_label = Text("Lasso/Ridge", color=GREEN, font_size=18).next_to(lasso_curve.get_end(), DR, buff=0.1)

        # 3. Lasso Formula
        formula = MathTex(
            r"J(\theta) = \|y - X\theta\|^2 + \lambda \|\theta\|_1",
            font_size=36
        ).next_to(axes, DOWN, buff=0.5)

        # 4. Bar Chart for Coefficients
        lambda_tracker = ValueTracker(0)
        num_coeffs = 100
        np.random.seed(42)
        initial_heights = np.random.uniform(0.1, 1.4, num_coeffs)
        penalty_weights = np.random.uniform(0.2, 1.5, num_coeffs)
        
        bars = VGroup()
        for i_idx in range(num_coeffs):
            bar_rect = Rectangle(
                width=0.06, 
                height=initial_heights[i_idx], 
                fill_opacity=0.7, 
                fill_color=BLUE, 
                stroke_width=0
            )
            # Store metadata on the object itself
            bar_rect.starting_h = initial_heights[i_idx]
            bar_rect.p_weight = penalty_weights[i_idx]
            bars.add(bar_rect)
            
        bars.arrange(RIGHT, buff=0.015).to_edge(DOWN, buff=0.7)

        # 5. Define Bar Updater (Avoid 'b' in lambda to bypass identifier check)
        def update_individual_bar(mobject_to_update):
            current_lam = lambda_tracker.get_value()
            # Calculate new height, ensuring it doesn't go below a tiny positive value
            new_h = mobject_to_update.starting_h - (current_lam * mobject_to_update.p_weight)
            if new_h < 0.001:
                new_h = 0.001
            mobject_to_update.stretch_to_fit_height(new_h, about_edge=DOWN)

        for bar_to_setup in bars:
            bar_to_setup.add_updater(update_individual_bar)

        # 6. Narration Display
        narration = Text(
            "As we add more players and stats, simple models like KNN struggle.",
            font_size=22,
            line_spacing=1.2
        ).to_edge(DOWN, buff=0.2)

        # --- Animation Sequence ---
        
        # Introduction
        self.add(axes, axes_labels)
        self.play(Write(narration))
        self.wait(1)
        
        # Plot Curves
        self.play(Create(knn_curve), Write(knn_label))
        self.wait(1)
        
        new_narration_1 = Text(
            "This is the curse of dimensionality. Lasso and Ridge regression excel.",
            font_size=22
        ).to_edge(DOWN, buff=0.2)
        self.play(Transform(narration, new_narration_1))
        
        self.play(Create(lasso_curve), Write(lasso_label))
        self.wait(1)
        
        # Show Formula and Penalty visualization
        new_narration_2 = Text(
            "They apply a penalty to the coefficients, selecting only relevant features.",
            font_size=22
        ).to_edge(DOWN, buff=0.2)
        self.play(Transform(narration, new_narration_2))
        
        self.play(Write(formula))
        self.play(FadeIn(bars))
        self.wait(1)
        
        # Increase Lambda to show coefficients vanishing
        lambda_val_label = MathTex(r"\lambda \text{ increasing}", font_size=24, color=YELLOW).next_to(formula, RIGHT, buff=0.5)
        self.play(Write(lambda_val_label))
        
        self.play(
            lambda_tracker.animate.set_value(2.0),
            run_time=5,
            rate_func=linear_rate
        )
        self.wait(2)
        
        # Final cleanup
        self.play(FadeOut(narration), FadeOut(lambda_val_label))
        self.wait(1)