from manim import *
import numpy as np

class SpatialGridEncoding(Scene):
    def construct(self):
        # Configuration
        n = 5  # Representing n = 4 * radius + 1 (for radius=1)
        colors = [BLUE, GREEN, RED]
        
        # 1. Create hexagonal grid of circles
        hex_grid = VGroup()
        for r in range(n):
            for c in range(n):
                # Calculate hexagonal positions in 2D
                x = (c - n/2) * 0.7
                y = (r - n/2) * 0.6
                if r % 2 == 1:
                    x += 0.35
                circle = Circle(radius=0.2, color=WHITE, stroke_width=2)
                circle.move_to([x, y, 0])
                hex_grid.add(circle)
        
        hex_grid.center()
        
        # Display the board
        self.play(Create(hex_grid), run_time=2)
        self.wait(1)

        # 2. Animate tilting into a perspective view (simulated in 2D)
        # We use stretch and shear to create the illusion of a 3D tilt
        tilt_factor = 0.5
        shear_factor = -0.3
        
        self.play(
            hex_grid.animate.stretch(tilt_factor, dim=1).shear(shear_factor, LEFT),
            run_time=2
        )
        self.wait(1)

        # 3. Transform into square grid layers
        # Create 3 distinct layers
        layer_self = VGroup()
        layer_target = VGroup()
        layer_opponent = VGroup()
        
        for layer, color in zip([layer_self, layer_target, layer_opponent], colors):
            for r in range(n):
                for c in range(n):
                    sq = Square(side_length=0.45, stroke_width=1.5)
                    sq.set_stroke(color=color)
                    sq.set_fill(color=color, opacity=0.3)
                    # Position squares in a grid
                    sq.move_to([(c - n/2) * 0.5, (r - n/2) * 0.5, 0])
                    layer.add(sq)
            # Apply same tilt transformation to layers
            layer.stretch(tilt_factor, dim=1).shear(shear_factor, LEFT)

        # Positioning layers vertically on the screen to simulate a 3D stack
        layer_target.shift(UP * 2)
        layer_self.shift(ORIGIN)
        layer_opponent.shift(DOWN * 2)

        # Morph the board into the three layers
        self.play(
            ReplacementTransform(hex_grid.copy(), layer_self),
            ReplacementTransform(hex_grid.copy(), layer_target),
            ReplacementTransform(hex_grid, layer_opponent),
            run_time=2
        )
        self.wait(1)

        # 4. Labels and Formulas
        # Formula: n = 4 * board radius + 1
        formula = MathTex("n = 4 \\times \\text{board radius} + 1").to_edge(DOWN, buff=0.5)
        # Dimensions: n x n x 3
        dim_label = MathTex("n \\times n \\times 3").to_corner(UR, buff=1)
        
        # Layer labels
        label_target = Text("Target Zone (Layer 2)", color=GREEN).scale(0.4).next_to(layer_target, LEFT, buff=0.5)
        label_self = Text("Self Pieces (Layer 1)", color=BLUE).scale(0.4).next_to(layer_self, LEFT, buff=0.5)
        label_opponent = Text("Opponent Pieces (Layer 3)", color=RED).scale(0.4).next_to(layer_opponent, LEFT, buff=0.5)

        self.play(
            Write(formula),
            Write(dim_label),
            FadeIn(label_target),
            FadeIn(label_self),
            FadeIn(label_opponent)
        )
        self.wait(1)

        # 5. Highlight pieces as per the voiceover
        self.play(Indicate(layer_self, color=BLUE))
        self.play(Indicate(layer_target, color=GREEN))
        self.play(Indicate(layer_opponent, color=RED))

        self.wait(2)