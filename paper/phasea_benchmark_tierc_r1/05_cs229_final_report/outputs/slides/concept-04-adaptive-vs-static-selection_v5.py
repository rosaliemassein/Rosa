from manim import *
import numpy as np

class AdaptiveVSStaticSelection(Scene):
    def construct(self):
        # Titles for the two sides
        static_title = Text("Static Benchmark", font_size=32).to_edge(UP).shift(LEFT * 3.5)
        adaptive_title = Text("Logistic Model", font_size=32).to_edge(UP).shift(RIGHT * 3.5)
        self.add(static_title, adaptive_title)

        # Floorplans
        fp_left = Rectangle(width=4, height=2.5, color=WHITE).shift(LEFT * 3.5 + UP * 0.5)
        fp_right = Rectangle(width=4, height=2.5, color=WHITE).shift(RIGHT * 3.5 + UP * 0.5)
        fp_left_bg = Rectangle(width=4, height=2.5, fill_opacity=0.1, fill_color=WHITE).move_to(fp_left)
        fp_right_bg = Rectangle(width=4, height=2.5, fill_opacity=0.1, fill_color=WHITE).move_to(fp_right)
        self.add(fp_left_bg, fp_right_bg, fp_left, fp_right)

        # Static Highlights (Fixed zones)
        static_dots = VGroup(*[
            Dot(fp_left.get_center() + np.array([x, y, 0]), color=BLUE)
            for x, y in [(-1.0, 0.5), (0.4, -0.4), (1.1, 0.2)]
        ])
        self.add(static_dots)

        # Timeline Tracker
        time_tracker = ValueTracker(0)

        # Possible zones for the adaptive model to toggle
        zone_coords = [
            [x, y, 0] for x in np.linspace(-1.5, 1.5, 5) for y in np.linspace(-0.8, 0.8, 3)
        ]

        # Adaptive highlights flickering/changing based on time
        def get_adaptive_dots():
            t = time_tracker.get_value()
            # Use deterministic pseudo-random logic based on time
            dots = VGroup()
            for i, coord in enumerate(zone_coords):
                # Different zones pulse at different frequencies/phases
                if np.sin(i * 0.5 + t * 4) > 0.6:
                    dots.add(Dot(fp_right.get_center() + np.array(coord), color=GREEN))
            return dots

        adaptive_dots = always_redraw(get_adaptive_dots)
        self.add(adaptive_dots)

        # Axes for the Recall Error graph
        axes = Axes(
            x_range=[0, 4, 1], 
            y_range=[0, 1, 0.5],
            x_length=10,
            y_length=2,
            axis_config={"include_tip": False}
        ).to_edge(DOWN, buff=0.8)

        month_labels = VGroup(*[
            Text(m, font_size=20).next_to(axes.c2p(i, 0), DOWN)
            for i, m in enumerate(["May", "June", "July", "Aug", "Sept"])
        ])
        graph_label = Text("Missed Requests (Recall Error)", font_size=24).next_to(axes, UP, buff=0.1)
        self.add(axes, month_labels, graph_label)

        # Graph drawing functions
        def get_static_path():
            # Static error remains high and relatively constant
            return axes.plot(lambda x: 0.8 + 0.05 * np.cos(x * 3), color=BLUE, x_range=[0, max(0.01, time_tracker.get_value())])

        def get_adaptive_path():
            # Adaptive error starts high but drops as the model learns/adapts
            return axes.plot(lambda x: 0.4 * np.exp(-x) + 0.15 + 0.1 * np.sin(x * 5), color=GREEN, x_range=[0, max(0.01, time_tracker.get_value())])

        static_path = always_redraw(get_static_path)
        adaptive_path = always_redraw(get_adaptive_path)
        
        indicator = always_redraw(lambda: Line(
            axes.c2p(time_tracker.get_value(), 0),
            axes.c2p(time_tracker.get_value(), 1),
            color=YELLOW, stroke_width=2
        ))

        self.add(static_path, adaptive_path, indicator)

        # Animation
        self.play(
            time_tracker.animate.set_value(4),
            run_time=10,
            rate_func=lambda t: t # Explicit linear rate function
        )

        # Final Tags
        static_tag = Text("Static", color=BLUE, font_size=18).next_to(axes.c2p(4, 0.8), RIGHT)
        adaptive_tag = Text("Logistic", color=GREEN, font_size=18).next_to(axes.c2p(4, 0.15), RIGHT)
        self.play(Write(static_tag), Write(adaptive_tag))
        self.wait(2)