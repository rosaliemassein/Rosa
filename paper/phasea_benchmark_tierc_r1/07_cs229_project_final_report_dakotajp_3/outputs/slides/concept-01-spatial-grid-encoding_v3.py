from manim import *
import numpy as np

class Concept01SpatialGridEncoding(Scene):
    def construct(self):
        # 1. Setup and Board Radius
        board_radius = 2
        n = 4 * board_radius + 1
        
        # 2. Create Hexagonal Grid of Circles
        # Standard axial coordinates for a hexagon
        hex_grid = VGroup()
        for r in range(-board_radius, board_radius + 1):
            for q in range(-board_radius, board_radius + 1):
                if abs(r + q) <= board_radius:
                    # Convert axial to pixel coordinates
                    x = 0.5 * (1.5 * q)
                    y = 0.5 * (np.sqrt(3) * (r + q / 2))
                    circle = Circle(radius=0.2, color=WHITE, stroke_width=2)
                    circle.move_to([x, y, 0])
                    hex_grid.add(circle)
        
        hex_grid.center()
        
        # 3. Animate Hexagonal Grid
        self.play(Create(hex_grid), run_time=1.5)
        self.wait(0.5)

        # 4. Tilt into 3D perspective
        self.play(
            hex_grid.animate.set_euler_angles(phi=60 * DEGREES, theta=-30 * DEGREES),
            run_time=1.5
        )
        self.wait(0.5)

        # 5. Morph into a Square Grid of Cells
        # We'll create a flat n x n grid of squares first
        square_grid = VGroup(*[
            Square(side_length=0.3, stroke_width=1, fill_opacity=0.1, fill_color=WHITE)
            for _ in range(n * n)
        ]).arrange_in_grid(rows=n, cols=n, buff=0.05)
        square_grid.set_euler_angles(phi=60 * DEGREES, theta=-30 * DEGREES)
        
        self.play(
            ReplacementTransform(hex_grid, square_grid),
            run_time=1.5
        )
        self.wait(0.5)

        # 6. Split into three separate layers floating vertically
        # Layer 1: Self (Blue), Layer 2: Target (Green), Layer 3: Opponent (Red)
        layer_spacing = 1.2
        
        layer1 = square_grid.copy().set_color(BLUE).shift(UP * layer_spacing)
        layer2 = square_grid.copy().set_color(GREEN).shift(ORIGIN)
        layer3 = square_grid.copy().set_color(RED).shift(DOWN * layer_spacing)
        
        # Add highlights to make them look like data layers
        for layer, color, indices in zip(
            [layer1, layer2, layer3], 
            [BLUE, GREEN, RED],
            [[10, 12, 14, 25], [40, 41, 42], [60, 62, 70]]
        ):
            layer.set_fill(color, opacity=0.3)
            for i in indices:
                if i < len(layer):
                    layer[i].set_fill(color, opacity=0.8)

        self.play(
            ReplacementTransform(square_grid, VGroup(layer1, layer2, layer3)),
            run_time=2
        )
        
        # 7. Labels and Dimensions
        # Label each layer
        label_1 = Text("Current Player", font_size=20).next_to(layer1, LEFT, buff=0.5)
        label_2 = Text("Target Zone", font_size=20).next_to(layer2, LEFT, buff=0.5)
        label_3 = Text("Opponent Pieces", font_size=20).next_to(layer3, LEFT, buff=0.5)
        
        # Math labels
        formula_label = MathTex("n = 4 \\times \\text{board radius} + 1", font_size=30).to_corner(UL)
        dim_label = MathTex("n \\times n \\times 3", font_size=42, color=YELLOW).to_edge(RIGHT, buff=1.5)

        self.play(
            FadeIn(label_1), FadeIn(label_2), FadeIn(label_3),
            Write(formula_label),
            Write(dim_label)
        )
        
        # 8. Final Narration/Text
        narration_text = Text(
            "Encoding hex-geometry into a\nthree-layered square stack.",
            font_size=24,
            line_spacing=1.2
        ).to_edge(DOWN, buff=0.5)
        
        self.play(FadeIn(narration_text))
        self.wait(3)