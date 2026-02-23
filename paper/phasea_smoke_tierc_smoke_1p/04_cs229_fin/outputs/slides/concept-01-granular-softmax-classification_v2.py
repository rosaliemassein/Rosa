from manim import *
import numpy as np

class SoftmaxDemo(Scene):
    def construct(self):
        # 1. Input Image (Placeholder for the plastic bottle)
        # Using a square with text as a fallback if the image is missing, 
        # but following instructions to use ImageMobject.
        try:
            bottle_img = ImageMobject("img-12.jpeg").scale(1.2)
        except:
            bottle_img = Rectangle(height=2, width=1.5, color=GRAY).add(Text("Bottle", font_size=20))
        
        bottle_img.to_edge(LEFT, buff=0.5)
        bottle_label = Text("Input Image", font_size=24).next_to(bottle_img, DOWN)

        # 2. CNN Layers
        cnn_layers = VGroup(*[
            Rectangle(width=0.2, height=1.5 + (i * 0.2), fill_opacity=0.3, fill_color=BLUE)
            for i in range(4)
        ]).arrange(RIGHT, buff=0.15).next_to(bottle_img, RIGHT, buff=0.8)
        
        cnn_text = Text("CNN Layers", font_size=20).next_to(cnn_layers, DOWN)
        
        # 3. Arrow from image to CNN
        arrow1 = Arrow(bottle_img.get_right(), cnn_layers.get_left(), buff=0.1)

        # 4. Raw values vector (20 raw values x_i)
        # We represent this as a column vector with some ellipsis to fit 20 values visually
        raw_scores = np.array([-1.2, 0.5, 2.8, -0.3, 0.1, -0.5, 0.8, -1.0, 0.2, -0.4, 
                               0.6, -0.7, 0.3, -0.2, 0.9, -1.1, 0.4, -0.8, 0.5, -0.1])
        
        # Adjust indices to make index 2 (Plastic Bottle) the highest
        raw_scores[2] = 4.5 
        
        vector_box = SurroundingRectangle(VGroup(*[Dot() for _ in range(10)]), color=WHITE)
        vector_elements = VGroup(*[
            MathTex(f"x_{{{i+1}}}", font_size=18) for i in range(20)
        ]).arrange(DOWN, buff=0.05).scale(0.8)
        
        # To make 20 values fit, we condense them
        vector_container = VGroup(
            MathTex(r"\begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_{20} \end{bmatrix}", font_size=36)
        ).next_to(cnn_layers, RIGHT, buff=0.8)
        
        arrow2 = Arrow(cnn_layers.get_right(), vector_container.get_left(), buff=0.1)
        raw_label = MathTex("x_i", font_size=30).next_to(vector_container, UP)

        # 5. Softmax Formula
        formula = MathTex(
            r"\text{softmax}(x_{i}) = \frac{e^{x_{i}}}{\sum_{j=1}^{20} e^{x_{j}}}",
            font_size=34
        ).to_edge(UP, buff=0.5)

        # 6. Horizontal Bar Chart (Probabilities)
        # Calculate softmax
        exp_scores = np.exp(raw_scores)
        probabilities = exp_scores / np.sum(exp_scores)
        
        chart_origin = RIGHT * 4 + DOWN * 2
        bar_group = VGroup()
        for i, p in enumerate(probabilities):
            bar = Rectangle(
                width=p * 4.0, # Scale width by probability
                height=0.1,
                fill_opacity=0.8,
                fill_color=YELLOW if i == 2 else BLUE,
                stroke_width=0.5
            )
            bar_group.add(bar)
        
        bar_group.arrange(DOWN, buff=0.05).to_edge(RIGHT, buff=0.5)
        
        chart_label = Text("Probabilities", font_size=20).next_to(bar_group, UP)

        # 7. Animations
        self.play(FadeIn(bottle_img), Write(bottle_label))
        self.play(GrowArrow(arrow1), Create(cnn_layers), Write(cnn_text))
        self.wait(0.5)
        
        self.play(GrowArrow(arrow2), Write(vector_container), Write(raw_label))
        self.wait(0.5)
        
        self.play(Write(formula))
        self.wait(1)
        
        # Transform vector scores into horizontal bars
        self.play(
            LaggedStart(*[FadeIn(bar, shift=RIGHT) for bar in bar_group], lag_ratio=0.05),
            Write(chart_label)
        )
        
        # 8. Indicate highest bar and label
        highest_bar = bar_group[2]
        self.play(Indicate(highest_bar, scale_factor=1.2, color=YELLOW))
        
        result_label = Text("Plastic Bottle", font_size=24, color=YELLOW).next_to(highest_bar, RIGHT)
        self.play(Write(result_label))
        
        self.wait(3)

# Note: Ensure numpy is installed as 'np' is used for the Softmax calculation.