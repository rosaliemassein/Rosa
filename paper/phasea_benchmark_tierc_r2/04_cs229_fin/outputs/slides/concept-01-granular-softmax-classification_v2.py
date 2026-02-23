from manim import *

class GranularSoftmaxClassification(Scene):
    def construct(self):
        # Load the image
        plastic_bottle_image = ImageMobject("img-12.jpeg")
        self.add(plastic_bottle_image)

        # Explanation text
        explanation = Text("Softmax transforms neural network outputs into a probability distribution.")
        self.play(Write(explanation), run_time=2)

        # CNN layers and raw scores
        self.next_to(explanation, DOWN)
        self.play(Create(Circle(radius=2)), run_time=1)  # Placeholder for CNN layers
        arrows = [
            Arrow(ORIGIN, RIGHT),   # Image to layer 1
            Arrow(RIGHT, DOWN),    # Layer 1 to layer 2
            Arrow(DOWN, RIGHT)     # Layer 2 to layer 3
        ]
        self.play(Create(arrows), run_time=1)

        raw_values = VGroup(
            *[MathTex(r"x_{i}") for i in range(1, 21)]
        )
        self.play(Create(raw_values), run_time=3)
        self.wait(2)

        # Animated softmax formula
        self.next_to(raw_values, DOWN, buff=1)
        soft_max_formula = MathTex(r"softmax(x_{i})=\frac{e^{x_{i}}}{\sum_{j=1}^{n}e^{x_{j}}}")
        self.play(Write(soft_max_formula), run_time=2)
        self.wait()

        # BarChart representing probabilities
        bars = [
            Rectangle(width=0.6, height=0.2*value, color=RED) for value in range(1, 21)
        ]
        bars[0].next_to(soft_max_formula, RIGHT)
        self.play(Create(bars[0]), run_time=1)

        # Indicate the highest bar and label it
        self.next_to(bars[0], RIGHT)
        bars[1].next_to(soft_max_formula, RIGHT)
        self.play(Create(bars[1]), run_time=1)

        # Add indicators and labels
        self.play(
            Indicate(bars[0]),
            Write(Text("Plastic Bottle", color=RED)),
        )
        self.wait(2)

        # Fade out
        self.play(FadeOut(bars), run_time=1)
        self.wait()