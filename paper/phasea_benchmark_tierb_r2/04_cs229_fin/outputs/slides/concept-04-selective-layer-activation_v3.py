from manim import *

class Concept04SelectiveLayerActivation(Scene):
    def construct(self):
        # Create a horizontal chain of 24 'Square' objects representing layers 0 to 23
        layers = VGroup(*[
            Square(side_length=0.35, fill_opacity=0.6) 
            for _ in range(24)
        ])
        layers.arrange(RIGHT, buff=0.15)
        layers.move_to(UP * 1.5)

        # Color layers 0-6 gray (labeled 'Frozen Backbone')
        for i in range(0, 7):
            layers[i].set_color(GRAY)
        
        # Color layers 7-10 bright blue with a 'Glow' effect (labeled 'Active Semantics')
        for i in range(7, 11):
            layers[i].set_color(BLUE)
            layers[i].set_stroke(BLUE, width=6)
        
        # Color layers 11-22 gray
        for i in range(11, 23):
            layers[i].set_color(GRAY)
        
        # Color layer 23 bright orange (labeled 'Active Head')
        layers[23].set_color(ORANGE)
        layers[23].set_stroke(ORANGE, width=6)

        # Labels
        frozen_label = Text("Frozen Backbone", font_size=20, color=GRAY).next_to(layers[0:7], DOWN, buff=0.4)
        active_sem_label = Text("Active Semantics", font_size=20, color=BLUE).next_to(layers[7:11], UP, buff=0.4)
        active_head_label = Text("Active Head", font_size=20, color=ORANGE).next_to(layers[23], UP, buff=0.4)

        # Narration text (Replaced Paragraph with Text and line breaks for compatibility)
        narration_str = (
            "The breakthrough in efficiency came from 'targeted' fine-tuning.\n"
            "Instead of retraining the whole YOLO model, the team froze\n"
            "the backbone and only activated high-level semantic layers (7-10)\n"
            "and the classification head (23), achieving 86% accuracy."
        )
        narration = Text(narration_str, font_size=24, line_spacing=0.8).to_edge(DOWN, buff=0.5)

        # Try to load image as mentioned in prompt
        try:
            image = ImageMobject("img-10.jpeg")
            image.scale(1.2).move_to(ORIGIN)
            self.add(image)
        except:
            # If image missing, continue without it
            pass

        # Add components to scene
        self.add(layers, frozen_label, active_sem_label, active_head_label, narration)

        # Define pulses for layers 7, 8, 9, 10, and 23
        active_indices = [7, 8, 9, 10, 23]
        pulses = [
            Flash(
                layers[i], 
                color=layers[i].get_color(), 
                flash_radius=0.4, 
                line_length=0.2,
                run_time=0.5
            ) 
            for i in active_indices
        ]

        # Animate a 'Succession' of pulses moving through the selected squares
        self.play(Succession(*pulses))
        
        # Continuous animation of pulses to represent "gradients updating"
        self.play(
            AnimationGroup(
                *[Indicate(layers[i], scale_factor=1.2, color=layers[i].get_color()) for i in active_indices],
                run_time=2,
                lag_ratio=0.2
            )
        )

        self.wait(2)