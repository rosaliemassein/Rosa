from manim import *

class GranularSoftmaxClassification(Scene):
    def construct(self):
        # 1. Input Image of a plastic bottle
        # Note: If 'img-12.jpeg' is not in the directory, Manim will raise an error.
        # We assume the file exists as per the prompt instructions.
        try:
            bottle = ImageMobject("img-12.jpeg")
        except:
            # Fallback for local testing if image is missing
            bottle = RoundedRectangle(height=3, width=1.5, color=WHITE, fill_opacity=0.2)
            bottle.add(Text("Plastic Bottle", font_size=15).rotate(90*DEGREES))
            
        bottle.scale(0.7).to_edge(LEFT, buff=0.5)
        self.add(bottle)

        # 2. CNN Layers
        # Draw a series of vertical rectangles representing CNN layers
        cnn_layers = VGroup(*[
            Rectangle(width=0.25, height=2.0 + (i * 0.2), color=BLUE, fill_opacity=0.3)
            for i in range(4)
        ]).arrange(RIGHT, buff=0.15).next_to(bottle, RIGHT, buff=0.7)
        
        cnn_label = Text("CNN Layers", font_size=20).next_to(cnn_layers, UP)
        
        self.play(
            Create(cnn_layers),
            Write(cnn_label),
            run_time=1.5
        )

        # 3. Column Vector of 20 Raw Values (x_i)
        # Using vector notation to represent 20 values cleanly
        raw_values = MathTex(
            r"x = \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_{20} \end{bmatrix}",
            font_size=36
        ).next_to(cnn_layers, RIGHT, buff=0.8)
        
        arrow_to_x = Arrow(cnn_layers.get_right(), raw_values.get_left(), buff=0.1)
        
        self.play(
            GrowArrow(arrow_to_x),
            Write(raw_values)
        )

        # 4. Softmax Formula
        # softmax(x_{i})=\frac{e^{x_{i}}}{\sum_{j=1}^{n}e^{x_{j}}}
        formula = MathTex(
            r"\text{softmax}(x_{i}) = \frac{e^{x_{i}}}{\sum_{j=1}^{n} e^{x_{j}}}",
            font_size=32
        ).to_edge(UP, buff=0.5).shift(RIGHT * 2)
        
        self.play(FadeIn(formula, shift=DOWN))

        # 5. Horizontal Bar Chart (Probability Distribution)
        # Creating a custom horizontal bar chart using Rectangles
        probabilities = [0.02] * 20
        probabilities[15] = 0.8  # Target index for 'Plastic Bottle'
        probabilities[4] = 0.08
        probabilities[10] = 0.05
        
        bars = VGroup()
        for p in probabilities:
            bar = Rectangle(
                width=p * 4.0 + 0.05, # Map probability to width
                height=0.12,
                fill_opacity=0.8,
                color=BLUE,
                stroke_width=1
            )
            bars.add(bar)
        
        bars.arrange(DOWN, buff=0.05, aligned_edge=LEFT)
        bars.next_to(formula, DOWN, buff=0.8).align_to(formula, LEFT)
        
        chart_title = Text("Probabilities", font_size=18).next_to(bars, UP, buff=0.2)

        # Transition: Transform the vector into the bar chart
        self.play(
            Transform(raw_values.copy(), bars),
            FadeIn(bars),
            Write(chart_title)
        )

        # 6. Indicate the highest bar and label it 'Plastic Bottle'
        highest_bar = bars[15]
        result_label = Text("Plastic Bottle", color=YELLOW, font_size=24).next_to(highest_bar, RIGHT, buff=0.3)
        
        self.play(
            Indicate(highest_bar, color=YELLOW, scale_factor=1.2),
            Create(result_label)
        )

        self.wait(3)