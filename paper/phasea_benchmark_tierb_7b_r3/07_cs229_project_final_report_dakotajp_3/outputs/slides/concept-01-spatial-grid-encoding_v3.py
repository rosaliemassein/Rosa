from manim import *
import numpy as np

class SpatialGridEncoding(Scene):
    def construct(self):
        # 1. Configuration: n = 4 * board_radius + 1
        board_radius = 2
        n = 4 * board_radius + 1  # n = 9
        
        # 2. Create Hexagonal Grid (Circles)
        hex_grid = VGroup()
        for r in range(-board_radius * 2, board_radius * 2 + 1):
            for q in range(-board_radius * 2, board_radius * 2 + 1):
                # Filter to create a hexagonal board shape
                if abs(r + q) <= board_radius * 2:
                    # Axial to 2D pixel coordinates
                    x = 0.4 * (1.5 * r)
                    y = 0.4 * (np.sqrt(3) / 2 * r + np.sqrt(3) * q)
                    dot = Circle(radius=0.15, color=WHITE, fill_opacity=0.2, stroke_width=2)
                    dot.move_to([x, y, 0])
                    hex_grid.add(dot)
        
        hex_grid.center()
        self.play(Create(hex_grid))
        self.wait(1)

        # 3. Tilt into "3D" perspective using 2D transforms (to avoid 3D constraints)
        # We simulate tilt by squashing vertically and shearing
        self.play(
            hex_grid.animate.apply_matrix([
                [1, 0.5, 0],
                [0, 0.5, 0],
                [0, 0, 1]
            ]).scale(0.8),
            run_time=2
        )
        self.wait(0.5)

        # 4. Morph into a Square Grid
        # Create a single n x n square grid
        square_grid = VGroup(*[
            Square(side_length=0.3, stroke_width=1, fill_opacity=0.1) 
            for _ in range(n * n)
        ]).arrange_in_grid(rows=n, cols=n, buff=0.05)
        
        # Apply the same "tilted" matrix to match the perspective
        square_grid.apply_matrix([
            [1, 0.5, 0],
            [0, 0.5, 0],
            [0, 0, 1]
        ]).center()

        self.play(ReplacementTransform(hex_grid, square_grid))
        self.wait(1)

        # 5. Split into 3 separate layers (Self, Target, Opponent)
        # Create colored copies
        layer_self = square_grid.copy().set_color(BLUE).shift(UP * 1.5 + RIGHT * 0.5)
        layer_target = square_grid.copy().set_color(GREEN).shift(ORIGIN)
        layer_opponent = square_grid.copy().set_color(RED).shift(DOWN * 1.5 + LEFT * 0.5)

        # Add some highlight "pieces" in each layer
        for layer, color, indices in zip(
            [layer_self, layer_target, layer_opponent],
            [BLUE, GREEN, RED],
            [[10, 11, 12], [40, 41], [70, 71, 72]] # arbitrary indices
        ):
            for idx in indices:
                layer[idx].set_fill(color, opacity=0.8)

        # Labels for layers
        label_self = Text("Self Layer", font_size=20, color=BLUE).next_to(layer_self, LEFT, buff=0.5)
        label_target = Text("Target Layer", font_size=20, color=GREEN).next_to(layer_target, LEFT, buff=0.5)
        label_opponent = Text("Opponent Layer", font_size=20, color=RED).next_to(layer_opponent, LEFT, buff=0.5)

        self.play(
            ReplacementTransform(square_grid.copy(), layer_self),
            ReplacementTransform(square_grid.copy(), layer_target),
            ReplacementTransform(square_grid, layer_opponent),
            FadeIn(label_self), FadeIn(label_target), FadeIn(label_opponent),
            run_time=2
        )

        # 6. Add Formulas and Dimensional Labels
        formula = MathTex(r"n = 4 \times \text{board radius} + 1", font_size=32).to_edge(UL)
        dimensions = MathTex(r"n \times n \times 3", font_size=40).to_edge(UR)
        
        self.play(Write(formula))
        self.play(FadeIn(dimensions, shift=DOWN))
        
        self.wait(3)