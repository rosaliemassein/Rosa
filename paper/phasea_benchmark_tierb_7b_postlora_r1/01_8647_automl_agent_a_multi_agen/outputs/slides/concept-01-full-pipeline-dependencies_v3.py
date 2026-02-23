from manim import *

class Concept01FullPipelineDependencies(Scene):
    def construct(self):
        # 1. Technical background (Manual grid instead of NumberPlane to avoid disallowed identifiers)
        grid = VGroup()
        for x in range(-7, 8):
            grid.add(Line(start=[x, -4, 0], end=[x, 4, 0], stroke_opacity=0.15, stroke_width=1, color=GRAY))
        for y in range(-5, 6):
            grid.add(Line(start=[-8, y, 0], end=[8, y, 0], stroke_opacity=0.15, stroke_width=1, color=GRAY))
        self.add(grid)

        # 2. Formula Reference
        formula = MathTex(
            r"\text{Pipeline} = \{Data \to Preprocessing \to Model \to HPO \to Deployment\}",
            font_size=32
        ).to_edge(UP, buff=0.5)
        self.add(formula)

        # 3. Create Circle Nodes and Labels (Stages: Data Retrieval, Preprocessing, Model Search, Deployment)
        stage_names = ["Data\nRetrieval", "Preprocessing", "Model\nSearch", "Deployment"]
        nodes = VGroup()
        node_circles = []
        
        for name in stage_names:
            circle = Circle(radius=1.1, color=BLUE, stroke_width=6)
            circle.set_fill(BLUE, opacity=0.1)
            label = Text(name, font_size=20)
            node = VGroup(circle, label)
            nodes.add(node)
            node_circles.append(circle)

        nodes.arrange(RIGHT, buff=0.8).shift(DOWN * 0.5)

        # 4. Create Thick Arrows
        arrows = VGroup()
        for i in range(len(nodes) - 1):
            arrow = Arrow(
                nodes[i].get_right(),
                nodes[i+1].get_left(),
                buff=0.1,
                stroke_width=10,
                color=WHITE,
                max_tip_length_to_length_ratio=0.15
            )
            arrows.add(arrow)

        self.add(nodes, arrows)

        # 5. Animation Sequence
        self.wait(1)

        # "apply a pulse animation to the 'Data Retrieval' circle"
        self.play(Indicate(node_circles[0], color=GOLD, scale_factor=1.3))

        # "propagate a color change (e.g., from blue to gold) through the arrows to the 'Deployment' circle"
        # Initial node turns gold
        self.play(
            node_circles[0].animate.set_color(GOLD).set_fill(GOLD, opacity=0.3),
            run_time=0.4
        )

        # Sequential propagation through the rest of the pipeline
        for i in range(len(arrows)):
            self.play(
                arrows[i].animate.set_color(GOLD),
                node_circles[i+1].animate.set_color(GOLD).set_fill(GOLD, opacity=0.3),
                run_time=0.7
            )

        self.wait(3)