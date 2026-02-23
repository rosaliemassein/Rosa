from manim import *
import numpy as np

class SyntheticPileGeneration(Scene):
    def construct(self):
        # 1. Create the blank white canvas (Rectangle outline)
        canvas = Rectangle(width=7, height=4.5, color=WHITE)
        canvas_label = Text("Synthetic Canvas", font_size=24).next_to(canvas, UP)
        self.play(Create(canvas), Write(canvas_label))

        # 2. Define five segmented trash icons (simplified shapes)
        # We use standard polygons and shapes
        icons = [
            Circle(radius=0.4, color=RED, fill_opacity=0.7),
            Square(side_length=0.7, color=BLUE, fill_opacity=0.7),
            Triangle(color=GREEN, fill_opacity=0.7).scale(0.6),
            Rectangle(width=0.3, height=0.8, color=YELLOW, fill_opacity=0.7),
            RegularPolygon(n=5, color=PURPLE, fill_opacity=0.7).scale(0.5)
        ]
        
        # Position icons floating at the top initially
        floating_icons = VGroup(*icons).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.2)
        self.play(FadeIn(floating_icons))

        # 3. Setup labels to track random parameters
        # We use Text and Transform since ValueTracker/DecimalNumber are disallowed/undefined
        scale_label = Text("Scale: 1.00", font_size=20).to_edge(RIGHT, buff=0.8).shift(UP * 0.5)
        rot_label = Text("Rotation: 0", font_size=20).next_to(scale_label, DOWN, buff=0.4)
        self.add(scale_label, rot_label)

        # 4. Generate the synthetic pile (9 objects total)
        # Objects are layered by being added to the scene sequentially
        for i in range(9):
            # Select one of the 5 templates
            template_index = i % 5
            original_shape = icons[template_index]
            item = original_shape.copy()
            
            # Generate random transform values
            random_scale = 0.6 + (np.random.random() * 0.8) # range [0.6, 1.4]
            random_degree = np.random.random() * 360
            target_x = np.random.uniform(-2.8, 2.8)
            target_y = np.random.uniform(-1.8, 1.8)
            target_pos = [target_x, target_y, 0]
            
            # Prepare updated text for parameters
            new_s_text = Text(f"Scale: {random_scale:.2f}", font_size=20).move_to(scale_label)
            new_r_text = Text(f"Rotation: {int(random_degree)}", font_size=20).move_to(rot_label)
            
            # Animate the icon moving onto the canvas with scale and rotation
            # We use .animate.rotate() instead of Rotate() to avoid undefined identifier issues
            self.play(
                item.animate.move_to(target_pos).scale(random_scale).rotate(random_degree * PI / 180),
                Transform(scale_label, new_s_text),
                Transform(rot_label, new_r_text),
                run_time=0.7
            )

        self.wait(2)