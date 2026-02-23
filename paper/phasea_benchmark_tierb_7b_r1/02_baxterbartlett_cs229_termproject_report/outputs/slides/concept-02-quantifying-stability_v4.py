from manim import *

class StabilityExplanation(Scene):
    def construct(self):
        # 1. Manual Coordinate System for Velocity Plot
        # Origin for plot (Bottom Left)
        plot_origin = LEFT * 5.5 + DOWN * 1.5
        x_len = 5.0
        y_len = 4.0
        
        x_axis = Line(plot_origin, plot_origin + RIGHT * x_len, color=WHITE)
        y_axis = Line(plot_origin, plot_origin + UP * y_len, color=WHITE)
        
        x_label = MathTex(r"Time (s)", font_size=24).next_to(x_axis, DOWN)
        y_label = MathTex(r"RPM", font_size=24).next_to(y_axis, LEFT)
        
        velocity_data = [30, 28, 31, 30, 29, 30, 30, 31, 30, 28,
                         32, 30, 29, 30, 31, 30, 30, 32, 30, 30]
        
        # Mapping function: time 0-20 -> x_len, rpm 25-35 -> y_len
        def get_plot_coords(t, v):
            x_val = plot_origin[0] + (t / 20.0) * x_len
            y_val = plot_origin[1] + ((v - 25.0) / 10.0) * y_len
            return [x_val, y_val, 0]

        dots = VGroup(*[
            Dot(get_plot_coords(i, velocity_data[i]), radius=0.06, color=YELLOW) 
            for i in range(len(velocity_data))
        ])
        
        self.play(Create(x_axis), Create(y_axis), Write(x_label), Write(y_label))
        self.play(Create(dots), run_time=2)
        self.wait()

        # 2. Highlight last 20% (time 16 to 20)
        h_start = get_plot_coords(16, 25)
        h_end = get_plot_coords(20, 35)
        highlight_rect = Rectangle(
            width=h_end[0] - h_start[0],
            height=h_end[1] - h_start[1],
            fill_color=BLUE,
            fill_opacity=0.3,
            stroke_width=0
        ).move_to([ (h_start[0] + h_end[0])/2, (h_start[1] + h_end[1])/2, 0])
        
        ss_text = Text("Last 20%", font_size=18, color=BLUE).next_to(highlight_rect, UP)
        self.play(FadeIn(highlight_rect), Write(ss_text))
        self.wait()

        # 3. Manual Histogram on the right
        histo_origin = RIGHT * 2.5 + DOWN * 1.5
        h_x_axis = Line(histo_origin, histo_origin + RIGHT * 4, color=WHITE)
        h_title = Text("Histogram", font_size=24).next_to(h_x_axis, UP, buff=3.5)
        
        # Data: 28(2), 29(2), 30(12), 31(3), 32(1) - slightly adjusted for visual
        # Using real counts from velocity_data: 28:2, 29:2, 30:12, 31:2, 32:2
        vals = [28, 29, 30, 31, 32]
        counts = [2, 2, 12, 2, 2]
        
        bars = VGroup()
        for i, count in enumerate(counts):
            bar_h = (count / 15.0) * 3.5
            bar_w = 0.5
            bar = Rectangle(
                width=bar_w, height=bar_h, 
                fill_color=YELLOW if vals[i] == 30 else BLUE,
                fill_opacity=0.7, stroke_width=1
            )
            bar.move_to(histo_origin + RIGHT * (i + 0.5) * 0.8 + UP * bar_h / 2)
            bars.add(bar)
            
        self.play(Create(h_x_axis), Write(h_title))
        self.play(Create(bars))
        self.wait()

        # 4. Stability Formula
        formula = MathTex(
            r"\text{Stability} = \frac{\text{counts at mode}}{\text{counts not at mode}}",
            font_size=32
        ).to_edge(DOWN, buff=0.5)
        
        # mode is 30 (count 12), others are (2+2+2+2 = 8)
        calc = MathTex(
            r"\text{Stability} = \frac{12}{8} = 1.5",
            font_size=32
        ).move_to(formula.get_center())
        
        self.play(Write(formula))
        self.wait(2)
        self.play(Transform(formula, calc))
        self.wait(2)