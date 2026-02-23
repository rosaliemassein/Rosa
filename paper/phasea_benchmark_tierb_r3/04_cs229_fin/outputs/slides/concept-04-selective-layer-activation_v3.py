from manim import *

class SelectiveLayerActivation(Scene):
    def construct(self):
        # Create a horizontal chain of 24 Square objects representing layers 0 to 23
        layers = VGroup(*[Square(side_length=0.35) for _ in range(24)])
        layers.arrange(RIGHT, buff=0.1)
        layers.move_to(UP * 0.5)

        # Style layers 0-6: Frozen Backbone (Gray)
        for i in range(0, 7):
            layers[i].set_stroke(color=GRAY)
            layers[i].set_fill(color=GRAY, opacity=0.5)

        # Style layers 7-10: Active Semantics (Blue with glow-like stroke)
        active_semantics = layers[7:11]
        for layer in active_semantics:
            layer.set_stroke(color=BLUE, width=8)
            layer.set_fill(color=BLUE, opacity=0.8)

        # Style layers 11-22: Frozen (Gray)
        for i in range(11, 23):
            layers[i].set_stroke(color=GRAY)
            layers[i].set_fill(color=GRAY, opacity=0.5)

        # Style layer 23: Active Head (Orange)
        active_head = layers[23]
        active_head.set_stroke(color=ORANGE, width=8)
        active_head.set_fill(color=ORANGE, opacity=0.8)

        # Labels (replacing disallowed Brace with basic Text positioning)
        label_frozen = Text("Frozen Backbone", font_size=18, color=GRAY).next_to(layers[0:7], DOWN, buff=0.5)
        label_semantics = Text("Active Semantics", font_size=18, color=BLUE).next_to(layers[7:11], DOWN, buff=0.5)
        label_head = Text("Active Head", font_size=18, color=ORANGE).next_to(layers[23], DOWN, buff=0.5)

        # Group components
        all_layers = VGroup(layers, label_frozen, label_semantics, label_head)
        self.add(all_layers)

        # Narrative description (simulating the voiceover context)
        description = Text(
            "Freezing Backbone, Training Head and Semantic Layers", 
            font_size=24, 
            color=WHITE
        ).to_edge(DOWN, buff=1)
        self.add(description)

        # Pulse animation: succession of pulses through layers 7-10 and then layer 23
        # This represents gradients updating only in selected regions
        pulse_indices = [7, 8, 9, 10, 23]
        
        # We loop the succession twice to emphasize the "training" process
        for _ in range(2):
            self.play(
                Succession(
                    *[Indicate(layers[i], color=layers[i].get_color(), scale_factor=1.5) for i in pulse_indices],
                    lag_ratio=0.2
                ),
                run_time=2.5
            )

        self.wait(1)