from manim import *
import numpy as np

class GravNetMessagePassing(Scene):
    def construct(self):
        # Manual definitions for potentially missing constants
        MY_GOLD = "#FFD700"
        MY_UL = UP + LEFT
        MY_PI = 3.14159265
        
        # 1. Create a scatter plot of dots representing irregular cells
        nodes = VGroup()
        rows, cols = 7, 9
        for i in range(rows):
            for j in range(cols):
                # Basic grid positioning
                x = (j - cols / 2) * 0.9
                y = (i - rows / 2) * 0.9
                # Hexagonal offset
                if i % 2 == 1:
                    x += 0.45
                # Add irregularity
                pos = np.array([
                    x + np.random.uniform(-0.15, 0.15),
                    y + np.random.uniform(-0.15, 0.15),
                    0
                ])
                dot = Dot(point=pos, radius=0.08, color=WHITE)
                nodes.add(dot)

        # 2. Identify the central dot
        center_index = len(nodes) // 2 + 2
        center_node = nodes[center_index]

        # 3. Formula for distance-weighting (using Text since MathTex is disallowed)
        formula = Text("V = exp(-d^2)", color=MY_GOLD).scale(0.7)
        formula.to_edge(MY_UL)

        # 4. Create connections (arrows) with dynamic updaters
        # Using a list and then VGroup to manage connections
        arrows = VGroup()
        
        for node in nodes:
            if node == center_node:
                continue
            
            # Initial arrow
            arrow = Arrow(
                center_node.get_center(), 
                node.get_center(), 
                buff=0.1, 
                color=MY_GOLD,
                max_tip_length_to_length_ratio=0.15
            )
            
            # Define updater function to handle dynamic scaling
            def update_connection(arr_obj, target_node=node):
                p1 = center_node.get_center()
                p2 = target_node.get_center()
                dist = np.linalg.norm(p1 - p2)
                
                # Connection weight formula: exp(-d^2)
                # We scale the distance for better visual effect in 2D space
                weight = np.exp(-(dist**2) / 3.0)
                
                # Check for visibility threshold
                if weight < 0.05:
                    arr_obj.set_opacity(0)
                else:
                    # Re-render the arrow based on new positions
                    new_arrow = Arrow(
                        p1, p2, 
                        buff=0.1, 
                        color=MY_GOLD, 
                        stroke_width=weight * 10
                    )
                    arr_obj.become(new_arrow)
                    arr_obj.set_opacity(weight)

            arrow.add_updater(update_connection)
            arrows.add(arrow)

        # 5. Build Animation Sequence
        self.add(nodes)
        self.play(
            center_node.animate.set_color(RED).scale(1.4),
            Write(formula),
            run_time=1.5
        )
        self.add(arrows)
        self.wait(1)

        # 6. "Learned Features" update - Dynamic node movement
        # Prepare random movement for every node
        move_actions = []
        for node in nodes:
            # Shift nodes to simulate the transition in learned feature space
            new_pos = node.get_center() + np.array([
                np.random.uniform(-1.2, 1.2),
                np.random.uniform(-1.2, 1.2),
                0
            ])
            # Keep dots roughly within screen bounds
            new_pos[0] = np.clip(new_pos[0], -6, 6)
            new_pos[1] = np.clip(new_pos[1], -3, 3)
            move_actions.append(node.animate.move_to(new_pos))

        # Text explanation for the animation segment
        explanation = Text(
            "Graph structure updates in learned feature space",
            font_size=24
        ).to_edge(DOWN)
        
        self.play(
            *move_actions,
            FadeIn(explanation),
            run_time=6
        )
        
        self.wait(2)
        
        # 7. Final fade out
        self.play(
            FadeOut(arrows),
            FadeOut(nodes),
            FadeOut(formula),
            FadeOut(explanation)
        )
        self.wait(1)