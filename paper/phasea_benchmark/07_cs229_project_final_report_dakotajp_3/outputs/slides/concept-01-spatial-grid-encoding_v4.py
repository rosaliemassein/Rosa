from manim import *
import numpy as np

class ConceptGridEncoding(Scene):
    def construct(self):
        # 1. Setup Parameters
        board_radius = 2
        n = 4 * board_radius + 1  # n = 9
        
        # 2. Create Hexagonal Grid
        hex_grid = VGroup()
        for r in range(-board_radius * 2, board_radius * 2 + 1):
            for q in range(-board_radius * 2, board_radius * 2 + 1):
                if abs(r + q) <= board_radius * 2:
                    # Axial to Pixel conversion
                    x = 0.4 * (1.5 * q)
                    y = 0.4 * (np.sqrt(3)/2 * q + np.sqrt(3) * r)
                    hex_grid.add(Circle(radius=0.1, color=WHITE, fill_opacity=0.2, fill_color=WHITE).move_to([x, y, 0]))
        
        hex_grid.move_to(ORIGIN)

        # Narration 1
        intro_text = Text(
            "Transforming the hexagonal board into grids.",
            font_size=24
        ).to_edge(UP)
        
        self.play(Create(hex_grid), Write(intro_text))
        self.wait(1)

        # 3. Simulate 3D Tilt (Pseudo-3D using 2D transforms)
        # We squash vertically and shear to give a perspective feel
        tilt_group = VGroup(hex_grid)
        self.play(
            tilt_group.animate.apply_matrix([[1, 0.5, 0], [0, 0.5, 0], [0, 0, 1]]),
            intro_text.animate.to_corner(UL).scale(0.7),
            run_time=1.5
        )
        self.wait(0.5)

        # 4. Morph into a Square Grid
        # Create a grid of squares (n x n)
        side = 0.3
        square_grid = VGroup(*[
            Square(side_length=side).move_to([i * (side + 0.05) - (n * side)/2, j * (side + 0.05) - (n * side)/2, 0])
            for i in range(n)
            for j in range(n)
        ]).set_stroke(WHITE, 1)
        
        # Apply the same "tilt" to the square grid so the transition is seamless
        square_grid.apply_matrix([[1, 0.5, 0], [0, 0.5, 0], [0, 0, 1]])

        self.play(ReplacementTransform(hex_grid, square_grid), run_time=1.5)
        self.wait(0.5)

        # 5. Split into Three Layers
        # We'll create 3 colored copies and offset them vertically in the 2D plane
        # to look like a stack.
        layer_spacing = 1.2
        
        layer_self = square_grid.copy().set_color(BLUE).set_stroke(BLUE, 1)
        layer_target = square_grid.copy().set_color(GREEN).set_stroke(GREEN, 1)
        layer_opponent = square_grid.copy().set_color(RED).set_stroke(RED, 1)
        
        # Add semi-transparency and some "occupied" cells
        layers = [layer_self, layer_target, layer_opponent]
        colors = [BLUE, GREEN, RED]
        
        for layer, color in zip(layers, colors):
            layer.set_fill(color, opacity=0.3)
            # Highlight some cells to represent pieces
            for k in range(0, len(layer), 10):
                layer[k].set_fill(color, opacity=0.9)

        # Position them in a vertical stack
        stack = VGroup(
            layer_self.shift(UP * layer_spacing),
            layer_target,
            layer_opponent.shift(DOWN * layer_spacing)
        ).move_to(LEFT * 2)

        self.play(
            ReplacementTransform(VGroup(square_grid), stack),
            run_time=2
        )

        # 6. Labels and Formula
        label_dim = MathTex("n \\times n \\times 3").scale(1.2).next_to(stack, RIGHT, buff=1)
        label_formula = MathTex("n = 4 \\times \\text{board radius} + 1").scale(0.7).to_corner(DL)
        
        layer_labels = VGroup(
            Text("Layer 1: Self", font_size=18, color=BLUE).next_to(layer_self, RIGHT),
            Text("Layer 2: Target", font_size=18, color=GREEN).next_to(layer_target, RIGHT),
            Text("Layer 3: Opponent", font_size=18, color=RED).next_to(layer_opponent, RIGHT)
        )

        voiceover_text2 = Text(
            "The CNN 'sees' spatial relationships between pegs and goals.",
            font_size=20
        ).to_edge(DOWN)

        self.play(
            Write(label_dim),
            Write(label_formula),
            Write(layer_labels),
            FadeIn(voiceover_text2)
        )
        
        self.wait(3)