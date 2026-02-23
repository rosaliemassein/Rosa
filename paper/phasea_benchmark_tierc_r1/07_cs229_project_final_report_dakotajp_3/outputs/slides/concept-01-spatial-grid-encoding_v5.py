from manim import *

class ConceptGridEncoding(Scene):
    def construct(self):
        # 1. Setup Parameters
        board_radius = 2
        n = 4 * board_radius + 1  # n = 9
        
        # 2. Create Hexagonal Grid
        # Using a simplified hexagonal representation with circles
        hex_grid = VGroup()
        for r in range(-board_radius, board_radius + 1):
            for q in range(-board_radius, board_radius + 1):
                if abs(r + q) <= board_radius:
                    # Hex-to-Cartesian conversion for 2D positioning
                    x = (q + r * 0.5) * 0.6
                    y = (r * 0.866) * 0.6
                    dot = Circle(radius=0.2, color=WHITE, stroke_width=2, fill_opacity=0.3)
                    dot.move_to([x, y, 0])
                    hex_grid.add(dot)
        hex_grid.center()
        
        self.play(Create(hex_grid))
        self.wait(1)

        # 3. Tilt into Perspective (2D Perspective Simulation)
        # We rotate and then scale vertically to simulate a "tilted" 3D look in 2D
        tilted_view = hex_grid.copy()
        tilted_view.rotate(45 * DEGREES)
        tilted_view.stretch(0.5, dim=1) # Squash on Y axis to simulate perspective
        
        self.play(Transform(hex_grid, tilted_view))
        self.wait(1)

        # 4. Create Square Grid Layers (n x n x 3)
        # We'll create three layers: Red (Bottom), Green (Middle), Blue (Top)
        layers = VGroup()
        layer_colors = [RED, GREEN, BLUE]
        
        for i, color in enumerate(layer_colors):
            # Create the n x n grid of squares
            layer = VGroup(*[
                Square(side_length=0.3, stroke_width=1, color=color, fill_opacity=0.15)
                for _ in range(n * n)
            ])
            layer.arrange_in_grid(rows=n, cols=n, buff=0.02)
            
            # Apply the same "tilted" transformation to each square layer
            layer.rotate(45 * DEGREES)
            layer.stretch(0.5, dim=1)
            
            # Stack them vertically in the 2D plane (Layer 0 at bottom, Layer 2 at top)
            layer.shift(UP * (i - 1) * 1.6)
            layers.add(layer)

        # 5. Morph Board into Layers
        # Using ReplacementTransform to transition from the hex board to the multi-layered stack
        self.play(ReplacementTransform(hex_grid, layers))
        self.wait(1)

        # 6. Highlight pieces based on the concept
        # Blue Layer (Self - Top)
        self_indices = [40, 41, 49, 50, 31, 32]
        # Green Layer (Target - Middle)
        target_indices = [0, 1, 2, 9, 10, 18]
        # Red Layer (Opponent - Bottom)
        opp_indices = [75, 76, 77, 80, 68, 69]

        self.play(
            *[layers[2][idx].animate.set_fill(BLUE, opacity=0.8) for idx in self_indices],
            *[layers[1][idx].animate.set_fill(GREEN, opacity=0.8) for idx in target_indices],
            *[layers[0][idx].animate.set_fill(RED, opacity=0.8) for idx in opp_indices],
            run_time=2
        )

        # 7. Add Dimension Labels and Formula
        dim_label = MathTex(r"n \times n \times 3").scale(1.2).to_edge(RIGHT).shift(UP * 2)
        formula_label = MathTex(r"n = 4 \times \text{board radius} + 1").scale(0.8).to_corner(DL)
        
        # Legend labels to identify layers
        l1 = Text("Layer 1: Self (Blue)", color=BLUE, font_size=20).next_to(dim_label, DOWN, aligned_edge=LEFT)
        l2 = Text("Layer 2: Target (Green)", color=GREEN, font_size=20).next_to(l1, DOWN, aligned_edge=LEFT)
        l3 = Text("Layer 3: Opponent (Red)", color=RED, font_size=20).next_to(l2, DOWN, aligned_edge=LEFT)
        
        self.play(
            Write(dim_label),
            Write(formula_label),
            Write(l1),
            Write(l2),
            Write(l3)
        )
        
        self.wait(2)

        # Final emphasis on the square grid architecture
        self.play(
            layers.animate.scale(1.1).shift(LEFT * 1.5),
            VGroup(dim_label, l1, l2, l3).animate.shift(LEFT * 0.5),
            run_time=1.5
        )
        self.wait(3)