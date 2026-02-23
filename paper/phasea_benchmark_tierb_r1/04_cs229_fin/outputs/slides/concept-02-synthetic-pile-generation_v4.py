from manim import *
import random

class ConceptScene02(Scene):
    def construct(self):
        # Blank white canvas
        canvas = Rectangle(width=8, height=6, color=WHITE, fill_opacity=0.1)
        canvas_label = Text("Canvas", font_size=24).next_to(canvas, UP)
        self.play(Create(canvas), Write(canvas_label))

        # Segmented trash icons (using different shapes to represent different objects)
        colors = [BLUE, GREEN, RED, YELLOW, ORANGE]
        
        # Define shapes manually to ensure compatibility
        source_icons = VGroup(
            Circle(radius=0.4, color=BLUE, fill_opacity=0.8),
            Square(side_length=0.8, color=GREEN, fill_opacity=0.8),
            Triangle(color=RED, fill_opacity=0.8).scale(0.6),
            Star(color=YELLOW, fill_opacity=0.8).scale(0.5),
            RegularPolygon(n=6, color=ORANGE, fill_opacity=0.8).scale(0.5)
        )
            
        source_icons.arrange(DOWN, buff=0.5).to_edge(LEFT, buff=1)
        source_label = Text("Segmented Objects", font_size=20).next_to(source_icons, UP)
        
        self.play(
            FadeIn(source_icons),
            Write(source_label)
        )
        self.wait(0.5)

        # Labels to show 'scale' and 'rotation' without using ValueTracker or DecimalNumber
        scale_label = Text("Scale: 1.00", font_size=24).to_edge(RIGHT, buff=1).shift(UP)
        rot_label = Text("Rotation: 0.0", font_size=24).next_to(scale_label, DOWN, buff=0.5)

        self.play(FadeIn(scale_label), FadeIn(rot_label))

        # Generate 9 objects onto the canvas
        for i in range(9):
            # Randomly pick a source icon to clone
            original_idx = i % 5
            icon_copy = source_icons[original_idx].copy()
            
            # Generate random transform values
            target_scale = random.uniform(0.6, 1.4)
            target_rotation = random.uniform(0, 360)
            
            # Calculate a random position inside the canvas bounds
            target_pos = [
                random.uniform(-3.0, 3.0),
                random.uniform(-2.0, 2.0),
                0
            ]

            # Create new text objects for the "tracker" display
            new_scale_label = Text(f"Scale: {target_scale:.2f}", font_size=24).move_to(scale_label)
            new_rot_label = Text(f"Rotation: {target_rotation:.1f}", font_size=24).move_to(rot_label)
            
            # Ensure layering by setting z_index
            icon_copy.set_z_index(i)
            
            # Animate the movement and the labels simultaneously
            self.play(
                Transform(scale_label, new_scale_label),
                Transform(rot_label, new_rot_label),
                icon_copy.animate.scale(target_scale).rotate(target_rotation * DEGREES).move_to(target_pos),
                run_time=0.7
            )

        self.wait(3)