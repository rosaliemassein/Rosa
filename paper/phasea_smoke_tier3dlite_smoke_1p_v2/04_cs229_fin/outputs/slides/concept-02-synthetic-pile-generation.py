from manim import *
import random

class SyntheticPileGeneration(Scene):
    def construct(self):
        # Layout
        background = Rectangle(color=WHITE, height=8, width=14)
        trash_icons = [
            MathTex(r"C", color=RED).scale(2),
            MathTex(r"\text{B}", color=BLUE).scale(2),
            MathTex(r"P", color=YELLOW).scale(2),
        ]
        icons = []
        for i, icon in enumerate(trash_icons):
            icons.append(icon.shift(LEFT * (i - 1)))

        # Value trackers
        scale_tracker = ValueTracker(1)
        rotation_tracker = ValueTracker(0)

        # Display icons on the canvas
        for icon in icons:
            self.play(FadeIn(icon), run_time=1)
            self.wait(0.5)

        # Animate icons onto the canvas with rotation and scaling
        for icon in icons:
            scale_factor = random.uniform(0.5, 1.5)
            rotation_angle = random.uniform(-PI/2, PI/2)
            scale_tracker.set_value(scale_factor)
            rotation_tracker.set_value(rotation_angle)
            self.play(Transform(icon, icon.scale(scale_tracker.get_value()).rotate(rotation_tracker.get_value())), run_time=2)
            self.wait(1)

        # Create a crowded scene by overlapping objects
        for i in range(5):
            self.play(Transform(VGroup(*icons), VGroup(*icons).shift(DOWN * (i - 1))), run_time=2)
            self.wait(0.5)

        self.wait(3)