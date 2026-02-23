from manim import *

class Concept01SpatialGridEncoding(Scene):
    def construct(self):
        # 1. Voice Narration / Objective
        intro_text = Text("Hexagonal Board to Square Grid Encoding", font_size=32).to_edge(UP)
        self.play(Write(intro_text))
        
        # 2. Create Hexagonal Grid
        hex_grid = VGroup()
        # Radius 2 board (total 5 rows)
        rows_counts = [3, 4, 5, 4, 3]
        for r, count in enumerate(rows_counts):
            for c in range(count):
                dot = Circle(radius=0.15, color=WHITE, stroke_width=2)
                # Offset calculation for hex grid centering
                x = (c - (count - 1) / 2) * 0.4
                y = (r - 2) * 0.35
                dot.move_to([x, y, 0])
                hex_grid.add(dot)
        
        self.play(Create(hex_grid))
        self.wait(1)

        # 3. Morph Hex Grid into Square Grid
        # Create a 5x5 square grid
        n = 5
        square_grid = VGroup()
        for i in range(n):
            for j in range(n):
                sq = Square(side_length=0.5, stroke_width=2).move_to([
                    (j - (n - 1) / 2) * 0.55,
                    (i - (n - 1) / 2) * 0.55,
                    0
                ])
                square_grid.add(sq)
        
        self.play(
            ReplacementTransform(hex_grid, square_grid),
            intro_text.animate.set_opacity(0.5)
        )
        self.wait(1)

        # 4. Simulate the 3D perspective tilt and split into 3 layers
        # To avoid 3D Scene restrictions, we use 2D offsets to simulate a stack.
        
        layer_spacing = 1.2
        
        # Layer 1: Self pieces (Blue) - Top Layer
        layer_1 = square_grid.copy().set_color(BLUE).set_stroke(opacity=0.6)
        # Highlight some 'Self' pieces
        for idx in [6, 7, 11, 12]:
            layer_1[idx].set_fill(BLUE, opacity=0.8)
            
        # Layer 2: Target zone (Green) - Middle Layer
        layer_2 = square_grid.copy().set_color(GREEN).set_stroke(opacity=0.6)
        # Highlight 'Target' zone
        for idx in [21, 22, 23]:
            layer_2[idx].set_fill(GREEN, opacity=0.8)
            
        # Layer 3: Opponent pieces (Red) - Bottom Layer
        layer_3 = square_grid.copy().set_color(RED).set_stroke(opacity=0.6)
        # Highlight 'Opponent' pieces
        for idx in [2, 3, 8]:
            layer_3[idx].set_fill(RED, opacity=0.8)

        # Group layers for simulated tilt
        layers = VGroup(layer_3, layer_2, layer_1) # Bottom to Top order
        
        # Position them with a vertical offset to look like a floating stack
        self.play(
            FadeOut(square_grid),
            layer_1.animate.shift(UP * layer_spacing + RIGHT * 0.5),
            layer_2.animate.shift(RIGHT * 0.5),
            layer_3.animate.shift(DOWN * layer_spacing + RIGHT * 0.5),
            run_time=2
        )

        # 5. Labeling
        label_style = {"font_size": 24}
        label_1 = Text("Layer 1: Current Player (Blue)", color=BLUE, **label_style).next_to(layer_1, LEFT, buff=0.5)
        label_2 = Text("Layer 2: Target Zone (Green)", color=GREEN, **label_style).next_to(layer_2, LEFT, buff=0.5)
        label_3 = Text("Layer 3: Opponents (Red)", color=RED, **label_style).next_to(layer_3, LEFT, buff=0.5)

        self.play(
            Write(label_1),
            Write(label_2),
            Write(label_3)
        )
        self.wait(1)

        # 6. Final Formula and Dimensions
        formula = MathTex(r"n = 4 \times \text{board radius} + 1", font_size=32).to_corner(UL)
        dims = MathTex(r"n \times n \times 3", font_size=42, color=YELLOW).to_edge(DOWN, buff=0.5)
        
        self.play(
            FadeIn(formula),
            Write(dims)
        )
        
        # Final visual emphasis
        self.play(dims.animate.scale(1.2).set_color(ORANGE), run_time=0.5)
        self.play(dims.animate.scale(1/1.2).set_color(YELLOW), run_time=0.5)
        
        self.wait(2)