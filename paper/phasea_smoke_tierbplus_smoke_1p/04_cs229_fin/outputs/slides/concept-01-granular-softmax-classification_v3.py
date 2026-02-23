from manim import *

class SoftmaxAnimation(Scene):
    def construct(self):
        # 1. Input Image Placeholder (Representing the plastic bottle)
        input_box = Square(side_length=1.8, color=WHITE)
        input_label = Text("Plastic Bottle", font_size=20).move_to(input_box)
        input_group = VGroup(input_box, input_label).to_edge(LEFT, buff=0.5)

        # 2. CNN Layers (Vertical Rectangles)
        cnn_layers = VGroup(*[
            Rectangle(height=2.5, width=0.25, fill_opacity=0.7, color=BLUE)
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.15).next_to(input_group, RIGHT, buff=0.8)
        
        cnn_text = Text("CNN Layers", font_size=18).next_to(cnn_layers, UP)

        # 3. Raw values (Column Vector x_i)
        # Creating a column of 20 small segments to represent the vector
        raw_vector_elements = VGroup(*[
            Line(LEFT*0.2, RIGHT*0.2, stroke_width=2, color=RED) for _ in range(20)
        ]).arrange(DOWN, buff=0.07)
        
        vector_label = MathTex("x_i", color=RED, font_size=30).next_to(raw_vector_elements, LEFT, buff=0.1)
        bracket_l = Tex("[", font_size=100).scale(0.5).next_to(raw_vector_elements, LEFT, buff=0.05)
        bracket_r = Tex("]", font_size=100).scale(0.5).next_to(raw_vector_elements, RIGHT, buff=0.05)
        vector_group = VGroup(raw_vector_elements, vector_label, bracket_l, bracket_r).next_to(cnn_layers, RIGHT, buff=0.8)

        # 4. Data Flow Arrows
        arrow1 = Arrow(input_group.get_right(), cnn_layers.get_left(), buff=0.1, color=GRAY)
        arrow2 = Arrow(cnn_layers.get_right(), vector_group.get_left(), buff=0.1, color=GRAY)

        # 5. Softmax Formula (Top Center)
        softmax_formula = MathTex(
            r"softmax(x_{i})=\frac{e^{x_{i}}}{\sum_{j=1}^{20}e^{x_{j}}}",
            color=WHITE, font_size=36
        ).to_edge(UP, buff=0.5)

        # 6. Manually constructed Bar Chart (since BarChart identifier failed)
        # Using Axes + Rectangles for maximum compatibility
        chart_axes = Axes(
            x_range=[0, 20, 1],
            y_range=[0, 1, 0.5],
            x_length=4.5,
            y_length=2.5,
            axis_config={"include_tip": False, "stroke_width": 1},
            tips=False
        ).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.5)

        # Create bars for the chart
        bars = VGroup()
        for i in range(20):
            # One bar (index 5) is high to represent "Plastic Bottle"
            prob_height = 0.8 if i == 5 else 0.05 + (0.1 * (i % 3) / 3)
            # Create rectangle aligned to the axis
            bar = Rectangle(
                width=chart_axes.x_axis.get_unit_size() * 0.7,
                height=prob_height * chart_axes.y_axis.get_unit_size(),
                fill_opacity=0.8,
                fill_color=GREEN,
                stroke_width=1
            )
            bar.move_to(chart_axes.c2p(i + 0.5, 0), aligned_edge=DOWN)
            bars.add(bar)

        # --- ANIMATION ---

        # Step 1: Input and CNN
        self.play(FadeIn(input_group))
        self.play(Create(cnn_layers), Write(cnn_text))
        self.play(GrowArrow(arrow1))
        self.wait(0.5)

        # Step 2: Extract Features to Vector
        self.play(GrowArrow(arrow2))
        self.play(Create(bracket_l), Create(bracket_r), Create(raw_vector_elements), Write(vector_label))
        self.wait(1)

        # Step 3: Show Softmax Formula
        self.play(Write(softmax_formula))
        self.wait(1)

        # Step 4: Transform to Probabilities (Bar Chart)
        self.play(Create(chart_axes))
        # Transform the vector elements into the bars
        self.play(
            ReplacementTransform(raw_vector_elements.copy(), bars),
            run_time=2
        )
        self.wait(1)

        # Step 5: Highlight result
        winning_bar = bars[5]
        result_label = Text("Plastic Bottle", font_size=20, color=YELLOW).next_to(winning_bar, UP, buff=0.2)
        
        self.play(
            Indicate(winning_bar, color=YELLOW, scale_factor=1.3),
            Write(result_label)
        )
        self.wait(2)