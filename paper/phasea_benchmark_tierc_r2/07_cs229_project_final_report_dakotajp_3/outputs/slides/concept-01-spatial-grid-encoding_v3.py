from manim import *
import numpy as np

class SpatialGridEncoding(Scene):
    def construct(self):
        # Configuration
        board_radius = 2
        n = 4 * board_radius + 1  # n = 9
        circle_radius = 0.15
        
        # 1. Create Hexagonal Grid
        hex_grid = VGroup()
        for q in range(-4, 5):
            for r in range(-4, 5):
                if abs(q) <= 4 and abs(r) <= 4 and abs(q + r) <= 4:
                    # Axial to pixel conversion
                    x = 0.4 * (3/2 * q)
                    y = 0.4 * (np.sqrt(3)/2 * q + np.sqrt(3) * r)
                    hex_grid.add(Circle(radius=circle_radius, color=WHITE, stroke_width=2).move_to([x, y, 0]))
        
        hex_grid.move_to(ORIGIN)

        # 2. Show Hex Board
        self.play(Create(hex_grid))
        self.wait(1)

        # 3. Simulate 3D Tilt in 2D
        # We scale the y-axis and rotate to simulate perspective
        tilted_hex_grid = hex_grid.copy().scale(0.8).rotate(15 * DEGREES).stretch(0.5, dim=1)
        self.play(ReplacementTransform(hex_grid, tilted_hex_grid))
        self.wait(0.5)

        # 4. Morph into a Square Grid (tilted)
        square_grid_base = VGroup(*[
            Square(side_length=0.3, stroke_width=1, color=GRAY)
            for _ in range(n * n)
        ]).arrange_in_grid(rows=n, cols=n, buff=0.05)
        
        # Apply the same "tilt" transformation to the square grid
        square_grid_base.rotate(15 * DEGREES).stretch(0.5, dim=1).move_to(ORIGIN)

        self.play(ReplacementTransform(tilted_hex_grid, square_grid_base))
        self.wait(1)

        # 5. Split into 3 Separate Floating Layers (using Y-offset to simulate depth)
        def create_layer(color, offset_vec):
            layer = VGroup(*[
                Square(side_length=0.3, fill_color=color, fill_opacity=0.3, stroke_width=1, stroke_color=color)
                for _ in range(n * n)
            ]).arrange_in_grid(rows=n, cols=n, buff=0.05)
            layer.rotate(15 * DEGREES).stretch(0.5, dim=1)
            layer.shift(offset_vec)
            return layer

        # Layers: Layer 1 (Top/Blue), Layer 2 (Mid/Green), Layer 3 (Bottom/Red)
        layer1 = create_layer(BLUE, UP * 1.5 + RIGHT * 0.5)
        layer2 = create_layer(GREEN, ORIGIN)
        layer3 = create_layer(RED, DOWN * 1.5 + LEFT * 0.5)

        # Animate explosion into layers
        self.play(
            ReplacementTransform(square_grid_base.copy(), layer2),
            ReplacementTransform(square_grid_base.copy(), layer1),
            ReplacementTransform(square_grid_base, layer3),
            run_time=2
        )
        self.wait(1)

        # 6. Highlight specific zones per "remarks"
        # Mark some 'Self' pieces in Layer 1
        for i in [12, 13, 21, 22]:
            layer1[i].set_fill(BLUE, opacity=0.9)
        # Mark 'Target' zone in Layer 2
        for i in [72, 73, 80, 81]:
            layer2[i].set_fill(GREEN, opacity=0.9)
        # Mark 'Opponent' pieces in Layer 3
        for i in [40, 41, 49, 50]:
            layer3[i].set_fill(RED, opacity=0.9)

        self.play(
            layer1.animate.set_stroke(opacity=1),
            layer2.animate.set_stroke(opacity=1),
            layer3.animate.set_stroke(opacity=1)
        )
        self.wait(1)

        # 7. Labels
        label_dims = MathTex("n \\times n \\times 3").scale(1.2).to_corner(UR)
        formula = MathTex("n = 4 \\times \\text{board radius} + 1").scale(0.8).next_to(label_dims, DOWN)
        
        goal_text = Text(
            "Hexagonal board represented as a multi-layered square grid", 
            font_size=24
        ).to_edge(DOWN)

        self.play(
            Write(label_dims),
            Write(formula),
            FadeIn(goal_text)
        )
        
        # 8. Final presentation shift
        all_layers = VGroup(layer1, layer2, layer3)
        self.play(all_layers.animate.scale(0.7).to_edge(LEFT))
        
        self.wait(3)