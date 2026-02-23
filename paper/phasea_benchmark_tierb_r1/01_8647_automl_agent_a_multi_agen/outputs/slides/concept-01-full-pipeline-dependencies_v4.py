from manim import *

class ConceptPipelineDependencies(Scene):
    def construct(self):
        # Manual background grid instead of NumberPlane to satisfy constraints
        background_lines = VGroup()
        for i in range(-7, 8):
            background_lines.add(Line(i * RIGHT + 4 * UP, i * RIGHT + 4 * DOWN, stroke_opacity=0.1, color=GRAY))
        for j in range(-4, 5):
            background_lines.add(Line(8 * LEFT + j * UP, 8 * RIGHT + j * UP, stroke_opacity=0.1, color=GRAY))
        self.add(background_lines)
        
        title = Text("Full-Stage AutoML Pipeline", font_size=36)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        # 1. Create the Nodes (4 large circles as requested)
        stages = ["Data Retrieval", "Preprocessing", "Model Search", "Deployment"]
        nodes = VGroup()
        
        for name in stages:
            circle = Circle(radius=0.9, color=BLUE, fill_opacity=0.1)
            label = Text(name, font_size=18).move_to(circle.get_center())
            nodes.add(VGroup(circle, label))
            
        nodes.arrange(RIGHT, buff=1.0).shift(UP * 0.5)

        # 2. Create Connecting Arrows
        arrows = VGroup()
        for i in range(len(nodes) - 1):
            arrow = Arrow(
                nodes[i].get_right(), 
                nodes[i+1].get_left(), 
                buff=0.1, 
                stroke_width=8, 
                color=BLUE
            )
            arrows.add(arrow)

        # 3. Formula reference at bottom
        formula = MathTex(
            r"\text{Pipeline} = \{ \text{Data} \to \text{Preprocessing} \to \text{Model} \to \text{HPO} \to \text{Deployment} \}",
            font_size=28
        )
        formula.to_edge(DOWN, buff=1.2)

        self.add(nodes, arrows, formula)

        # 4. Animation Sequence
        self.play(Write(title))
        self.wait(1)

        # "Imagine your raw data as the foundation..."
        # Pulse animation on 'Data Retrieval'
        self.play(
            nodes[0][0].animate.scale(1.2).set_color(GOLD),
            run_time=1
        )
        self.play(
            nodes[0][0].animate.scale(1/1.2),
            run_time=1
        )

        # "...ripples through the entire structure..."
        # Propagate color change (Blue -> Gold) through arrows and circles
        self.play(nodes[0][1].animate.set_color(GOLD))
        
        for i in range(len(arrows)):
            self.play(
                arrows[i].animate.set_color(GOLD),
                nodes[i+1][0].animate.set_color(GOLD),
                nodes[i+1][1].animate.set_color(GOLD),
                run_time=0.7
            )

        # "...dictating which models are viable..."
        self.play(
            Indicate(nodes[2], color=GOLD, scale_factor=1.1),
            run_time=1.5
        )

        # "...and which hyperparameters need tuning."
        # Highlight HPO in the formula
        self.play(
            formula.animate.set_color(GOLD),
            run_time=2
        )

        # "AutoML-Agent manages this complexity..."
        # Highlight the end-to-end flow
        self.play(
            Succession(
                Flash(nodes[0], color=WHITE),
                Flash(nodes[3], color=WHITE),
            ),
            run_time=3
        )

        self.wait(2)