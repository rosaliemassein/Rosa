from manim import *
import numpy as np
import random

class SyntheticPileGeneration(Scene):
    def construct(self):
        # 1. Blank canvas (White rectangle)
        # We use a white rectangle to represent the canvas as per the remarks.
        canvas = Rectangle(width=10, height=6, color=WHITE, fill_opacity=1)
        canvas_border = Rectangle(width=10, height=6, color=GRAY)
        canvas_label = Text("Synthetic Canvas", color=BLACK).scale(0.6).to_edge(UP, buff=0.2)
        self.add(canvas, canvas_border, canvas_label)

        # 2. UI for Scale/Rotation
        # Since ValueTracker and DecimalNumber are disallowed, we use Text and .become()
        info_bg = Rectangle(width=3.5, height=1.5, color=BLACK, fill_opacity=0.9).to_corner(UL, buff=0.2)
        info_border = Rectangle(width=3.5, height=1.5, color=WHITE).move_to(info_bg)
        
        scale_label = Text("Scale: 1.00", font_size=24, color=WHITE).move_to(info_bg.get_center() + UP * 0.3)
        rot_label = Text("Rotate: 0 deg", font_size=24, color=WHITE).move_to(info_bg.get_center() + DOWN * 0.3)
        
        self.add(info_bg, info_border, scale_label, rot_label)

        # 3. Trash "Icons" templates
        # Using basic shapes with distinct colors to represent segmented objects
        icon_types = [
            lambda: Rectangle(width=0.4, height=0.9, color=BLUE, fill_opacity=1),   # Bottle-like
            lambda: Circle(radius=0.35, color=GREEN, fill_opacity=1),               # Can-like
            lambda: Square(side_length=0.6, color=YELLOW, fill_opacity=1),          # Paper-like
            lambda: Triangle(color=RED, fill_opacity=1).scale(0.5),                 # Scrap-like
            lambda: RegularPolygon(n=6, color=PURPLE, fill_opacity=1).scale(0.4)    # Misc-like
        ]

        # 4. Process Loop (9 objects as per remarks)
        for i in range(9):
            # Select a shape from our "segmented" icons
            icon = icon_types[i % len(icon_types)]()
            
            # Start the icon at a random floating position off-center
            start_x = random.choice([-5.5, 5.5])
            start_y = random.uniform(-3, 3)
            icon.move_to([start_x, start_y, 0])
            
            # Sample random target values for synthetic generation
            s_factor = round(random.uniform(0.6, 1.7), 2)
            r_angle = random.randint(0, 359)
            target_x = random.uniform(-3.5, 3.5)
            target_y = random.uniform(-2, 2)

            # Prepare the updated text for UI
            new_scale_label = Text(f"Scale: {s_factor:.2f}", font_size=24, color=WHITE).move_to(scale_label)
            new_rot_label = Text(f"Rotate: {r_angle} deg", font_size=24, color=WHITE).move_to(rot_label)

            # Animate the "sampling" phase
            self.play(
                FadeIn(icon),
                scale_label.animate.become(new_scale_label),
                rot_label.animate.become(new_rot_label),
                run_time=0.4
            )

            # Move onto canvas with layering (Z-index ensures overlapping)
            icon.set_z_index(i + 1)
            self.play(
                icon.animate.move_to([target_x, target_y, 0]).scale(s_factor).rotate(r_angle * DEGREES),
                run_time=0.7
            )
            self.wait(0.1)

        self.wait(2)