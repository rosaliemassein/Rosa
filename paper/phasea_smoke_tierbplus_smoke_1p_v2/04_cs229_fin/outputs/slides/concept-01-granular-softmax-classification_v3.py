from manim import *

class Concept01GranularSoftmaxClassification(Scene):
    def construct(self):
        # 1. Left side: Input Image (Simulated plastic bottle image)
        input_image_rect = RoundedRectangle(corner_radius=0.1, height=2.5, width=2, color=WHITE)
        input_label = Text("Plastic Bottle\n(Input)", font_size=18).move_to(input_image_rect)
        input_group = VGroup(input_image_rect, input_label).to_edge(LEFT, buff=0.5)
        
        # 2. CNN Layers: Series of vertical rectangles
        cnn_layers = VGroup(*[
            Rectangle(width=0.15, height=1.2 + (i * 0.15), fill_opacity=0.5, color=BLUE)
            for i in range(5)
        ]).arrange(RIGHT, buff=0.15).next_to(input_group, RIGHT, buff=0.6)
        
        cnn_text = Text("CNN Layers", font_size=16).next_to(cnn_layers, UP, buff=0.2)
        
        # Data flow arrows
        arrow1 = Arrow(input_group.get_right(), cnn_layers.get_left(), buff=0.1, max_tip_length_to_length_ratio=0.2)
        
        # 3. Column vector of 20 raw values (x_i)
        raw_vector = MathTex(
            r"x_i = \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_{20} \end{bmatrix}",
            font_size=30
        ).next_to(cnn_layers, RIGHT, buff=0.6)
        
        arrow2 = Arrow(cnn_layers.get_right(), raw_vector.get_left(), buff=0.1, max_tip_length_to_length_ratio=0.2)

        # Initial Animation Sequence
        self.play(FadeIn(input_group))
        self.play(Create(arrow1), Create(cnn_layers), Write(cnn_text))
        self.play(Create(arrow2), Write(raw_vector))
        self.wait(1)

        # 4. Softmax formula appearing
        softmax_formula = MathTex(
            r"\text{softmax}(x_{i}) = \frac{e^{x_{i}}}{\sum_{j=1}^{n}e^{x_{j}}}",
            font_size=36
        ).to_edge(UP, buff=0.5)
        
        self.play(Write(softmax_formula))
        self.wait(1)

        # 5. Transform raw values into a Bar Chart
        # Since 'BarChart' was reported as undefined, we build it manually using Axes and Rectangles
        axes = Axes(
            x_range=[0, 20, 1],
            y_range=[0, 1.1, 0.5],
            x_length=5,
            y_length=2.5,
            axis_config={"include_tip": False}
        ).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.5)
        
        # Define probabilities (index 12 is the plastic bottle)
        probs = [0.03] * 20
        probs[12] = 0.85
        
        bars = VGroup()
        for i, p in enumerate(probs):
            # Calculate height relative to axes
            bar_height = p * (axes.y_length / 1.1)
            bar = Rectangle(
                width=(axes.x_length / 20) * 0.7,
                height=bar_height,
                fill_color=BLUE,
                fill_opacity=0.8,
                stroke_width=1,
                color=BLUE
            )
            bar.move_to(axes.c2p(i + 0.5, 0), aligned_edge=DOWN)
            bars.add(bar)
            
        chart_group = VGroup(axes, bars)

        # Move previous elements to make room
        left_elements = VGroup(input_group, cnn_layers, cnn_text, arrow1, arrow2, raw_vector)
        
        self.play(
            left_elements.animate.scale(0.6).to_edge(LEFT, buff=0.3),
            FadeIn(axes),
            LaggedStart(*[FadeIn(b, shift=UP*0.2) for b in bars], lag_ratio=0.05)
        )
        
        # 6. Indicate the highest bar and label it 'Plastic Bottle'
        winning_bar = bars[12]
        self.play(Indicate(winning_bar, color=YELLOW, scale_factor=1.2))
        
        label = Text("Plastic Bottle", color=YELLOW, font_size=20).next_to(winning_bar, UP, buff=0.1)
        self.play(Write(label))
        
        self.wait(2)