from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Setup Grid (3x3)
        grid = VGroup(*[
            Square(side_length=1).set_stroke(WHITE, 1).set_fill(WHITE, opacity=0.1)
            for _ in range(9)
        ]).arrange_in_grid(rows=3, cols=3, buff=0)
        
        # Initial states: Center is RED, some neighbors are RED or BLUE
        grid[1].set_fill(RED, opacity=0.8)
        grid[3].set_fill(RED, opacity=0.8)
        grid[5].set_fill(RED, opacity=0.8)
        grid[7].set_fill(BLUE, opacity=0.8)
        grid[4].set_fill(RED, opacity=0.8)
        
        grid_group = VGroup(grid).scale(1.2).to_edge(LEFT, buff=1.5)
        self.add(grid_group)

        # 2. Formula
        formula = MathTex(r"R_t = \text{Border}_t - \text{Border}_{t-1}").to_edge(UP)
        self.play(Write(formula))

        # 3. Highlight Center and Neighbors
        center_pixel = grid[4]
        neighbor_indices = [1, 3, 5, 7]
        neighbors = VGroup(*[grid[i] for i in neighbor_indices])
        
        focus_rect = SurroundingRectangle(center_pixel, color=YELLOW, buff=0)
        self.play(Create(focus_rect))
        self.play(neighbors.animate.set_stroke(YELLOW, 3))
        self.wait(0.5)

        # 4. Prepare border highlight objects (Manual creation)
        cp = center_pixel.get_center()
        s = 1.2 * (center_pixel.side_length / 2) # Account for scaling of grid_group
        
        # New boundaries (Green lines)
        top_border = Line(cp + [-s, s, 0], cp + [s, s, 0], color=GREEN, stroke_width=8)
        left_border = Line(cp + [-s, s, 0], cp + [-s, -s, 0], color=GREEN, stroke_width=8)
        right_border = Line(cp + [s, s, 0], cp + [s, -s, 0], color=GREEN, stroke_width=8)
        
        # Lost boundary (Red line and manual cross)
        bottom_border = Line(cp + [-s, -s, 0], cp + [s, -s, 0], color=RED, stroke_width=8)
        cross_line1 = Line(ORIGIN, 0.2 * (UR + DL), color=RED).move_to(bottom_border)
        cross_line2 = Line(ORIGIN, 0.2 * (UL + DR), color=RED).move_to(bottom_border)
        manual_cross = VGroup(cross_line1, cross_line2)

        # 5. Animate Flip and Reward
        reward_text = Text("+2", color=GREEN).scale(1.2).next_to(grid_group, UP, buff=0.5)
        
        self.play(
            center_pixel.animate.set_fill(BLUE),
            run_time=1
        )
        self.play(
            Create(top_border), 
            Create(left_border), 
            Create(right_border),
            Create(bottom_border), 
            Create(manual_cross),
            Write(reward_text)
        )
        self.wait(1)

        # 6. Manual Bar Chart (Since Axes/BarChart are restricted)
        chart_origin = RIGHT * 3 + DOWN * 2
        y_axis = Line(chart_origin, chart_origin + UP * 4, color=GREY)
        x_axis = Line(chart_origin, chart_origin + RIGHT * 4, color=GREY)
        
        bar1 = Rectangle(height=1.0, width=0.8, fill_color=BLUE, fill_opacity=0.8, stroke_color=WHITE)
        bar1.move_to(chart_origin + RIGHT * 1 + UP * 0.5)
        
        bar2 = Rectangle(height=3.0, width=0.8, fill_color=GREEN, fill_opacity=0.8, stroke_color=WHITE)
        bar2.move_to(chart_origin + RIGHT * 2.5 + UP * 1.5)
        
        label1 = Text("t-1", font_size=20).next_to(bar1, DOWN)
        label2 = Text("t", font_size=20).next_to(bar2, DOWN)
        chart_title = Text("Cumulative Reward", font_size=24).next_to(y_axis, UP).shift(RIGHT * 1.5)
        
        chart_group = VGroup(y_axis, x_axis, bar1, bar2, label1, label2, chart_title)
        
        self.play(Create(y_axis), Create(x_axis), Write(chart_title))
        self.play(FadeIn(bar1), Write(label1))
        self.play(FadeIn(bar2), Write(label2))
        self.wait(2)

        # Cleanup
        self.play(
            FadeOut(top_border), FadeOut(left_border), FadeOut(right_border),
            FadeOut(bottom_border), FadeOut(manual_cross), FadeOut(focus_rect),
            FadeOut(neighbors)
        )
        self.wait(1)