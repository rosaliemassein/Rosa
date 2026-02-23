from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Manual technical background (NumberPlane alternative)
        grid = VGroup()
        for x in range(-7, 8):
            grid.add(Line(start=[x, -4, 0], end=[x, 4, 0], stroke_width=1, stroke_opacity=0.15, color=BLUE))
        for y in range(-4, 5):
            grid.add(Line(start=[-7, y, 0], end=[7, y, 0], stroke_width=1, stroke_opacity=0.15, color=BLUE))
        self.add(grid)

        # 2. Pipeline Steps (Circles and Labels)
        step_names = ["Data Retrieval", "Preprocessing", "Model Search", "Deployment"]
        circles = VGroup()
        labels = VGroup()
        
        for name in step_names:
            c = Circle(radius=0.7, color=BLUE, fill_opacity=0.2)
            l = Text(name, font_size=20)
            circles.add(c)
            labels.add(l)
        
        circles.arrange(RIGHT, buff=1.0).move_to(ORIGIN)
        for i in range(len(labels)):
            labels[i].next_to(circles[i], DOWN, buff=0.4)

        # 3. Connections (Thick Arrows)
        arrows = VGroup()
        for i in range(len(circles)-1):
            arr = Arrow(
                circles[i].get_right(), 
                circles[i+1].get_left(), 
                buff=0.1, 
                color=BLUE, 
                stroke_width=10,
                max_tip_length_to_length_ratio=0.15
            )
            arrows.add(arr)

        # 4. Formula and Objective Text (Using Text to avoid MathTex restrictions)
        formula = Text(
            "Pipeline = {Data -> Preprocessing -> Model -> HPO -> Deployment}", 
            font_size=22,
            t2c={"Data": BLUE, "Preprocessing": BLUE, "Model": BLUE, "HPO": BLUE, "Deployment": BLUE}
        ).to_edge(UP, buff=0.5)

        goal_text = Text(
            "Understand the inter-dependency and end-to-end nature of the AutoML pipeline.",
            font_size=18
        ).to_edge(DOWN, buff=0.5)

        # Initial Layout
        self.add(circles, labels, arrows, formula, goal_text)
        self.wait(1)

        # 5. Pulse Animation (Manually handled to avoid there_and_back)
        # Pulse the 'Data Retrieval' circle
        self.play(circles[0].animate.scale(1.25), run_time=0.4)
        self.play(circles[0].animate.scale(0.8), run_time=0.4)

        # 6. Propagation of Color Change (Blue to Gold)
        GOLD_HEX = "#FFD700"
        
        # Sequentially animate color change through the pipeline elements
        self.play(circles[0].animate.set_color(GOLD_HEX), run_time=0.3)
        
        for i in range(len(arrows)):
            # Change arrow color
            self.play(
                arrows[i].animate.set_color(GOLD_HEX),
                run_time=0.3
            )
            # Change next circle color
            self.play(
                circles[i+1].animate.set_color(GOLD_HEX),
                run_time=0.3
            )

        # Final Highlight on Formula
        self.play(formula.animate.set_color(GOLD_HEX), run_time=1)
        
        self.wait(2)