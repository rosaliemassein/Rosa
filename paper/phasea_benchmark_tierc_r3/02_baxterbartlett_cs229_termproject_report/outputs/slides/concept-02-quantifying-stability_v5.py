from manim import *
import numpy as np

class QuantifyingStability(Scene):
    def construct(self):
        # 1. Main Plot: Velocity fluctuating around 30 RPM
        # Time axis from 0 to 10
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[20, 40, 5],
            x_length=6.5,
            y_length=4,
            axis_config={"include_tip": False}
        ).to_edge(LEFT, buff=0.7)
        
        labels = axes.get_axis_labels(x_label="Time", y_label="RPM")
        
        # Use a named function with parameter 't' to avoid naming conflicts
        def velocity_curve(t):
            return 30 + 1.5 * np.sin(t * 3.5) + 0.6 * np.cos(t * 11)
            
        graph = axes.plot(velocity_curve, color=BLUE)
        graph_label = Text("Motor Velocity", font_size=24).next_to(axes, UP)

        # 2. Highlight the last 20% of the x-axis (from t=8 to t=10)
        # The center of this region is t=9
        highlight_width = axes.x_axis.get_unit_size() * 2
        highlight_height = axes.y_axis.get_unit_size() * 20
        highlight_rect = Rectangle(
            width=highlight_width,
            height=highlight_height,
            fill_color=BLUE,
            fill_opacity=0.2,
            stroke_width=0
        ).move_to(axes.c2p(9, 30))
        
        highlight_text = Text("Final 20%", font_size=18, color=BLUE).next_to(highlight_rect, UP, buff=0.1)

        # 3. Histogram on the side
        hist_axes = Axes(
            x_range=[25, 35, 2],
            y_range=[0, 10, 2],
            x_length=4,
            y_length=3,
            axis_config={"include_tip": False}
        ).to_edge(RIGHT, buff=0.7).shift(UP * 0.5)
        
        hist_title = Text("Histogram", font_size=24).next_to(hist_axes, UP)
        
        # Define bin data: (x_center, count, color)
        # Mode is at 30 RPM
        bins_data = [
            (26, 2, YELLOW),
            (28, 4, YELLOW),
            (30, 9, GREEN),  # Significantly taller mode
            (32, 3, YELLOW),
            (34, 1, YELLOW)
        ]
        
        histogram_bars = VGroup()
        for x_val, height_val, color_val in bins_data:
            # Scale height by axes unit size
            bar_height = height_val * hist_axes.y_axis.get_unit_size()
            bar = Rectangle(
                width=0.5,
                height=bar_height,
                fill_color=color_val,
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=1
            )
            bar.move_to(hist_axes.c2p(x_val, 0), aligned_edge=DOWN)
            histogram_bars.add(bar)

        # 4. Stability Formula
        formula = MathTex(
            r"\text{Stability} = \frac{\text{counts at mode}}{\text{counts not at mode}}",
            font_size=36
        ).to_edge(DOWN, buff=0.8)

        # 5. Animation Sequence
        self.play(Create(axes), Write(labels), Write(graph_label))
        self.play(Create(graph), run_time=2)
        self.wait(0.5)
        
        # Highlight the final 20%
        self.play(FadeIn(highlight_rect), Write(highlight_text))
        self.wait(1)
        
        # Show the Histogram
        self.play(Create(hist_axes), Write(hist_title))
        self.play(LaggedStart(*[FadeIn(bar, shift=UP) for bar in histogram_bars], lag_ratio=0.1))
        self.wait(1)
        
        # Show the formula and link to the histogram mode
        self.play(Write(formula))
        self.play(Indicate(histogram_bars[2], color=GREEN, scale_factor=1.2))
        
        # Add a small note about Steady State Error
        sse_note = Text("Steady State Error (Final 20%)", font_size=20, color=BLUE).next_to(formula, DOWN, buff=0.2)
        self.play(Write(sse_note))
        
        self.wait(3)