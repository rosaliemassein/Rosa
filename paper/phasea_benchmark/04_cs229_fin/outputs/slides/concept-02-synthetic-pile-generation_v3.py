from manim import *
import numpy as np

class Concept02SyntheticPileGeneration(Scene):
    def construct(self):
        # Create a blank white canvas representing the workspace
        canvas = Rectangle(width=6.5, height=4.5, color=WHITE, fill_opacity=1)
        canvas_outline = Rectangle(width=6.5, height=4.5, color=GRAY)
        self.add(canvas, canvas_outline)

        # Segmented trash icons (5 types)
        # Using standard colors to avoid identifier errors
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE]
        
        icon_templates = [
            Circle(radius=0.35),
            Square(side_length=0.6),
            Triangle().scale(0.5),
            RoundedRectangle(width=0.7, height=0.4, corner_radius=0.1),
            RegularPolygon(n=5).scale(0.4)
        ]

        base_icons = VGroup()
        for i, shape in enumerate(icon_templates):
            shape.set_fill(colors[i], opacity=1)
            shape.set_stroke(color=BLACK, width=1)
            # Position icons outside the canvas initially
            pos_x = 5.0 if i > 2 else -5.0
            pos_y = (i % 3) * 1.5 - 1.5
            shape.move_to([pos_x, pos_y, 0])
            base_icons.add(shape)

        self.add(base_icons)

        # UI labels for script variables (simulating trackers)
        scale_label = Text("Scale: 1.00", font_size=24).to_corner(UL).shift(RIGHT * 0.5).set_color(BLACK)
        rot_label = Text("Rotation: 0", font_size=24).next_to(scale_label, DOWN, aligned_edge=LEFT).set_color(BLACK)
        self.add(scale_label, rot_label)

        # Process: Randomly sample, scale, and rotate 9 objects onto the canvas
        # We pre-define some deterministic "random" values for stability
        for i in range(9):
            # Sampling: copy one of the base icons
            sample_idx = i % 5
            moving_icon = base_icons[sample_idx].copy()
            
            # Simulated random transformations
            s_val = 0.7 + (i * 0.13) % 0.6
            r_val = (i * 37) % 360
            pos_x = (i * 1.1) % 5.0 - 2.5
            pos_y = (i * 0.9) % 3.0 - 1.5
            
            # Prepare updated text for the labels
            new_scale_text = Text(f"Scale: {s_val:.2f}", font_size=24).move_to(scale_label).set_color(BLACK)
            new_rot_text = Text(f"Rotation: {int(r_val)}", font_size=24).move_to(rot_label).set_color(BLACK)
            
            # Increase Z-index to show layering/overlap
            moving_icon.set_z_index(i + 1)
            
            # Animate the creation process
            self.play(
                moving_icon.animate.move_to([pos_x, pos_y, 0]).scale(s_val).rotate(r_val * DEGREES),
                Transform(scale_label, new_scale_text),
                Transform(rot_label, new_rot_text),
                run_time=0.6
            )

        self.wait(2)