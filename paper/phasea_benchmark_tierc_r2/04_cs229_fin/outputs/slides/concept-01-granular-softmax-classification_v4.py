from manim import *

class GranularSoftmaxClassification(Scene):
    def construct(self):
        # 1. Input Image (Left)
        # Using a rectangle placeholder with the label if the image reference is needed
        input_image = Rectangle(height=2.5, width=2, color=BLUE)
        input_label = Text("Plastic Bottle\n(Input)", font_size=20).move_to(input_image.get_center())
        input_group = VGroup(input_image, input_label).to_edge(LEFT, buff=0.5)
        
        # 2. CNN Layers (Series of vertical rectangles)
        cnn_layers = VGroup(*[
            Rectangle(height=3.5, width=0.4, fill_opacity=0.6, color=BLUE)
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.25)
        cnn_layers.next_to(input_group, RIGHT, buff=1.0)
        
        layer_tag = Text("Deep CNN Layers", font_size=24).next_to(cnn_layers, UP)
        arrow1 = Arrow(input_group.get_right(), cnn_layers.get_left(), buff=0.1)

        # 3. Raw Scores (Column vector of x_i)
        # Built manually to ensure compatibility
        raw_elements = VGroup(
            MathTex("x_1"),
            MathTex("x_2"),
            MathTex("\\vdots"),
            MathTex("x_{20}")
        ).arrange(DOWN, buff=0.3)
        
        left_bracket = MathTex(r"\left[").scale(2.5)
        right_bracket = MathTex(r"\right]").scale(2.5)
        left_bracket.next_to(raw_elements, LEFT, buff=0.1)
        right_bracket.next_to(raw_elements, RIGHT, buff=0.1)
        
        raw_vector = VGroup(raw_elements, left_bracket, right_bracket)
        raw_vector.next_to(cnn_layers, RIGHT, buff=1.0)
        
        vector_label = MathTex("x_i", font_size=36).next_to(raw_vector, UP)
        arrow2 = Arrow(cnn_layers.get_right(), raw_vector.get_left(), buff=0.1)

        # 4. Softmax Formula
        formula = MathTex(
            r"softmax(x_{i})=\frac{e^{x_{i}}}{\sum_{j=1}^{n}e^{x_{j}}}",
            font_size=38
        ).to_edge(UP, buff=0.5)

        # 5. Probabilities (Horizontal Bar Chart)
        # We manually build bars to represent the probability distribution
        probs = [0.05, 0.1, 0.75, 0.05, 0.05] # Significant weight on the 3rd category
        bars = VGroup()
        for p in probs:
            bar = Rectangle(height=0.4, width=p*4.5, fill_opacity=0.8, color=BLUE)
            bars.add(bar)
        
        bars.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        bars.shift(RIGHT * 3.5 + DOWN * 0.5)
        
        # Highlight the "Plastic Bottle" bar
        bars[2].set_color(YELLOW)
        
        bar_label = Text("Probabilities", font_size=24).next_to(bars, UP)
        winner_text = Text("Plastic Bottle", color=YELLOW, font_size=28).next_to(bars[2], RIGHT, buff=0.3)

        # ANIMATION SEQUENCE
        self.play(FadeIn(input_group))
        self.play(
            Create(arrow1),
            Create(cnn_layers),
            Write(layer_tag)
        )
        self.wait(0.5)
        
        self.play(
            Create(arrow2),
            Write(raw_vector),
            Write(vector_label)
        )
        self.wait(1)
        
        self.play(Write(formula))
        self.wait(1)
        
        # Transform concept: Data flow into Bar Chart
        self.play(
            FadeIn(bars, shift=RIGHT),
            Write(bar_label)
        )
        self.wait(1)
        
        # Final indication
        self.play(Indicate(bars[2], color=YELLOW, scale_factor=1.2))
        self.play(Write(winner_text))
        self.wait(3)