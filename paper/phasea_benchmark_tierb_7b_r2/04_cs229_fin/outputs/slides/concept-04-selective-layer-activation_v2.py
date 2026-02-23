from manim import *

class SelectiveLayerActivation(Scene):
    def construct(self):
        # Create a horizontal chain of 24 Square objects representing layers 0 to 23
        # We scale them down to fit all 24 on the screen
        layers = VGroup(*[Square(side_length=0.4) for _ in range(24)]).arrange(RIGHT, buff=0.1)
        layers.move_to(ORIGIN)

        # Style the layers according to the instructions
        glows = VGroup()
        for i, layer in enumerate(layers):
            if 0 <= i <= 6:
                # Color layers 0-6 gray (Frozen Backbone)
                layer.set_style(fill_color=GRAY, fill_opacity=0.5, stroke_color=GRAY_A, stroke_width=1)
            elif 7 <= i <= 10:
                # Color layers 7-10 bright blue with a 'Glow' effect (Active Semantics)
                layer.set_style(fill_color=BLUE, fill_opacity=0.8, stroke_color=WHITE, stroke_width=2)
                # Simulating a Glow effect with a larger, semi-transparent square behind
                glow = layer.copy().scale(1.3).set_fill(BLUE, opacity=0.3).set_stroke(width=0)
                glows.add(glow)
            elif 11 <= i <= 22:
                # Color layers 11-22 gray
                layer.set_style(fill_color=GRAY, fill_opacity=0.5, stroke_color=GRAY_A, stroke_width=1)
            elif i == 23:
                # Color layer 23 bright orange (Active Head)
                layer.set_style(fill_color=ORANGE, fill_opacity=0.8, stroke_color=WHITE, stroke_width=2)
                # Simulating a Glow effect
                glow = layer.copy().scale(1.3).set_fill(ORANGE, opacity=0.3).set_stroke(width=0)
                glows.add(glow)

        # Labels for the different sections
        label_frozen = Text("Frozen Backbone", font_size=20).next_to(layers[0:7], UP, buff=0.5)
        label_active_s = Text("Active Semantics", font_size=20, color=BLUE).next_to(layers[7:11], UP, buff=0.5)
        label_active_h = Text("Active Head", font_size=20, color=ORANGE).next_to(layers[23], UP, buff=0.5)
        
        # Group everything and center
        all_mobjects = VGroup(glows, layers, label_frozen, label_active_s, label_active_h)
        all_mobjects.center()

        # Initial display
        self.add(glows, layers)
        self.play(
            Write(label_frozen),
            Write(label_active_s),
            Write(label_active_h)
        )
        self.wait(1)

        # Animate a 'Succession' of pulses moving through the blue and orange squares
        active_indices = [7, 8, 9, 10, 23]
        pulses = [
            Indicate(layers[i], color=WHITE, scale_factor=1.5) 
            for i in active_indices
        ]

        # Use Succession to play them one after another
        self.play(Succession(*pulses, run_time=4))
        
        self.wait(2)