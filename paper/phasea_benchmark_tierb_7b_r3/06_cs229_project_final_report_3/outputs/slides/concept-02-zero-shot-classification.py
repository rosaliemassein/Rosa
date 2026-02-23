from manim import *

class ZeroShotClassifier(Scene):
    def construct(self):
        self.camera.background_color = "#F8EBCD"
        
        # Create the vector 'v' representing the image
        v = Arrow(start=ORIGIN, end=3*RIGHT, color=BLUE)
        self.play(Create(v))
        
        # Create a large matrix 'X' where each row is a country name
        X = VGroup(*[Text(country, color=GREEN).to_edge(UP) for country in ["France", "Germany", "Italy"]])
        for i, text in enumerate(X):
            text.shift(RIGHT * (2.5 * i - 1))
        self.play(FadeIn(X))
        
        # Pulsing highlight for the dot product operation
        matrix_row = X[0].copy()
        self.play(Transform(matrix_row, matrix_row.scale(1.2)))
        
        # Create a bar chart that updates in real-time
        labels = [Text(country, color=GREEN) for country in ["France", "Germany", "Italy"]]
        bars = VGroup(*[Rectangle(height=0.5, width=2, color=BLUE).next_to(label, DOWN) for label in labels])
        bars.shift(RIGHT * (2.5 * 0 - 1))
        self.play(Create(bars))
        
        # Animate the update of the bar chart
        probabilities = [1, 0.5, 2]
        for i, bar in enumerate(bars):
            new_height = probabilities[i] * 0.5
            self.play(Transform(bar, bar.scale_to_width(new_height)))
        
        # Transform the dot product expression into the final probability vector
        h_formula = MathTex(r"h(\mathbf{v};\mathbf{X})=\frac{\exp(\mathbf{X}\mathbf{v})}{\sum_{j=1}^{N}\exp(\mathbf{X}_{j}^{T}\mathbf{v})}", color=RED)
        h_formula.to_edge(DOWN).shift(LEFT * 3)
        self.play(Write(h_formula))
        
        # Highlight the maximum probability
        max_prob_bar = bars[2]
        self.play(Indicate(max_prob_bar, color=RED))
        
        self.wait()