from manim import *
import numpy as np

class GranularSoftmaxClassification(Scene):
    def construct(self):
        # 1. Input Image (Using a labeled rectangle to ensure compatibility)
        bottle_rect = Rectangle(height=2.5, width=1.8, color=GRAY)
        bottle_label = Text("Plastic Bottle\nImage", font_size=18).move_to(bottle_rect.get_center())
        bottle = VGroup(bottle_rect, bottle_label).to_edge(LEFT, buff=0.5)
        
        # 2. CNN Layers
        # Vertical rectangles representing layers
        cnn_layers = VGroup(*[
            Rectangle(width=0.3, height=2.0, fill_opacity=0.3, color=BLUE)
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.15).next_to(bottle, RIGHT, buff=0.8)
        
        layer_label = Text("CNN Layers", font_size=20).next_to(cnn_layers, UP)
        
        # 3. Column Vector of 20 Raw Values
        # Mock data representing scores for 20 categories
        raw_scores = np.array([-1.0, 0.4, 1.8, -0.2, 0.7, 1.3, 3.8, -0.9, 0.1, 0.8, 
                               -0.4, 1.0, 6.5, 0.2, -1.9, 1.1, 0.7, -0.3, 0.5, 1.2])
        
        vector = VGroup(*[
            Square(side_length=0.12, stroke_width=1).set_fill(WHITE, opacity=0.2)
            for _ in range(20)
        ]).arrange(DOWN, buff=0.04).next_to(cnn_layers, RIGHT, buff=0.8)
        
        vector_label = MathTex("x_i").next_to(vector, UP)
        
        # Arrows for data flow
        arrow1 = Arrow(bottle.get_right(), cnn_layers.get_left(), buff=0.1)
        arrow2 = Arrow(cnn_layers.get_right(), vector.get_left(), buff=0.1)

        # 4. Softmax Formula
        formula = MathTex(
            r"softmax(x_{i}) = \frac{e^{x_{i}}}{\sum_{j=1}^{20}e^{x_{j}}}"
        ).to_edge(UP, buff=0.5)

        # Calculate Probabilities for the bars
        exp_scores = np.exp(raw_scores)
        probabilities = exp_scores / np.sum(exp_scores)
        
        # 5. Horizontal Bar Chart
        bar_group = VGroup()
        for i, p in enumerate(probabilities):
            # Map probability to a bar width
            bar_width = p * 4.5 + 0.05 # Add a tiny baseline for visibility
            bar = Rectangle(
                width=bar_width, 
                height=0.1, 
                stroke_width=1, 
                fill_opacity=0.8, 
                color=BLUE
            )
            bar_group.add(bar)
        
        bar_group.arrange(DOWN, buff=0.05).move_to(RIGHT * 3.5)
        # Align all bars to the left edge of the group
        for bar in bar_group:
            bar.align_to(bar_group, LEFT)
        
        # Identify the highest bar (index 12 in our dummy data)
        max_idx = np.argmax(probabilities)
        highest_bar = bar_group[max_idx]
        
        label_plastic = Text("Plastic Bottle", font_size=22, color=YELLOW).next_to(highest_bar, RIGHT, buff=0.3)

        # --- Animations ---
        self.play(FadeIn(bottle))
        self.wait(0.5)
        
        self.play(
            GrowArrow(arrow1), 
            Create(cnn_layers), 
            Write(layer_label)
        )
        self.wait(0.5)
        
        self.play(
            GrowArrow(arrow2), 
            Create(vector), 
            Write(vector_label)
        )
        self.wait(1)
        
        self.play(Write(formula))
        self.wait(1)
        
        # Transition to probability distribution
        self.play(
            FadeOut(vector_label),
            FadeOut(arrow2),
            FadeOut(cnn_layers),
            FadeOut(layer_label),
            FadeOut(arrow1),
            bottle.animate.scale(0.5).to_corner(UL),
            ReplacementTransform(vector, bar_group)
        )
        self.wait(0.5)
        
        # Highlight result
        self.play(
            highest_bar.animate.set_color(YELLOW),
            Indicate(highest_bar)
        )
        self.play(Write(label_plastic))
        
        self.wait(2)