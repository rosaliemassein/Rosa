from manim import *

class GranularSoftmaxClassification(Scene):
    def construct(self):
        # 1. Image of a plastic bottle (Input) on the left
        # We use a placeholder if the image file is not found
        try:
            bottle_image = ImageMobject("img-12.jpeg").scale(1.2)
        except:
            bottle_image = VGroup(
                Rectangle(height=3, width=1.5, color=GRAY),
                Text("Bottle", font_size=20)
            )
        
        bottle_image.to_edge(LEFT, buff=0.5)
        
        # 2. CNN Layers (Vertical rectangles)
        cnn_layers = VGroup(*[
            Rectangle(height=2.0, width=0.2, fill_opacity=0.7, color=BLUE, stroke_width=2) 
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.15).next_to(bottle_image, RIGHT, buff=0.7)
        
        cnn_label = Text("Deep CNN", font_size=18).next_to(cnn_layers, UP)

        # 3. Arrow for data flow
        arrow1 = Arrow(bottle_image.get_right(), cnn_layers.get_left(), buff=0.1)

        # 4. Column vector of 20 raw values (x_i)
        # Representing 20 values with a truncated matrix
        raw_vector = MathTex(
            r"x_i = \begin{bmatrix} 2.4 \\ 1.1 \\ \vdots \\ -0.5 \end{bmatrix}",
            font_size=32
        ).next_to(cnn_layers, RIGHT, buff=0.7)
        
        arrow2 = Arrow(cnn_layers.get_right(), raw_vector.get_left(), buff=0.1)

        # 5. Softmax Formula appearing at the top
        softmax_formula = MathTex(
            r"\text{softmax}(x_{i})=\frac{e^{x_{i}}}{\sum_{j=1}^{n}e^{x_{j}}}",
            font_size=34
        ).to_edge(UP, buff=0.4)

        # 6. Manual Bar Chart for probabilities (replacing BarChart class for compatibility)
        # Heights represent probabilities
        prob_data = [
            0.05, 0.02, 0.08, 0.03, 0.04, 0.02, 0.03, 0.65, 0.01, 0.01, 
            0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01
        ]
        
        # We'll build the bars manually using Rectangles
        bars = VGroup()
        for p in prob_data:
            bar = Rectangle(
                height=p * 3.5 + 0.01, # scaled height
                width=0.15,
                fill_opacity=0.8,
                fill_color=BLUE,
                stroke_width=1
            )
            bars.add(bar)
        
        bars.arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
        bars.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.5)

        # Label for the highest bar
        highest_bar = bars[7] # index 7 corresponds to 0.65
        result_label = Text("Plastic Bottle", font_size=20, color=YELLOW).next_to(highest_bar, UP, buff=0.2)
        
        # x-axis for the chart
        x_axis = Line(bars.get_left(), bars.get_right(), color=WHITE).next_to(bars, DOWN, buff=0)

        # --- ANIMATION SEQUENCE ---
        
        # Step 1: Input and CNN
        self.play(FadeIn(bottle_image))
        self.play(Create(cnn_layers), Write(cnn_label))
        self.play(Create(arrow1))
        self.wait(0.5)

        # Step 2: Extract raw scores (x_i)
        self.play(Create(arrow2))
        self.play(Write(raw_vector))
        self.wait(1)

        # Step 3: Introduce Softmax Formula
        self.play(Write(softmax_formula))
        self.wait(1)

        # Step 4: Transform raw values into the bar chart
        self.play(
            FadeOut(raw_vector),
            FadeOut(arrow2),
            Create(x_axis),
            Create(bars),
            run_time=2
        )
        
        # Step 5: Indicate the most likely material
        self.play(
            Indicate(highest_bar, color=YELLOW),
            Write(result_label)
        )
        
        self.wait(2)