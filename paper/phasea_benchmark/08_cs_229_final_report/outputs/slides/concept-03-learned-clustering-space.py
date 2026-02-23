from manim import *

class LearnedClusteringSpace(Scene):
    def construct(self):
        # Create a split-screen view
        screen = VGroup(Dot(), Dot()).arrange(DOWN, buff=1.5)
        self.play(Create(screen))

        # Left part: Physical Space
        physical_space = NumberPlane(x_range=(-3, 2), y_range=(-2.5, 2.5), color=BLUE)
        physical_space.add_labels(labels=[R"0", R"\sqrt{2}", R"\pi"], font_size=24)
        self.play(Create(physical_space), run_time=2)

        # Right part: Learned Space
        learned_space = NumberPlane(x_range=(-6, 6), y_range=(-10, 10), color=GREEN)
        learned_space.add_labels(labels=[R"0", R"\sqrt{3}", R"\pi"], font_size=24)
        self.play(Create(learned_space), run_time=2)

        # Placement for the dashed circles
        circle_1 = Circle(radius=3, color=RED).move_to(2 * RIGHT)
        circle_2 = Circle(radius=3, color=BLUE).move_to(2 * LEFT)
        self.add(circle_1)
        self.add(circle_2)

        # Voiceover
        self.play(Write(Text(R"The real power of this model is that it doesn't cluster hits in the physical x-y-z space of the detector. Instead, it maps every hit into a completely new, multi-dimensional 'learned coordinate' space.")))
        self.wait()

        # Goal
        self.play(Write(Text(R"Demonstrate the transformation from physical detector coordinates to the learned clustering space.")))
        self.wait()

        # Remarks
        self.play(Write(Text(R"Create a split-screen view. On the left, show a 'Physical Space' NumberPlane with two overlapping clusters of hits. On the right, show a 'Learned Space' NumberPlane.")))
        self.wait()

        # Move dots from physical to learned space
        dot_1 = Dot(0.5 * RIGHT)
        dot_2 = Dot(0.35 * LEFT)
        dots = VGroup(dot_1, dot_2)
        self.play(Transform(physical_space.get_dots(), dots), run_time=3)

        # Draw dashed circles in learned space
        dashed_circle_1 = DashedLine(circle_1.get_center(), circle_1.get_center()[0] * RIGHT + 3 * UP)
        dashed_circle_2 = DashedLine(circle_2.get_center(), circle_2.get_center()[0] * LEFT + 3 * UP)
        self.play(Create(dashed_circle_1), Create(dashed_circle_2))

        # Remarks
        self.play(Write(Text(R"In the physical space, the clusters should overlap heavily. In the learned space, the dots should magically rearrange into two distinct, separated circular distributions.")))
        self.wait()

        # Remarks
        self.play(Write(Text(R"Draw a dashed circle around each cluster in the learned space to indicate successful classification.")))
        self.wait()