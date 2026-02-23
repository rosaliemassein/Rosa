from manim import *

class GranularSoftmaxClassification(Scene):
    def construct(self):
        # 1. Input Image (Using a placeholder to ensure it runs without external files)
        bottle_placeholder = Rectangle(height=2.5, width=2, color=BLUE, fill_opacity=0.3)
        bottle_text = Text("Plastic Bottle\n(Input Image)", font_size=24).move_to(bottle_placeholder)
        bottle = VGroup(bottle_placeholder, bottle_text).to_edge(LEFT, buff=0.5)

        # 2. CNN Layers
        rect1 = Rectangle(width=0.4, height=3.0, color=YELLOW).next_to(bottle, RIGHT, buff=0.8)
        rect2 = Rectangle(width=0.4, height=2.0, color=YELLOW).next_to(rect1, RIGHT, buff=0.4)
        rect3 = Rectangle(width=0.4, height=1.0, color=YELLOW).next_to(rect2, RIGHT, buff=0.4)
        cnn_layers = VGroup(rect1, rect2, rect3)
        
        # Labels for layers
        cnn_label = Text("CNN Layers", font_size=20).next_to(cnn_layers, UP)

        # Data flow arrows
        arrow_in = Arrow(bottle.get_right(), rect1.get_left(), buff=0.1)
        arrow1 = Arrow(rect1.get_right(), rect2.get_left(), buff=0.1)
        arrow2 = Arrow(rect2.get_right(), rect3.get_left(), buff=0.1)
        arrows = VGroup(arrow_in, arrow1, arrow2)

        # 3. Column Vector of 20 Raw Values
        # Using a loop to create 20 x_i labels
        x_values = VGroup(*[
            MathTex(f"x_{{{i}}}", font_size=18) for i in range(1, 21)
        ]).arrange(DOWN, buff=0.05).next_to(rect3, RIGHT, buff=1.0)
        
        vector_box = SurroundingRectangle(x_values, color=WHITE, buff=0.1)
        vector_group = VGroup(x_values, vector_box)
        vector_label = MathTex("x_i", font_size=30).next_to(vector_box, UP)
        
        arrow_to_vec = Arrow(rect3.get_right(), vector_box.get_left(), buff=0.1)

        # 4. Softmax Formula
        formula = MathTex(
            r"\text{softmax}(x_{i}) = \frac{e^{x_{i}}}{\sum_{j=1}^{n}e^{x_{j}}}",
            font_size=34
        ).to_edge(UP + RIGHT, buff=0.5)

        # 5. Horizontal Bar Chart (constructed manually for custom categories)
        # We want 20 bars, one specifically representing the plastic bottle
        bars = VGroup()
        target_idx = 14  # Index of the high probability bar
        for i in range(20):
            bar_len = 0.2 if i != target_idx else 3.5
            bar_color = BLUE if i != target_idx else GREEN
            b = Rectangle(height=0.12, width=bar_len, fill_opacity=0.8, color=bar_color, stroke_width=1)
            bars.add(b)
        
        bars.arrange(DOWN, buff=0.08).next_to(vector_box, RIGHT, buff=1.5)
        
        # 6. Indicate highest bar and labels
        max_bar = bars[target_idx]
        classification_label = Text("Plastic Bottle", color=GREEN, font_size=24).next_to(max_bar, RIGHT)

        # Animation Sequence
        self.play(FadeIn(bottle), Write(cnn_label))
        self.play(Create(cnn_layers), Create(arrows))
        self.wait(0.5)
        
        self.play(Create(arrow_to_vec), Write(vector_label), FadeIn(vector_group))
        self.wait(1)

        self.play(Write(formula))
        self.wait(1)

        # Transition vector to BarChart
        self.play(
            ReplacementTransform(vector_group.copy(), bars),
            run_time=2
        )
        
        self.play(Indicate(max_bar))
        self.play(Write(classification_label))
        
        # Narration / Text overlays
        narration_box = Rectangle(height=1.5, width=8, fill_color=BLACK, fill_opacity=0.8, stroke_color=BLUE)
        narration_box.to_edge(DOWN)
        
        voice_text = Text(
            "Softmax turns raw scores into a probability distribution,\nnormalizing them so the sum equals one.",
            font_size=24
        ).move_to(narration_box)
        
        self.play(FadeIn(narration_box), Write(voice_text))
        self.wait(3)
        
        goal_text = Text(
            "Goal: Map images into 20 distinct categories.",
            font_size=24, color=YELLOW
        ).move_to(narration_box)
        
        self.play(Transform(voice_text, goal_text))
        self.wait(3)

        self.play(FadeOut(narration_box), FadeOut(voice_text))
        self.wait(2)

# To compile this, use: manim -pql filename.py GranularSoftmaxClassification