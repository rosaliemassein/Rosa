import numpy as np
from manim import *

class GranularSoftmaxClassification(Scene):
    def construct(self):
        # 1. Input Image Section
        try:
            bottle = ImageMobject("img-12.jpeg").scale(1.2)
        except:
            # Fallback if image is missing
            bottle_rect = Rectangle(height=2, width=1.5, color=BLUE).set_fill(BLUE, opacity=0.3)
            bottle_text = Text("Plastic Bottle", font_size=18).move_to(bottle_rect)
            bottle = Group(bottle_rect, bottle_text)
            
        bottle.to_edge(LEFT, buff=0.5).shift(UP * 0.5)
        bottle_label = Text("Input", font_size=24).next_to(bottle, UP)

        # 2. CNN Layers
        # Using standard colors instead of BLUE_A/B/C/D
        cnn_layers = VGroup()
        for i in range(3):
            layer = Rectangle(height=3 - i*0.5, width=0.4, color=BLUE)
            layer.set_fill(BLUE, opacity=0.4 + i*0.2)
            cnn_layers.add(layer)
        cnn_layers.arrange(RIGHT, buff=0.2).next_to(bottle, RIGHT, buff=0.8)
        cnn_label = Text("CNN Layers", font_size=20).next_to(cnn_layers, UP)

        # 3. Data Flow Arrows
        arrow1 = Arrow(bottle.get_right(), cnn_layers.get_left(), buff=0.1)

        # 4. Raw Values Column Vector
        # We represent the 20 values compactly
        raw_scores_tex = MathTex(
            r"x = \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_{10} \\ \vdots \\ x_{20} \end{bmatrix}",
            font_size=34
        ).next_to(cnn_layers, RIGHT, buff=0.8)
        
        arrow2 = Arrow(cnn_layers.get_right(), raw_scores_tex.get_left(), buff=0.1)

        # 5. Softmax Formula
        formula = MathTex(
            r"softmax(x_{i}) = \frac{e^{x_{i}}}{\sum_{j=1}^{20}e^{x_{j}}}",
            font_size=36
        ).to_edge(UP, buff=0.3)

        # 6. Manual Bar Chart (Replacing disallowed Axes)
        chart_origin = RIGHT * 2.5 + DOWN * 2.5
        y_axis = Line(chart_origin, chart_origin + UP * 4.5, color=WHITE)
        x_axis = Line(chart_origin, chart_origin + RIGHT * 3.5, color=WHITE)
        chart_label = Text("Probabilities", font_size=20).next_to(x_axis, DOWN)

        bars = VGroup()
        # Seed for reproducibility if needed, but np is imported now
        np.random.seed(42)
        for i in range(20):
            # We'll make the 13th bar (index 12) the "winner"
            is_winner = (i == 12)
            bar_width = 3.0 if is_winner else np.random.uniform(0.1, 0.7)
            bar_height = 0.15
            
            bar = Rectangle(
                width=bar_width,
                height=bar_height,
                stroke_width=1,
                fill_opacity=0.8
            )
            bar.set_fill(YELLOW if is_winner else BLUE)
            # Position relative to manual axis
            bar.align_to(chart_origin, LEFT)
            bar.shift(UP * (i * 0.22 + 0.1))
            bars.add(bar)

        winner_label = Text("Plastic Bottle", color=YELLOW, font_size=22).next_to(bars[12], RIGHT, buff=0.2)

        # ANIMATION SEQUENCE
        self.play(FadeIn(bottle), Write(bottle_label))
        self.play(GrowArrow(arrow1))
        self.play(Create(cnn_layers), Write(cnn_label))
        self.wait(0.5)

        self.play(GrowArrow(arrow2))
        self.play(Write(raw_scores_tex))
        self.wait(1)

        self.play(Write(formula))
        self.wait(1)

        # Transform raw values into Bar Chart
        self.play(Create(y_axis), Create(x_axis), Write(chart_label))
        # Using Create instead of GrowFromEdge as it was reported undefined
        self.play(
            LaggedStart(*[Create(b) for b in bars], lag_ratio=0.05),
            run_time=2
        )
        self.wait(1)

        # Indicate the highest bar
        self.play(Indicate(bars[12], color=YELLOW, scale_factor=1.2))
        self.play(Write(winner_label))
        self.wait(2)

        # Final cleanup/pause
        self.play(Indicate(formula, color=YELLOW))
        self.wait(3)