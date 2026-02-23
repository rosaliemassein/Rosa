from manim import *

class GranularSoftmaxClassification(Scene):
    def construct(self):
        # 1. Image of a plastic bottle (Represented by a labeled rectangle for portability)
        bottle_rect = Rectangle(height=3, width=2.2, color=GRAY)
        bottle_label = Text("Plastic Bottle\n(Input)", font_size=20).move_to(bottle_rect)
        bottle_group = VGroup(bottle_rect, bottle_label).to_edge(LEFT, buff=0.5)

        # 2. CNN layers (Vertical rectangles)
        cnn_layers = VGroup(*[
            Rectangle(height=2.5, width=0.4, fill_opacity=0.7, color=BLUE)
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.4).next_to(bottle_group, RIGHT, buff=0.8)
        
        cnn_title = Text("Deep CNN", font_size=24).next_to(cnn_layers, UP)
        arrow_in = Arrow(bottle_group.get_right(), cnn_layers.get_left(), buff=0.1)

        # 3. Column vector of raw values (x_i)
        vector_box = Rectangle(height=4.5, width=1.0, color=WHITE).next_to(cnn_layers, RIGHT, buff=0.8)
        vector_items = VGroup(*[
            MathTex(f"x_{{{i}}}") for i in range(1, 4)
        ] + [MathTex(r"\vdots")] + [MathTex(r"x_{20}")])
        vector_items.arrange(DOWN, buff=0.3).move_to(vector_box)
        vector_title = MathTex(r"x_i").next_to(vector_box, UP)
        
        arrow_to_vec = Arrow(cnn_layers.get_right(), vector_box.get_left(), buff=0.1)

        # Initial Animation
        self.play(FadeIn(bottle_group))
        self.play(Create(cnn_layers), Write(cnn_title), Create(arrow_in))
        self.play(Create(vector_box), Write(vector_items), Write(vector_title), Create(arrow_to_vec))
        self.wait(1)

        # 4. Softmax Formula
        softmax_formula = MathTex(
            r"\text{softmax}(x_{i}) = \frac{e^{x_{i}}}{\sum_{j=1}^{20} e^{x_{j}}}"
        ).scale(0.8).to_edge(UP, buff=0.5).shift(RIGHT * 3)
        
        self.play(Write(softmax_formula))
        self.wait(1)

        # 5. Transform raw values into a horizontal BarChart (Probabilities)
        # Using a representative subset of the 20 categories
        probs = [0.08, 0.12, 0.65, 0.05, 0.03, 0.07] 
        bars = VGroup()
        for p in probs:
            # Create a bar where width is proportional to probability
            bar = Rectangle(width=p * 4.0 + 0.1, height=0.35, fill_opacity=0.8, color=BLUE)
            bars.add(bar)
        
        bars.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        bars.next_to(vector_box, RIGHT, buff=1.8)
        
        # Highlight the highest probability bar
        bars[2].set_color(GREEN)
        
        chart_title = Text("Probabilities", font_size=24).next_to(bars, UP)

        # Animation: Data flowing from vector to probabilities
        self.play(Write(chart_title))
        self.play(
            LaggedStart(*[
                ReplacementTransform(vector_items[min(i, 2)].copy(), bars[i])
                for i in range(len(probs))
            ], run_time=2)
        )
        self.wait(1)

        # 6. Indicate highest bar and label 'Plastic Bottle'
        self.play(Indicate(bars[2], color=YELLOW))
        
        bottle_result = Text("Plastic Bottle", color=YELLOW, font_size=28).next_to(bars[2], RIGHT, buff=0.3)
        self.play(Write(bottle_result))
        self.wait(2)

        # Final Scene Exit
        all_elements = VGroup(
            bottle_group, cnn_layers, cnn_title, arrow_in, 
            vector_box, vector_items, vector_title, arrow_to_vec,
            softmax_formula, bars, chart_title, bottle_result
        )
        self.play(FadeOut(all_elements))
        self.wait(1)