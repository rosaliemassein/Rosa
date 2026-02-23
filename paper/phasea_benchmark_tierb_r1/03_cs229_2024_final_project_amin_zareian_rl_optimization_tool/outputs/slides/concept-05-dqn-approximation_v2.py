from manim import *

class Concept05DQNApproximation(Scene):
    def construct(self):
        # 1. Display Formula
        formula = MathTex(r"Q(s, a; \theta) \approx Q^*(s, a)")
        formula.to_edge(UP)
        self.play(Write(formula))

        # 2. Create 5x5 pixel grid
        # Using Squares to represent pixels
        grid = VGroup(*[
            Square(side_length=0.4, fill_color=WHITE, fill_opacity=0.2, stroke_width=2)
            for _ in range(25)
        ])
        grid.arrange_in_grid(rows=5, buff=0.1)
        grid.shift(LEFT * 4)
        
        grid_title = Text("5x5 Input Grid", font_size=24).next_to(grid, UP)
        
        self.play(Create(grid), Write(grid_title))
        self.wait(1)

        # 3. Flatten the grid into a 1D vector
        # Create the vector mobjects (circles to represent the data points)
        vector = VGroup(*[
            Circle(radius=0.1, fill_color=BLUE, fill_opacity=0.8, stroke_width=1)
            for _ in range(25)
        ])
        vector.arrange(DOWN, buff=0.05)
        vector.move_to(LEFT * 1.5)
        
        vector_label = Text("Flattened Vector (25 values)", font_size=20).next_to(vector, UP)

        # Animation: Move squares to circle positions and transform
        self.play(
            grid_title.animate.become(vector_label),
            ReplacementTransform(grid.copy(), vector),
            run_time=2
        )
        self.wait(1)

        # 4. Create Neural Network (Input, Hidden, Output)
        # Input Layer (reuse vector)
        hidden_layer = VGroup(*[Circle(radius=0.15, color=WHITE) for _ in range(8)])
        hidden_layer.arrange(DOWN, buff=0.2)
        hidden_layer.move_to(RIGHT * 1)
        
        output_layer = VGroup(*[Circle(radius=0.15, color=WHITE) for _ in range(5)])
        output_layer.arrange(DOWN, buff=0.4)
        output_layer.move_to(RIGHT * 3.5)
        
        output_labels = VGroup(*[
            Text(f"Flip {i+1}", font_size=16).next_to(output_layer[i], RIGHT)
            for i in range(5)
        ])

        # Connections (Lines)
        connections1 = VGroup()
        for v in vector[::4]: # sparse connections for visual clarity
            for h in hidden_layer:
                connections1.add(Line(v.get_right(), h.get_left(), stroke_width=0.5, stroke_opacity=0.3))
        
        connections2 = VGroup()
        for h in hidden_layer:
            for o in output_layer:
                connections2.add(Line(h.get_right(), o.get_left(), stroke_width=0.5, stroke_opacity=0.3))

        self.play(
            Create(hidden_layer),
            Create(output_layer),
            Create(connections1),
            Create(connections2),
            Write(output_labels)
        )
        self.wait(1)

        # 5. Animate "Flow" through the network
        flow_dots = VGroup(*[
            Dot(v.get_center(), color=YELLOW, radius=0.05)
            for v in vector[::3]
        ])
        
        self.play(
            LaggedStart(*[
                v.animate.move_to(hidden_layer[len(hidden_layer)//2].get_center()).set_opacity(0)
                for v in flow_dots
            ], lag_ratio=0.1),
            run_time=1.5
        )

        # 6. Highlight the output node with the highest value
        max_index = 2 # Let's say the 3rd node is highest
        highlight_rect = SurroundingRectangle(output_layer[max_index], color=YELLOW, buff=0.1)
        
        self.play(
            output_layer[max_index].animate.set_fill(YELLOW, opacity=1),
            Create(highlight_rect)
        )
        self.wait(1)

        # 7. Show the corresponding pixel in the original grid flipping
        # We'll map "Flip 3" to a specific pixel in the original grid
        target_pixel_index = 12 # Middle pixel
        pixel_to_flip = grid[target_pixel_index]
        
        # Flash the output and then the pixel
        self.play(Indicate(output_layer[max_index]))
        self.play(
            pixel_to_flip.animate.set_fill(YELLOW, opacity=1).set_stroke(YELLOW),
            run_time=1
        )
        
        # 8. Narrative text at the bottom
        voiceover_text = Text(
            "The DQN approximates the Q-values for large state spaces.",
            font_size=20
        ).to_edge(DOWN)
        
        self.play(Write(voiceover_text))
        self.wait(3)

        # Cleanup
        self.play(
            FadeOut(grid),
            FadeOut(vector),
            FadeOut(hidden_layer),
            FadeOut(output_layer),
            FadeOut(connections1),
            FadeOut(connections2),
            FadeOut(output_labels),
            FadeOut(grid_title),
            FadeOut(voiceover_text),
            FadeOut(highlight_rect),
            FadeOut(formula)
        )