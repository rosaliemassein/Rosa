from manim import *

class Concept04AdaptiveVSStaticSelection(Scene):
    def construct(self):
        # 1. Labels and Layout
        static_title = Text("Static Benchmark", font_size=24).shift(LEFT * 3.5 + UP * 3.5)
        adaptive_title = Text("Adaptive ML Model", font_size=24).shift(RIGHT * 3.5 + UP * 3.5)
        self.add(static_title, adaptive_title)

        # 2. Floorplan Creation (Manual Grids)
        def create_grid(center_pos):
            grid = VGroup(*[
                Rectangle(width=0.8, height=0.6, stroke_width=2, color=GRAY)
                for _ in range(12)
            ]).arrange_in_grid(rows=4, cols=3, buff=0.1).move_to(center_pos)
            return grid

        static_grid = create_grid(LEFT * 3.5 + UP * 1.5)
        adaptive_grid = create_grid(RIGHT * 3.5 + UP * 1.5)
        
        # Static Highlights (Frozen: ASHRAE "Rules of Thumb")
        static_fixed_indices = [1, 4, 7]
        for idx in static_fixed_indices:
            static_grid[idx].set_fill(RED, opacity=0.5)
        
        self.add(static_grid, adaptive_grid)

        # 3. Manual Timeline and Graph Construction
        # Since 'Axes' is disallowed, we build it from Lines
        graph_origin = DOWN * 3 + LEFT * 5
        x_axis = Line(graph_origin, graph_origin + RIGHT * 10, color=WHITE)
        y_axis = Line(graph_origin, graph_origin + UP * 2.5, color=WHITE)
        graph_label = Text("Missed Requests (Recall Error)", font_size=18).next_to(y_axis, UP, buff=0.2).shift(RIGHT * 2)
        
        self.add(x_axis, y_axis, graph_label)

        months = ["May", "Jun", "Jul", "Aug", "Sep"]
        month_positions = []
        for i, month_text in enumerate(months):
            pos = graph_origin + RIGHT * (i * 2.5)
            month_positions.append(pos)
            label = Text(month_text, font_size=18).next_to(pos, DOWN)
            self.add(label)

        # Timeline indicator
        indicator = Dot(color=YELLOW).move_to(month_positions[0])
        self.add(indicator)

        # 4. Data for Animations
        # Error values (y-coordinates relative to origin)
        static_err_y = [2.0, 1.8, 2.2, 2.3, 2.0]
        ml_err_y = [0.6, 0.4, 0.7, 0.5, 0.3]
        
        # ML active zones flickering over time
        ml_active_states = [
            [1, 4],                # May
            [0, 1, 3, 4, 6, 7],    # Jun (More stress)
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], # Jul (Heatwave - High Stress)
            [1, 4, 7, 10],         # Aug
            [4]                    # Sep (Low Stress)
        ]

        # 5. Animation Loop
        for i in range(len(months) - 1):
            # Calculate graph line segments
            p1_static = month_positions[i] + UP * static_err_y[i]
            p2_static = month_positions[i+1] + UP * static_err_y[i+1]
            
            p1_ml = month_positions[i] + UP * ml_err_y[i]
            p2_ml = month_positions[i+1] + UP * ml_err_y[i+1]
            
            # 1. Move timeline and draw graph
            self.play(
                indicator.animate.move_to(month_positions[i+1]),
                Create(Line(p1_static, p2_static, color=RED, stroke_width=4)),
                Create(Line(p1_ml, p2_ml, color=GREEN, stroke_width=4)),
                run_time=1.2
            )
            
            # 2. Update Adaptive ML Grid highlights
            current_active = ml_active_states[i+1]
            grid_anims = []
            for idx, rect in enumerate(adaptive_grid):
                if idx in current_active:
                    grid_anims.append(rect.animate.set_fill(YELLOW, opacity=0.7).set_color(YELLOW))
                else:
                    grid_anims.append(rect.animate.set_fill(BLACK, opacity=0).set_color(GRAY))
            
            self.play(*grid_anims, run_time=0.6)
            self.wait(0.4)

        self.wait(2)