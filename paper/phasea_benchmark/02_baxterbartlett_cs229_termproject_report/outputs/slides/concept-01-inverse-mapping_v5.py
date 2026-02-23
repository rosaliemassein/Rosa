from manim import *
import numpy as np

class ConceptInverseMapping(Scene):
    def construct(self):
        # 1. Constants and Helper
        PI = 3.1415926535
        
        # 2. Create the split screen layout (Input Box & Output Box)
        # We avoid 'Rectangle' and 'SurroundingRectangle' as per constraints.
        
        # Left: Desired Behavior
        in_t1 = Text("Desired Behavior", font_size=24)
        in_t2 = Text("Rise Time", font_size=18)
        in_t3 = Text("Steady State Error", font_size=18)
        in_t4 = Text("Stability", font_size=18)
        inputs_text = VGroup(in_t1, in_t2, in_t3, in_t4).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        c1 = LEFT * 4
        inputs_text.move_to(c1)
        w1, h1 = inputs_text.width + 0.5, inputs_text.height + 0.5
        input_box = VGroup(
            Line(c1 + [-w1/2, h1/2, 0], c1 + [w1/2, h1/2, 0]),
            Line(c1 + [w1/2, h1/2, 0], c1 + [w1/2, -h1/2, 0]),
            Line(c1 + [w1/2, -h1/2, 0], c1 + [-w1/2, -h1/2, 0]),
            Line(c1 + [-w1/2, -h1/2, 0], c1 + [-w1/2, h1/2, 0])
        )
        input_group = VGroup(inputs_text, input_box)

        # Right: PID Constants
        out_t1 = Text("PID Constants", font_size=24)
        out_t2 = Text("Kp, Ki, Kd", font_size=18)
        outputs_text = VGroup(out_t1, out_t2).arrange(DOWN, buff=0.2)
        
        c2 = RIGHT * 4
        outputs_text.move_to(c2)
        w2, h2 = outputs_text.width + 0.5, outputs_text.height + 0.5
        output_box = VGroup(
            Line(c2 + [-w2/2, h2/2, 0], c2 + [w2/2, h2/2, 0]),
            Line(c2 + [w2/2, h2/2, 0], c2 + [w2/2, -h2/2, 0]),
            Line(c2 + [w2/2, -h2/2, 0], c2 + [-w2/2, -h2/2, 0]),
            Line(c2 + [-w2/2, -h2/2, 0], c2 + [-w2/2, h2/2, 0])
        )
        output_group = VGroup(outputs_text, output_box)

        # Arrow between them
        connector = Arrow(c1 + [w1/2, 0, 0], c2 + [-w2/2, 0, 0], buff=0.1)
        
        diagram = VGroup(input_group, output_group, connector)

        # Animation: Initial view
        self.play(Create(input_group), Create(output_group))
        self.play(Create(connector))
        self.wait(1)

        # "Flips the script": Rotate the entire diagram 180 degrees
        self.play(diagram.animate.rotate(PI))
        self.wait(1)
        
        # Shrink and move up to clear space for the plot
        self.play(diagram.animate.scale(0.6).to_edge(UP, buff=0.5))

        # 3. Add PID Formula using Text
        formula = Text("U = Kp*e + Ki*Integral(e) + Kd*de/dt", font_size=22)
        formula.next_to(diagram, DOWN, buff=0.4)
        self.play(Write(formula))

        # 4. Motor velocity plot (Manual construction without 'Axes')
        p_origin = DOWN * 2.5 + LEFT * 3.5
        x_axis = Line(p_origin, p_origin + RIGHT * 7)
        y_axis = Line(p_origin, p_origin + UP * 2.5)
        x_tip = Arrow(p_origin + RIGHT * 6.8, p_origin + RIGHT * 7.3, buff=0)
        y_tip = Arrow(p_origin + UP * 2.3, p_origin + UP * 2.8, buff=0)
        
        x_label = Text("Time", font_size=16).next_to(x_axis, DOWN, buff=0.1)
        y_label = Text("RPM", font_size=16).next_to(y_axis, LEFT, buff=0.1)
        
        # Horizontal setpoint as a series of small lines (Dashed effect)
        target_height = 1.8
        setpoint = VGroup(*[
            Line(p_origin + [x, target_height, 0], p_origin + [x + 0.15, target_height, 0], stroke_opacity=0.6)
            for x in np.arange(0, 7, 0.3)
        ])
        
        # Plot curve using many small Line segments to form a path
        curve_lines = VGroup()
        last_point = p_origin
        # Function: 1 - exp(-0.5t) * cos(3t)
        for time_step in np.linspace(0, 8, 120):
            val = 1 - np.exp(-0.5 * time_step) * np.cos(3 * time_step)
            # Map time[0,8] to x[0,7] and val to y
            curr_point = p_origin + [(time_step/8)*7, val * target_height, 0]
            if time_step > 0:
                curve_lines.add(Line(last_point, curr_point, color=YELLOW, stroke_width=4))
            last_point = curr_point

        self.play(Create(x_axis), Create(y_axis), Create(x_tip), Create(y_tip), Write(x_label), Write(y_label))
        self.play(Create(setpoint))
        self.play(Create(curve_lines), run_time=3)

        # 5. Add Rise Time and Steady State Error markers manually
        # Rise time: approx first crossing of target
        rt_end_x = (0.55 / 8) * 7
        rt_marker = Line(p_origin + [0, -0.3, 0], p_origin + [rt_end_x, -0.3, 0], color=BLUE)
        rt_t1 = Line(p_origin + [0, -0.2, 0], p_origin + [0, -0.4, 0], color=BLUE)
        rt_t2 = Line(p_origin + [rt_end_x, -0.2, 0], p_origin + [rt_end_x, -0.4, 0], color=BLUE)
        rt_txt = Text("Rise Time", font_size=14, color=BLUE).next_to(rt_marker, DOWN, buff=0.1)
        
        self.play(Create(rt_marker), Create(rt_t1), Create(rt_t2), Write(rt_txt))

        # Steady State Error: marker at the end of the plot
        sse_x = 7
        # The value at t=8 is roughly 1 - exp(-4)*cos(24) approx 0.98. Target is 1.0.
        sse_marker = Line(p_origin + [sse_x, target_height, 0], p_origin + [sse_x, target_height - 0.1, 0], color=RED)
        sse_txt = Text("Steady State Error", font_size=14, color=RED).next_to(sse_marker, RIGHT, buff=0.1)
        
        self.play(Create(sse_marker), Write(sse_txt))

        self.wait(3)