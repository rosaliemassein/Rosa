from manim import *
import numpy as np

class Concept01SpatialGridEncoding(Scene):
    def construct(self):
        # 1. Define the board parameters
        # n = 4 * board_radius + 1
        board_radius = 2
        n = 9
        
        # 2. Create the hexagonal grid of circles
        # Using a simple axial coordinate logic to generate a hex-shaped layout
        hex_circles = VGroup()
        for r in range(-board_radius, board_radius + 1):
            for q in range(-board_radius, board_radius + 1):
                if abs(r + q) <= board_radius:
                    # Cartesian conversion
                    x_pos = 0.5 * (3/2 * r)
                    y_pos = 0.5 * (np.sqrt(3)/2 * r + np.sqrt(3) * q)
                    dot = Circle(radius=0.15, color=WHITE, stroke_width=2)
                    dot.move_to([x_pos, y_pos, 0])
                    hex_circles.add(dot)
        
        hex_circles.move_to(ORIGIN)
        
        # Initial display
        self.play(Create(hex_circles), run_time=2)
        self.wait(1)

        # 3. Simulate "tilting" into perspective using 2D scaling/stretching
        # Since move_camera/3D is disallowed, we simulate the effect
        tilted_hexes = hex_circles.copy()
        self.play(
            tilted_hexes.animate.stretch(0.5, dim=1).scale(0.8).set_stroke(opacity=0.6),
            FadeOut(hex_circles),
            run_time=1.5
        )

        # 4. Morph into a square grid of cells (n x n)
        square_grid = VGroup()
        cell_size = 0.3
        grid_offset = (n - 1) * cell_size / 2
        
        for i in range(n):
            for j in range(n):
                cell = Square(side_length=cell_size, color=WHITE, stroke_width=1)
                cell.move_to([i * cell_size - grid_offset, j * cell_size - grid_offset, 0])
                square_grid.add(cell)
        
        # Keep the "tilted" look for the square grid initially
        square_grid.stretch(0.5, dim=1).scale(0.8)
        
        self.play(ReplacementTransform(tilted_hexes, square_grid), run_time=2)
        self.wait(1)

        # 5. Split this square grid into three separate, semi-transparent layers floating vertically
        # We define a vertical offset for the 2D "stack"
        v_offset = 1.6
        
        layer1 = square_grid.copy().set_color(BLUE).shift(UP * v_offset)
        layer2 = square_grid.copy().set_color(GREEN).shift(ORIGIN)
        layer3 = square_grid.copy().set_color(RED).shift(DOWN * v_offset)
        
        # Add highlight "pegs" to show data encoding
        def get_pegs(grid, color, indices):
            pegs = VGroup()
            for idx in indices:
                peg = Square(side_length=cell_size, fill_opacity=0.8, fill_color=color, stroke_width=0)
                peg.move_to(grid[idx].get_center())
                peg.match_points(grid[idx]) # Ensures the peg matches the tilted shape
                pegs.add(peg)
            return pegs

        # Highlight random pieces for demonstration
        pegs1 = get_pegs(layer1, BLUE, [12, 13, 21, 22])
        pegs2 = get_pegs(layer2, GREEN, [40, 41, 49, 50])
        pegs3 = get_pegs(layer3, RED, [60, 61, 70, 71])

        # Layer labels
        label1 = Text("Layer 1: Current Player", font_size=18, color=BLUE).next_to(layer1, RIGHT, buff=0.5)
        label2 = Text("Layer 2: Target Zone", font_size=18, color=GREEN).next_to(layer2, RIGHT, buff=0.5)
        label3 = Text("Layer 3: Opponent", font_size=18, color=RED).next_to(layer3, RIGHT, buff=0.5)

        # Dimension Label
        dim_label = MathTex("n \\times n \\times 3", color=WHITE).to_corner(UL)
        formula = MathTex("n = 4 \\times 2 + 1 = 9", color=GRAY).scale(0.7).next_to(dim_label, DOWN, aligned_edge=LEFT)

        # Animation: Splitting the layers
        self.play(
            ReplacementTransform(square_grid.copy(), layer1),
            ReplacementTransform(square_grid.copy(), layer2),
            ReplacementTransform(square_grid, layer3),
            run_time=2
        )
        
        self.play(
            FadeIn(pegs1), FadeIn(pegs2), FadeIn(pegs3),
            Write(label1), Write(label2), Write(label3),
            Write(dim_label), Write(formula),
            run_time=1.5
        )
        
        self.wait(2)