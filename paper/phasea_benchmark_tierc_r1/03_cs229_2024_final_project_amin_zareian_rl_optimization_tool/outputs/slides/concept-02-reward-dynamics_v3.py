from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Formula Header
        formula = MathTex(r"R_t = \text{Border}_{t} - \text{Border}_{t-1}").to_edge(UP)
        self.add(formula)

        # 2. Create 3x3 Grid
        grid = VGroup(*[
            Square(side_length=1.0, fill_opacity=1.0).set_stroke(WHITE, width=1)
            for _ in range(9)
        ]).arrange_in_grid(rows=3, cols=3, buff=0.1)
        grid.shift(LEFT * 3)

        # Initialize colors: All Red, except Top Neighbor (index 1) is Blue
        for i in range(9):
            grid[i].set_fill(RED)
        grid[1].set_fill(BLUE)
        
        self.add(grid)

        # 3. Highlight Center Pixel and Neighbors
        center = grid[4]
        neighbor_indices = [1, 3, 5, 7]
        neighbor_group = VGroup(*[grid[i] for i in neighbor_indices])
        
        highlight_box = SurroundingRectangle(center, color=YELLOW, buff=0.05)
        self.play(Create(highlight_box))
        self.wait(0.5)

        # 4. Prepare Border Visuals
        # Top border (between center 4 and top 1) - Initial border (Red/Blue)
        # Left (4/3), Right (4/5), Bottom (4/7) - Initial non-borders (Red/Red)
        
        cp = center.get_center()
        side = 1.0 / 2
        
        top_line = Line(cp + [ -side, side, 0], cp + [side, side, 0], stroke_width=8)
        left_line = Line(cp + [-side, -side, 0], cp + [-side, side, 0], stroke_width=8)
        right_line = Line(cp + [side, -side, 0], cp + [side, side, 0], stroke_width=8)
        bottom_line = Line(cp + [-side, -side, 0], cp + [side, -side, 0], stroke_width=8)

        # 5. Animate Flip and Rewards
        # Flip center to Blue
        # New State: Center(B), Top(B), Left(R), Right(R), Bottom(R)
        # Lost border: Top (now B-B)
        # New borders: Left, Right, Bottom (now B-R)
        # Net change: +3 (new) - 1 (lost) = +2
        
        self.play(center.animate.set_fill(BLUE), run_time=1)
        
        # Show lost border (Red X)
        top_line.set_color(RED)
        cross = VGroup(
            Line(top_line.get_center() + [-0.1, -0.1, 0], top_line.get_center() + [0.1, 0.1, 0]),
            Line(top_line.get_center() + [-0.1, 0.1, 0], top_line.get_center() + [0.1, -0.1, 0])
        ).set_color(RED)
        
        self.play(Create(top_line), Create(cross))
        
        # Show new borders (Green)
        new_borders = VGroup(left_line, right_line, bottom_line).set_color(GREEN)
        self.play(Create(new_borders))
        
        # Floating text
        reward_val = Text("+2", color=GREEN).scale(1.2)
        reward_val.next_to(center, RIGHT, buff=0.5)
        self.play(Write(reward_val), reward_val.animate.shift(UP * 0.5))

        # 6. Manual Bar Chart (Cumulative Reward)
        # Using Axes and Rectangles to ensure compatibility
        axes = Axes(
            x_range=[0, 3, 1],
            y_range=[0, 5, 1],
            x_length=3,
            y_length=3,
            axis_config={"include_tip": False}
        ).to_edge(RIGHT, buff=1)
        
        chart_label = Text("Cumulative Reward", font_size=24).next_to(axes, UP)
        
        # Bars
        bar1 = Rectangle(width=0.6, height=0.5, fill_opacity=1, color=BLUE)
        bar1.move_to(axes.c2p(1, 0), aligned_edge=DOWN)
        
        bar2 = Rectangle(width=0.6, height=1.5, fill_opacity=1, color=BLUE)
        bar2.move_to(axes.c2p(2, 0), aligned_edge=DOWN)
        
        self.play(Create(axes), Write(chart_label))
        self.play(FadeIn(bar1))
        self.wait(0.5)
        self.play(Transform(bar1.copy(), bar2)) # Visual growth
        self.add(bar2)
        
        self.wait(2)