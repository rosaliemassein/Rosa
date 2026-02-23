from manim import *
import numpy as np

class ConceptSlide02RegularityTradeoff(Scene):
    def construct(self):
        # 1. Setup Axes and Curves
        axes = Axes(
            x_range=[1, 10, 1],
            y_range=[0, 100, 10],
            x_length=6,
            y_length=5,
            axis_config={"include_tip": True}
        ).to_edge(LEFT, buff=0.5)
        
        axes_labels = axes.get_axis_labels(
            Tex("Number of Players").scale(0.6), 
            Tex("Mean Squared Error").scale(0.6)
        )

        # Explicit functions to avoid "x" being flagged as an undefined identifier in lambdas
        def get_knn_val(t_val):
            # Dips then rises sharply (overfitting)
            return 4 * (t_val - 3.5)**2 + 25
        
        def get_lasso_val(t_val):
            # Steady decline
            return 85 / (t_val**0.45)

        knn_curve = axes.plot(get_knn_val, x_range=[1, 6], color=RED)
        knn_label = Tex("KNN", color=RED).scale(0.7).next_to(knn_curve, UR, buff=0.1)
        
        lasso_curve = axes.plot(get_lasso_val, x_range=[1, 10], color=GREEN)
        lasso_label = Tex("Lasso/Ridge", color=GREEN).scale(0.7).next_to(lasso_curve, RIGHT, buff=0.1)

        # 2. Formula from Prompt
        formula = MathTex(
            r"J(\theta) = \|y - X\theta\|^2 + \lambda \|\theta\|_1",
            font_size=36
        ).to_edge(UP, buff=0.5)

        # 3. Bar Chart for Coefficients (Shrinking/Vanishing)
        num_coefficients = 80
        np.random.seed(42)
        initial_vals = np.random.uniform(0.5, 3.5, num_coefficients)
        
        bars_group = VGroup()
        for v in initial_vals:
            rect = Rectangle(
                width=0.04, 
                height=v, 
                fill_opacity=0.8, 
                fill_color=BLUE, 
                stroke_width=0.5
            )
            bars_group.add(rect)
        
        bars_group.arrange(RIGHT, buff=0.02, aligned_edge=DOWN).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.5)
        
        # We need a stable reference for the baseline to re-align bars after stretching
        baseline_y_coord = bars_group.get_bottom()[1]
        
        # 4. Tracker and Updaters
        lambda_tracker_val = ValueTracker(0.0)
        
        # Using a fixed position for the label
        lambda_label_pos = bars_group.get_top() + UP * 1.2
        lambda_label_obj = MathTex(r"\lambda = 0.0").move_to(lambda_label_pos)

        # Named updater functions to avoid "m" identifier issues
        def update_label_text(target_mob):
            current_v = lambda_tracker_val.get_value()
            new_tex = MathTex(f"\\lambda = {current_v:.1f}").move_to(lambda_label_pos)
            target_mob.become(new_tex)

        def update_bars_heights(target_group):
            alpha = lambda_tracker_val.get_value()
            for index, single_bar in enumerate(target_group):
                h_orig = initial_vals[index]
                # Lasso shrinkage logic: subtract penalty, clamp at zero
                h_curr = h_orig - (alpha / 3.0)
                
                if h_curr <= 0.05:
                    single_bar.set_fill(opacity=0)
                    single_bar.set_stroke(opacity=0)
                    single_bar.stretch_to_fit_height(0.01)
                else:
                    single_bar.set_fill(opacity=0.8)
                    single_bar.set_stroke(opacity=1)
                    single_bar.stretch_to_fit_height(h_curr)
                
                # Manual re-alignment to the bottom baseline
                single_bar.set_y(baseline_y_coord + single_bar.get_height() / 2)

        # 5. Narration Text (Subtitle)
        voice_over = Text(
            "Lasso applies a penalty to coefficients,\neffectively selecting only key features.",
            font_size=20,
            color=WHITE
        ).to_edge(DOWN, buff=0.3)

        # 6. Animation Sequence
        self.add(axes, axes_labels, knn_curve, knn_label, lasso_curve, lasso_label, formula, bars_group, lambda_label_obj, voice_over)
        
        # Attach updaters before starting the animation
        lambda_label_obj.add_updater(update_label_text)
        bars_group.add_updater(update_bars_heights)
        
        # Use a simple lambda rate function to avoid "linear" identifier issue
        self.play(
            lambda_tracker_val.animate.set_value(10.0),
            run_time=8,
            rate_func=lambda t_val: t_val
        )
        self.wait(2)

        # Clean up updaters
        lambda_label_obj.remove_updater(update_label_text)
        bars_group.remove_updater(update_bars_heights)