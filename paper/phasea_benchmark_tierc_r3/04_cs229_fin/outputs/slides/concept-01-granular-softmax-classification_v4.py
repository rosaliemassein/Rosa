from manim import *

class GranularSoftmaxClassification(Scene):
    def construct(self):
        # 1. Input Image on the left
        try:
            # Attempt to load the referenced image
            input_image = ImageMobject("img-12.jpeg").scale(1.2).to_edge(LEFT, buff=0.5)
        except:
            # Fallback if image file is not found
            input_image = RoundedRectangle(height=2, width=1.5, color=BLUE, fill_opacity=0.3).to_edge(LEFT, buff=0.5)
            input_image.add(Text("Plastic Bottle", font_size=16).move_to(input_image))
            
        img_label = Text("Input Image", font_size=20).next_to(input_image, DOWN)

        # 2. CNN Layers (Represented as vertical rectangles)
        cnn_layers = VGroup(*[
            Rectangle(width=0.4, height=2.0 - i*0.4, fill_opacity=0.5, color=WHITE)
            for i in range(3)
        ]).arrange(RIGHT, buff=0.2).next_to(input_image, RIGHT, buff=0.8)

        # 3. Data flow arrows
        arrow1 = Arrow(input_image.get_right(), cnn_layers.get_left(), buff=0.1)

        # 4. Raw scores (MathTex labeled 'x_i' as a column vector)
        raw_scores = MathTex(r"x_i = \begin{bmatrix} 2.3 \\ 0.5 \\ \vdots \\ -1.2 \end{bmatrix}", font_size=36)
        raw_scores.next_to(cnn_layers, RIGHT, buff=0.8)
        arrow2 = Arrow(cnn_layers.get_right(), raw_scores.get_left(), buff=0.1)

        # 5. Softmax formula appearing at the top
        softmax_formula = MathTex(
            r"softmax(x_{i}) = \frac{e^{x_{i}}}{\sum_{j=1}^{n} e^{x_{j}}}",
            font_size=34
        ).to_edge(UP, buff=0.5)

        # 6. Horizontal Bar Chart (Probabilities for 20 categories)
        # Visualizing a subset for clarity while maintaining the '20 categories' concept
        probs = [0.03, 0.02, 0.05, 0.75, 0.02, 0.01, 0.02, 0.03, 0.01, 0.04, 0.02]
        bars = VGroup(*[
            Rectangle(height=0.2, width=p*5, fill_opacity=0.8, color=BLUE)
            for p in probs
        ]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        
        bars.to_edge(RIGHT, buff=1.2).shift(DOWN*0.5)
        
        # Label the highest bar (index 3 corresponds to 0.75 probability)
        highest_bar = bars[3]
        highest_bar.set_color(YELLOW)
        bar_label = Text("Plastic Bottle", font_size=24, color=YELLOW).next_to(highest_bar, RIGHT, buff=0.3)

        # --- Animation Sequence ---
        # Show input and CNN layers
        self.play(FadeIn(input_image), Write(img_label))
        self.play(Create(arrow1), Create(cnn_layers))
        self.wait(1)
        
        # Show data flowing into raw vector
        self.play(Create(arrow2), Write(raw_scores))
        self.wait(1)
        
        # Show Softmax formula
        self.play(Write(softmax_formula))
        self.wait(1.5)
        
        # Transform/Transition into probability bar chart
        self.play(
            FadeOut(raw_scores),
            FadeOut(arrow2),
            Create(bars),
            run_time=2
        )
        self.wait(1)
        
        # Indicate the most likely material as specified in remarks
        self.play(Indicate(highest_bar, scale_factor=1.1, color=YELLOW))
        self.play(Write(bar_label))
        self.wait(3)