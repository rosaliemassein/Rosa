from manim import *

class ConceptZeroShotClassification(Scene):
    def construct(self):
        # 1. Image Vector Representation
        v_rect = Rectangle(width=0.6, height=3, color=YELLOW, fill_opacity=0.3)
        v_label = MathTex(r"\mathbf{v}", color=YELLOW).next_to(v_rect, DOWN)
        v_group = VGroup(v_rect, v_label).to_edge(LEFT, buff=1)
        v_title = Text("Image Vector", font_size=20).next_to(v_rect, UP)

        # 2. Matrix X (Text Embeddings)
        x_box = Rectangle(width=2.5, height=4, color=BLUE, fill_opacity=0.1)
        x_label = MathTex(r"\mathbf{X}", color=BLUE).move_to(x_box)
        
        # Representative rows for countries
        row_count = 5
        rows = VGroup(*[
            Line(
                x_box.get_left() + RIGHT*0.2 + UP*(1.4 - i*0.7), 
                x_box.get_right() - RIGHT*0.2 + UP*(1.4 - i*0.7), 
                stroke_width=2, color=BLUE
            )
            for i in range(row_count)
        ])
        
        country_names = ["USA", "Canada", "France", "UK", "Germany"]
        c_labels = VGroup(*[
            Text(country_names[i], font_size=16).next_to(rows[i], LEFT, buff=0.2)
            for i in range(row_count)
        ])
        
        x_group = VGroup(x_box, x_label, rows, c_labels).next_to(v_group, RIGHT, buff=1.5)
        x_title = Text("Country Embeddings", font_size=20).next_to(x_box, UP)

        # 3. Formula
        formula = MathTex(
            r"h(\mathbf{v};\mathbf{X})=\frac{\exp(\mathbf{X}\mathbf{v})}{\sum_{j=1}^{N}\exp(\mathbf{X}_{j}^{T}\mathbf{v})}",
            font_size=36
        ).to_edge(UP, buff=0.5)

        # 4. Manual Bar Chart (to avoid Axes issues)
        chart_origin = RIGHT * 4.5 + DOWN * 1.5
        x_axis = Line(chart_origin, chart_origin + RIGHT * 3, color=WHITE)
        y_axis = Line(chart_origin, chart_origin + UP * 3, color=WHITE)
        chart_title = Text("Softmax Probabilities", font_size=18).next_to(y_axis, UP)
        
        # Labels for the bars
        bar_labels = VGroup(*[
            Text(country_names[i], font_size=12).move_to(chart_origin + RIGHT * (0.4 + i*0.6) + DOWN * 0.3)
            for i in range(5)
        ])
        
        # Initial flat bars
        bars = VGroup(*[
            Rectangle(width=0.4, height=0.1, color=BLUE, fill_opacity=0.6)
            .move_to(chart_origin + RIGHT * (0.4 + i*0.6), aligned_edge=DOWN)
            for i in range(5)
        ])

        # --- Animations ---

        # Phase 1: Show Vector and Matrix
        self.play(Create(v_group), Write(v_title))
        self.play(Create(x_group), Write(x_title))
        self.play(Write(formula))
        self.wait(1)

        # Phase 2: Dot Product Pulsing
        # Instead of 140, we do a few key ones to demonstrate
        highlight = Rectangle(width=2.7, height=0.4, color=RED, stroke_width=4).move_to(rows[0])
        self.play(FadeIn(highlight))
        
        # Pulse through some rows
        for i in [1, 2]:
            self.play(highlight.animate.move_to(rows[i]), run_time=0.4)
        
        # Phase 3: Transformation to Probabilities
        self.play(Create(x_axis), Create(y_axis), Write(chart_title), Write(bar_labels))
        self.play(Create(bars))
        self.wait(0.5)

        # Softmax result: France (index 2) shoots up
        # We define new rectangles with specific heights
        new_heights = [0.3, 0.4, 2.6, 0.5, 0.2]
        new_bars = VGroup()
        for i in range(5):
            nb = Rectangle(
                width=0.4, 
                height=new_heights[i], 
                color=RED if i == 2 else BLUE, 
                fill_opacity=0.8
            ).move_to(chart_origin + RIGHT * (0.4 + i*0.6), aligned_edge=DOWN)
            new_bars.add(nb)

        # Transform dot product pulse into the probability update
        self.play(
            Transform(bars, new_bars),
            highlight.animate.scale(1.1).set_color(RED),
            run_time=1.5
        )

        # Final prediction highlight
        prediction_text = Text("Prediction: France", color=RED, font_size=24).next_to(formula, DOWN, buff=0.3)
        self.play(
            Write(prediction_text),
            Indicate(bar_labels[2], color=RED),
            Indicate(c_labels[2], color=RED)
        )
        
        self.wait(2)