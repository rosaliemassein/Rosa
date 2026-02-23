from manim import *

class Concept05DQNApproximation(Scene):
    def construct(self):
        # 1. Pixel Grid Setup
        pixel_grid = VGroup(*[
            Square(side_length=0.4, fill_opacity=0.8, fill_color=WHITE, stroke_width=1)
            for _ in range(25)
        ]).arrange_in_grid(rows=5, cols=5, buff=0.1).shift(LEFT * 4)
        
        grid_label = Text("5x5 State Grid", font_size=24).next_to(pixel_grid, UP)
        self.play(Create(pixel_grid), Write(grid_label))
        self.wait(1)

        # 2. Flattening the grid into a 1D vector (0s and 1s)
        flattened_vector = VGroup()
        for i in range(25):
            sq = Square(side_length=0.2, fill_opacity=0.8, fill_color=WHITE, stroke_width=0.5)
            # Fill with 0 or 1 strings for visualization
            val = "1" if i % 3 == 0 or i % 7 == 0 else "0"
            txt = Text(val, font_size=12, color=BLACK).move_to(sq.get_center())
            flattened_vector.add(VGroup(sq, txt))
        
        flattened_vector.arrange(DOWN, buff=0.05).scale(0.8).shift(LEFT * 1)
        
        self.play(
            ReplacementTransform(pixel_grid.copy(), flattened_vector),
            grid_label.animate.scale(0.8).next_to(flattened_vector, UP)
        )
        self.wait(1)

        # 3. Deep Q-Network Visualization (Input -> Hidden -> Output)
        hidden_layer = VGroup(*[Circle(radius=0.15, color=BLUE, fill_opacity=0.5) for _ in range(8)]).arrange(DOWN, buff=0.2).shift(RIGHT * 1.5)
        output_layer = VGroup(*[Circle(radius=0.15, color=GREEN, fill_opacity=0.5) for _ in range(12)]).arrange(DOWN, buff=0.15).shift(RIGHT * 4)
        
        nn_label = Text("Deep Q-Network", font_size=24).move_to(UP * 3 + RIGHT * 2.5)
        
        # Connections between Flattened Vector (Input) and Hidden Layer
        connections1 = VGroup(*[
            Line(flattened_vector[i].get_right(), hidden_layer[j].get_left(), stroke_width=0.5, stroke_opacity=0.2)
            for i in range(0, 25, 4) for j in range(8)
        ])
        # Connections between Hidden Layer and Output Layer
        connections2 = VGroup(*[
            Line(hidden_layer[i].get_right(), output_layer[j].get_left(), stroke_width=0.5, stroke_opacity=0.2)
            for i in range(8) for j in range(12)
        ])

        self.play(Create(hidden_layer), Create(output_layer), Write(nn_label))
        self.play(Create(connections1), Create(connections2), run_time=1.5)
        self.wait(1)

        # 4. Highlight best output and corresponding pixel flip
        target_index = 12 # Middle pixel
        highlight_circle = output_layer[5].copy().set_color(YELLOW).set_stroke(width=4)
        output_text = Text("Max Q-Value: Action 13", font_size=18, color=YELLOW).next_to(output_layer[5], RIGHT)
        
        self.play(
            Create(highlight_circle),
            Write(output_text),
            output_layer[5].animate.set_fill(YELLOW, opacity=1)
        )
        
        # Highlight the pixel in the original 5x5 grid
        pixel_to_flip = pixel_grid[target_index]
        self.play(
            pixel_to_flip.animate.set_fill(RED, opacity=1),
            Flash(pixel_to_flip, color=RED)
        )
        self.wait(1)

        # 5. Formula and Voiceover text display
        formula = MathTex(r"Q(s, a; \theta) \approx Q^*(s, a)").scale(1.2).to_edge(DOWN, buff=1.2)
        # Replacing constant ITALIC with string "ITALIC" to prevent undefined identifier errors
        voiceover_text = Text(
            "Approximating rewards with a Deep Q-Network.",
            font_size=20,
            slant="ITALIC"
        ).next_to(formula, DOWN, buff=0.3)

        self.play(Write(formula))
        self.play(FadeIn(voiceover_text))
        self.wait(3)