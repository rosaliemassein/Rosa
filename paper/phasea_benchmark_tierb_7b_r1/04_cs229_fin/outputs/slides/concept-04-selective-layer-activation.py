from manim import *

class SelectiveLayerActivation(Scene):
    def construct(self):
        # Create 24 squares representing model layers
        layers = [Square() for _ in range(24)]
        layer_names = ['0-6', '7-10', '11-22', '23']
        layer_colors = [GRAY, BLUE, GRAY, ORANGE]

        for i in range(24):
            layers[i].set_fill(layer_colors[i % 4], opacity=1)
            if i < 7:
                layers[i].to_edge(LEFT).shift(RIGHT * (i + 1))
            elif i < 11:
                layers[i].to_edge(LEFT).shift(RIGHT * (i + 3))
            elif i < 23:
                layers[i].to_edge(LEFT).shift(RIGHT * (i + 5))
            else:
                layers[i].to_edge(LEFT).shift(RIGHT * (i + 7))

        # Add labels to the layers
        labels = [Text(name) for name in layer_names]
        label_positions = [LEFT, LEFT, LEFT, RIGHT]
        for i in range(4):
            labels[i].next_to(layers[i * 6], UP, buff=0.2).set_color(WHITE)

        # Create pulses for animation
        pulse = Circle(radius=0.1, fill_color=WHITE)
        pulses = [pulse.copy().next_to(layers[i], RIGHT * 2, buff=0.5) for i in range(7, 11)]
        pulses.extend([pulse.copy().next_to(layers[23], RIGHT * 2, buff=0.5)])

        # Animation
        for pulse in pulses:
            self.play(Create(pulse), run_time=0.5)
            self.wait(0.2)
            self.play(FadeOut(pulse), run_time=0.3)

        # Final state
        self.wait(2)