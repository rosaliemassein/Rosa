from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Blank canvas represented by a white rectangle
        canvas = Rectangle(width=8, height=6, color=WHITE)
        canvas.set_fill(WHITE, opacity=0.1)
        self.add(canvas)

        # 2. UI Labels for Scale and Rotation (Avoid ValueTracker due to restrictions)
        scale_label = Text("Scale: 1.00", font_size=24).to_corner(UL, buff=0.5)
        rot_label = Text("Rotation: 0°", font_size=24).next_to(scale_label, DOWN, aligned_edge=LEFT)
        self.add(scale_label, rot_label)

        # 3. Define trash icon shapes and standard colors
        colors = [YELLOW, RED, GREEN, BLUE, ORANGE, PURPLE, GOLD, WHITE, GRAY]
        
        icons = []
        for i in range(9):
            c = colors[i % len(colors)]
            shape_type = i % 3
            if shape_type == 0:
                icon = Circle(radius=0.4, color=c, fill_opacity=0.8)
            elif shape_type == 1:
                icon = Square(side_length=0.7, color=c, fill_opacity=0.8)
            else:
                icon = Triangle(color=c, fill_opacity=0.8).scale(0.6)
            
            # Position first 5 floating around the canvas
            if i < 5:
                # Deterministic pseudo-random positions to avoid external dependencies
                x_pos = -5 if i % 2 == 0 else 5
                y_pos = (i - 2) * 1.5
                icon.move_to([x_pos, y_pos, 0])
                self.add(icon)
            icons.append(icon)

        # 4. Animate each icon moving onto the canvas with rotation and scaling
        for i, item in enumerate(icons):
            # If not already on screen, start from the bottom
            if i >= 5:
                item.move_to([0, -4.5, 0])
                self.add(item)
            
            # Deterministic variation for "random" scale, rotation, and position
            s_val = 0.6 + (i * 0.13) % 1.0
            r_val = i * 40
            target_x = ((i * 1.7) % 6) - 3
            target_y = ((i * 1.1) % 4) - 2
            
            # Create updated labels for this step
            new_scale_text = Text(f"Scale: {s_val:.2f}", font_size=24).to_corner(UL, buff=0.5)
            new_rot_text = Text(f"Rotation: {int(r_val)}°", font_size=24).next_to(new_scale_text, DOWN, aligned_edge=LEFT)
            
            # Animate movement, scaling, and rotation simultaneously
            # Objects added later in the loop naturally have higher Z-indices (overlap)
            self.play(
                item.animate.scale(s_val).rotate(r_val * DEGREES).move_to([target_x, target_y, 0]),
                Transform(scale_label, new_scale_text),
                Transform(rot_label, new_rot_text),
                run_time=0.6
            )

        # 5. Hold final scene showing the synthetic pile
        self.wait(2)