from manim import *

class RewardDynamics(Scene):
    def construct(self):
        # Formula as a reference at the top
        formula = MathTex(r"R_t = \text{Border}_{t} - \text{Border}_{t-1}").to_edge(UP)
        self.add(formula)

        # 1. Create a 3x3 grid
        grid = VGroup(*[Square(side_length=1, fill_opacity=0.8) for _ in range(9)])
        grid.arrange_in_grid(rows=3, cols=3, buff=0).shift(LEFT * 3)
        
        # Initialize colors
        for i in range(9):
            grid[i].set_fill(RED)
        grid[1].set_fill(BLUE)
        grid[0].set_fill(BLUE)
        grid[2].set_fill(BLUE)
        self.add(grid)

        # Highlight the center pixel and focus on its 4 neighbors
        center_pixel = grid[4]
        neighbor_indices = [1, 3, 5, 7]
        neighbor_highlights = VGroup(*[
            Square(side_length=1).move_to(grid[i]).set_stroke(YELLOW, 5) 
            for i in neighbor_indices
        ])
        
        self.play(Create(neighbor_highlights))
        self.wait(0.5)

        # Define geometry for borders around the center pixel
        cp = center_pixel.get_center()
        b_bottom = Line(cp + DOWN*0.5 + LEFT*0.5, cp + DOWN*0.5 + RIGHT*0.5)
        b_left = Line(cp + LEFT*0.5 + UP*0.5, cp + LEFT*0.5 + DOWN*0.5)
        b_right = Line(cp + RIGHT*0.5 + UP*0.5, cp + RIGHT*0.5 + DOWN*0.5)

        # Manual Bar Chart setup (avoiding Axes class to prevent environment-specific errors)
        chart_base = RIGHT * 3.5 + DOWN * 1.5
        x_axis = Line(chart_base, chart_base + RIGHT * 3.5)
        y_axis = Line(chart_base, chart_base + UP * 3)
        y_label = MathTex(r"\text{Cumulative Reward}").scale(0.5).next_to(y_axis, UP)
        self.play(Create(x_axis), Create(y_axis), Write(y_label))

        # --- Step 1: Flip Center Red -> Blue (+2 Reward) ---
        self.play(center_pixel.animate.set_fill(BLUE))
        
        # Green highlights for new borders created
        new_borders = VGroup(b_bottom, b_left, b_right).set_color(GREEN).set_stroke(width=10)
        reward_p2 = MathTex("+2", color=GREEN).scale(1.5).next_to(center_pixel, RIGHT, buff=0.8)
        
        self.play(Create(new_borders), Write(reward_p2))
        
        # Update Bar Chart (Bar 1)
        bar1 = Rectangle(width=0.6, height=2, fill_opacity=1, fill_color=GREEN, stroke_width=0)
        bar1.move_to(chart_base + RIGHT * 0.8 + UP * 1.0)
        self.play(FadeIn(bar1, shift=UP))
        self.wait(1)

        # --- Step 2: Flip Center Blue -> Red (-2 Reward) ---
        # Reset visual markers for the second flip
        self.play(FadeOut(reward_p2), FadeOut(new_borders))
        self.play(center_pixel.animate.set_fill(RED))
        
        # Lost borders marked with Red 'X'
        x_mark = VGroup(Line(UP + LEFT, DOWN + RIGHT), Line(UP + RIGHT, DOWN + LEFT)).scale(0.2).set_color(RED)
        lost_marks = VGroup(*[x_mark.copy().move_to(line_obj.get_center()) for line_obj in [b_bottom, b_left, b_right]])
        reward_m2 = MathTex("-2", color=RED).scale(1.5).next_to(center_pixel, RIGHT, buff=0.8)
        
        self.play(Create(lost_marks), Write(reward_m2))
        
        # Update Bar Chart (Bar 2: value returns to zero line)
        bar2 = Rectangle(width=0.6, height=0.1, fill_opacity=1, fill_color=RED, stroke_width=0)
        bar2.move_to(chart_base + RIGHT * 2.0 + UP * 0.05)
        self.play(FadeIn(bar2))
        
        self.wait(2)