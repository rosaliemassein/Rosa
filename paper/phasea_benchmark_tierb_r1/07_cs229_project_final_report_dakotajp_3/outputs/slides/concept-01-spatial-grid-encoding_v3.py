from manim import *

class ConceptSpatialGridEncoding(Scene):
    def construct(self):
        # 1. Setup Parameters
        # Using a radius that makes the grid visually manageable
        board_radius = 1
        n = 4 * board_radius + 1  # n = 5
        
        # 2. Create Hexagonal Grid
        # We represent the hexagonal board with circles in a 2D layout
        hex_grid = VGroup()
        for r in range(-2, 3):
            # Number of circles in this row to create a hexagonal shape
            num_cols = 5 - abs(r)
            for c in range(num_cols):
                dot = Circle(radius=0.18, color=WHITE, stroke_width=2)
                # Position calculation for hexagonal arrangement
                x = (c - (num_cols - 1) / 2) * 0.5
                y = r * 0.433
                dot.move_to([x, y, 0])
                hex_grid.add(dot)
        
        hex_grid.move_to(ORIGIN)
        self.play(Create(hex_grid), run_time=1.5)
        self.wait(1)

        # 3. Animate tilting into a "3D" perspective using 2D transformations
        # (Stretch and Rotate simulate the tilt without using ThreeDScene)
        self.play(
            hex_grid.animate.scale(0.9).stretch(0.4, dim=1).rotate(20 * DEGREES),
            run_time=2
        )
        self.wait(1)

        # 4. Morph the hexagonal grid into a square grid of cells
        square_grid = VGroup()
        cell_size = 0.45
        for i in range(n):
            for j in range(n):
                cell = Square(side_length=cell_size * 0.9, stroke_width=2)
                # Layout in an n x n square grid
                cell.move_to([
                    (i - (n - 1) / 2) * cell_size,
                    (j - (n - 1) / 2) * cell_size,
                    0
                ])
                square_grid.add(cell)
        
        # Apply the same "3D-like" perspective to the square grid
        square_grid.stretch(0.4, dim=1).rotate(20 * DEGREES)

        self.play(ReplacementTransform(hex_grid, square_grid), run_time=2)
        self.wait(1)

        # 5. Split this square grid into three separate layers floating "vertically"
        # We simulate vertical floating by shifting layers along the UP/RIGHT diagonal
        stack_offset = UP * 1.6 + RIGHT * 0.4
        
        # Layer 1: Self (Blue)
        layer_1 = square_grid.copy().set_color(BLUE).set_stroke(BLUE, opacity=0.8)
        # Layer 2: Target (Green) - This stays in the middle
        layer_2 = square_grid.copy().set_color(GREEN).set_stroke(GREEN, opacity=0.8)
        # Layer 3: Opponent (Red)
        layer_3 = square_grid.copy().set_color(RED).set_stroke(RED, opacity=0.8)

        # Highlight pieces in each layer (encoding specific cells)
        # Indices for a 5x5 grid (0-24)
        for idx in [6, 7, 11]: 
            layer_1[idx].set_fill(BLUE, opacity=0.7)
        for idx in [12]: 
            layer_2[idx].set_fill(GREEN, opacity=0.7)
        for idx in [13, 17, 18]: 
            layer_3[idx].set_fill(RED, opacity=0.7)

        self.play(
            layer_1.animate.shift(stack_offset),
            layer_3.animate.shift(-stack_offset),
            ReplacementTransform(square_grid, layer_2),
            run_time=2.5
        )
        self.wait(1)

        # 6. Labels and Dimensions
        formula = MathTex(r"n = 4 \times \text{board radius} + 1").to_edge(UP, buff=0.5)
        dim_label = MathTex(r"n \times n \times 3").to_edge(DOWN, buff=1)
        
        # Adding labels for each layer
        label_1 = Text("Layer 1: Self Pieces", color=BLUE).scale(0.4).next_to(layer_1, LEFT, buff=0.5)
        label_2 = Text("Layer 2: Target Zone", color=GREEN).scale(0.4).next_to(layer_2, LEFT, buff=0.5)
        label_3 = Text("Layer 3: Opponent Pieces", color=RED).scale(0.4).next_to(layer_3, LEFT, buff=0.5)

        self.play(
            Write(formula),
            Write(dim_label),
            FadeIn(label_1),
            FadeIn(label_2),
            FadeIn(label_3)
        )
        
        self.wait(3)