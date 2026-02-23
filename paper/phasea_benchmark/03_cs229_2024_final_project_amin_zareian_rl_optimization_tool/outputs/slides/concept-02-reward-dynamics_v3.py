from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Setup Formula
        formula = MathTex(r"R_t = Border_{t} - Border_{t-1}").to_edge(UP)
        self.add(formula)

        # 2. Create a 3x3 Grid
        # Using simple loops and VGroups for maximum compatibility
        colors = [
            BLUE, BLUE, BLUE,
            RED,  RED,  RED,
            BLUE, RED,  BLUE
        ]
        
        squares = []
        for i in range(9):
            sq = Square(side_length=0.8)
            sq.set_fill(colors[i], opacity=0.6)
            sq.set_stroke(WHITE, width=2)
            squares.append(sq)
            
        row1 = VGroup(*squares[0:3]).arrange(RIGHT, buff=0.1)
        row2 = VGroup(*squares[3:6]).arrange(RIGHT, buff=0.1)
        row3 = VGroup(*squares[6:9]).arrange(RIGHT, buff=0.1)
        grid = VGroup(row1, row2, row3).arrange(DOWN, buff=0.1).shift(LEFT * 3)
        
        self.play(Create(grid))

        # 3. Focus on center pixel and highlight neighbors
        center_sq = squares[4]
        neighbor_indices = [1, 3, 5, 7]
        neighbor_group = VGroup(*[squares[i] for i in neighbor_indices])
        
        self.play(center_sq.animate.set_stroke(YELLOW, width=6))
        self.play(neighbor_group.animate.set_stroke(WHITE, width=6))
        self.wait(0.5)

        # 4. Animate the center pixel flipping from Red to Blue
        # Before: 1 neighbor (top) has different color (Blue vs Red). Border = 1.
        # After: 3 neighbors (left, right, bottom) have different color (Red vs Blue). Border = 3.
        # Change = 3 - 1 = +2.
        self.play(center_sq.animate.set_fill(BLUE))

        # 5. Visualize new borders (Green) and lost borders (Red X)
        # Lost border on top
        lost_line = Line(
            center_sq.get_corner(UL), center_sq.get_corner(UR), 
            color=RED, stroke_width=8
        ).shift(UP * 0.05)
        
        # Simple X mark using two lines
        x_mark = VGroup(
            Line(LEFT, RIGHT).rotate(45 * DEGREES),
            Line(LEFT, RIGHT).rotate(-45 * DEGREES)
        ).scale(0.15).move_to(lost_line).set_color(RED)

        # New borders on left, right, bottom
        new_left = Line(center_sq.get_corner(UL), center_sq.get_corner(DL), color=GREEN, stroke_width=8).shift(LEFT * 0.05)
        new_right = Line(center_sq.get_corner(UR), center_sq.get_corner(DR), color=GREEN, stroke_width=8).shift(RIGHT * 0.05)
        new_bottom = Line(center_sq.get_corner(DL), center_sq.get_corner(DR), color=GREEN, stroke_width=8).shift(DOWN * 0.05)

        self.play(Create(new_left), Create(new_right), Create(new_bottom), Create(lost_line))
        self.play(Create(x_mark))

        # 6. Reward Text
        reward_text = Text("+2", color=GREEN).next_to(grid, RIGHT, buff=0.5)
        self.play(Write(reward_text))

        # 7. Manual Bar Chart using Axes and Rectangles
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 5, 1],
            x_length=4,
            y_length=3,
            axis_config={"include_tip": False}
        ).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.5)
        
        axes_labels = axes.get_axis_labels(x_label="step", y_label="Reward")

        # Create bars as simple Rectangles
        def get_bar(val, pos_x, color=YELLOW):
            height = abs(axes.coords_to_point(0, val)[1] - axes.coords_to_point(0, 0)[1])
            bar = Rectangle(
                width=0.5, 
                height=height,
                fill_opacity=0.8,
                fill_color=color,
                stroke_width=1
            )
            bar.move_to(axes.coords_to_point(pos_x, 0), aligned_edge=DOWN)
            return bar

        bar1 = get_bar(1.0, 1)
        bar2 = get_bar(1.5, 2)
        bar3 = get_bar(3.5, 3, color=GREEN) # The new state after +2 reward

        self.play(Create(axes), Write(axes_labels))
        self.play(Create(bar1), Create(bar2))
        self.wait(0.5)
        self.play(Create(bar3))

        # 8. Final narration text
        narration = Text(
            "Spatial arrangement becomes value-driven decisions.",
            font_size=24
        ).to_edge(DOWN)
        self.play(Write(narration))
        self.wait(2)