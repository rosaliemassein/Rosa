from manim import *

class ZeroShotClassifier(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = "#F8EBCD"
        text_color = BLACK

        # 1. Define image vector 'v'
        v_label = MathTex(r"\mathbf{v}", color=text_color).shift(LEFT * 5 + UP * 1.5)
        v_rect = Rectangle(width=0.6, height=3, color=BLUE, fill_opacity=0.6)
        v_rect.next_to(v_label, DOWN)
        v_group = VGroup(v_label, v_rect)

        # 2. Define Matrix 'X' with country names
        X_label = MathTex(r"\mathbf{X}", color=text_color).shift(LEFT * 2 + UP * 1.5)
        countries = ["France", "Germany", "Italy", "Japan", "Brazil"]
        X_rows = VGroup()
        for name in countries:
            row_bg = Rectangle(width=3, height=0.5, color=GREEN, fill_opacity=0.2)
            row_text = Text(name, font_size=20, color=text_color)
            row = VGroup(row_bg, row_text)
            X_rows.add(row)
        X_rows.arrange(DOWN, buff=0.1).next_to(X_label, DOWN)
        X_group = VGroup(X_label, X_rows)

        # 3. Manual Bar Chart construction (replacing Axes)
        chart_origin = RIGHT * 2 + DOWN * 1.5
        x_axis = Line(chart_origin, chart_origin + RIGHT * 4, color=text_color)
        y_axis = Line(chart_origin, chart_origin + UP * 3, color=text_color)
        
        max_h = 2.5
        bar_width = 0.5
        bars = VGroup()
        bar_labels = VGroup()
        
        for i, name in enumerate(countries):
            # Initial small bars
            bar = Rectangle(
                width=bar_width, 
                height=0.1, 
                fill_color=BLUE, 
                fill_opacity=0.8, 
                stroke_width=1
            )
            bar.move_to(chart_origin + RIGHT * (0.8 * (i + 0.5)), aligned_edge=DOWN)
            bars.add(bar)
            
            lbl = Text(name, font_size=14, color=text_color)
            lbl.next_to(bar, DOWN, buff=0.1)
            bar_labels.add(lbl)
            
        chart_group = VGroup(x_axis, y_axis, bars, bar_labels)

        # 4. Formula
        formula = MathTex(
            r"h(\mathbf{v};\mathbf{X}) = \frac{\exp(\mathbf{X}\mathbf{v})}{\sum_{j=1}^{N}\exp(\mathbf{X}_{j}^{T}\mathbf{v})}",
            color=text_color, font_size=34
        ).to_edge(DOWN, buff=0.5)

        # --- Animations ---

        self.play(FadeIn(v_group), FadeIn(X_group))
        self.play(Create(x_axis), Create(y_axis), FadeIn(bars), Write(bar_labels))
        self.wait(0.5)

        # Probabilities logic
        final_probs = [0.85, 0.05, 0.03, 0.04, 0.03]
        
        # Dot product scan simulation
        for i in range(len(countries)):
            highlight = SurroundingRectangle(X_rows[i], color=YELLOW, buff=0.1)
            self.play(Create(highlight), run_time=0.2)
            
            # Animate the specific bar for this calculation
            new_height = max(final_probs[i] * max_h, 0.1)
            self.play(
                bars[i].animate.stretch_to_fit_height(new_height, about_edge=DOWN),
                run_time=0.3
            )
            self.play(FadeOut(highlight), run_time=0.1)

        # Show full formula
        self.play(Write(formula))
        
        # Highlight final prediction (France)
        self.play(
            bars[0].animate.set_color(RED),
            Indicate(X_rows[0], color=RED),
            run_time=1.5
        )

        self.wait(2)