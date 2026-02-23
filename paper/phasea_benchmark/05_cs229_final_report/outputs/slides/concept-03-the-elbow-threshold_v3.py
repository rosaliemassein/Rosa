from manim import *
import numpy as np

class TheElbowThreshold(Scene):
    def construct(self):
        axes_obj = Axes(
            x_range=[0, 1.1, 0.2],
            y_range=[0, 1.1, 0.2],
            x_length=6,
            y_length=4,
            axis_config={"include_tip": True}
        ).to_edge(LEFT, buff=0.5)

        def get_curve_y(recall_input):
            return 1 - (1 - recall_input)**4

        curve_graph = axes_obj.plot(get_curve_y, x_range=[0, 1], color=BLUE)

        axis_label_x = Text("Fraction of Zones Flagged", font_size=20)
        axis_label_y = Text("Recall", font_size=20)
        labels_obj = axes_obj.get_axis_labels(x_label=axis_label_x, y_label=axis_label_y)

        zones_container = VGroup()
        for placeholder_idx in range(20):
            zones_container.add(Square(side_length=0.4, fill_opacity=0.2, color=GRAY, stroke_width=2))
        zones_container.arrange_in_grid(rows=4, cols=5, buff=0.1)
        zones_container.to_edge(RIGHT, buff=1)

        val_tracker = ValueTracker(0.05)
        moving_dot_obj = Dot(color=YELLOW)

        def update_dot_position(mobject_param):
            current_value_x = val_tracker.get_value()
            current_value_y = get_curve_y(current_value_x)
            mobject_param.move_to(axes_obj.c2p(current_value_x, current_value_y))

        moving_dot_obj.add_updater(update_dot_position)

        def update_zones_color_state(vgroup_param):
            highlight_threshold = int(val_tracker.get_value() * 20)
            for loop_idx, square_mobj in enumerate(vgroup_param):
                if loop_idx < highlight_threshold:
                    square_mobj.set_fill(YELLOW, opacity=0.8)
                    square_mobj.set_color(YELLOW)
                else:
                    square_mobj.set_fill(GRAY, opacity=0.2)
                    square_mobj.set_color(GRAY)

        zones_container.add_updater(update_zones_color_state)

        formula_tex_obj = MathTex(r"Recall = \frac{TP}{TP + FN}").scale(0.8).to_corner(UL)
        
        def linear_rate_func(t_param):
            return t_param

        self.add(axes_obj, labels_obj, zones_container, formula_tex_obj)
        self.play(Create(curve_graph), run_time=2)
        self.add(moving_dot_obj)
        
        self.play(
            val_tracker.animate.set_value(0.9), 
            run_time=4, 
            rate_func=linear_rate_func
        )
        self.wait(0.5)
        self.play(val_tracker.animate.set_value(0.35), run_time=2)
        
        elbow_point_coord = axes_obj.c2p(0.35, get_curve_y(0.35))
        elbow_indicator_circle = Circle(radius=0.4, color=YELLOW).move_to(elbow_point_coord)
        elbow_text_label = Text("The Elbow", font_size=24, color=YELLOW).next_to(elbow_indicator_circle, UR)
        
        self.play(Create(elbow_indicator_circle), Write(elbow_text_label))
        self.play(Flash(elbow_point_coord, color=YELLOW))
        self.play(Indicate(elbow_indicator_circle))
        
        self.wait(3)