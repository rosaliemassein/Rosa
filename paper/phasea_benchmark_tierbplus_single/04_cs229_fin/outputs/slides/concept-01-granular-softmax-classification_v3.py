from manim import *

class GranularSoftmax(Scene):
    def construct(self):
        # 1. Image of a plastic bottle (input) on the left
        try:
            bottle_image = ImageMobject("img-12.jpeg").scale(1.2)
        except:
            # Fallback if image not found
            bottle_image = Rectangle(height=2.5, width=2, color=GRAY, fill_opacity=0.5)
            bottle_image.add(Text("Plastic Bottle", font_size=20))
            
        bottle_image.to_edge(LEFT, buff=0.8)
        input_label = Text("Input Image", font_size=24).next_to(bottle_image, DOWN)
        self.play(FadeIn(bottle_image), Write(input_label))
        self.wait(1)

        # 2. CNN layers (series of vertical rectangles)
        cnn_layers = VGroup(*[
            Rectangle(width=0.4, height=3, color=BLUE, fill_opacity=0.3) 
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.2).next_to(bottle_image, RIGHT, buff=0.8)
        cnn_label = Text("CNN Layers", font_size=20).next_to(cnn_layers, DOWN)
        
        arrow_to_cnn = Arrow(bottle_image.get_right(), cnn_layers.get_left(), buff=0.1)
        
        self.play(
            GrowArrow(arrow_to_cnn),
            Create(cnn_layers),
            Write(cnn_label)
        )
        self.wait(1)

        # 3. Column vector of 20 raw values (MathTex labeled 'x_i')
        # We'll display a representative subset to keep the screen clean
        x_elements = VGroup(*[
            MathTex(f"x_{{{i}}}", font_size=18) for i in range(1, 11)
        ])
        dots = MathTex(r"\vdots", font_size=18)
        x_elements.add(dots)
        x_elements.add(MathTex(f"x_{{20}}", font_size=18))
        x_elements.arrange(DOWN, buff=0.1)
        
        bracket_l = MathTex(r"\left[", font_size=40).scale(2.2).next_to(x_elements, LEFT, buff=0.1)
        bracket_r = MathTex(r"\right]", font_size=40).scale(2.2).next_to(x_elements, RIGHT, buff=0.1)
        raw_vector = VGroup(bracket_l, x_elements, bracket_r).scale(0.8).next_to(cnn_layers, RIGHT, buff=0.8)
        
        vector_label = MathTex("x_i", font_size=30).next_to(raw_vector, UP)
        arrow_to_vector = Arrow(cnn_layers.get_right(), raw_vector.get_left(), buff=0.1)

        self.play(
            GrowArrow(arrow_to_vector),
            FadeIn(raw_vector),
            Write(vector_label)
        )
        self.wait(1)

        # 4. Softmax formula appearing at the top
        softmax_formula = MathTex(
            r"\text{softmax}(x_{i}) = \frac{e^{x_{i}}}{\sum_{j=1}^{20} e^{x_{j}}}",
            font_size=36
        ).to_edge(UP, buff=0.5)
        self.play(Write(softmax_formula))
        self.wait(1)

        # 5. Transform raw values into a horizontal BarChart (manual construction)
        # Using a VGroup of rectangles to avoid BarChart identifier issues
        bar_height = 0.15
        spacing = 0.08
        probabilities = [0.05, 0.02, 0.03, 0.04, 0.75, 0.01, 0.02, 0.01, 0.03, 0.04] # simplified to 10 for visual clarity
        
        bars = VGroup()
        for i, p in enumerate(probabilities):
            color = YELLOW if i == 4 else BLUE
            bar = Rectangle(
                height=bar_height, 
                width=p * 4, 
                color=color, 
                fill_opacity=0.8, 
                stroke_width=1
            )
            bar.align_to(ORIGIN, LEFT)
            bars.add(bar)
            
        bars.arrange(DOWN, buff=spacing, center=False).shift(RIGHT * 3 + DOWN * 0.5)
        
        # Axis for the chart
        y_axis = Line(bars.get_top() + UP*0.1, bars.get_bottom() + DOWN*0.1).align_to(bars, LEFT)
        x_axis = Line(bars.get_bottom(), bars.get_bottom() + RIGHT*4)
        chart_group = VGroup(y_axis, x_axis, bars)
        chart_title = Text("Probabilities", font_size=20).next_to(chart_group, UP)

        self.play(
            FadeOut(raw_vector),
            FadeOut(arrow_to_vector),
            FadeOut(vector_label),
            FadeOut(cnn_layers),
            FadeOut(cnn_label),
            FadeOut(arrow_to_cnn),
            Create(y_axis),
            Create(x_axis),
            Write(chart_title),
            LaggedStart(*[Create(b) for b in bars], lr_speed=2)
        )
        self.wait(1)

        # 6. Indicate the highest bar and label it 'Plastic Bottle'
        highest_bar = bars[4]
        self.play(Indicate(highest_bar, scale_factor=1.2))
        
        winner_label = Text("Plastic Bottle (High Confidence)", color=YELLOW, font_size=24).next_to(highest_bar, RIGHT, buff=0.3)
        self.play(Write(winner_label))
        
        self.wait(2)