from manim import *

class Concept01SpatialGridEncoding(Scene):
    def construct(self):
        # 1. Setup Board dimensions
        # n = 4 * board_radius + 1. If radius is 2, n=9. 
        # For visual clarity in a 2D scene, we use n=7.
        n = 7
        
        # Narration text
        voice_text = Text(
            "To teach a neural network Chinese Checkers, we transform\nthe hexagonal board into a language it understands: grids.", 
            font_size=24, 
            color=YELLOW
        ).to_edge(UP)
        self.play(Write(voice_text))
        self.wait(1)

        # 2. Hexagonal grid of circles (2D representation)
        hex_circles = VGroup()
        for i in range(n):
            for j in range(n):
                # Offset every other row to simulate hexagonal layout
                x_offset = 0.2 if i % 2 == 1 else 0
                circle = Circle(radius=0.15, stroke_width=2, color=GRAY)
                circle.move_to([j * 0.5 + x_offset - (n*0.5)/2, i * 0.4 - (n*0.4)/2, 0])
                hex_circles.add(circle)
        
        hex_circles.center().shift(DOWN * 0.5)
        self.play(LaggedStart(*[Create(c) for c in hex_circles], lag_ratio=0.02))
        self.wait(1)

        # 3. Tilt into perspective using a 2D matrix transformation (Shear + Scale)
        # This simulates a 3D look without using ThreeDScene features
        perspective_matrix = [[1, 0.5, 0], [0, 0.5, 0], [0, 0, 1]]
        
        self.play(
            hex_circles.animate.apply_matrix(perspective_matrix).scale(0.8).shift(DOWN * 1),
            run_time=2
        )
        self.wait(0.5)

        # 4. Morph into square grid
        square_grid = VGroup()
        for i in range(n):
            for j in range(n):
                sq = Square(side_length=0.35, stroke_width=1, color=WHITE)
                sq.move_to([j * 0.4, i * 0.4, 0])
                square_grid.add(sq)
        
        square_grid.apply_matrix(perspective_matrix).scale(0.8).move_to(hex_circles.get_center())
        
        self.play(ReplacementTransform(hex_circles, square_grid))
        self.wait(1)

        # 5. Split into three layers (Self, Target, Opponent)
        # Stack them vertically in 2D using a shift
        layer_offset = UP * 1.5 + RIGHT * 0.5
        
        l_self = square_grid.copy().set_color(BLUE).set_stroke(BLUE, opacity=1)
        l_target = square_grid.copy().set_color(GREEN).set_stroke(GREEN, opacity=1)
        l_opponent = square_grid.copy().set_color(RED).set_stroke(RED, opacity=1)

        # Highlight specific "encoded" cells in each layer
        l_self[10].set_fill(BLUE, opacity=0.7)
        l_self[12].set_fill(BLUE, opacity=0.7)
        l_target[24].set_fill(GREEN, opacity=0.7)
        l_opponent[30].set_fill(RED, opacity=0.7)
        l_opponent[32].set_fill(RED, opacity=0.7)

        self.play(
            l_self.animate.shift(layer_offset * 2),
            l_target.animate.shift(layer_offset * 1),
            l_opponent.animate.shift(layer_offset * 0),
            square_grid.animate.set_stroke(opacity=0.1),
            run_time=2
        )

        # Labels for layers
        label_self = Text("Layer 1: Self", font_size=20, color=BLUE).next_to(l_self, RIGHT, buff=0.5)
        label_target = Text("Layer 2: Target", font_size=20, color=GREEN).next_to(l_target, RIGHT, buff=0.5)
        label_opponent = Text("Layer 3: Opponent", font_size=20, color=RED).next_to(l_opponent, RIGHT, buff=0.5)

        self.play(Write(label_self), Write(label_target), Write(label_opponent))

        # 6. Final dimensions and Formula
        formula = MathTex(r"n = 4 \times \text{board radius} + 1", font_size=30).to_corner(DL, buff=1)
        dims = MathTex(r"n \times n \times 3", font_size=42, color=YELLOW).to_corner(DR, buff=1)
        
        self.play(Write(formula), Write(dims))
        self.wait(3)