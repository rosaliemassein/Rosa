from manim import *

class RewardDynamics(Scene):
    def construct(self):
        # 1. Setup Grid and Formula
        formula = MathTex(r"R_t = \text{Border}_{t} - \text{Border}_{t-1}").to_edge(UP)
        
        # Create 3x3 grid
        # Center is index 4. Neighbors: 1 (Up), 3 (Left), 5 (Right), 7 (Down)
        grid = VGroup(*[Square(side_length=1) for _ in range(9)]).arrange_in_grid(3, 3, buff=0.1)
        grid.shift(LEFT * 3)
        
        # Initial Colors logic:
        # Before flip: Center(4) is RED. Neighbors 1,3,5 are RED. Neighbor 7 is BLUE.
        # Boundary at bottom (4 vs 7).
        colors = [
            GRAY, RED,  GRAY,
            RED,  RED,  RED,
            GRAY, BLUE, GRAY
        ]
        for i, color in enumerate(colors):
            grid[i].set_fill(color, opacity=0.8)
            grid[i].set_stroke(WHITE, width=2)

        self.add(grid, formula)
        self.wait(1)

        # 2. Highlight neighbors
        center = grid[4]
        neighbors_indices = [1, 3, 5, 7]
        neighbors = VGroup(*[grid[i] for i in neighbors_indices])
        
        highlights = VGroup(*[
            Rectangle(width=1.1, height=1.1, color=YELLOW, stroke_width=4).move_to(grid[i])
            for i in neighbors_indices
        ])
        
        self.play(
            Indicate(center, color=YELLOW),
            Create(highlights),
            run_time=1.5
        )
        self.wait(0.5)

        # 3. Animate the flip (Red to Blue)
        # Flip center Red -> Blue: 
        # New borders at Top(1), Left(3), Right(5) (Blue vs Red) -> +3
        # Lost border at Bottom(7) (Blue vs Blue) -> -1
        # Total Reward = +2
        
        self.play(
            center.animate.set_fill(BLUE),
            FadeOut(highlights),
            run_time=1
        )

        # 4. Show borders created and lost
        # Manually create green lines for new borders
        border_top = Line(center.get_corner(UL), center.get_corner(UR), color=GREEN, stroke_width=8)
        border_left = Line(center.get_corner(UL), center.get_corner(DL), color=GREEN, stroke_width=8)
        border_right = Line(center.get_corner(UR), center.get_corner(DR), color=GREEN, stroke_width=8)
        
        # Manually create red X for lost border at bottom
        border_bottom_pos = Line(center.get_corner(DL), center.get_corner(DR)).get_center()
        red_x = VGroup(
            Line(UL, DR, color=RED, stroke_width=6),
            Line(UR, DL, color=RED, stroke_width=6)
        ).scale(0.2).move_to(border_bottom_pos)
        
        self.play(
            Create(border_top),
            Create(border_left),
            Create(border_right),
            Create(red_x),
            run_time=1
        )

        # 5. Display floating reward text
        reward_text = Text("+2", color=GREEN, font_size=44).next_to(center, UR, buff=0.1)
        self.play(
            Write(reward_text),
            reward_text.animate.shift(UP * 0.5),
            run_time=1
        )

        # 6. Manual Bar Chart using Axes and Rectangles
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 8, 2],
            x_length=4,
            y_length=3,
            axis_config={"include_tip": False}
        ).to_edge(RIGHT, buff=1)
        
        chart_labels = axes.get_axis_labels(x_label="t", y_label="Reward")
        
        # Values: t-2=2, t-1=4, t=6
        bar_heights = [2, 4, 6]
        bars = VGroup()
        for i, val in enumerate(bar_heights):
            # Calculate height in scene units
            h = (axes.c2p(0, val)[1] - axes.c2p(0, 0)[1])
            bar = Rectangle(
                width=0.6, 
                height=h, 
                fill_color=BLUE, 
                fill_opacity=0.7, 
                stroke_color=WHITE
            )
            bar.move_to(axes.c2p(i + 1, 0), DOWN)
            bars.add(bar)

        # Initial state: only first two bars
        current_bars = VGroup(bars[0], bars[1])
        growing_bar = bars[2].copy()
        growing_bar.stretch_to_fit_height(0.01, about_edge=DOWN)

        self.play(
            Create(axes),
            Create(chart_labels),
            FadeIn(current_bars),
            FadeIn(growing_bar)
        )
        self.wait(0.5)
        
        # Animate the cumulative growth
        self.play(
            Transform(growing_bar, bars[2]),
            reward_text.animate.scale(0.6).next_to(bars[2], UP, buff=0.1),
            run_time=1.5
        )

        self.wait(2)