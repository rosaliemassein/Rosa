from manim import *

class SelectiveLayerActivation(Scene):
    def construct(self):
        # Create a horizontal chain of 24 'Square' objects representing layers 0 to 23
        layers = VGroup(*[Square(side_length=0.3) for _ in range(24)])
        layers.arrange(RIGHT, buff=0.1)
        layers.move_to(ORIGIN)

        # Color segments based on the logic provided
        # 0-6: Frozen Backbone (Gray)
        for i in range(0, 7):
            layers[i].set_color(GRAY)
        
        # 7-10: Active Semantics (Blue)
        for i in range(7, 11):
            layers[i].set_color(BLUE)
            
        # 11-22: Frozen intermediate layers (Gray)
        for i in range(11, 23):
            layers[i].set_color(GRAY)
            
        # 23: Active Head (Orange)
        layers[23].set_color(ORANGE)

        # Labels
        frozen_label = Text("Frozen Backbone", font_size=16, color=GRAY).next_to(layers[0:7], UP, buff=0.4)
        semantics_label = Text("Active Semantics", font_size=16, color=BLUE).next_to(layers[7:11], DOWN, buff=0.4)
        head_label = Text("Active Head", font_size=16, color=ORANGE).next_to(layers[23], UP, buff=0.4)

        # Visual Glow Effect for active layers (7-10 and 23)
        active_indices = [7, 8, 9, 10, 23]
        glows = VGroup()
        for idx in active_indices:
            # Create a slightly larger, semi-transparent copy to simulate a glow
            glow = layers[idx].copy()
            glow.set_stroke(layers[idx].get_color(), width=10, opacity=0.3)
            glow.scale(1.2)
            glows.add(glow)

        # Add initial static elements
        self.add(layers, frozen_label, semantics_label, head_label, glows)

        # Animate pulses moving through the blue squares (7-10) and the orange square (23)
        # Using a list of Indicate animations
        pulses = [
            Indicate(layers[i], color=layers[i].get_color(), scale_factor=1.5)
            for i in active_indices
        ]

        # Execute the succession of pulses
        self.play(
            Succession(*pulses),
            run_time=3
        )

        self.wait(2)