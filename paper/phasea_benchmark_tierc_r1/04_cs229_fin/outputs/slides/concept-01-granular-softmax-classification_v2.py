from manim import *

class Concept01GranularSoftmaxClassification(Scene):
    def construct(self):
        # 1. Input Image of a plastic bottle
        # We use ImageMobject as specified in the prompt
        try:
            bottle = ImageMobject("img-12.jpeg").scale(1.2).to_edge(LEFT, buff=0.5)
        except:
            # Fallback if the image file is not found
            bottle = Rectangle(height=2.5, width=1.8, color=BLUE).set_fill(BLUE, opacity=0.3).to_edge(LEFT, buff=0.5)
            bottle_label = Text("Plastic Bottle", font_size=20).move_to(bottle)
            bottle.add(bottle_label)
        
        # 2. CNN Layers: Series of vertical rectangles
        layer_labels = ["Conv", "Pool", "Conv", "Pool", "FC"]
        cnn_layers = VGroup()
        for label in layer_labels:
            rect = Rectangle(height=2.5, width=0.7, color=WHITE).set_fill(WHITE, opacity=0.1)
            txt = Text(label, font_size=16).rotate(90 * DEGREES)
            cnn_layers.add(VGroup(rect, txt))
        cnn_layers.arrange(RIGHT, buff=0.3).next_to(bottle, RIGHT, buff=0.8)
        
        # 3. Arrows showing data flow
        arrow_to_cnn = Arrow(bottle.get_right(), cnn_layers.get_left(), buff=0.1)
        
        # 4. Column vector of 20 raw values (x_i)
        # Using a vertical group to represent the vector of scores
        vector_elements = VGroup(*[MathTex(f"x_{{{i}}}") for i in range(1, 6)])
        vector_elements.add(MathTex(r"\vdots"))
        vector_elements.add(MathTex(r"x_{20}"))
        vector_elements.arrange(DOWN, buff=0.15)
        vector_box = SurroundingRectangle(vector_elements, buff=0.2, color=GRAY_A)
        vector_label = MathTex("x_i").next_to(vector_box, UP, buff=0.2)
        vector_group = VGroup(vector_elements, vector_box, vector_label).next_to(cnn_layers, RIGHT, buff=0.8)
        
        arrow_to_vec = Arrow(cnn_layers.get_right(), vector_group.get_left(), buff=0.1)
        
        # Animation sequence
        self.play(FadeIn(bottle))
        self.play(Create(cnn_layers), GrowArrow(arrow_to_cnn))
        self.play(Create(vector_group), GrowArrow(arrow_to_vec))
        self.wait(1)
        
        # 5. Softmax formula appearing at the top
        formula = MathTex(
            r"softmax(x_{i})=\frac{e^{x_{i}}}{\sum_{j=1}^{n}e^{x_{j}}}",
            color=YELLOW
        ).to_edge(UP, buff=0.5)
        self.play(Write(formula))
        self.wait(1)
        
        # 6. Horizontal Bar Chart (Probability Distribution)
        # We manually construct a horizontal chart using Axes for precision
        axes = Axes(
            x_range=[0, 1, 0.5],
            y_range=[0, 20, 1],
            x_length=3,
            y_length=5,
            tips=False,
            axis_config={"include_numbers": False, "stroke_opacity": 0.5}
        ).next_to(vector_group, RIGHT, buff=1.2)
        
        bars = VGroup()
        for i in range(20):
            # Index 15 represents the "Plastic Bottle" category with high probability
            prob_val = 0.88 if i == 15 else (0.02 if i % 2 == 0 else 0.05)
            bar = Rectangle(
                width=prob_val * 2.8, # Scale width to the axes
                height=0.15,
                fill_opacity=0.8,
                fill_color=GREEN if i == 15 else BLUE,
                stroke_width=0.5
            )
            bar.align_to(axes.c2p(0, i, 0), LEFT)
            bars.add(bar)
        
        # Transform the vector group into the bars to represent calculation
        self.play(
            ReplacementTransform(vector_group.copy(), bars),
            Create(axes)
        )
        self.wait(1)
        
        # 7. Indicate the highest bar and label it "Plastic Bottle"
        self.play(Indicate(bars[15], color=GREEN, scale_factor=1.2))
        label_max = Text("Plastic Bottle", color=GREEN, font_size=20).next_to(bars[15], RIGHT, buff=0.2)
        self.play(Write(label_max))
        
        # Final Title
        title = Text("Deep CNN + Softmax Classification", font_size=24, color=WHITE).to_edge(DOWN)
        self.play(FadeIn(title))
        self.wait(2)