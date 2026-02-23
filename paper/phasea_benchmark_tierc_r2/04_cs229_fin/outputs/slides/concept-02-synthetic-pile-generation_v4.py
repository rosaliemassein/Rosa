import numpy as np
from manim import *

class Concept02SyntheticPileGeneration(Scene):
    def construct(self):
        # 1. Blank white Rectangle representing the canvas
        canvas = Rectangle(width=8, height=5.5, color=WHITE, stroke_width=2)
        canvas.set_fill(WHITE, opacity=0.05)
        self.add(canvas)

        # 2. Five segmented trash icons (placeholder shapes) floating around
        # We'll place them to the right of the canvas initially
        icon_templates = VGroup(
            Circle(color=RED, fill_opacity=0.8),
            Square(color=BLUE, fill_opacity=0.8),
            Triangle(color=GREEN, fill_opacity=0.8),
            Star(color=YELLOW, fill_opacity=0.8),
            RegularPolygon(n=6, color=ORANGE, fill_opacity=0.8)
        ).scale(0.4)
        
        icon_templates.arrange(DOWN, buff=0.4).to_edge(RIGHT, buff=0.5)
        
        icon_label = Text("Source Icons", font_size=24).next_to(icon_templates, UP)
        self.add(icon_templates, icon_label)

        # 3. ValueTracker to show random numbers for 'scale' and 'rotation'
        scale_tracker = ValueTracker(1.0)
        rotation_tracker = ValueTracker(0)

        # Labels for the trackers
        scale_val = DecimalNumber(1.0, num_decimal_places=2).scale(0.8)
        rotation_val = DecimalNumber(0, num_decimal_places=0).scale(0.8)

        scale_display = VGroup(
            Text("Scale: ", font_size=30),
            scale_val
        ).arrange(RIGHT).to_corner(UL, buff=0.5)
        
        rotation_display = VGroup(
            Text("Rotation: ", font_size=30),
            rotation_val,
            Text("°", font_size=30)
        ).arrange(RIGHT, buff=0.1).next_to(scale_display, DOWN, aligned_edge=LEFT)

        # Using named functions for updaters to avoid identifier issues
        def update_scale_val(mob):
            mob.set_value(scale_tracker.get_value())

        def update_rotation_val(mob):
            mob.set_value(rotation_tracker.get_value())

        scale_val.add_updater(update_scale_val)
        rotation_val.add_updater(update_rotation_val)

        self.add(scale_display, rotation_display)

        # 4. Animate icons moving onto the canvas (9 objects total)
        # We ensure they overlap by using random positions and increasing Z-indices
        for i in range(9):
            # Select a random template index
            source_idx = i % 5
            source_icon = icon_templates[source_idx]
            
            # Generate random transformation values
            target_scale = np.random.uniform(0.6, 1.8)
            target_rotation = np.random.uniform(0, 360)
            target_pos = [
                np.random.uniform(-3, 1), # Within canvas X
                np.random.uniform(-2, 2), # Within canvas Y
                0
            ]

            # Update tracker values visually
            self.play(
                scale_tracker.animate.set_value(target_scale),
                rotation_tracker.animate.set_value(target_rotation),
                run_time=0.3
            )

            # Create a copy and animate movement onto canvas
            moving_icon = source_icon.copy()
            # Explicitly set layering
            moving_icon.set_z_index(i + 1)
            
            self.play(
                moving_icon.animate.move_to(target_pos)
                .scale(target_scale)
                .rotate(target_rotation * DEGREES),
                run_time=0.7
            )

        self.wait(2)