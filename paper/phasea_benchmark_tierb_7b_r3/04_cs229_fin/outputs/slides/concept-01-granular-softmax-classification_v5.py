from manim import *

class SoftmaxExplanation(Scene):
    def construct(self):
        # 1. Plastic bottle image (input) on the left
        # We use a placeholder rectangle for the input image to ensure reliability
        bottle_image = VGroup(
            RoundedRectangle(corner_radius=0.1, height=2.5, width=1.5, color=BLUE, fill_opacity=0.1),
            Text("Input Image", font_size=18)
        )
        bottle_image.to_edge(LEFT, buff=0.5)

        # 2. CNN layers (series of vertical rectangles)
        cnn_layers = VGroup(*[
            Rectangle(height=2.5 - i*0.4, width=0.4, fill_opacity=0.2, color=WHITE)
            for i in range(3)
        ]).arrange(RIGHT, buff=0.2).next_to(bottle_image, RIGHT, buff=0.8)
        
        cnn_text = Text("CNN Layers", font_size=20).next_to(cnn_layers, UP)
        arrow1 = Arrow(bottle_image.get_right(), cnn_layers.get_left(), buff=0.1)

        # 3. Column vector of 20 raw values (MathTex labeled x_i)
        raw_vector = MathTex(
            r"\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_{20} \end{bmatrix}",
            font_size=32
        ).next_to(cnn_layers, RIGHT, buff=0.8)
        
        arrow2 = Arrow(cnn_layers.get_right(), raw_vector.get_left(), buff=0.1)

        # Display CNN data flow
        self.play(FadeIn(bottle_image))
        self.play(Create(cnn_layers), Write(cnn_text), GrowArrow(arrow1))
        self.play(Write(raw_vector), GrowArrow(arrow2))
        self.wait(1)

        # 4. Softmax formula appearing
        softmax_formula = MathTex(
            r"\text{softmax}(x_{i})=\frac{e^{x_{i}}}{\sum_{j=1}^{n}e^{x_{j}}}",
            font_size=36
        ).to_edge(UP, buff=0.5)
        
        self.play(Write(softmax_formula))
        self.wait(1)

        # 5. Manual Bar Chart construction (to avoid disallowed Axes/BarChart)
        chart_origin = RIGHT * 2 + DOWN * 2
        y_axis = Line(chart_origin, chart_origin + UP * 4, color=WHITE)
        x_axis = Line(chart_origin, chart_origin + RIGHT * 4, color=WHITE)
        
        # Probabilities for 20 categories (simplified for visual clarity)
        # Plastic Bottle at index 3 is high
        probs = [0.05, 0.02, 0.03, 0.85, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
        bars = VGroup()
        for i, p in enumerate(probs):
            bar_height = p * 3.5
            bar = Rectangle(
                width=0.2,
                height=bar_height,
                fill_color=BLUE,
                fill_opacity=0.8,
                stroke_width=1
            )
            bar.move_to(chart_origin + RIGHT * (0.4 * i + 0.3), aligned_edge=DOWN)
            bars.add(bar)

        # Animate the transition
        self.play(
            VGroup(bottle_image, cnn_layers, cnn_text, arrow1, arrow2).animate.scale(0.6).to_edge(LEFT, buff=0.3),
            ReplacementTransform(raw_vector, bars),
            Create(y_axis),
            Create(x_axis),
            softmax_formula.animate.scale(0.8).shift(LEFT * 1.5)
        )

        # 6. Indicate the highest bar and label it 'Plastic Bottle'
        max_bar = bars[3]
        self.play(Indicate(max_bar, color=YELLOW))
        
        label = Text("Plastic Bottle", font_size=20, color=YELLOW).next_to(max_bar, UP, buff=0.1)
        self.play(Write(label))

        self.wait(3)