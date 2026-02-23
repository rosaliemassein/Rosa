from manim import *

class Concept01GranularSoftmaxClassification(Scene):
    def construct(self):
        # Left side: Plastic bottle image
        plastic_bottle_image = ImageMobject("img-12.jpeg").scale(0.5).to_edge(LEFT)
        self.play(FadeIn(plastic_bottle_image))
        
        # CNN layers
        cnn_layers = VGroup(*[Rectangle(width=0.2, height=1) for _ in range(5)]).arrange(RIGHT).next_to(plastic_bottle_image, RIGHT)
        self.play(FadeIn(cnn_layers))
        
        # Data flow arrows
        data_arrows = VGroup(*[Arrow(start=l.get_right(), end=l.get_right() + 0.5 * RIGHT, color=BLUE) for l in cnn_layers])
        self.play(FadeIn(data_arrows))
        
        # Column vector of raw values
        raw_values = VGroup(*[MathTex(r"x_{" + str(i+1) + r"}").next_to(cnn_layers[i], UP, buff=0.2) for i in range(5)]).arrange(RIGHT)
        self.play(FadeIn(raw_values))
        
        # Right side: Softmax formula
        softmax_formula = MathTex(r"\text{softmax}(x_{i}) = \frac{e^{x_{i}}}{\sum_{j=1}^{n}e^{x_{j}}}")
        softmax_formula.scale(0.8).next_to(cnn_layers, RIGHT, buff=2)
        self.play(FadeIn(softmax_formula))
        
        # Transform raw values into probabilities
        probability_bars = VGroup(*[Rectangle(width=0.1, height=raw_values[i].get_center()[1] + 0.5) for i in range(5)]).arrange(RIGHT, buff=0.2)
        probability_bars.next_to(softmax_formula, RIGHT, buff=1)
        self.play(Transform(raw_values, probability_bars))
        
        # Indicate the highest bar
        max_index = 2  # Assuming the highest probability is at index 2 for simplicity
        max_bar = probability_bars[max_index]
        rect_15 = SurroundingRectangle(max_bar, color=WHITE, buff=-0.02)
        self.play(FadeIn(rect_15))
        
        # Label the highest bar
        max_label = MathTex(r"\text{Plastic Bottle}")
        max_label.scale(0.7).next_to(max_bar, UP, buff=0.1)
        self.play(FadeIn(max_label))
        
        self.wait(2)