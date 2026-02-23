from manim import *

class SelectiveLayerActivation(Scene):
    def construct(self):
        # Create a horizontal chain of 24 Square objects representing layers 0 to 23
        layers = VGroup(*[Square(side_length=0.35) for _ in range(24)])
        layers.arrange(RIGHT, buff=0.1)
        layers.center()

        # Define colors
        frozen_color = GRAY
        active_sem_color = BLUE
        active_head_color = ORANGE

        # Color layers according to logic
        # 0-6: Frozen Backbone
        # 7-10: Active Semantics
        # 11-22: Frozen
        # 23: Active Head
        for i in range(24):
            if 0 <= i <= 6:
                layers[i].set_color(frozen_color).set_fill(frozen_color, opacity=0.3)
            elif 7 <= i <= 10:
                layers[i].set_color(active_sem_color).set_fill(active_sem_color, opacity=0.6)
                layers[i].set_stroke(width=5)
            elif 11 <= i <= 22:
                layers[i].set_color(frozen_color).set_fill(frozen_color, opacity=0.3)
            elif i == 23:
                layers[i].set_color(active_head_color).set_fill(active_head_color, opacity=0.7)
                layers[i].set_stroke(width=5)

        # Labels
        frozen_label = Text("Frozen Backbone", font_size=16).next_to(layers[0:7], DOWN, buff=0.5)
        active_sem_label = Text("Active Semantics", font_size=16, color=active_sem_color).next_to(layers[7:11], UP, buff=0.5)
        active_head_label = Text("Active Head", font_size=16, color=active_head_color).next_to(layers[23], UP, buff=0.5)

        # Presentation
        self.play(
            Create(layers),
            Write(frozen_label),
            Write(active_sem_label),
            Write(active_head_label)
        )
        self.wait(1)

        # Pulse animation for active layers (7-10 and 23)
        active_indices = [7, 8, 9, 10, 23]
        
        # We create a sequence of pulses moving through the specific layers
        for idx in active_indices:
            self.play(
                AnimationGroup(
                    Indicate(layers[idx], scale_factor=1.4, color=layers[idx].get_color()),
                    Flash(layers[idx], color=layers[idx].get_color(), flash_radius=0.4),
                    run_time=0.5
                )
            )

        # Final emphasis on the active strategy
        self.play(
            *[layers[idx].animate.set_stroke(width=8) for idx in active_indices],
            lag_ratio=0.1
        )
        self.wait(2)