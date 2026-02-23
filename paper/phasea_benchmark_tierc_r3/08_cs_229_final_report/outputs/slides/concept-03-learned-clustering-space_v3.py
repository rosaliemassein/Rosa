from manim import *

class LearnedClusteringSpace(Scene):
    def construct(self):
        self.setup_axes()
        self.create_planes()
        self.transform_dots()

    def setup_axes(self):
        axes = Axes(x_range=(-5, 5), y_range=(-5, 5))
        self.axes = axes
        self.add(axes)

    def create_planes(self):
        plane_x = NumberPlane(x_range=(-5, 5), y_range=(-5, 5), color=BLUE)
        plane_y = NumberPlane(x_range=(-5, 5), y_range=(-5, 5), color=GREEN)
        plane_x.label_axes(x_label="Physical Space", y_label="Physical Space")
        plane_y.label_axes(x_label="Learned Space", y_label="Learned Space")
        self.plane_x = plane_x
        self.plane_y = plane_y

    def transform_dots(self):
        # Create dots for the first cluster
        dot1 = Dot(color=RED)
        dot2 = Dot(color=RED)

        # Create dots for the second cluster
        dot3 = Dot(color=YELLOW)
        dot4 = Dot(color=YELLOW)

        # Arrange dots in the physical space
        plane_x.add(dot1, dot2)
        plane_y.add(dot3, dot4)

        # Transform dots to the learned space
        self.play(Transform(plane_x.dots[0], plane_y, scale=1.5), Transform(plane_x.dots[1], plane_y, scale=1.5),
                Transform(plane_x.dots[2], plane_y, scale=1.5), Transform(plane_x.dots[3], plane_y, scale=1.5))

        # Draw dashed circles in the learned space
        circle_red = DashedLine(plane_y.c2p(1, 0), plane_y.c2p(-1, 0), color=RED)
        circle_yellow = DashedLine(plane_y.c2p(1, 0), plane_y.c2p(-1, 0), color=YELLOW)
        self.play(Create(circle_red), Create(circle_yellow))

        # Narration
        text = Text(self.voice, font="Comic Neue", t2e={"The real power of this model is that it doesn't cluster hits in the physical x-y-z space of the detector. Instead, it maps every hit into a completely new, multi-dimensional 'learned coordinate' space."})
        text.to_edge(DOWN)
        self.add(text)

    def get_plane_y(self):
        return self.plane_y