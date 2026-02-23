from manim import *

class SelectiveLayerActivation(Scene):
    def construct(self):
        # Create horizontal chain of 24 'Square' objects representing layers 0 to 23
        squares = VGroup(*[
            Square(side_length=0.3, fill_opacity=0.6, stroke_width=2) 
            for _ in range(24)
        ])
        squares.arrange(RIGHT, buff=0.1)
        squares.center()

        # Color layers according to the strategy
        # Layers 0-6: Gray (Frozen Backbone)
        for i in range(0, 7):
            squares[i].set_fill(GRAY, opacity=0.5)
            squares[i].set_color(GRAY)
        
        # Layers 7-10: Bright Blue (Active Semantics)
        for i in range(7, 11):
            squares[i].set_fill(BLUE, opacity=0.8)
            squares[i].set_color(BLUE)
            
        # Layers 11-22: Gray
        for i in range(11, 23):
            squares[i].set_fill(GRAY, opacity=0.5)
            squares[i].set_color(GRAY)
            
        # Layer 23: Bright Orange (Active Head)
        squares[23].set_fill(ORANGE, opacity=0.8)
        squares[23].set_color(ORANGE)

        # Labels
        frozen_label = Text("Frozen Backbone", font_size=16, color=GRAY).next_to(squares[0:7], UP, buff=0.5)
        active_semantics_label = Text("Active Semantics", font_size=16, color=BLUE).next_to(squares[7:11], UP, buff=0.5)
        active_head_label = Text("Active Head", font_size=16, color=ORANGE).next_to(squares[23], UP, buff=0.5)
        
        labels = VGroup(frozen_label, active_semantics_label, active_head_label)

        # Create glow effect for active layers (7-10 and 23)
        # Using larger strokes to simulate glow
        glows = VGroup()
        active_indices = [7, 8, 9, 10, 23]
        for i in active_indices:
            glow = squares[i].copy()
            glow.set_stroke(squares[i].get_color(), width=10, opacity=0.3)
            glow.scale(1.15)
            glows.add(glow)

        # Initial Animation
        self.play(Create(squares), run_time=1.5)
        self.play(Write(labels))
        self.play(FadeIn(glows))
        self.wait(0.5)

        # Succession of pulses moving through the blue and orange squares
        # We use Indicate which provides a "there and back" scaling and coloring pulse
        pulses = [
            Indicate(squares[7], color=BLUE, scale_factor=1.4),
            Indicate(squares[8], color=BLUE, scale_factor=1.4),
            Indicate(squares[9], color=BLUE, scale_factor=1.4),
            Indicate(squares[10], color=BLUE, scale_factor=1.4),
            Indicate(squares[23], color=ORANGE, scale_factor=1.4)
        ]

        self.play(Succession(*pulses), run_time=3)
        
        # Second pass of updates to represent iterative training
        self.play(
            LaggedStart(
                *[Indicate(squares[i], scale_factor=1.3) for i in active_indices],
                lag_ratio=0.15
            ),
            run_time=2
        )

        self.wait(2)