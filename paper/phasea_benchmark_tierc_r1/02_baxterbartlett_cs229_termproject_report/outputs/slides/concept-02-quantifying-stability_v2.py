from manim import *
import numpy as np

class StabilityConcept(Scene):
    def construct(self):
        # 1. Setup Axes for Velocity Plot
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 50, 10],
            x_length=6,
            y_length=4,
            axis_config={"include_tip": False}
        ).to_edge(LEFT, buff=0.5)
        
        labels = axes.get_axis_labels(x_label="Time", y_label="RPM")
        
        # Generate noisy data around 30 RPM
        np.random.seed(42)
        x_vals = np.linspace(0, 10, 100)
        # Create a fluctuating signal around 30
        y_vals = 30 + 5 * np.sin(2 * PI * x_vals) + np.random.normal(0, 2, 100)
        
        plot = axes.plot_line_graph(x_vals, y_vals, add_vertex_dots=False, line_color=WHITE)
        
        # 2. Highlight the last 20% of the x-axis (Steady State Error area)
        highlight_rect = Rectangle(
            width=axes.x_axis.get_unit_size() * 2,
            height=axes.y_axis.get_unit_size() * 50,
            fill_color=BLUE,
            fill_opacity=0.3,
            stroke_width=0
        )
        highlight_rect.move_to(axes.c2p(9, 25)) # Centered at 90% (8 to 10)
        
        sse_label = Text("Steady State Error Region", font_size=18).next_to(highlight_rect, UP)

        # 3. Create a Histogram on the right
        # We simulate bins: 20-25, 25-35 (mode), 35-40
        hist_axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 10, 2],
            x_length=3,
            y_length=3,
            tips=False,
            axis_config={"include_numbers": False}
        ).to_edge(RIGHT, buff=1)
        
        # Rectangles representing histogram bars
        bar_widths = 0.6
        bar1 = Rectangle(width=bar_widths, height=1.0, fill_opacity=0.8, color=GRAY).move_to(hist_axes.c2p(1, 0.5))
        bar_mode = Rectangle(width=bar_widths, height=2.5, fill_opacity=0.8, color=YELLOW).move_to(hist_axes.c2p(2, 1.25))
        bar3 = Rectangle(width=bar_widths, height=0.8, fill_opacity=0.8, color=GRAY).move_to(hist_axes.c2p(3, 0.4))
        
        hist_group = VGroup(hist_axes, bar1, bar_mode, bar3)
        hist_label = Text("Frequency (Histogram)", font_size=20).next_to(hist_axes, UP)
        mode_text = Text("Mode (30 RPM)", font_size=16, color=YELLOW).next_to(bar_mode, UP, buff=0.1)

        # 4. Stability Formula
        formula = MathTex(
            r"\text{Stability} = \frac{\text{counts at mode}}{\text{counts not at mode}}",
            color=WHITE
        ).scale(0.8).to_edge(DOWN, buff=0.5)

        # --- Animations ---
        
        # Part 1: Plotting and Voiceover start
        self.play(Create(axes), Write(labels))
        self.play(Create(plot), run_time=2)
        self.wait(1)
        
        # Part 2: Steady State Error Highlight
        self.play(FadeIn(highlight_rect), Write(sse_label))
        self.wait(1)
        
        # Part 3: Histogram
        self.play(Create(hist_axes), Write(hist_label))
        self.play(
            FadeIn(bar1, shift=UP),
            FadeIn(bar_mode, shift=UP),
            FadeIn(bar3, shift=UP)
        )
        self.play(Write(mode_text))
        self.wait(1)
        
        # Part 4: Formula
        self.play(Write(formula))
        self.play(formula.animate.set_color_by_tex("Stability", YELLOW))
        self.wait(2)

        # Clean up for final message
        self.play(
            FadeOut(axes), FadeOut(plot), FadeOut(labels), 
            FadeOut(highlight_rect), FadeOut(sse_label),
            FadeOut(hist_group), FadeOut(hist_label), FadeOut(mode_text)
        )
        
        final_text = Text("Quantifying behavior for regression models", font_size=32)
        self.play(Transform(formula, final_text))
        self.wait(2)

# Ensure the script runs with: manim -pql file_name.py StabilityConcept