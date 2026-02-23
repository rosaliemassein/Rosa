from manim import *

class RewardDynamics(Scene):
    def construct(self):
        # 1. Create a 3x3 grid using Squares
        grid = VGroup(*[
            Square(side_length=0.8).set_stroke(WHITE, 1)
            for _ in range(9)
        ]).arrange_in_grid(rows=3, cols=3, buff=0.1)
        
        # Setup initial colors
        # Neighbors: 1(T), 3(L), 5(R), 7(B)
        # We want 1, 3, 5 to be RED and 7 to be BLUE. Center 4 starts RED.
        initial_colors = [
            WHITE, RED,  WHITE,
            RED,   RED,  RED,
            WHITE, BLUE, WHITE
        ]
        for i, color in enumerate(initial_colors):
            grid[i].set_fill(color, opacity=0.7)
            
        self.add(grid)
        self.wait(0.5)

        # 2. Highlight the center pixel and its neighbors
        center_pixel = grid[4]
        # Use Rectangle instead of SurroundingRectangle to be safe
        center_highlight = Rectangle(width=0.9, height=0.9, color=YELLOW).move_to(center_pixel)
        
        neighbor_indices = [1, 3, 5, 7]
        neighbor_highlights = VGroup(*[
            Rectangle(width=0.85, height=0.85, color=YELLOW, stroke_width=2).move_to(grid[i])
            for i in neighbor_indices
        ])
        
        self.play(Create(center_highlight))
        self.play(FadeIn(neighbor_highlights))
        self.wait(1)

        # 3. Animate the center pixel flipping from Red to Blue
        self.play(center_pixel.animate.set_fill(BLUE))
        self.wait(0.5)

        # 4. Visualize reward change: New borders (Green) and Lost borders (Red X)
        # Border logic: center is now BLUE. 
        # Neighbors 1, 3, 5 are RED (3 new borders).
        # Neighbor 7 is BLUE (1 lost border).
        
        def get_line_between(idx1, idx2):
            p1 = grid[idx1].get_center()
            p2 = grid[idx2].get_center()
            mid = (p1 + p2) / 2
            if abs(p1[0] - p2[0]) < 0.1: # Vertical
                return Line(mid + LEFT*0.4, mid + RIGHT*0.4, stroke_width=8)
            else: # Horizontal
                return Line(mid + UP*0.4, mid + DOWN*0.4, stroke_width=8)

        # New borders
        nb1 = get_line_between(4, 1).set_color(GREEN)
        nb2 = get_line_between(4, 3).set_color(GREEN)
        nb3 = get_line_between(4, 5).set_color(GREEN)
        new_borders = VGroup(nb1, nb2, nb3)

        # Lost border (Red X)
        lb_line = get_line_between(4, 7).set_color(RED)
        # Create a manual X
        cross_l1 = Line(lb_line.get_center() + UL*0.2, lb_line.get_center() + DR*0.2, color=RED, stroke_width=4)
        cross_l2 = Line(lb_line.get_center() + UR*0.2, lb_line.get_center() + DL*0.2, color=RED, stroke_width=4)
        cross = VGroup(cross_l1, cross_l2)

        self.play(Create(new_borders))
        self.play(Create(lb_line), Create(cross))
        
        # Display floating text
        reward_text = MathTex("R_t = +2", color=GREEN).scale(1.2)
        reward_text.next_to(grid, RIGHT, buff=0.5)
        self.play(Write(reward_text))
        self.wait(1)

        # 5. Link to a manual BarChart (Axes and Rects)
        # Move grid up to make room
        everything = VGroup(grid, center_highlight, neighbor_highlights, new_borders, lb_line, cross, reward_text)
        self.play(everything.animate.scale(0.7).to_edge(UP))

        # Manual Axes
        origin = DOWN * 2.5 + LEFT * 2
        y_axis = Line(origin, origin + UP * 2)
        x_axis = Line(origin, origin + RIGHT * 4)
        axes = VGroup(y_axis, x_axis)
        
        y_label = Text("Reward", font_size=20).next_to(y_axis, UP)
        x_label = Text("Time", font_size=20).next_to(x_axis, RIGHT)

        # Cumulative bars: [1, 3, 4] (showing growth)
        bar_data = [0.5, 1.5, 2.0] # heights
        bars = VGroup()
        for i, h in enumerate(bar_data):
            bar = Rectangle(
                width=0.6, 
                height=h, 
                fill_opacity=0.8, 
                fill_color=BLUE, 
                stroke_width=1
            )
            bar.move_to(origin + RIGHT * (i + 1) + UP * (h/2), aligned_edge=DOWN)
            bars.add(bar)

        self.play(Create(axes), Write(y_label), Write(x_label))
        
        for bar in bars:
            self.play(Create(bar), run_time=0.5)
            
        self.wait(2)