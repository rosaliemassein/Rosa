from manim import *

class GranularSoftmaxClassification(Scene):
    def construct(self):
        # Image of a plastic bottle
        plastic_bottle = ImageMobject("img-12.jpeg").scale(0.5).to_edge(LEFT)
        
        # CNN layers
        cnn_layer1 = Rectangle(height=2, width=0.5).next_to(plastic_bottle, RIGHT)
        cnn_layer2 = Rectangle(height=1.5, width=0.5).next_to(cnn_layer1, RIGHT)
        cnn_layer3 = Rectangle(height=1, width=0.5).next_to(cnn_layer2, RIGHT)
        
        # Raw values
        raw_values = VGroup(*[
            MathTex(r"x_{}").set_color(BLUE).next_to(cnn_layer3, RIGHT, buff=0.5)
            for i in range(20)
        ]).arrange(RIGHT, buff=0.5)
        
        # Softmax formula
        softmax_eq = MathTex(r"\text{softmax}(x_i) = \frac{e^{x_i}}{\sum_{j=1}^{n} e^{x_j}}").to_edge(RIGHT).shift(UP)
        
        # Bar chart
        bar_chart = VGroup(*[
            Rectangle(height=0.5, width=0.3).next_to(RIGHT * (i + 1), RIGHT, buff=0.3)
            for i in range(20)
        ]).arrange(RIGHT, buff=0.3).scale(0.6)
        
        # Animation
        self.add(plastic_bottle, cnn_layer1, cnn_layer2, cnn_layer3)
        self.wait(1)
        self.play(FadeIn(cnn_layer2), FadeIn(cnn_layer3))
        self.wait(1)
        self.play(FadeOut(cnn_layer2), FadeOut(raw_values[0:8]))
        self.wait(1)
        self.play(Create(bar_chart))
        self.wait(1)
        self.play(FadeIn(raw_values[8:20]))
        self.wait(1)
        self.play(Create(softmax_eq))
        self.wait(2)
        
        # Indicate highest probability
        max_probability = bar_chart[14]
        self.play(Indicate(max_probability, color=RED))
        self.wait(2)
        
        # Label highest probability
        label = MathTex(r"Plastic Bottle").next_to(max_probability, DOWN)
        self.play(Write(label))
        self.wait(2)