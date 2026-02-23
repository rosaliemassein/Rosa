from manim import *
import numpy as np

class SpatialGridEncoding(Scene):
    def construct(self):
        # 1. Configuration
        board_radius = 2
        n = 4 * board_radius + 1  # n = 9
        hex_spacing = 0.4
        
        # 2. Create Hexagonal Grid (Circles)
        # Using a simple hex layout for a Chinese Checkers representation
        hex_grid = VGroup()
        for i in range(-4, 5):
            for j in range(-4, 5):
                # Filter to form a hexagonal shape
                if abs(i + j) <= 4:
                    x = (i + j * 0.5) * hex_spacing
                    y = j * (np.sqrt(3) / 2) * hex_spacing
                    dot = Circle(radius=0.12, color=WHITE, stroke_width=2)
                    dot.move_to([x, y, 0])
                    hex_grid.add(dot)
        
        hex_grid.move_to(ORIGIN)

        # 3. Create Square Grid
        square_grid = VGroup()
        grid_size = n * 0.35
        cell_size = grid_size / n
        for i in range(n):
            for j in range(n):
                sq = Square(side_length=cell_size, stroke_width=1, color=WHITE)
                sq.move_to([
                    (j - n/2) * cell_size + cell_size/2,
                    (i - n/2) * cell_size + cell_size/2,
                    0
                ])
                square_grid.add(sq)
        
        square_grid.move_to(ORIGIN)

        # 4. Animation Step 1: Hex Board
        self.play(Create(hex_grid), run_time=1.5)
        self.wait(1)

        # 5. Animation Step 2: Morph to Square Grid and simulate "tilt"
        # We simulate the tilt by scaling and shearing in 2D
        tilted_square_grid = square_grid.copy().apply_matrix([
            [1, 0.5, 0],
            [0, 0.5, 0],
            [0, 0, 1]
        ]).scale(0.8)

        self.play(
            Transform(hex_grid, tilted_square_grid),
            run_time=2
        )
        self.wait(1)

        # 6. Create Three Layers
        # Layer 1: Blue (Self), Layer 2: Green (Target), Layer 3: Red (Opponent)
        # We'll use the tilted grid shape for all
        layer_base = tilted_square_grid.copy()
        
        l_self = layer_base.copy().set_color(BLUE).set_stroke(BLUE, opacity=0.8).set_fill(BLUE, opacity=0.2)
        l_target = layer_base.copy().set_color(GREEN).set_stroke(GREEN, opacity=0.8).set_fill(GREEN, opacity=0.2)
        l_opponent = layer_base.copy().set_color(RED).set_stroke(RED, opacity=0.8).set_fill(RED, opacity=0.2)

        # Labels for layers
        label_self = Text("Self Layer", color=BLUE).scale(0.4)
        label_target = Text("Target Zone", color=GREEN).scale(0.4)
        label_opponent = Text("Opponent Pieces", color=RED).scale(0.4)

        # Grouping and initial stack (collapsed)
        layers = VGroup(l_opponent, l_target, l_self) # Bottom to Top order
        
        # 7. Animation Step 3: Vertical Splitting
        # To show "floating vertically" in 2D, we shift them upwards with offsets
        self.remove(hex_grid)
        self.add(l_opponent, l_target, l_self)
        
        self.play(
            l_self.animate.shift(UP * 2.2 + RIGHT * 0.2),
            l_target.animate.shift(UP * 1.1 + RIGHT * 0.1),
            # l_opponent stays mostly at bottom
            run_time=2
        )

        # Position labels next to layers
        label_self.next_to(l_self, LEFT, buff=0.2)
        label_target.next_to(l_target, LEFT, buff=0.2)
        label_opponent.next_to(l_opponent, LEFT, buff=0.2)

        self.play(FadeIn(label_self), FadeIn(label_target), FadeIn(label_opponent))
        self.wait(1)

        # 8. Dimensions Label
        formula = MathTex(r"n \times n \times 3").to_edge(UR, buff=1)
        formula_val = MathTex(r"n = 4 \times \text{radius} + 1").scale(0.7).next_to(formula, DOWN)
        
        background_rect = SurroundingRectangle(VGroup(formula, formula_val), color=WHITE, fill_opacity=0.1)
        
        self.play(
            Write(formula),
            FadeIn(formula_val),
            Create(background_rect)
        )
        
        # Highlight some "pieces" to show encoding
        # Randomly color some cells in the layers to simulate game state
        for i in [12, 25, 40]:
            l_self[i].set_fill(BLUE, opacity=0.8)
        for i in [60, 61, 62]:
            l_target[i].set_fill(GREEN, opacity=0.8)
        for i in [5, 18, 30]:
            l_opponent[i].set_fill(RED, opacity=0.8)
            
        self.play(Flash(l_self[25]), Flash(l_opponent[18]))
        self.wait(2)