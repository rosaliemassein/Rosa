from manim import *
import numpy as np

class Concept05DQNApproximation(Scene):
    def construct(self):
        # 1. Formula and Title
        formula = MathTex(r"Q(s, a; \theta) \approx Q^*(s, a)").to_edge(UP, buff=0.5)
        self.add(formula)

        # 2. 5x5 Pixel Grid
        # Create a grid of squares to represent pixels
        grid = VGroup(*[
            Square(side_length=0.4, fill_opacity=0.1, stroke_width=2, color=WHITE)
            for _ in range(25)
        ]).arrange_in_grid(5, 5, buff=0.1).shift(UP * 0.5)
        
        # Set some initial "pixel" values (simulating a simple shape)
        active_indices = [6, 7, 8, 11, 13, 16, 17, 18]
        for idx in active_indices:
            grid[idx].set_fill(WHITE, opacity=0.8)

        self.play(Create(grid))
        self.wait(1)

        # 3. Flattening Animation
        # Create a 1D vector representation (25 small squares in a row)
        vector = VGroup(*[
            Square(side_length=0.2, fill_opacity=0.1, stroke_width=1, color=WHITE)
            for _ in range(25)
        ]).arrange(RIGHT, buff=0.05).next_to(grid, DOWN, buff=1)

        # Ensure vector looks like the flattened grid
        for i in range(25):
            vector[i].set_fill(grid[i].get_fill_color(), opacity=grid[i].get_fill_opacity())

        flatten_text = Text("Flattening Grid to 1D Vector", font_size=20).next_to(vector, DOWN, buff=0.3)

        self.play(
            ReplacementTransform(grid.copy(), vector),
            Write(flatten_text),
            run_time=2
        )
        self.wait(1)

        # 4. Neural Network Construction
        # Move objects up to make room for NN
        all_top = VGroup(grid, vector, flatten_text, formula)
        self.play(all_top.animate.shift(UP * 1.5).scale(0.8))

        # NN Layers (Simplified for visualization)
        input_layer = VGroup(*[Circle(radius=0.08, color=BLUE) for _ in range(10)]).arrange(DOWN, buff=0.1)
        hidden_layer = VGroup(*[Circle(radius=0.08, color=BLUE) for _ in range(7)]).arrange(DOWN, buff=0.15)
        output_layer = VGroup(*[Circle(radius=0.08, color=RED) for _ in range(10)]).arrange(DOWN, buff=0.1)
        
        nn = VGroup(input_layer, hidden_layer, output_layer).arrange(RIGHT, buff=1.2).shift(DOWN * 2)
        
        # Connections
        connections = VGroup()
        # Connect input to hidden
        for i in range(len(input_layer)):
            for j in range(len(hidden_layer)):
                connections.add(Line(input_layer[i].get_right(), hidden_layer[j].get_left(), stroke_width=0.5, stroke_opacity=0.2))
        # Connect hidden to output
        for i in range(len(hidden_layer)):
            for j in range(len(output_layer)):
                connections.add(Line(hidden_layer[i].get_right(), output_layer[j].get_left(), stroke_width=0.5, stroke_opacity=0.2))

        self.play(
            Create(input_layer),
            Create(hidden_layer),
            Create(output_layer),
            Create(connections),
            FadeOut(flatten_text),
            run_time=2
        )

        # 5. Flowing Values
        # Lines from vector to input layer
        flow_lines = VGroup(*[
            Line(vector[int(i*2.5)].get_bottom(), input_layer[i].get_top(), stroke_width=1, color=YELLOW, stroke_opacity=0.3)
            for i in range(len(input_layer))
        ])
        
        self.play(Create(flow_lines), run_time=1)
        
        # Pulse animation to show information flow
        pulses = [
            Indicate(input_layer, color=YELLOW, scale_factor=1.1),
            Indicate(hidden_layer, color=YELLOW, scale_factor=1.1),
            Indicate(output_layer, color=YELLOW, scale_factor=1.1)
        ]
        self.play(Succession(*pulses), run_time=1.5)

        # 6. Highlight Output and Flip Pixel
        # Let's say node 4 corresponds to flipping pixel index 12 (center)
        target_node_idx = 4
        target_pixel_idx = 12
        
        output_label = Text("Flip Pixel 12", font_size=18, color=RED).next_to(output_layer[target_node_idx], RIGHT)
        
        self.play(
            output_layer[target_node_idx].animate.set_fill(RED, opacity=1).scale(1.5),
            Write(output_label)
        )
        self.wait(0.5)

        # Highlight the pixel flip in the grid
        self.play(
            grid[target_pixel_idx].animate.set_fill(YELLOW, opacity=0.8),
            Indicate(grid[target_pixel_idx], color=YELLOW)
        )
        
        # Final descriptive text
        conclusion = Text("DQN approximates Q-values for pixel actions", font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(2)