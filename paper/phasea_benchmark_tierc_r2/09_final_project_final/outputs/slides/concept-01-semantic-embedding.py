from manim import *

class SemanticEmbeddingScene(Scene):
    def construct(self):
        # Create a 3D NumberPlane
        plane = NumberPlane()

        # Pop up floating text labels for 'Deep Learning', 'Neural Networks', and 'Robotics'
        dl_text = Text("Deep Learning").scale(0.5).to_edge(DR)
        nn_text = Text("Neural Networks").scale(0.5).next_to(dl_text, RIGHT)
        robotics_text = Text("Robotics").scale(0.5).next_to(nn_text, RIGHT)

        self.play(Create(plane), Write(dl_text), Write(nn_text), Write(robotics_text))

        # Animate the text labels transforming into Dot objects at specific coordinates
        dl_dot = Dot().scale(1.5).move_to(plane.c2p(0, 3))
        nn_dot = Dot().scale(1.5).move_to(plane.c2p(0, 1))
        robotics_dot = Dot().scale(1.5).move_to(plane.c2p(-3, 0))

        self.play(Transform(dl_text, dl_dot), Transform(nn_text, nn_dot), Transform(robotics_text, robotics_dot))

        # Use a dashed line to show the distance between 'Deep Learning' and 'Neural Networks'
        line = DashedLine(dl_dot.get_center(), nn_dot.get_center())
        self.play(Create(line))
        
        # Display the word 'Machine' and its vector, the word 'Learning' and its vector
        machine = Text("Machine").scale(0.5).next_to(nn_text, RIGHT)
        learning = Text("Learning").scale(0.5).next_to(machine, RIGHT)

        self.play(Create(machine), Create(learning))

        # Use Transform to merge them into a single central vector representing the average position
        combined_dot = Dot().scale(2).move_to(plane.c2p(-1, 1))
        self.play(Transform(machine, combined_dot), Transform(learning, combined_dot))

        # Display the formula
        formula = MathTex(r"v_{phrase} = \frac{1}{n} \sum_{i=1}^{n} v_{i}")
        formula.move_to(plane.c2p(0, 3))
        self.play(FadeIn(formula))

        self.wait()