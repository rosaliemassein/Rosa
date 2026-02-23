from manim import *

class Concept01Scene(Scene):
    def construct(self):
        # Background setup - manual grid for technical feel as NumberPlane is restricted
        grid = VGroup()
        for x in range(-7, 8):
            grid.add(Line([x, -4, 0], [x, 4, 0], stroke_opacity=0.1, stroke_width=1))
        for y in range(-4, 5):
            grid.add(Line([-7, y, 0], [7, y, 0], stroke_opacity=0.1, stroke_width=1))
        self.add(grid)

        # Formula at the top
        formula = MathTex(
            r"Pipeline = \{Data \to Preprocessing \to Model \to HPO \to Deployment\}",
            font_size=32
        ).to_edge(UP)

        # Nodes: Data Retrieval, Preprocessing, Model Search, Deployment
        titles = ["Data\nRetrieval", "Pre-\nprocessing", "Model\nSearch", "Deployment"]
        colors = [BLUE, RED, GREEN, YELLOW]
        positions = [LEFT * 4.5, LEFT * 1.5, RIGHT * 1.5, RIGHT * 4.5]

        nodes = VGroup()
        for t, c, p in zip(titles, colors, positions):
            circ = Circle(radius=0.9, color=c, fill_opacity=0.1)
            circ.move_to(p)
            lbl = Text(t, font_size=18).move_to(p)
            nodes.add(VGroup(circ, lbl))

        # Thick Arrows connecting the nodes
        arrows = VGroup()
        for i in range(len(nodes) - 1):
            arr = Arrow(
                nodes[i][0].get_right(), 
                nodes[i+1][0].get_left(), 
                buff=0.1, 
                stroke_width=10, 
                max_tip_length_to_length_ratio=0.2,
                color=WHITE
            )
            arrows.add(arr)

        # Construction sequence
        self.play(Write(formula))
        self.play(
            LaggedStart(*[Create(n) for n in nodes], lag_ratio=0.2),
            run_time=2
        )
        self.play(
            LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.2),
            run_time=1.5
        )
        self.wait(0.5)

        # Ripple animation: Pulse Data Retrieval then propagate color change
        # Pulse animation
        self.play(Indicate(nodes[0], scale_factor=1.2, color=WHITE))

        # Propagate color change from blue (start) to gold through arrows and nodes
        propagation_anims = []
        for i in range(len(arrows)):
            # Change arrow to gold
            propagation_anims.append(arrows[i].animate.set_color(GOLD))
            # Change subsequent node circle to gold
            propagation_anims.append(nodes[i+1][0].animate.set_color(GOLD))

        self.play(
            LaggedStart(*propagation_anims, lag_ratio=0.4),
            run_time=3
        )
        
        self.wait(2)