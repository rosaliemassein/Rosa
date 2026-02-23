from manim import *
import random

class SyntheticPileGeneration(Scene):
    def construct(self):
        # 1. Blank white Rectangle representing the canvas
        canvas = Rectangle(width=8, height=5, fill_color=WHITE, fill_opacity=1, stroke_color=GRAY)
        canvas_label = Text("Synthetic Canvas", color=BLACK, font_size=20).to_edge(UP, buff=0.5)
        self.add(canvas, canvas_label)

        # 2. Display five segmented trash icons floating around it
        # We use different shapes with distinct colors as placeholders for segmented icons
        colors = [BLUE, RED, GREEN, YELLOW, ORANGE]
        templates = VGroup(
            Circle(radius=0.4, fill_opacity=1), # Bottle representation
            Rectangle(width=0.6, height=0.8, fill_opacity=1), # Can representation
            Triangle(fill_opacity=1).scale(0.6), # Paper scrap
            RoundedRectangle(width=0.7, height=0.4, corner_radius=0.1, fill_opacity=1), # Cardboard
            Star(color=GOLD, fill_opacity=1).scale(0.5) # Generic trash
        )
        
        for i, icon in enumerate(templates):
            icon.set_color(colors[i])
        
        templates.arrange(DOWN, buff=0.4).to_edge(LEFT, buff=0.5)
        self.add(templates)

        # 3. Use ValueTrackers/DecimalNumbers for 'scale' and 'rotation' display
        scale_label = Text("Current Scale:", font_size=24).to_corner(UL).shift(RIGHT * 0.5)
        scale_val = DecimalNumber(1.0, num_decimal_places=2).next_to(scale_label, RIGHT)
        
        rot_label = Text("Current Rotation:", font_size=24).next_to(scale_label, DOWN, aligned_edge=LEFT)
        rot_val = DecimalNumber(0, num_decimal_places=0, unit="^\\circ").next_to(rot_label, RIGHT)
        
        ui_group = VGroup(scale_label, scale_val, rot_label, rot_val)
        self.add(ui_group)

        # 4. Animate each icon moving onto the canvas (Total 9 objects for a crowded scene)
        random.seed(42)
        pile_objects = VGroup()

        for i in range(9):
            # Select from the templates (cycling through the 5 types)
            source_index = i % 5
            icon_copy = templates[source_index].copy()
            
            # Randomly sample parameters
            target_scale = random.uniform(0.6, 1.8)
            target_rotation = random.uniform(0, TAU)
            # Ensure placement within the white rectangle (canvas) boundaries
            target_position = [
                random.uniform(-3.2, 3.2),
                random.uniform(-1.8, 1.8),
                0
            ]
            
            # Animate the 'sampling' values on the UI
            self.play(
                scale_val.animate.set_value(target_scale),
                rot_val.animate.set_value(target_rotation * 180 / PI),
                run_time=0.25
            )
            
            # Overlap handling: Setting Z-index ensures newer objects can appear above older ones
            icon_copy.set_z_index(i + 1)
            
            # Apply Rotate and Scale transforms as they move to the canvas
            self.play(
                icon_copy.animate.move_to(target_position).scale(target_scale).rotate(target_rotation),
                run_time=0.7
            )
            pile_objects.add(icon_copy)
            self.wait(0.1)

        # Final pause to see the crowded synthetic pile
        self.wait(2)