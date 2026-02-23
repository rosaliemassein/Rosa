from manim import *

class ConceptRewardDynamics(Scene):
    def construct(self):
        # 1. Setup Grid (3x3 pixels)
        # Using Squares to represent pixels
        grid = VGroup(*[
            Square(side_length=1).set_fill(RED, opacity=0.8).set_stroke(WHITE, width=2)
            for _ in range(9)
        ]).arrange_in_grid(rows=3, cols=3, buff=0).shift(LEFT * 3)

        # Set specific neighbor to BLUE to create initial border
        # Indices: 0 1 2 / 3 4 5 / 6 7 8. 4 is center. 5 is Right neighbor.
        grid[5].set_fill(BLUE, opacity=0.8)
        
        # 2. Setup UI elements (Title, Formula, Chart)
        title = Text("Reward Dynamics: Border Change", font_size=32).to_edge(UP)
        formula = MathTex(r"R_t = Border_{t} - Border_{t-1}").next_to(title, DOWN)
        
        # Manual Bar Chart using Axes and Rectangles
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 10, 2],
            x_length=4,
            y_length=3,
            axis_config={"include_tip": False}
        ).shift(RIGHT * 3.5 + DOWN * 0.5)
        chart_label = Text("Cumulative Reward", font_size=24).next_to(axes, UP)
        
        self.add(grid, title, formula, axes, chart_label)

        # 3. Highlighting the logic focus
        center_idx = 4
        neighbor_indices = [1, 3, 5, 7] # Top, Left, Right, Bottom
        
        hl_center = SurroundingRectangle(grid[center_idx], color=YELLOW, buff=0)
        hl_neighbors = VGroup(*[
            SurroundingRectangle(grid[i], color=YELLOW, buff=-0.05) 
            for i in neighbor_indices
        ])
        
        self.play(Create(hl_center))
        self.play(FadeIn(hl_neighbors))
        self.wait(1)

        # 4. Show initial border (RED center vs BLUE neighbor 5)
        initial_border = Line(
            grid[center_idx].get_corner(UR), grid[center_idx].get_corner(DR), 
            color=WHITE, stroke_width=6
        )
        self.add(initial_border)
        self.wait(1)

        # 5. The Flip Animation (RED -> BLUE)
        self.play(
            grid[center_idx].animate.set_fill(BLUE),
            FadeOut(initial_border),
            run_time=1
        )

        # 6. Visualize Resulting Border Changes
        # Gain borders: Center(BLUE) vs Neighbors 1, 3, 7 (RED)
        b_top = Line(grid[4].get_corner(UL), grid[4].get_corner(UR), color=GREEN, stroke_width=8)
        b_left = Line(grid[4].get_corner(UL), grid[4].get_corner(DL), color=GREEN, stroke_width=8)
        b_bottom = Line(grid[4].get_corner(DL), grid[4].get_corner(DR), color=GREEN, stroke_width=8)
        
        # Lost border: Center(BLUE) vs Neighbor 5 (BLUE)
        lost_edge = Line(grid[4].get_corner(UR), grid[4].get_corner(DR), color=RED, stroke_width=4)
        # Manual Cross (X)
        cross_x = VGroup(
            Line(UP + LEFT, DOWN + RIGHT), 
            Line(UP + RIGHT, DOWN + LEFT)
        ).scale(0.15).move_to(lost_edge.get_center()).set_color(RED)

        reward_val = Text("+2", color=GREEN, font_size=44).next_to(grid[4], UR, buff=0.2)

        self.play(
            Create(b_top), Create(b_left), Create(b_bottom),
            Create(lost_edge), Create(cross_x),
            Write(reward_val)
        )
        self.wait(1)

        # 7. Update Reward Chart
        # Create a bar representing the reward
        reward_bar = Rectangle(
            width=0.5, 
            height=2 * (3/10), # scale: y_length/y_max = 3/10
            fill_color=GREEN, 
            fill_opacity=0.8,
            stroke_width=1
        ).move_to(axes.c2p(1, 0), aligned_edge=DOWN)
        
        self.play(FadeIn(reward_bar, shift=UP))
        self.wait(1)

        # 8. Narration Text
        narration = Text(
            "Agent receives positive reward for increasing borders.\nThis turns spatial problems into value-driven decisions.",
            font_size=22,
            line_spacing=1.2
        ).to_edge(DOWN)
        
        self.play(Write(narration))
        self.wait(3)

        # 9. Final Cleanup
        self.play(
            FadeOut(hl_center), FadeOut(hl_neighbors),
            FadeOut(b_top), FadeOut(b_left), FadeOut(b_bottom),
            FadeOut(lost_edge), FadeOut(cross_x), FadeOut(reward_val)
        )
        self.wait(1)