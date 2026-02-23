from manim import *
import numpy as np

class SpatialGridEncoding(Scene):
    def construct(self):
        # Configuration
        board_radius = 2
        # n = 4 * radius + 1 = 9
        n = 9
        
        # 1. Voice/Concept Introduction: Hexagonal Grid
        # Create a basic hexagonal arrangement of circles
        hex_grid = VGroup()
        for r in range(-board_radius * 2, board_radius * 2 + 1):
            for q in range(-board_radius * 2, board_radius * 2 + 1):
                if abs(r + q) <= board_radius * 2:
                    # Hexagonal to Cartesian conversion
                    x = 0.4 * (1.5 * q)
                    y = 0.4 * (np.sqrt(3) / 2 * q + np.sqrt(3) * r)
                    dot = Dot(radius=0.12, color=WHITE)
                    dot.move_to([x, y, 0])
                    hex_grid.add(dot)
        
        hex_grid.move_to(ORIGIN)
        
        # Formula label
        formula = MathTex("n = 4 \\times \\text{board radius} + 1").to_edge(UP)
        
        self.play(Create(hex_grid))
        self.play(Write(formula))
        self.wait(1)

        # 2. Tilt and Morph into Square Grid
        # Since 3D is disallowed, we simulate the "tilt" by scaling and shearing in 2D
        # Then transform to the square coordinate system
        square_grid = VGroup()
        cell_size = 0.35
        for i in range(n):
            for j in range(n):
                rect = Square(side_length=cell_size, stroke_width=1, color=WHITE)
                rect.move_to([(j - n/2) * cell_size, (i - n/2) * cell_size, 0])
                square_grid.add(rect)
        square_grid.move_to(ORIGIN)

        self.play(
            hex_grid.animate.shear(-0.2, direction=RIGHT).scale(0.8),
            run_time=1
        )
        self.play(ReplacementTransform(hex_grid, square_grid))
        self.wait(1)

        # 3. Create three-layered stack
        # To simulate a 3D stack in 2D, we offset the layers diagonally
        layer_colors = [BLUE, GREEN, RED]
        layer_names = ["Layer 1: Current Player (Self)", "Layer 2: Target Destination", "Layer 3: Opponent Pieces"]
        
        layers = VGroup()
        for color in layer_colors:
            layer = square_grid.copy()
            layer.set_color(color).set_stroke(opacity=0.3)
            # Add some "encoded state" highlights to the grid
            for i, cell in enumerate(layer):
                if (i * 7) % 13 < 2:  # Decorative logic for piece placement
                    cell.set_fill(color, opacity=0.6)
            layers.add(layer)

        # Hide the base grid to show the split
        self.play(FadeOut(square_grid))

        # Separate layers vertically/diagonally
        layer_labels = VGroup()
        for i, (layer, name) in enumerate(zip(layers, layer_names)):
            # Distribute layers in 2D to look like a floating stack
            target_pos = (i - 1) * 1.5 * UP + (i - 1) * 0.8 * RIGHT
            label = Text(name, font_size=20, color=layer_colors[i])
            label.next_to(layer, RIGHT, buff=0.5)
            
            # Grouping layer and its label to move them together
            layer_with_label = VGroup(layer, label)
            self.play(
                layer_with_label.animate.move_to(target_pos).scale(0.8),
                run_time=1
            )

        # 4. Dimension label
        dims_label = MathTex("n \\times n \\times 3").to_edge(DOWN)
        self.play(Write(dims_label))
        
        self.wait(2)

        # Final cleanup for nice visual
        self.play(
            FadeOut(formula),
            layers.animate.arrange(RIGHT, buff=0.5).move_to(ORIGIN).scale(0.7),
            FadeOut(VGroup(*[m for m in self.mobjects if isinstance(m, Text)]))
        )
        self.wait(1)