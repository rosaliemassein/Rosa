from manim import *

class SpatialGridEncoding(Scene):
    def construct(self):
        # 1. Define Formula and Initial Board Data
        board_radius = 2
        n_val = 4 * board_radius + 1
        formula = MathTex(r"n = 4 \times \text{board radius} + 1").to_edge(UP)
        self.play(Write(formula))
        
        # Create hexagonal grid of circles to represent the board
        hex_grid = VGroup()
        for r in range(-board_radius, board_radius + 1):
            for q in range(-board_radius, board_radius + 1):
                if abs(r + q) <= board_radius:
                    # Axial to 2D Cartesian conversion
                    x_pos = 0.5 * (3**0.5 * q + (3**0.5 / 2) * r)
                    y_pos = 0.5 * (1.5 * r)
                    hex_grid.add(Circle(radius=0.18, color=WHITE, fill_opacity=0.3).move_to([x_pos, y_pos, 0]))
        
        hex_grid.center()
        self.play(Create(hex_grid))
        self.wait(1)

        # 2. Simulate 3D tilt (Using 2D stretch and rotation)
        self.play(
            hex_grid.animate.stretch(0.5, dim=1).rotate(-15 * DEGREES),
            formula.animate.scale(0.7).to_corner(UL)
        )
        self.wait(0.5)

        # 3. Morph into a square grid (n x n)
        # Based on formula: n = 4*2 + 1 = 9
        n = 9
        square_grid = VGroup()
        cell_size = 0.35
        for i in range(n):
            for j in range(n):
                square_grid.add(
                    Square(side_length=cell_size, stroke_width=1)
                    .move_to([(i - (n-1)/2) * cell_size, (j - (n-1)/2) * cell_size, 0])
                )
        square_grid.center()
        
        # Morph the board into the grid
        self.play(ReplacementTransform(hex_grid, square_grid))
        self.wait(1)

        # 4. Separate into three semi-transparent floating layers
        # Layer 1: Self (Blue)
        layer1 = square_grid.copy().set_color(BLUE).set_stroke(BLUE, 1).set_fill(BLUE, opacity=0.15)
        # Layer 2: Target (Green)
        layer2 = square_grid.copy().set_color(GREEN).set_stroke(GREEN, 1).set_fill(GREEN, opacity=0.15)
        # Layer 3: Opponent (Red)
        layer3 = square_grid.copy().set_color(RED).set_stroke(RED, 1).set_fill(RED, opacity=0.15)

        # Position them to look like a vertical stack in 2D perspective
        self.play(
            layer1.animate.shift(UP * 2.2 + RIGHT * 0.4),
            layer2.animate.shift(ORIGIN),
            layer3.animate.shift(DOWN * 2.2 + LEFT * 0.4),
            FadeOut(square_grid),
            run_time=2
        )

        # Highlight pieces on each layer to show encoding
        l1_highlights = [20, 21, 22]
        l2_highlights = [40, 41, 42]
        l3_highlights = [60, 61, 62]

        self.play(
            *[layer1[idx].animate.set_fill(BLUE, opacity=0.8) for idx in l1_highlights],
            *[layer2[idx].animate.set_fill(GREEN, opacity=0.8) for idx in l2_highlights],
            *[layer3[idx].animate.set_fill(RED, opacity=0.8) for idx in l3_highlights],
        )

        # 5. Label dimensions and semantic layers
        dim_label = MathTex(r"n \times n \times 3", color=YELLOW).to_edge(RIGHT, buff=1.2)
        
        l1_tag = Text("Current Player", color=BLUE, font_size=20).next_to(layer1, LEFT, buff=0.5)
        l2_tag = Text("Target Zone", color=GREEN, font_size=20).next_to(layer2, LEFT, buff=0.5)
        l3_tag = Text("Opponent Pieces", color=RED, font_size=20).next_to(layer3, LEFT, buff=0.5)

        self.play(
            Write(dim_label),
            Write(l1_tag),
            Write(l2_tag),
            Write(l3_tag)
        )

        self.wait(3)