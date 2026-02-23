from manim import *
import numpy as np

class GravNetMessagePassing(Scene):
    def construct(self):
        # Create a 2D scatter plot of dots representing ECal cells
        # Note: 3D features are restricted, so we simulate the irregular geometry in 2D
        dots = VGroup()
        # Generate points in a roughly hexagonal irregular grid
        for x in range(-3, 4):
            for y in range(-2, 3):
                # Offset every other row for hexagonal layout
                shift_x = 0.5 if y % 2 == 0 else 0
                # Add noise to represent the irregular LDMX calorimeter geometry
                pos_x = x + shift_x + np.random.uniform(-0.15, 0.15)
                pos_y = y * 0.85 + np.random.uniform(-0.15, 0.15)
                dot = Dot(point=[pos_x, pos_y, 0], radius=0.08, color=GRAY)
                dots.add(dot)

        # Central dot to highlight and act as the node processing local connections
        central_idx = len(dots) // 2
        central_dot = dots[central_idx]

        self.add(dots)
        self.play(FadeIn(dots))
        self.play(central_dot.animate.set_color(RED).scale(1.3))
        self.wait(0.5)

        # Potential formula reference: V = exp(-d^2)
        formula = MathTex(r"V_{jk} = \exp(-d_{jk}^2)").to_corner(UL)
        self.play(Write(formula))

        # VGroup to hold dynamic connection arrows with an updater
        connection_layer = VGroup()

        def update_connections(vg):
            # Clear previous arrows and calculate new ones based on dynamic dot positions
            new_submobjects = []
            c_pos = central_dot.get_center()
            
            for dot in dots:
                if dot == central_dot:
                    continue
                
                d_pos = dot.get_center()
                # Euclidean distance in the learned feature space (here simulated in 2D)
                dist = np.linalg.norm(c_pos - d_pos)
                # Connection strength weighted by potential
                weight = np.exp(-(dist**2))
                
                # Show connections that have a meaningful strength
                if weight > 0.05:
                    # Arrow parameters scale with the connection weight
                    arr = Arrow(
                        start=c_pos,
                        end=d_pos,
                        buff=0.05,
                        stroke_width=weight * 10,
                        max_tip_length_to_length_ratio=0.2,
                        color=BLUE
                    )
                    arr.set_opacity(weight)
                    new_submobjects.append(arr)
            
            vg.set_submobjects(new_submobjects)

        # Attach updater for continuous recalculation during movement
        connection_layer.add_updater(update_connections)
        self.add(connection_layer)
        self.wait(1)

        # Animate dots moving to simulate updates in "learned features"
        # As dots move, the updater dynamically shifts the connections and their weights
        dot_moves = []
        for dot in dots:
            target = dot.get_center() + np.array([
                np.random.uniform(-1.0, 1.0),
                np.random.uniform(-1.0, 1.0),
                0
            ])
            dot_moves.append(dot.animate.move_to(target))

        self.play(*dot_moves, run_time=5)
        self.wait(1)

        # Narrative text explaining the dynamic nature of GravNet
        conclusion = Text(
            "Graph structure is determined by learned feature distance.",
            font_size=24
        ).to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(2)

        # Clean up the scene
        self.play(
            FadeOut(dots),
            FadeOut(connection_layer),
            FadeOut(formula),
            FadeOut(conclusion)
        )
        self.wait(1)