from manim import *
import numpy as np

class SpatialGridEncoding(Scene):
    def construct(self):
        # Configuration: n = 4 * board_radius + 1
        # For a compact visualization, we'll use a board radius of 1, so n = 5
        n_val = 5
        board_radius = 1
        
        # 1. Create Hexagonal Grid
        # Using axial coordinates (q, r) to represent the hexagonal layout
        hex_grid = VGroup()
        for q in range(-board_radius, board_radius + 1):
            r1 = max(-board_radius, -q - board_radius)
            r2 = min(board_radius, -q + board_radius)
            for r in range(r1, r2 + 1):
                # Convert axial coordinates to 2D pixel coordinates
                # x = size * 3/2 * q
                # y = size * sqrt(3)/2 * q + sqrt(3) * r
                x_pos = 0.7 * (1.5 * q)
                y_pos = 0.7 * (np.sqrt(3)/2 * q + np.sqrt(3) * r)
                circle = Circle(radius=0.2, color=BLUE, fill_opacity=0.8, fill_color=BLUE)
                circle.move_to([x_pos, y_pos, 0])
                hex_grid.add(circle)
        
        hex_grid.move_to(ORIGIN)
        
        # Display initial hexagonal board
        self.play(Create(hex_grid))
        self.wait(1)
        
        # 2. Simulate tilting into 3D perspective using 2D transformations
        # Shear the grid and squash it vertically to mimic a 3D plane
        tilt_matrix = [[1, 0.5, 0], [0, 0.5, 0], [0, 0, 1]]
        self.play(hex_grid.animate.apply_matrix(tilt_matrix), run_time=1.5)
        self.wait(0.5)
        
        # 3. Create Square Grid Layers
        def create_square_layer(color):
            layer = VGroup()
            cell_size = 0.4
            for i in range(n_val):
                for j in range(n_val):
                    square = Square(side_length=cell_size, color=color, fill_opacity=0.3, fill_color=color)
                    # Center the grid
                    square.move_to([(i - n_val/2 + 0.5) * cell_size, (j - n_val/2 + 0.5) * cell_size, 0])
                    layer.add(square)
            # Apply same perspective tilt to the square layers
            layer.apply_matrix(tilt_matrix)
            return layer

        layer_self = create_square_layer(BLUE)
        layer_target = create_square_layer(GREEN)
        layer_opp = create_square_layer(RED)
        
        # 4. Morph the hexagonal board into the first square grid layer
        self.play(ReplacementTransform(hex_grid, layer_self))
        self.wait(0.5)
        
        # 5. Stack the layers vertically (simulated with 2D offsets)
        # Shift Layer 1 up-right and Layer 3 down-left to create a floating stack effect
        stack_offset = np.array([0.5, 1.5, 0])
        
        self.play(
            layer_self.animate.shift(stack_offset),
            FadeIn(layer_target), # Layer 2 stays centered
            layer_opp.animate.shift(-stack_offset),
            run_time=2
        )
        self.wait(1)
        
        # 6. Annotations and Labels
        # Dimension Label
        dim_label = MathTex(r"n \times n \times 3").scale(1.2).to_corner(UL, buff=0.5)
        formula_label = MathTex(r"n = 4 \times \text{board radius} + 1").scale(0.7).next_to(dim_label, DOWN, aligned_edge=LEFT)
        
        # Layer specific labels
        label_1 = Text("Layer 1: Self Pieces", color=BLUE).scale(0.4).next_to(layer_self, RIGHT, buff=0.5)
        label_2 = Text("Layer 2: Target Zone", color=GREEN).scale(0.4).next_to(layer_target, RIGHT, buff=0.5)
        label_3 = Text("Layer 3: Opponent Pieces", color=RED).scale(0.4).next_to(layer_opp, RIGHT, buff=0.5)
        
        self.play(
            Write(dim_label),
            Write(formula_label),
            FadeIn(label_1),
            FadeIn(label_2),
            FadeIn(label_3)
        )
        
        self.wait(2)