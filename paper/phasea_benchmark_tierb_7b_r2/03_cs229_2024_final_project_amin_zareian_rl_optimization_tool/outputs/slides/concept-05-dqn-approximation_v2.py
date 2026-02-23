from manim import *

class PixelOptimizationAnimation(Scene):
    def construct(self):
        # 1. Setup Formula
        formula = MathTex(r"Q(s, a; \theta) \approx Q^*(s, a)").to_edge(UP)
        self.play(Write(formula))
        self.wait(0.5)

        # 2. Create a 5x5 grid of pixels
        pixels = VGroup(*[
            Square(side_length=0.4, fill_opacity=1, color=WHITE, stroke_width=1)
            for _ in range(25)
        ]).arrange_in_grid(rows=5, cols=5, buff=0.1)
        
        # Set some random initial values (0s and 1s)
        for i, p in enumerate(pixels):
            if i % 3 == 0:
                p.set_fill(GRAY_E)
            else:
                p.set_fill(WHITE)

        self.play(Create(pixels))
        self.wait(1)

        # 3. Flatten the grid into a 1D vector
        self.play(
            pixels.animate.arrange(DOWN, buff=0.05).scale(0.5).to_edge(LEFT, buff=1),
            run_time=2
        )

        # 4. Create Neural Network Structure
        # Input layer (represented by the pixels themselves)
        input_layer = pixels
        
        # Hidden layer
        hidden_layer = VGroup(*[
            Circle(radius=0.15, color=BLUE, fill_opacity=0.5)
            for _ in range(8)
        ]).arrange(DOWN, buff=0.2).shift(RIGHT * 0.5)
        
        # Output layer
        output_layer = VGroup(*[
            Circle(radius=0.15, color=RED, fill_opacity=0.5)
            for _ in range(25)
        ]).arrange(DOWN, buff=0.05).scale(0.5).to_edge(RIGHT, buff=1)
        
        output_labels = Text("Action Values (Q)", font_size=20).next_to(output_layer, UP)

        # 5. Connect layers (showing a few sample lines for clarity)
        connections_in_hid = VGroup()
        for i in range(0, 25, 5): # Subset of lines to avoid visual clutter
            for j in range(len(hidden_layer)):
                line = Line(input_layer[i].get_right(), hidden_layer[j].get_left(), stroke_width=0.5, stroke_opacity=0.3)
                connections_in_hid.add(line)

        connections_hid_out = VGroup()
        for i in range(len(hidden_layer)):
            for j in range(0, 25, 5): # Subset
                line = Line(hidden_layer[i].get_right(), output_layer[j].get_left(), stroke_width=0.5, stroke_opacity=0.3)
                connections_hid_out.add(line)

        self.play(
            Create(hidden_layer),
            Create(output_layer),
            Create(output_labels),
            run_time=1
        )
        self.play(Create(connections_in_hid), Create(connections_hid_out), run_time=1)

        # 6. Highlight the output node with the highest value
        max_index = 12  # "Flip Pixel 13"
        highlight_circle = Circle(radius=0.12, color=YELLOW, stroke_width=4).move_to(output_layer[max_index])
        
        val_text = MathTex(r"\max", color=YELLOW, font_size=24).next_to(output_layer[max_index], RIGHT)

        self.play(
            output_layer[max_index].animate.set_fill(YELLOW, opacity=1),
            Create(highlight_circle),
            Write(val_text)
        )
        self.wait(1)

        # 7. Show corresponding pixel in the original grid flipping
        # First, reorganize the "vector" back into a grid briefly to show the flip or just target the index
        target_pixel = pixels[max_index]
        flash = Flash(target_pixel, color=YELLOW, run_time=1)
        
        self.play(
            flash,
            target_pixel.animate.set_fill(BLUE, opacity=1).set_color(BLUE),
        )
        self.wait(2)

        # 8. Fade out
        self.play(
            FadeOut(pixels),
            FadeOut(hidden_layer),
            FadeOut(output_layer),
            FadeOut(output_labels),
            FadeOut(connections_in_hid),
            FadeOut(connections_hid_out),
            FadeOut(highlight_circle),
            FadeOut(val_text),
            FadeOut(formula)
        )
        self.wait(1)