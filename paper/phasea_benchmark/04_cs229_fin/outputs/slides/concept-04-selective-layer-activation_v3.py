from manim import *

class SelectiveLayerActivation(Scene):
    def construct(self):
        # Create a horizontal chain of 24 'Square' objects representing layers 0 to 23
        layers = VGroup(*[
            Square(side_length=0.3, fill_opacity=0.6)
            for _ in range(24)
        ]).arrange(RIGHT, buff=0.12)
        layers.center()

        # Color the layers based on the strategy
        # Layers 0-6: Frozen Backbone (Gray)
        # Layers 7-10: Active Semantics (Blue)
        # Layers 11-22: Frozen (Gray)
        # Layer 23: Active Head (Orange)
        active_indices = [7, 8, 9, 10, 23]
        
        for i in range(24):
            if 7 <= i <= 10:
                layers[i].set_color(BLUE)
                layers[i].set_fill(BLUE, opacity=0.8)
            elif i == 23:
                layers[i].set_color(ORANGE)
                layers[i].set_fill(ORANGE, opacity=0.8)
            else:
                layers[i].set_color(GRAY)
                layers[i].set_fill(GRAY, opacity=0.4)

        # Create Labels
        backbone_label = Text("Frozen Backbone", font_size=18, color=GRAY).next_to(layers[0:7], UP)
        active_sem_label = Text("Active Semantics", font_size=18, color=BLUE).next_to(layers[7:11], DOWN, buff=0.5)
        active_head_label = Text("Active Head", font_size=18, color=ORANGE).next_to(layers[23], DOWN, buff=0.5)

        # Glow effect for active layers
        glows = VGroup()
        for idx in active_indices:
            glow = layers[idx].copy()
            glow.set_stroke(layers[idx].get_color(), width=10, opacity=0.3)
            glow.scale(1.2)
            glows.add(glow)

        # Initial Setup
        self.add(layers, glows)
        self.play(
            FadeIn(backbone_label),
            FadeIn(active_sem_label),
            FadeIn(active_head_label)
        )
        self.wait(0.5)

        # Succession of pulses through the blue and orange squares
        pulse_animations = [
            Indicate(layers[i], color=layers[i].get_color(), scale_factor=1.4)
            for i in active_indices
        ]
        
        # Run the pulse sequence twice
        for _ in range(2):
            self.play(Succession(*pulse_animations, run_time=2.5))

        # Final accuracy text
        accuracy = Text("86% Accuracy achieved via Selective Training", font_size=24).to_edge(UP)
        self.play(Write(accuracy))
        self.wait(2)