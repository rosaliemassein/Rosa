from manim import *
import numpy as np

class SpatialGridEncoding(Scene):
    def construct(self):
        # Define the board radius and calculate n
        board_radius = 1
        n = 4 * board_radius + 1 # n = 5
        
        # 1. Create the hexagonal grid of circles
        # Representing a simplified hex board
        hex_grid = VGroup()
        for r in range(-2, 3):
            cols = 5 - abs(r)
            for c in range(cols):
                circle = Circle(radius=0.2, stroke_width=2).set_color(WHITE)
                # Hexagonal coordinate mapping
                x = (c - cols / 2 + 0.5) * 0.5
                y = r * 0.45
                circle.move_to([x, y, 0])
                hex_grid.add(circle)
        
        self.play(Create(hex_grid))
        self.wait(1)

        # 2. Transform the hexagonal grid into a square grid of cells
        # We'll create an n x n grid
        square_grid = VGroup()
        for r in range(n):
            for c in range(n):
                sq = Square(side_length=0.4, stroke_width=2).set_color(WHITE)
                sq.move_to([(c - n/2 + 0.5) * 0.45, (r - n/2 + 0.5) * 0.45, 0])
                square_grid.add(sq)
        
        self.play(ReplacementTransform(hex_grid, square_grid))
        self.wait(1)

        # 3. Morph to a "3D" perspective using 2D transformations (Shear and Scale)
        # This avoids disallowed 3D features
        target_perspective = square_grid.copy()
        target_perspective.apply_matrix([[1, 0.5, 0], [0, 0.5, 0], [0, 0, 1]])
        
        self.play(square_grid.animate.become(target_perspective).scale(0.8).shift(DOWN * 1))
        self.wait(1)

        # 4. Split into three separate layers floating vertically
        # Layer 1: Self (Blue), Layer 2: Target (Green), Layer 3: Opponent (Red)
        
        layer_1 = square_grid.copy().set_color(BLUE).set_stroke(opacity=0.6)
        layer_2 = square_grid.copy().set_color(GREEN).set_stroke(opacity=0.6)
        layer_3 = square_grid.copy().set_color(RED).set_stroke(opacity=0.6)
        
        # Highlight some "pieces" in each layer
        # Random indices for visual representation
        for i in [2, 7, 8, 12]: layer_1[i].set_fill(BLUE, opacity=0.8)
        for i in [20, 21, 22]: layer_2[i].set_fill(GREEN, opacity=0.8)
        for i in [4, 9, 15, 18]: layer_3[i].set_fill(RED, opacity=0.8)

        layers = VGroup(layer_1, layer_2, layer_3)
        
        # Animate the layers splitting vertically
        self.play(
            layer_1.animate.shift(UP * 0.0),
            layer_2.animate.shift(UP * 1.5),
            layer_3.animate.shift(UP * 3.0),
            FadeOut(square_grid),
            run_time=2
        )

        # 5. Labels and MathTex
        label_n = MathTex("n \\times n \\times 3").to_edge(LEFT, buff=1).shift(UP * 1)
        formula = MathTex("n = 4 \\times \\text{board radius} + 1").scale(0.7).next_to(label_n, DOWN)
        
        l1_text = Text("Layer 1: Self", font_size=20, color=BLUE).next_to(layer_1, RIGHT, buff=0.5)
        l2_text = Text("Layer 2: Target", font_size=20, color=GREEN).next_to(layer_2, RIGHT, buff=0.5)
        l3_text = Text("Layer 3: Opponent", font_size=20, color=RED).next_to(layer_3, RIGHT, buff=0.5)

        self.play(
            Write(label_n),
            Write(formula),
            FadeIn(l1_text),
            FadeIn(l2_text),
            FadeIn(l3_text)
        )
        
        self.wait(3)