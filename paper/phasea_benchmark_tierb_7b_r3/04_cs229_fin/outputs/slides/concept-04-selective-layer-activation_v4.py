from manim import *

class SelectiveLayerActivation(Scene):
    def construct(self):
        # Create 24 squares representing model layers 0 to 23
        # Small side_length to ensure they all fit horizontally
        layers = VGroup(*[Square(side_length=0.3, fill_opacity=0.6) for _ in range(24)])
        layers.arrange(RIGHT, buff=0.1)
        layers.move_to(ORIGIN)

        # Color the layers based on the logic:
        # 0-6: Gray (Frozen Backbone)
        # 7-10: Blue (Active Semantics)
        # 11-22: Gray
        # 23: Orange (Active Head)
        for i in range(24):
            if 0 <= i <= 6:
                layers[i].set_color(GRAY)
            elif 7 <= i <= 10:
                layers[i].set_color(BLUE)
            elif 11 <= i <= 22:
                layers[i].set_color(GRAY)
            elif i == 23:
                layers[i].set_color(ORANGE)

        # Define labels and position them relative to groups
        # Replacing disallowed Brace with Text positioned relative to groups
        backbone_label = Text("Frozen Backbone", color=GRAY).scale(0.4)
        backbone_label.next_to(VGroup(*layers[0:7]), DOWN, buff=0.4)

        semantics_label = Text("Active Semantics", color=BLUE).scale(0.4)
        semantics_label.next_to(VGroup(*layers[7:11]), UP, buff=0.4)

        head_label = Text("Active Head", color=ORANGE).scale(0.4)
        head_label.next_to(layers[23], DOWN, buff=0.4)

        # Draw the layers and labels
        self.add(layers)
        self.play(
            FadeIn(backbone_label),
            FadeIn(semantics_label),
            FadeIn(head_label)
        )
        self.wait(1)

        # Define pulse animations for active layers (7, 8, 9, 10, and 23)
        # Indicate creates a scale-up and color-flash effect
        active_indices = [7, 8, 9, 10, 23]
        pulses = [
            Indicate(layers[i], color=layers[i].get_color(), scale_factor=1.6) 
            for i in active_indices
        ]

        # Succession makes the pulses move through the layers one after another
        self.play(Succession(*pulses, run_time=4))

        # Final visual feedback representing the success mentioned in the prompt
        accuracy_text = Text("86% Accuracy", color=GREEN).scale(0.7)
        accuracy_text.to_edge(DOWN, buff=1.0)
        self.play(Write(accuracy_text))
        
        self.wait(2)