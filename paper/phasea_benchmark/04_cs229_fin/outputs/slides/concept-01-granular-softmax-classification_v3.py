from manim import *

class GranularSoftmaxClassification(Scene):
    def construct(self):
        # 1. Input Image Placeholder (Plastic Bottle)
        # We use shapes to avoid external image dependencies
        image_box = RoundedRectangle(corner_radius=0.1, height=2.2, width=1.6, color=WHITE)
        image_text = Text("Plastic Bottle\n(Input)", font_size=18).move_to(image_box)
        bottle_group = VGroup(image_box, image_text).to_edge(LEFT, buff=0.5)

        # 2. CNN Layers
        # Vertical rectangles representing the layers
        cnn_layers = VGroup(
            Rectangle(width=0.4, height=3.2, fill_opacity=0.5, color=YELLOW),
            Rectangle(width=0.4, height=2.6, fill_opacity=0.5, color=GREEN),
            Rectangle(width=0.4, height=2.0, fill_opacity=0.5, color=BLUE)
        ).arrange(RIGHT, buff=0.4).next_to(bottle_group, RIGHT, buff=0.8)

        # 3. Data Flow Arrows
        arrow1 = Arrow(bottle_group.get_right(), cnn_layers[0].get_left(), buff=0.1)
        arrow2 = Arrow(cnn_layers[0].get_right(), cnn_layers[1].get_left(), buff=0.1)
        arrow3 = Arrow(cnn_layers[1].get_right(), cnn_layers[2].get_left(), buff=0.1)

        self.play(Create(bottle_group))
        self.play(
            LaggedStart(GrowArrow(arrow1), GrowArrow(arrow2), GrowArrow(arrow3), lag_ratio=0.3),
            LaggedStart(Create(cnn_layers[0]), Create(cnn_layers[1]), Create(cnn_layers[2]), lag_ratio=0.3)
        )

        # 4. Column Vector of 20 Raw Values (x_i)
        raw_rects = VGroup(*[
            Rectangle(width=0.5, height=0.12, stroke_width=1, fill_opacity=0.1) 
            for _ in range(20)
        ]).arrange(DOWN, buff=0.04).next_to(cnn_layers, RIGHT, buff=1.0)
        
        # Manually construct a bracket (since Brace is disallowed in this environment)
        v_line = Line(raw_rects.get_corner(UR) + RIGHT*0.1, raw_rects.get_corner(DR) + RIGHT*0.1)
        h_top = Line(v_line.get_start(), v_line.get_start() + LEFT*0.1)
        h_bottom = Line(v_line.get_end(), v_line.get_end() + LEFT*0.1)
        bracket = VGroup(v_line, h_top, h_bottom)
        
        vector_label = MathTex("x_i").next_to(v_line, RIGHT, buff=0.2)
        arrow_to_vec = Arrow(cnn_layers[2].get_right(), raw_rects.get_left(), buff=0.1)

        self.play(GrowArrow(arrow_to_vec), Create(raw_rects))
        self.play(Create(bracket), Write(vector_label))
        self.wait(1)

        # 5. Softmax Formula
        # Using the standard formula reference
        formula = MathTex(
            r"\text{softmax}(x_{i}) = \frac{e^{x_{i}}}{\sum_{j=1}^{n} e^{x_{j}}}"
        ).scale(0.8).to_edge(UP, buff=0.5)
        self.play(Write(formula))
        self.wait(1)

        # 6. Probability Bar Chart
        # 20 bars, one specifically taller to represent the classification
        bars = VGroup()
        for i in range(20):
            # Make the 15th category the "Plastic Bottle" winner
            h_val = 2.5 if i == 14 else 0.15
            bar = Rectangle(
                width=0.2, 
                height=h_val, 
                fill_opacity=0.7, 
                color=BLUE, 
                stroke_width=1
            )
            bars.add(bar)
        
        # Arrange bars horizontally with bottoms aligned
        bars.arrange(RIGHT, buff=0.1, aligned_edge=DOWN).to_edge(RIGHT, buff=0.5).shift(DOWN*0.5)

        # 7. Transform Raw Values to Probabilities
        self.play(
            ReplacementTransform(raw_rects, bars),
            FadeOut(bracket),
            FadeOut(vector_label),
            FadeOut(arrow_to_vec)
        )
        self.wait(0.5)

        # 8. Indicate and Label Results
        winner_bar = bars[14]
        result_label = Text("Plastic Bottle", font_size=22, color=YELLOW).next_to(winner_bar, UP, buff=0.3)
        
        self.play(Indicate(winner_bar, color=YELLOW), run_time=2)
        self.play(winner_bar.animate.set_color(YELLOW), Write(result_label))
        self.wait(2)