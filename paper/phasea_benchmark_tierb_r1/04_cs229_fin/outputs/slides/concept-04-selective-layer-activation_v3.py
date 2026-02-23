from manim import *

class SelectiveLayerActivation(Scene):
    def construct(self):
        # Create a horizontal chain of 24 'Square' objects representing layers 0 to 23
        # Small side_length to fit all 24 squares on screen horizontally
        squares = VGroup(*[Square(side_length=0.3, stroke_width=2) for _ in range(24)])
        squares.arrange(RIGHT, buff=0.1)
        squares.move_to(ORIGIN)

        # 1. Color layers 0-6 gray (Frozen Backbone)
        for i in range(0, 7):
            squares[i].set_color(GRAY)
            squares[i].set_fill(GRAY, opacity=0.3)

        # 2. Color layers 7-10 bright blue (Active Semantics)
        active_semantics_group = squares[7:11]
        for sq in active_semantics_group:
            sq.set_color(BLUE)
            sq.set_fill(BLUE, opacity=0.5)
            # Simulate a Glow effect with a slightly larger stroke copy
            glow = sq.copy().set_stroke(BLUE, width=6, opacity=0.4).scale(1.2)
            sq.add(glow)

        # 3. Color layers 11-22 gray
        for i in range(11, 23):
            squares[i].set_color(GRAY)
            squares[i].set_fill(GRAY, opacity=0.3)

        # 4. Color layer 23 bright orange (Active Head)
        squares[23].set_color(ORANGE)
        squares[23].set_fill(ORANGE, opacity=0.5)
        head_glow = squares[23].copy().set_stroke(ORANGE, width=6, opacity=0.4).scale(1.2)
        squares[23].add(head_glow)

        # Add Labels
        frozen_label = Text("Frozen Backbone", font_size=16, color=GRAY).next_to(squares[0:7], DOWN, buff=0.5)
        active_sem_label = Text("Active Semantics", font_size=16, color=BLUE).next_to(squares[7:11], UP, buff=0.5)
        active_head_label = Text("Active Head", font_size=16, color=ORANGE).next_to(squares[23], DOWN, buff=0.5)

        # Display squares and labels
        self.play(Create(squares), run_time=2)
        self.play(
            Write(frozen_label),
            Write(active_sem_label),
            Write(active_head_label)
        )
        self.wait(1)

        # Animation: Pulse moving through blue and orange squares
        active_indices = [7, 8, 9, 10, 23]
        
        # Create pulse circles for each active layer
        pulses = []
        for idx in active_indices:
            # Create a pulse effect using an expanding circle
            pulse_circle = Circle(radius=0.15, color=WHITE, stroke_width=2).move_to(squares[idx].get_center())
            pulse_anim = Succession(
                FadeIn(pulse_circle, scale=0.5),
                pulse_circle.animate.scale(2.5).set_stroke(opacity=0),
                FadeOut(pulse_circle)
            )
            pulses.append(pulse_anim)

        # Run the pulse sequence multiple times to represent training
        for _ in range(3):
            self.play(
                LaggedStart(*pulses, lag_ratio=0.15),
                run_time=1.5
            )

        self.wait(2)