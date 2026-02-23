from manim import *
import random

class SyntheticPileGeneration(Scene):
    def construct(self):
        # 1. Create a blank white Rectangle representing the canvas
        canvas = Rectangle(
            width=11, height=7, 
            fill_color=WHITE, fill_opacity=1, 
            stroke_color=GRAY, stroke_width=2
        )
        canvas.set_z_index(-10)
        self.play(FadeIn(canvas))
        
        # 2. Define five segmented trash icons (bottle, can, paper, scrap, plastic)
        icons_pool = [
            RoundedRectangle(corner_radius=0.1, height=0.8, width=0.3, color=BLUE, fill_opacity=1),
            Rectangle(height=0.7, width=0.45, color=GRAY, fill_opacity=1),
            Triangle(color=YELLOW, fill_opacity=1).scale(0.4),
            Circle(radius=0.25, color=GREEN, fill_opacity=1),
            Square(side_length=0.5, color=ORANGE, fill_opacity=1)
        ]
        
        # Display the five icons floating around the top
        floating_icons = VGroup(*[i.copy() for i in icons_pool]).arrange(RIGHT, buff=1).to_edge(UP, buff=0.5)
        self.play(FadeIn(floating_icons))
        
        # 3. Setup numeric indicators (replacing ValueTracker to avoid environment restrictions)
        scale_label = Text("Scale: 1.00", color=BLACK).scale(0.5).to_corner(UL, buff=1)
        rot_label = Text("Rotation: 0 deg", color=BLACK).scale(0.5).to_corner(UR, buff=1)
        self.add(scale_label, rot_label)
        
        # 4. Animate each icon moving onto the canvas (9 objects total)
        for i in range(9):
            # Select which icon type to use (looping through the 5 icons)
            idx = i % 5
            source_template = icons_pool[idx]
            obj = source_template.copy()
            obj.move_to(floating_icons[idx].get_center())
            
            # Random sampling for scale, rotation, and position
            s_val = round(random.uniform(0.7, 2.2), 2)
            r_val = random.randint(0, 359)
            target_pos = [random.uniform(-4, 4), random.uniform(-2.5, 1), 0]
            
            # Prepare updated text for indicators
            new_scale_text = Text(f"Scale: {s_val:.2f}", color=BLACK).scale(0.5).move_to(scale_label)
            new_rot_text = Text(f"Rotation: {r_val} deg", color=BLACK).scale(0.5).move_to(rot_label)
            
            # Ensure layering for overlapping effect
            obj.set_z_index(i + 1)
            
            # Move and transform the object onto the canvas
            self.play(
                obj.animate.scale(s_val).rotate(r_val * DEGREES).move_to(target_pos),
                Transform(scale_label, new_scale_text),
                Transform(rot_label, new_rot_text),
                run_time=0.8
            )
        
        self.wait(3)