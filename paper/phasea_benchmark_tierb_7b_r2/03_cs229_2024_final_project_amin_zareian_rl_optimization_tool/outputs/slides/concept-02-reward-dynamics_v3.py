from manim import *

class RewardDynamics(Scene):
    def construct(self):
        # 1. Setup Grid and Formula
        formula = MathTex(r"R_t = \text{Border}_{t} - \text{Border}_{t-1}").to_edge(UP)
        
        # Grid indices:
        # 0 1 2
        # 3 4 5
        # 6 7 8
        grid = VGroup(*[Square(side_length=1) for _ in range(9)]).arrange_in_grid(3, 3, buff=0)
        grid.shift(LEFT * 3)
        
        # Initial Colors: Center(4) is RED. Neighbor UP(1) is BLUE. Others RED or GRAY.
        grid[4].set_fill(RED, opacity=1)
        grid[1].set_fill(BLUE, opacity=1)
        grid[3].set_fill(RED, opacity=1)
        grid[5].set_fill(RED, opacity=1)
        grid[7].set_fill(RED, opacity=1)
        for i in [0, 2, 6, 8]:
            grid[i].set_fill(GRAY, opacity=0.3)
            
        self.add(formula, grid)

        # 2. Setup Existing Border (4 is RED, 1 is BLUE)
        # Position the line on the edge between center and top neighbor
        border_top = Line(
            grid[4].get_top() + LEFT * 0.5, 
            grid[4].get_top() + RIGHT * 0.5, 
            color=WHITE, 
            stroke_width=6
        )
        self.add(border_top)

        # 3. Animate the center pixel flipping from RED to BLUE
        self.play(grid[4].animate.set_fill(BLUE), run_time=1)
        
        # 4. Highlight borders lost (now 4 is BLUE and 1 is BLUE)
        # Manual Cross instead of 'Cross' class
        l1 = Line(UL, DR, color=RED).scale(0.2).move_to(border_top.get_center())
        l2 = Line(UR, DL, color=RED).scale(0.2).move_to(border_top.get_center())
        red_x = VGroup(l1, l2)
        
        self.play(Create(red_x))

        # 5. Highlight new borders created (4 is BLUE, neighbors 3,5,7 are RED)
        new_border_left = Line(grid[4].get_left() + UP*0.5, grid[4].get_left() + DOWN*0.5, color=GREEN, stroke_width=8)
        new_border_right = Line(grid[4].get_right() + UP*0.5, grid[4].get_right() + DOWN*0.5, color=GREEN, stroke_width=8)
        new_border_bottom = Line(grid[4].get_bottom() + LEFT*0.5, grid[4].get_bottom() + RIGHT*0.5, color=GREEN, stroke_width=8)
        
        self.play(
            Create(new_border_left),
            Create(new_border_right),
            Create(new_border_bottom),
            run_time=1
        )

        # 6. Display Reward Text
        reward_text = MathTex(r"+2", color=GREEN).scale(1.5).next_to(grid, RIGHT, buff=0.5)
        self.play(Write(reward_text), reward_text.animate.shift(UP * 0.5))

        # 7. Manual Bar Chart (Replacing disallowed 'Axes' class)
        chart_origin = RIGHT * 3 + DOWN * 2
        x_axis = Line(chart_origin, chart_origin + RIGHT * 4)
        y_axis = Line(chart_origin, chart_origin + UP * 3)
        y_label = MathTex(r"\text{Reward}").scale(0.7).next_to(y_axis, UP)
        x_label = MathTex(r"\text{Time}").scale(0.7).next_to(x_axis, RIGHT)
        
        bar1 = Rectangle(width=0.6, height=0.8, fill_opacity=0.8, color=BLUE).move_to(chart_origin + RIGHT * 0.8 + UP * 0.4)
        bar2 = Rectangle(width=0.6, height=2.2, fill_opacity=0.8, color=BLUE).move_to(chart_origin + RIGHT * 1.8 + UP * 1.1)
        
        self.play(Create(x_axis), Create(y_axis), Write(x_label), Write(y_label))
        self.play(FadeIn(bar1))
        self.wait(0.5)
        self.play(FadeIn(bar2))

        self.wait(2)