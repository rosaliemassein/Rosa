from manim import *
import numpy as np

class ConceptEncoding(Scene):
    def construct(self):
        # Configuration
        board_radius = 1
        n = 5
        cell_size = 0.5
        
        # 1. Create Hexagonal Grid
        hex_board = VGroup()
        for q in range(-2, 3):
            for r in range(-2, 3):
                # Standard axial coordinate constraint for a hexagonal board
                if abs(q) <= 2 and abs(r) <= 2 and abs(q + r) <= 2:
                    # Axial to Pixel coordinates
                    x = cell_size * (1.5 * q)
                    y = cell_size * (np.sqrt(3)/2 * q + np.sqrt(3) * r)
                    c = Circle(radius=0.18, color=WHITE, stroke_width=2)
                    c.move_to([x, y, 0])
                    hex_board.add(c)
        
        hex_board.move_to(ORIGIN)
        self.play(Create(hex_board))
        self.wait(1)

        # 2. Tilt into perspective and Prepare Grid Layers
        # We simulate 3D perspective by shearing and scaling in 2D
        perspective_shear = -0.4
        perspective_scale_y = 0.7
        
        layers = VGroup()
        colors = [BLUE, GREEN, RED]
        layer_labels_text = ["Self Pieces", "Target Zone", "Opponent Pieces"]
        
        for i in range(3):
            layer = VGroup()
            for r in range(n):
                for c in range(n):
                    sq = Square(side_length=cell_size, color=colors[i], stroke_width=1.5)
                    sq.set_fill(colors[i], opacity=0.15)
                    sq.move_to([c * cell_size, r * cell_size, 0])
                    layer.add(sq)
            layer.move_to(ORIGIN)
            layer.shear(perspective_shear, RIGHT)
            layer.scale(perspective_scale_y, UP)
            layers.add(layer)

        # Arrange layers vertically to simulate floating stacked layers
        layers.arrange(UP, buff=0.8)
        
        # Specific Highlights
        # Layer 1 (Self)
        for idx in [6, 7, 8]: layers[0][idx].set_fill(BLUE, opacity=0.8)
        # Layer 2 (Target)
        layers[1][12].set_fill(GREEN, opacity=0.8)
        # Layer 3 (Opponent)
        for idx in [16, 17, 18]: layers[2][idx].set_fill(RED, opacity=0.8)

        # 3. Animate Tilt and Morph
        self.play(
            hex_board.animate.shear(perspective_shear, RIGHT).scale(perspective_scale_y, UP),
            run_time=1.5
        )
        self.wait(0.5)

        # Morph board into the center square grid layer
        self.play(ReplacementTransform(hex_board, layers[1]))
        
        # Split into three layers
        self.play(
            FadeIn(layers[0], shift=UP * 0.5),
            FadeIn(layers[2], shift=DOWN * 0.5)
        )
        self.wait(1)

        # 4. Labels and Formula
        label_dim = MathTex(r"n \times n \times 3").scale(1.2).to_edge(UP, buff=0.5)
        formula = MathTex(r"n = 4 \times \text{board radius} + 1").scale(0.8).to_edge(DOWN, buff=0.5)
        
        self.play(Write(label_dim))
        self.play(Write(formula))
        
        # Add side labels for each layer
        for i in range(3):
            lbl = Text(layer_labels_text[i], font_size=20, color=colors[i])
            lbl.next_to(layers[i], RIGHT, buff=0.5)
            self.play(FadeIn(lbl), run_time=0.4)

        self.wait(3)