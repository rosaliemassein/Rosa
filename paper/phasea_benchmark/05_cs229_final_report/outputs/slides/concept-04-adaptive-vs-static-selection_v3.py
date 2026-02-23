from manim import *

class AdaptiveVsStaticSelection(Scene):
    def construct(self):
        # Split-screen divider
        div_line = Line(start=[0, 3.8, 0], end=[0, -1.2, 0], color=WHITE)
        self.add(div_line)

        # Titles for the two models
        text_static = Text("Static Benchmark", font_size=24, color=BLUE).move_to([-3.5, 3.5, 0])
        text_ml = Text("Logistic Model", font_size=24, color=YELLOW).move_to([3.5, 3.5, 0])
        self.add(text_static, text_ml)

        # Function to create a 3x3 floor grid
        def make_grid(start_x, start_y):
            group = VGroup()
            for i_val in range(3):
                for j_val in range(3):
                    cell_sq = Square(side_length=0.6, fill_opacity=0)
                    cell_sq.move_to([start_x + i_val * 0.7, start_y + j_val * 0.7, 0])
                    group.add(cell_sq)
            return group

        # Grids
        grid_l = make_grid(-4.2, 0.0)
        grid_r = make_grid(2.8, 0.0)

        # Static Highlights (Never change)
        for idx_l in [2, 4, 7]:
            grid_l[idx_l].set_fill(RED, opacity=0.8)
            grid_l[idx_l].set_stroke(RED, width=4)

        # Initial State for ML Highlights
        grid_r[1].set_fill(RED, opacity=0.8)
        grid_r[1].set_stroke(RED, width=4)

        self.add(grid_l, grid_r)

        # Timeline components (May to September)
        tl_bar = Line(start=[-5, -1.8, 0], end=[5, -1.8, 0], color=GRAY)
        self.add(tl_bar)
        
        month_list = ["May", "Jun", "Jul", "Aug", "Sep"]
        for i_month in range(5):
            pos_x_month = -5 + i_month * 2.5
            label_month = Text(month_list[i_month], font_size=18).move_to([pos_x_month, -2.2, 0])
            self.add(label_month)

        # Dot representing current time
        cursor = Dot(color=WHITE).move_to([-5, -1.8, 0])
        self.add(cursor)

        # Line Graph for 'Missed Requests'
        # Static error path (blue)
        static_error_vg = VGroup()
        static_pts = [[-5, -2.8, 0], [-2.5, -2.7, 0], [0, -2.9, 0], [2.5, -2.6, 0], [5, -2.8, 0]]
        for i_pt in range(4):
            static_error_vg.add(Line(static_pts[i_pt], static_pts[i_pt+1], color=BLUE))

        # ML error path (yellow)
        ml_error_vg = VGroup()
        ml_pts = [[-5, -3.6, 0], [-2.5, -3.8, 0], [0, -3.7, 0], [2.5, -3.9, 0], [5, -3.8, 0]]
        for i_pt in range(4):
            ml_error_vg.add(Line(ml_pts[i_pt], ml_pts[i_pt+1], color=YELLOW))

        lbl_stat = Text("Static Error", font_size=14, color=BLUE).move_to([5.8, -2.8, 0])
        lbl_ml_err = Text("ML Error", font_size=14, color=YELLOW).move_to([5.8, -3.8, 0])
        self.add(static_error_vg, ml_error_vg, lbl_stat, lbl_ml_err)

        # Animation sequence over months
        # The list defines which squares are 'on' for each step
        steps_highlights = [
            [1],             # May
            [0, 3],          # June
            [1, 2, 5, 8],    # July (Heatwave)
            [4, 6],          # August
            [2]              # September
        ]

        for i_step in range(1, 5):
            # Prepare a target version of the ML grid for the next month
            next_grid_r = make_grid(2.8, 0.0)
            for h_idx in steps_highlights[i_step]:
                next_grid_r[h_idx].set_fill(RED, opacity=0.8)
                next_grid_r[h_idx].set_stroke(RED, width=4)
            
            # Move timeline dot and transform grid to new highlights
            next_x_pos = -5 + i_step * 2.5
            self.play(
                cursor.animate.move_to([next_x_pos, -1.8, 0]),
                Transform(grid_r, next_grid_r),
                run_time=1.2
            )

        # Final summary text
        summary = Text("ML adaptively adjusts to building load and weather", font_size=20)
        summary.move_to([0, -4.5, 0])
        self.play(Write(summary))
        self.wait(2)