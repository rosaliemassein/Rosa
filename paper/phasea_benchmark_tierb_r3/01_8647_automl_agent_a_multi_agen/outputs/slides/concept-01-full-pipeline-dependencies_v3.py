from manim import *

class ConceptPipelineDependencies(Scene):
    def construct(self):
        # 1. Background Grid (Manual replacement for NumberPlane)
        grid = VGroup()
        for x in range(-7, 8):
            grid.add(Line(start=[x, -4, 0], end=[x, 4, 0], stroke_opacity=0.1, stroke_width=1))
        for y in range(-4, 5):
            grid.add(Line(start=[-7, y, 0], end=[7, y, 0], stroke_opacity=0.1, stroke_width=1))
        self.add(grid)

        # 2. Define Circles and Labels
        # Remarks specify 4 circles: Data Retrieval, Preprocessing, Model Search, Deployment
        step_names = ["Data Retrieval", "Preprocessing", "Model Search", "Deployment"]
        circles = VGroup(*[
            Circle(radius=0.8, color=BLUE, fill_opacity=0.2) 
            for _ in range(4)
        ])
        circles.arrange(RIGHT, buff=1.2).shift(UP * 0.5)
        
        labels = VGroup(*[
            Text(name, font_size=20).next_to(circles[i], DOWN) 
            for i, name in enumerate(step_names)
        ])

        # 3. Create Arrows
        arrows = VGroup(*[
            Arrow(
                circles[i].get_right(), 
                circles[i+1].get_left(), 
                buff=0.1, 
                color=BLUE,
                stroke_width=8
            )
            for i in range(len(circles) - 1)
        ])

        # 4. Formula (Using the reference formula)
        formula = MathTex(
            r"Pipeline = \{Data \to Preprocessing \to Model \to HPO \to Deployment\}",
            font_size=28
        ).to_edge(DOWN, buff=1)

        # 5. Build Scene Animation
        self.play(Create(circles), Write(labels), run_time=1.5)
        self.play(Create(arrows), run_time=1)
        self.play(Write(formula), run_time=1)
        self.wait(1)

        # 6. Ripple Animation (Pulse + Color Propagation)
        # Pulse the first circle (Data Retrieval)
        self.play(circles[0].animate.scale(1.2).set_color(GOLD).set_fill(GOLD, opacity=0.4), run_time=0.4)
        self.play(circles[0].animate.scale(1/1.2), run_time=0.4)
        
        # Propagate color change through arrows and subsequent circles to Deployment
        for i in range(len(arrows)):
            self.play(
                arrows[i].animate.set_color(GOLD),
                circles[i+1].animate.set_color(GOLD).set_fill(GOLD, opacity=0.4),
                labels[i+1].animate.set_color(GOLD),
                run_time=0.6
            )

        # Final emphasis on the formula
        self.play(formula.animate.set_color(GOLD).scale(1.1), run_time=0.8)
        self.play(formula.animate.scale(1/1.1), run_time=0.8)

        self.wait(2)