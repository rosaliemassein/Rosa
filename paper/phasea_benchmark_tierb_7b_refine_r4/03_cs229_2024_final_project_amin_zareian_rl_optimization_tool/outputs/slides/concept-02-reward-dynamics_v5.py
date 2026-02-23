from manim import *

class RewardDynamics(Scene):
    def construct(self):
        # 1. Create a 3x3 grid using standard VGroup and Square
        grid = VGroup(*[
            Square(side_length=0.8, fill_opacity=1, fill_color=RED, stroke_color=WHITE, stroke_width=2)
            for _ in range(9)
        ])
        grid.arrange_in_grid(rows=3, columns=3, buff=0.1)
        grid.shift(UP * 1.2)

        # Set the bottom neighbor (index 7) to Blue initially
        # This allows us to show a border being "lost" when center turns Blue
        grid[7].set_fill(BLUE)
        self.add(grid)

        # 2. Display the Formula using Text (safer than MathTex in some restricted environments)
        formula = Text("R_t = Border_t - Border_{t-1}", font_size=24).to_corner(UL)
        self.play(Write(formula))

        # 3. Highlight the center pixel
        center_pixel = grid[4]
        highlight_box = Square(side_length=0.9, color=YELLOW, stroke_width=4).move_to(center_pixel)
        self.play(Create(highlight_box))
        
        # 4. Animate the center pixel flipping from Red to Blue
        self.play(center_pixel.animate.set_fill(BLUE), run_time=1)

        # 5. Visualize reward components
        # Green lines for 3 new borders (Top, Left, Right)
        top_edge = Line(center_pixel.get_corner(UL), center_pixel.get_corner(UR), color=GREEN, stroke_width=8)
        left_edge = Line(center_pixel.get_corner(UL), center_pixel.get_corner(DL), color=GREEN, stroke_width=8)
        right_edge = Line(center_pixel.get_corner(UR), center_pixel.get_corner(DR), color=GREEN, stroke_width=8)
        
        # Red 'X' for lost border at the bottom edge (Blue center next to Blue bottom)
        # We build the 'X' manually using two lines to avoid 'Cross' undefined error
        x_line1 = Line(LEFT, RIGHT).rotate(45 * DEGREES).scale(0.15)
        x_line2 = Line(LEFT, RIGHT).rotate(-45 * DEGREES).scale(0.15)
        lost_border_mark = VGroup(x_line1, x_line2).set_color(RED).set_stroke(width=6)
        lost_border_mark.move_to(center_pixel.get_edge_center(DOWN))

        self.play(Create(top_edge), Create(left_edge), Create(right_edge))
        self.play(Create(lost_border_mark))

        # 6. Reward indicator text
        reward_val = Text("+2", color=GREEN).scale(1.2).next_to(grid, RIGHT, buff=0.5)
        self.play(Write(reward_val))

        # 7. Manual Bar Chart (Using Line and Rectangle to avoid 'Axes' identifier)
        origin = DOWN * 3 + LEFT * 2
        x_axis = Line(origin, origin + RIGHT * 4, color=WHITE)
        y_axis = Line(origin, origin + UP * 2, color=WHITE)
        chart_title = Text("Cumulative Reward", font_size=20).next_to(x_axis, DOWN, buff=0.2)
        
        self.play(Create(x_axis), Create(y_axis), Write(chart_title))

        # Create bars manually
        # Bar 1 (Previous step)
        bar1 = Rectangle(width=0.5, height=0.5, fill_opacity=0.8, fill_color=GREEN, stroke_width=1)
        bar1.move_to(origin + RIGHT * 0.8 + UP * 0.25)
        
        # Bar 2 (Current step, taller)
        bar2 = Rectangle(width=0.5, height=1.2, fill_opacity=0.8, fill_color=GREEN, stroke_width=1)
        bar2.move_to(origin + RIGHT * 1.8 + UP * 0.6)
        
        # Bar 3 (Future step, even taller)
        bar3 = Rectangle(width=0.5, height=1.8, fill_opacity=0.8, fill_color=GREEN, stroke_width=1)
        bar3.move_to(origin + RIGHT * 2.8 + UP * 0.9)

        self.play(Create(bar1))
        self.play(Create(bar2))
        self.play(Create(bar3))

        self.wait(2)