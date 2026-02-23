from manim import *

class Concept01GranularSoftmaxClassification(Scene):
    def construct(self):
        # 1. Input Image Placeholder (instead of ImageMobject to ensure compilation)
        bottle_box = Rectangle(height=2.5, width=2.0, color=WHITE)
        bottle_label = Text("Plastic Bottle\n(Input)", font_size=20)
        bottle_image = VGroup(bottle_box, bottle_label).to_edge(LEFT, buff=0.5)

        # 2. CNN Layers (vertical rectangles)
        cnn_layers = VGroup(*[
            Rectangle(height=2.0 - i*0.4, width=0.4, fill_opacity=0.6, color=BLUE)
            for i in range(3)
        ]).arrange(RIGHT, buff=0.2).next_to(bottle_image, RIGHT, buff=0.6)
        
        layer_label = Text("CNN Layers", font_size=18).next_to(cnn_layers, UP)

        # 3. Arrows showing data flow
        arrow1 = Arrow(bottle_image.get_right(), cnn_layers.get_left(), buff=0.1)
        
        # 4. Column Vector of 20 raw values (x_i)
        # Using manual brackets as Brace is disallowed
        raw_scores_list = [MathTex(f"x_{{{i+1}}}") for i in range(3)] 
        raw_scores_list.append(MathTex(r"\vdots"))
        raw_scores_list.append(MathTex(f"x_{{20}}"))
        
        raw_scores_vgroup = VGroup(*raw_scores_list).arrange(DOWN, buff=0.2)
        
        # Manual bracket construction to replace Brace
        bracket_left = MathTex(r"\left[").scale(2.5).next_to(raw_scores_vgroup, LEFT, buff=0.1)
        bracket_right = MathTex(r"\right]").scale(2.5).next_to(raw_scores_vgroup, RIGHT, buff=0.1)
        
        vector_group = VGroup(raw_scores_vgroup, bracket_left, bracket_right).next_to(cnn_layers, RIGHT, buff=0.8)
        vector_label = MathTex("x_i").next_to(vector_group, UP)
        
        arrow2 = Arrow(cnn_layers.get_right(), vector_group.get_left(), buff=0.1)

        # 5. Softmax formula
        softmax_formula = MathTex(
            r"softmax(x_{i})=\frac{e^{x_{i}}}{\sum_{j=1}^{n}e^{x_{j}}}",
            color=YELLOW
        ).scale(0.85).to_edge(UP, buff=0.5).shift(RIGHT * 2)

        # 6. Manual Bar Chart construction (since BarChart is undefined)
        # Create 20 bar rectangles. One is high (index 3), others are low.
        bar_vals = [0.1] * 20
        bar_vals[3] = 2.0  # High probability for 'Plastic Bottle'
        
        bars = VGroup()
        for val in bar_vals:
            b = Rectangle(
                height=val, 
                width=0.12, 
                fill_opacity=0.8, 
                color=BLUE, 
                stroke_width=1
            )
            bars.add(b)
        
        bars.arrange(RIGHT, buff=0.08, aligned_edge=DOWN).next_to(vector_group, RIGHT, buff=1.0).shift(DOWN * 0.5)
        baseline = Line(bars.get_left(), bars.get_right()).align_to(bars, DOWN)
        chart_label = Text("Probabilities", font_size=20).next_to(bars, UP, buff=0.3)

        # 7. Animation Sequence
        self.play(FadeIn(bottle_image))
        self.wait(0.5)
        
        self.play(Create(arrow1), Create(cnn_layers), Write(layer_label))
        self.wait(0.5)
        
        self.play(
            Create(arrow2),
            FadeIn(bracket_left),
            FadeIn(bracket_right),
            LaggedStart(*[Write(score) for score in raw_scores_vgroup], lag_ratio=0.1),
            Write(vector_label)
        )
        self.wait(1)

        self.play(Write(softmax_formula))
        self.wait(1)

        # Transforming values into a distribution
        self.play(
            Create(baseline),
            LaggedStart(*[FadeIn(b, shift=UP*0.2) for b in bars], lag_ratio=0.05),
            Write(chart_label)
        )
        self.wait(1)

        # 8. Indicate highest bar and label it
        highest_bar = bars[3]
        self.play(Indicate(highest_bar, color=GREEN))
        
        result_text = Text("Plastic Bottle", color=GREEN, font_size=24).next_to(highest_bar, UP, buff=0.4)
        self.play(Write(result_text))
        
        self.wait(3)