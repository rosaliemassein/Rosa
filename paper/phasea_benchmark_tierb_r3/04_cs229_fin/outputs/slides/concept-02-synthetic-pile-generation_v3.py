from manim import *

class ConceptPileCreation(Scene):
    def construct(self):
        # 1. Setup Canvas (A white rectangle representing the training canvas)
        canvas = Rectangle(width=7, height=5, fill_color=WHITE, fill_opacity=1, stroke_color=GRAY)
        self.play(Create(canvas))
        
        # 2. Setup Icons (Representing segmented trash objects)
        # Using basic standard colors to avoid undefined identifier errors
        object_colors = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, GRAY, BLUE, RED]
        icons = VGroup()
        for i in range(5):
            # Create a mix of simple shapes to represent different trash items
            if i % 2 == 0:
                icon = Circle(radius=0.4, fill_opacity=1, color=object_colors[i])
            else:
                icon = Square(side_length=0.7, fill_opacity=1, color=object_colors[i])
            # Position them floating on the left side
            icon.move_to([-5.5, 2 - i * 1, 0])
            icons.add(icon)
        
        self.play(FadeIn(icons))
        
        # 3. Parameter Display Headers (Static text labels)
        scale_header = Text("Scale:", font_size=24).to_corner(UR, buff=0.5).shift(LEFT * 2)
        rotate_header = Text("Rotation:", font_size=24).next_to(scale_header, DOWN, aligned_edge=LEFT)
        self.add(scale_header, rotate_header)
        
        # 4. Dataset Generation Data (Predetermined "random" values for rotation and scale)
        # Each tuple: (pos_x, pos_y, scale_val, rotation_deg)
        generation_steps = [
            (0.1, 0.1, 1.2, 45), 
            (1.2, 0.8, 0.9, 110), 
            (-1.0, 0.5, 1.3, 30),
            (0.4, -1.2, 1.0, 190), 
            (-1.2, -0.7, 0.8, 15), 
            (1.5, -0.6, 1.4, 260),
            (-0.2, 1.3, 0.9, 75), 
            (0.7, 0.3, 1.1, 305), 
            (-0.4, -0.1, 0.7, 145)
        ]
        
        pile_objects = []
        
        # 5. Iteratively place 9 objects onto the canvas
        for i in range(9):
            if i < 5:
                # Use one of the existing floating icons
                active_obj = icons[i]
            else:
                # Create a new segmented icon from the right side
                active_obj = Triangle().scale(0.4).set_fill(object_colors[i], opacity=1).set_color(object_colors[i])
                active_obj.move_to([5.5, 2 - (i-5) * 1.2, 0])
                self.play(FadeIn(active_obj), run_time=0.2)
            
            px, py, ps, pr = generation_steps[i]
            
            # Display current "sampled" parameters using Text
            scale_val_text = Text(str(ps), font_size=24).next_to(scale_header, RIGHT)
            rotate_val_text = Text(str(pr) + " deg", font_size=24).next_to(rotate_header, RIGHT)
            self.add(scale_val_text, rotate_val_text)
            
            # Set Z-index to handle layering/overlapping
            active_obj.set_z_index(i + 1)
            
            # Convert degrees to radians for the rotation transform
            rotation_rad = pr * 3.14159265 / 180.0
            
            # Animate the object moving, scaling, and rotating onto the canvas
            self.play(
                active_obj.animate.move_to([px, py, 0]).scale(ps).rotate(rotation_rad),
                run_time=0.6
            )
            
            # Adjust opacity for some objects to highlight the "pile" layering effect
            if i > 4:
                active_obj.set_fill(opacity=0.7)
            
            # Cleanup current step text labels
            self.remove(scale_val_text, rotate_val_text)
            pile_objects.append(active_obj)
        
        # Final display of the synthetic pile
        self.wait(2)