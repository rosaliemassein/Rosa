from manim import *

class Concept01SpatialGridEncoding(Scene):
    def construct(self):
        # 1. Setup Parameters
        board_radius = 2
        n = 4 * board_radius + 1 # n = 9
        pi_val = 3.14159265
        sqrt3 = 1.73205081
        
        # 2. Create Hexagonal Grid
        # Using axial coordinates to create a hexagonal shape
        hex_grid = VGroup()
        for q in range(-board_radius, board_radius + 1):
            for r in range(-board_radius, board_radius + 1):
                if abs(q + r) <= board_radius:
                    # Hexagonal to Cartesian conversion
                    x_pos = 0.5 * (1.5 * q)
                    y_pos = 0.5 * (sqrt3 / 2.0 * q + sqrt3 * r)
                    hex_grid.add(Circle(radius=0.15, color=WHITE, stroke_width=2).move_to([x_pos, y_pos, 0]))
        
        hex_grid.move_to(ORIGIN)
        self.play(Create(hex_grid), run_time=1.5)
        self.wait(0.5)

        # 3. Simulate 3D Tilt via 2D Transformation
        # We apply a matrix to simulate a perspective view without using ThreeDScene
        tilted_hex = hex_grid.copy()
        # Matrix mimics a tilt: stretch y and shear x
        tilted_hex.apply_matrix([
            [1, 0.5, 0],
            [0, 0.5, 0],
            [0, 0, 1]
        ])
        tilted_hex.move_to(ORIGIN)
        self.play(Transform(hex_grid, tilted_hex), run_time=1.2)
        self.wait(0.5)

        # 4. Morph into Square Grid
        # Create a grid of cells (Squares)
        square_grid = VGroup()
        cell_size = 0.35
        for i in range(n):
            for j in range(n):
                cell = Square(side_length=cell_size, stroke_width=1, stroke_color=WHITE)
                cell.move_to([(i - n/2.0 + 0.5) * cell_size, (j - n/2.0 + 0.5) * cell_size, 0])
                square_grid.add(cell)
        
        # Apply the same "perspective" matrix to the square grid
        square_grid.apply_matrix([
            [1, 0.5, 0],
            [0, 0.5, 0],
            [0, 0, 1]
        ])
        square_grid.move_to(ORIGIN)
        
        self.play(Transform(hex_grid, square_grid), run_time=1.5)
        self.wait(0.5)

        # 5. Split into Three Layers
        layer_colors = [BLUE, GREEN, RED]
        layer_names = ["Self Pieces", "Target Zone", "Opponent Pieces"]
        
        layer_stack = VGroup()
        for i in range(3):
            # Create a layer with a specific color
            lyr = square_grid.copy()
            lyr.set_color(layer_colors[i])
            
            # Fill the layer with some semi-transparent highlights to represent data
            highlights = VGroup()
            # Selected indices for visual representation
            if i == 0:
                indices = [12, 13, 22, 40]
            elif i == 1:
                indices = [70, 71, 79, 80]
            else:
                indices = [5, 6, 15, 33]
                
            for idx in indices:
                highlight_sq = lyr[idx].copy()
                highlight_sq.set_fill(layer_colors[i], opacity=0.7)
                highlights.add(highlight_sq)
            
            # Combine grid lines and filled pieces
            layer_group = VGroup(lyr, highlights)
            # Shift vertically to show the stack
            layer_group.shift(UP * (i - 1) * 2.2)
            layer_stack.add(layer_group)

        # Animate the transition to the layered stack
        self.play(Transform(hex_grid, layer_stack), run_time=2)
        
        # 6. Labels and Text
        # Using Text as a replacement for MathTex
        dim_str = str(n) + " x " + str(n) + " x 3"
        dim_label = Text(dim_str, font_size=32).to_corner(UP + LEFT)
        formula_label = Text("n = 4 * radius + 1", font_size=22).next_to(dim_label, DOWN, aligned_edge=UP + LEFT)
        
        self.play(Write(dim_label), Write(formula_label))

        # Add labels to the side of each layer
        side_labels = VGroup()
        for i in range(3):
            lbl = Text(layer_names[i], color=layer_colors[i], font_size=20)
            lbl.next_to(layer_stack[i], RIGHT, buff=0.8)
            side_labels.add(lbl)
            
        self.play(FadeIn(side_labels))
        
        # Narration subtitle
        narration = Text(
            "Encoding the game state into a three-layered stack.",
            font_size=24
        ).to_edge(DOWN)
        self.play(Write(narration))
        
        self.wait(3)