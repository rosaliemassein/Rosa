from manim import *
import numpy as np

class SoftmaxAnimation(Scene):
    def construct(self):
        # 1. Input Image of a plastic bottle
        # Note: 'img-12.jpeg' is assumed to exist as per the original prompt
        try:
            plastic_bottle = ImageMobject("img-12.jpeg").scale(0.8)
        except:
            # Fallback if image is missing during compilation test
            plastic_bottle = RoundedRectangle(height=2, width=1.5, color=WHITE)
            bottle_label = Text("Image", font_size=20).move_to(plastic_bottle)
            plastic_bottle = Group(plastic_bottle, bottle_label)
            
        plastic_bottle.to_edge(LEFT, buff=1).shift(DOWN * 0.5)
        self.play(FadeIn(plastic_bottle))
        
        # 2. Draw a series of vertical rectangles representing CNN layers
        cnn_layers = VGroup(*[
            Rectangle(height=1.8, width=0.15, fill_opacity=0.8, fill_color=GREEN)
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.2).next_to(plastic_bottle, RIGHT, buff=0.8)
        
        # 3. Arrows to show data flow
        arrow1 = Arrow(plastic_bottle.get_right(), cnn_layers.get_left(), color=BLUE)
        
        # 4. Column vector of 20 raw values (MathTex labeled 'x_i')
        xi_label = MathTex(r"x_i").scale(1.2).next_to(cnn_layers, RIGHT, buff=0.8)
        arrow2 = Arrow(cnn_layers.get_right(), xi_label.get_left(), color=BLUE)
        
        self.play(Create(arrow1), Create(cnn_layers))
        self.play(Create(arrow2), Write(xi_label))
        
        # 5. Softmax formula appearing at the top
        softmax_formula = MathTex(
            r"\text{softmax}(x_{i}) = \frac{e^{x_{i}}}{\sum_{j=1}^{n} e^{x_{j}}}",
            font_size=36
        ).to_edge(UP, buff=0.5).shift(RIGHT * 2)
        self.play(Write(softmax_formula))
        
        # 6. Horizontal BarChart construction
        # Since BarChart class caused issues, we build a manual horizontal one
        # using 20 rectangles to represent the 20 categories.
        bars = VGroup()
        # Create 20 mock probability values
        probs = [0.03] * 20
        probs[12] = 0.8  # Index 12 will be our "Plastic Bottle"
        
        for i in range(20):
            bar_width = probs[i] * 4.0  # Scale the probability to a width
            bar = Rectangle(
                height=0.1, 
                width=max(0.05, bar_width), 
                fill_opacity=0.8, 
                fill_color=GREEN, 
                stroke_width=0.5
            )
            bars.add(bar)
        
        bars.arrange(DOWN, buff=0.08)
        bars.next_to(xi_label, RIGHT, buff=1.2).shift(DOWN * 0.2)
        
        # Transform the raw values label into the distribution
        self.play(ReplacementTransform(xi_label.copy(), bars))
        
        # 7. Indicate the highest bar and label it 'Plastic Bottle'
        # The 13th bar (index 12) is the highest
        max_bar = bars[12]
        self.play(
            max_bar.animate.set_color(RED),
            Indicate(max_bar, scale_factor=1.2, color=RED)
        )
        
        label = Text("Plastic Bottle", font_size=24, color=RED).next_to(max_bar, RIGHT, buff=0.3)
        self.play(Write(label))
        
        self.wait(2)