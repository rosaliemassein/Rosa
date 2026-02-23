from manim import *

class SyntheticPileGeneration(Scene):
    def construct(self):
        # Create the canvas
        canvas = Rectangle(width=8, height=6).set_color(WHITE)
        self.play(Create(canvas))

        # Create trash icons
        bottle = Text(" Bottle", color=BLUE).scale(0.5)
        can = Text(" Can", color=GREEN).scale(0.5)
        paper_scrap = Text(" Paper Scrap", color=YELLOW).scale(0.5)

        # Create labels for scale and rotation
        scale_label = Text("Scale").next_to(bottle, UP)
        rotation_label = Text("Rotation").next_to(can, DOWN)

        # Create ValueTrackers for scale and rotation
        scale_tracker = ValueTracker(1.0)
        rotation_tracker = ValueTracker(0)

        # Define the icons and their positions
        icons = [bottle, can, paper_scrap]
        positions = [(2, -1), (4, 0), (-3, 1)]

        # Animate icons landing on the canvas
        for icon, position in zip(icons, positions):
            icon.set_position(position)
            self.play(Create(icon), run_time=1)

        # Apply random scaling and rotation to each icon
        for icon in icons:
            scale_value = scale_tracker.get_value()
            rotation_value = rotation_tracker.get_value()
            self.play(Transform(icon, icon.scale(scale_value).rotate(rotation_value)), run_time=2)

        # Display scale and rotation labels
        self.play(Create(scale_label), Create(rotation_label))

        # Wait for final view
        self.wait(2)