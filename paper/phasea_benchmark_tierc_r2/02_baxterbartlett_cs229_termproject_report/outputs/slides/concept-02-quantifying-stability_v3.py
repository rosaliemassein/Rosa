from manim import *
import numpy as np

class StabilityExplanation(Scene):
    def construct(self):
        # 1. Create a velocity plot (motor fluctuating around 30 RPM)
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 60, 10],
            x_length=6,
            y_length=4,
            axis_config={"include_tip": False, "color": WHITE}
        ).to_edge(LEFT, buff=0.5)
        
        y_label = Text("RPM", font_size=20).next_to(axes.y_axis, UP)
        x_label = Text("Time", font_size=20).next_to(axes.x_axis, RIGHT)
        
        # Use a named function instead of a lambda to avoid 'x' identifier issues in some environments
        def velocity_curve(time_value):
            return 30 + 5 * np.sin(2 * time_value) + 2 * np.cos(5 * time_value)
            
        plot = axes.plot(velocity_curve, color=BLUE)
        
        self.play(Create(axes), Write(y_label), Write(x_label))
        self.play(Create(plot), run_time=2)
        self.wait(0.5)

        # 2. Highlight the last 20% of the x-axis (from 8 to 10)
        # Calculate coordinates for the rectangle
        start_point = axes.c2p(8, 0)
        end_point = axes.c2p(10, 60)
        
        highlight_rect = Rectangle(
            width=abs(end_point[0] - start_point[0]),
            height=abs(end_point[1] - start_point[1]),
            fill_color=BLUE,
            fill_opacity=0.3,
            stroke_width=0
        ).move_to(axes.c2p(9, 30))
        
        steady_state_text = Text("Final 20%", font_size=16, color=BLUE).next_to(highlight_rect, UP)
        
        self.play(FadeIn(highlight_rect), Write(steady_state_text))
        self.wait(1)

        # 3. Histogram appearing on the side
        hist_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 10, 2],
            x_length=3,
            y_length=3,
            axis_config={"include_tip": False}
        ).to_edge(RIGHT, buff=0.7).shift(UP * 0.5)
        
        # heights representing counts, the middle one (30 RPM) is tall
        heights = [1.5, 2.5, 7.5, 3.5, 1.2]
        bins = VGroup()
        for i in range(5):
            h_val = heights[i]
            # Map index to color: index 2 is the 'mode'
            bar_color = YELLOW if i == 2 else GRAY
            # Calculate height in scene units
            h_unit = h_val * (hist_axes.y_axis.get_unit_size())
            rect = Rectangle(
                width=0.4,
                height=h_unit,
                fill_color=bar_color,
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=1
            )
            rect.move_to(hist_axes.c2p(i + 0.5, 0), aligned_edge=DOWN)
            bins.add(rect)
            
        hist_title = Text("Histogram", font_size=20).next_to(hist_axes, UP)
        mode_label = Text("Mode", font_size=16, color=YELLOW).next_to(bins[2], UP, buff=0.1)

        self.play(Create(hist_axes), Write(hist_title))
        self.play(Create(bins), Write(mode_label))
        self.wait(1)

        # 4. Animate a fraction bar to define Stability
        # Stability = counts at mode / counts not at mode
        stability_formula = MathTex(
            "Stability", "=", "{ \\text{counts at mode} ", "\\over", " \\text{counts not at mode} }",
            font_size=32
        ).to_edge(DOWN, buff=1)
        
        self.play(Write(stability_formula[0:2])) # "Stability ="
        
        # Visual link: Highlight the mode bin and show numerator
        self.play(
            bins[2].animate.set_stroke(YELLOW, width=4),
            Write(stability_formula[2])
        )
        self.play(Write(stability_formula[3])) # Fraction bar
        
        # Visual link: Highlight other bins and show denominator
        other_bins = VGroup(bins[0], bins[1], bins[3], bins[4])
        self.play(
            other_bins.animate.set_stroke(RED, width=2),
            Write(stability_formula[4])
        )
        
        self.wait(3)