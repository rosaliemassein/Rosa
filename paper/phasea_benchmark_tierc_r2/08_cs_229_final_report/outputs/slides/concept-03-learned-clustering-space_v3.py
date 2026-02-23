from manim import *

class LearnedClusteringSpace(Scene):
    def construct(self):
        # Create physical space NumberPlane
        plane = NumberPlane()
        plane.set_color(RED)
        self.add(plane)

        # Create two overlapping clusters of dots
        cluster1 = VGroup(*[
            Dot(color=GREEN, radius=0.2) for _ in range(5)
        ]).arrange(buff=0.3).move_to(plane.c2p(-3, 0))
        cluster2 = VGroup(*[
            Dot(color=RED, radius=0.2) for _ in range(5)
        ]).arrange(buff=0.3).move_to(plane.c2p(3, 0))

        self.play(Create(cluster1), Create(cluster2))
        self.wait()

        # Draw dashed circles around each cluster
        circle1 = DashedLine(plane.c2p(-3, 0), plane.c2p(3, 0)).set_color(GREEN)
        circle2 = DashedLine(plane.c2p(3, 0), plane.c2p(-3, 0)).set_color(RED)
        self.play(Create(circle1), Create(circle2))
        self.wait()

        # Use Transform animation to move dots from physical space to learned space
        cluster1_learned = VGroup(*[
            Dot(color=GREEN, radius=0.2) for _ in range(5)
        ]).arrange(buff=0.3).move_to(plane.c2p(-1, 1))
        cluster2_learned = VGroup(*[
            Dot(color=RED, radius=0.2) for _ in range(5)
        ]).arrange(buff=0.3).move_to(plane.c2p(1, -1))

        self.play(Transform(cluster1, cluster1_learned), Transform(cluster2, cluster2_learned))
        self.wait()

        # Draw dashed circles around each learned space cluster
        circle1_learned = DashedLine(plane.c2p(-1, 1), plane.c2p(1, -1)).set_color(GREEN)
        circle2_learned = DashedLine(plane.c2p(1, -1), plane.c2p(-1, 1)).set_color(RED)
        self.play(Create(circle1_learned), Create(circle2_learned))
        self.wait()

        # Narration and explanation
        narration = Text("The real power of this model is that it doesn't cluster hits in the physical x-y-z space of the detector. Instead, it maps every hit into a completely new, multi-dimensional 'learned coordinate' space.").scale(0.8).to_edge(DOWN)
        explanation = Text("In this space, the complex, overlapping energy deposits from two different electrons are unwarped and pulled apart into distinct, easily separable blobs.").scale(0.8).to_edge(DOWN)
        self.play(Write(narration)), (Write(explanation))
        self.wait()