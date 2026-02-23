from manim import *
import numpy as np

class GravNetMessagePassing(Scene):
    def construct(self):
        # 1. Create a scatter plot of dots representing ECal cells in an irregular grid
        dots = VGroup()
        spacing = 0.8
        # Generate a jittered grid to simulate irregular detector geometry in 2D
        for i in range(-5, 6):
            for j in range(-4, 5):
                # Offset every other row for a hexagonal-like layout
                x_offset = 0.4 * spacing if j % 2 == 0 else 0
                pos = np.array([i * spacing + x_offset, j * spacing * 0.866, 0])
                # Add irregularity (jitter)
                pos += np.array([np.random.uniform(-0.2, 0.2), np.random.uniform(-0.2, 0.2), 0])
                dot = Dot(point=pos, radius=0.08, color=GRAY_B)
                dots.add(dot)

        # 2. Highlight one central dot
        central_dot = Dot(point=ORIGIN, radius=0.12, color=BLUE)
        # Add central dot to the dots group to include it in transformations
        dots.add(central_dot)
        
        # 3. Connections representing dynamic graph connections (weighted by distance)
        connections = VGroup()
        
        # Identify local neighbors to connect to the central dot
        for dot in dots:
            if dot == central_dot:
                continue
            
            # Check distance to define a local neighborhood
            dist = np.linalg.norm(dot.get_center() - central_dot.get_center())
            if dist < 2.2:
                # Create a line between the central node and neighbors
                # Using Line as a base for weighted arrows for cleaner scaling
                line = Line(central_dot.get_center(), dot.get_center(), color=WHITE)
                line.target_node = dot # Store reference to the neighbor dot
                
                # Define dynamic behavior using an updater to reflect distance-weighted connections
                def update_line_weight(obj):
                    start = central_dot.get_center()
                    end = obj.target_node.get_center()
                    # Calculate Euclidean distance d_jk
                    d = np.linalg.norm(end - start)
                    # Apply formula: V_jk = exp(-d^2)
                    weight = np.exp(-(d**2))
                    # Update position and appearance
                    obj.put_start_and_end_on(start, end)
                    # Scale thickness and opacity based on the learned potential
                    obj.set_stroke(width=weight * 14, opacity=weight)
                
                line.add_updater(update_line_weight)
                connections.add(line)

        # Formula display (V_jk = exp(-d^2))
        formula = MathTex(r"V_{jk} = \exp(-d_{jk}^2)", color=YELLOW).to_edge(UP)
        
        # 4. Background dots and initial state animation
        self.add(dots, connections)
        self.play(Write(formula))
        self.play(Indicate(central_dot, color=BLUE, scale_factor=1.4))
        self.wait(1)

        # 5. Animate the 'learned features' update
        # Dots move slightly to show the graph structure is not fixed by physical geometry
        move_anims = []
        for dot in dots:
            # Random drift for each hit in the feature space
            shift_vector = np.array([
                np.random.uniform(-1.2, 1.2), 
                np.random.uniform(-1.2, 1.2), 
                0
            ])
            move_anims.append(dot.animate.shift(shift_vector))
        
        # Run the movement animation; the lines update automatically due to the updaters
        self.play(AnimationGroup(*move_anims), run_time=5)
        self.wait(2)