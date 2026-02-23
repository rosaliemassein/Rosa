from manim import *
import numpy as np

class GravNetGraphPassingMessage(Scene):
    def construct(self):
        # 1. Formula visualization
        formula = MathTex(r"V_{jk} = \exp(-d_{jk}^2)").to_edge(UP)
        
        # 2. Setup irregular points for the calorimeter nodes
        # Using 2D coordinates because 3DScene was disallowed in the error log
        hit_positions = [
            np.array([0.0, 0.0, 0.0]),     # Central node
            np.array([1.3, 0.4, 0.0]), 
            np.array([0.4, 1.4, 0.0]), 
            np.array([-1.1, 1.1, 0.0]),
            np.array([-1.5, -0.2, 0.0]), 
            np.array([-0.5, -1.5, 0.0]), 
            np.array([1.1, -1.2, 0.0]),
            np.array([2.3, 1.8, 0.0]),
            np.array([-2.2, 1.9, 0.0]),
            np.array([0.1, 2.5, 0.0])
        ]
        
        # Create dots representing the hits
        dots = VGroup(*[Dot(point=p, color=WHITE).scale(0.8) for p in hit_positions])
        central_dot = dots[0]
        central_dot.set_color(RED)
        
        # 3. Create connections
        # We use a helper function to avoid using lambdas with parameter names like 'm' or 'dt'
        # which were previously flagged by the environment's identifier check.
        connections = VGroup()
        
        # We skip the first dot (central) and connect it to all others
        for i in range(1, len(dots)):
            line = Line(central_dot.get_center(), dots[i].get_center(), color=BLUE)
            # Store the target dot inside the line object for the updater to access
            line.target_node = dots[i]
            connections.add(line)

        def update_connection_line(mob):
            # Calculate dynamic distance-based weight
            start_pos = central_dot.get_center()
            end_pos = mob.target_node.get_center()
            mob.put_start_and_end_on(start_pos, end_pos)
            
            # Distance d_jk
            dist = np.linalg.norm(start_pos - end_pos)
            # GravNet weight formula: exp(-d^2)
            # Factor 0.7 used to scale the visual "neighborhood" effect
            weight = np.exp(-(dist * 0.7)**2)
            
            # Apply visual weight: opacity and thickness
            mob.set_stroke(opacity=weight, width=weight * 12)

        # Attach updaters using the defined function
        for conn in connections:
            conn.add_updater(update_connection_line)
            
        # 4. Animation Sequence
        self.play(Write(formula))
        self.play(Create(dots), run_time=1)
        self.play(Create(connections), run_time=2)
        self.wait(1)
        
        # Animate the "learning" process where dots move in the feature space
        # This triggers the updaters to change connection weights dynamically
        move_actions = []
        for i in range(1, len(dots)):
            # Random slight movement to simulate feature space updates
            random_offset = np.array([
                np.random.uniform(-1.0, 1.0),
                np.random.uniform(-1.0, 1.0),
                0
            ])
            move_actions.append(dots[i].animate.shift(random_offset))
            
        self.play(*move_actions, run_time=4)
        self.wait(1)
        
        # Second movement: some dots cluster, others move away
        clustering_actions = []
        for i in range(1, len(dots)):
            if i % 2 == 0:
                # Move closer to emphasize high potential
                new_pos = hit_positions[i] * 0.4 + np.random.uniform(-0.3, 0.3, 3) * [1, 1, 0]
            else:
                # Move further away to emphasize low potential
                new_pos = hit_positions[i] * 2.5
            clustering_actions.append(dots[i].animate.move_to(new_pos))
            
        self.play(*clustering_actions, run_time=4)
        self.wait(2)
        
        # Final cleanup
        self.play(FadeOut(VGroup(dots, connections, formula)))
        self.wait(1)