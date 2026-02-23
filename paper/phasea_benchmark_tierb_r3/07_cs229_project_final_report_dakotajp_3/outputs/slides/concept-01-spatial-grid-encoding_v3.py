from manim import *
import numpy as np

class Concept01SpatialGridEncoding(Scene):
    def construct(self):
        # Define board radius and n
        board_radius = 2
        n = 4 * board_radius + 1  # n = 9

        # 1. Create a hexagonal grid of circles
        hex_grid = VGroup()
        for r in range(-board_radius, board_radius + 1):
            for c in range(max(-board_radius, -r - board_radius), min(board_radius, -r + board_radius) + 1):
                # Standard axial to pixel conversion
                x = 0.5 * (3/2 * r)
                y = 0.5 * (np.sqrt(3)/2 * r + np.sqrt(3) * c)
                circle = Circle(radius=0.2, color=GOLD, stroke_width=2)
                circle.move_to([x, y, 0])
                hex_grid.add(circle)
        
        hex_grid.center()

        # Show the board
        self.play(Create(hex_grid))
        self.wait(1)

        # 2. Tilt into perspective (Simulated in 2D using scale/rotate)
        self.play(
            hex_grid.animate.stretch(0.5, dim=1).rotate(-20 * DEGREES),
            run_time=1.5
        )
        self.wait(0.5)

        # 3. Morph into a square grid of cells
        # Create a template for a square grid cell
        square_grid = VGroup(*[
            Square(side_length=0.35, stroke_width=1, color=WHITE)
            for _ in range(n * n)
        ]).arrange_in_grid(n, n, buff=0.05)
        
        # Match the "perspective" tilt
        square_grid.stretch(0.5, dim=1).rotate(-20 * DEGREES)
        square_grid.move_to(ORIGIN)

        self.play(ReplacementTransform(hex_grid, square_grid))
        self.wait(1)

        # 4. Split into three layers floating vertically (staggered in 2D)
        # Use a diagonal offset to simulate vertical stacking in a 2D plane
        stack_offset = UP * 1.0 + RIGHT * 0.5
        
        colors = [BLUE, GREEN, RED]
        labels = ["Self Pieces", "Target Zone", "Opponent Pieces"]
        layer_group = VGroup()

        for i, color in enumerate(colors):
            layer = VGroup(*[
                Square(side_length=0.35, fill_opacity=0.4, fill_color=color, stroke_width=1, stroke_color=color)
                for _ in range(n * n)
            ]).arrange_in_grid(n, n, buff=0.05)
            
            layer.stretch(0.5, dim=1).rotate(-20 * DEGREES)
            # Position each layer with an increasing offset
            layer.move_to(ORIGIN + i * stack_offset)
            layer_group.add(layer)

        # Animate the transition from the single grid to three floating layers
        self.play(
            ReplacementTransform(square_grid, layer_group[0]),
            FadeIn(layer_group[1]),
            FadeIn(layer_group[2]),
            run_time=2
        )
        self.wait(1)

        # 5. Label the dimensions and layers
        # Dimensions n x n x 3
        dim_tex = MathTex("n", "\\times", "n", "\\times", "3", color=YELLOW).scale(1.2)
        dim_tex.to_corner(UL)
        
        # Formula reference
        formula = MathTex("n = 4 \\times \\text{board radius} + 1", font_size=32)
        formula.next_to(dim_tex, DOWN, aligned_edge=LEFT)

        # Legend for layers
        legend = VGroup()
        for i, (color, name) in enumerate(zip(colors, labels)):
            item = Text(f"Layer {i+1}: {name}", color=color, font_size=24)
            legend.add(item)
        legend.arrange(DOWN, aligned_edge=LEFT).to_corner(DL)

        self.play(
            Write(dim_tex),
            FadeIn(formula),
            FadeIn(legend)
        )

        self.wait(3)