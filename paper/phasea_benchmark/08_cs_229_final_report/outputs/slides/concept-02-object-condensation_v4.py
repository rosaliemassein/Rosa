from manim import *
import numpy as np

class ConceptAnimation(Scene):
    def construct(self):
        # Using Text instead of Tex/MathTex as they were disallowed
        formula = Text("q_i = arctanh(beta_i) + q_min", font_size=24)
        formula.to_edge(UP)
        self.add(formula)

        # Hit coordinates for the simulation
        # Using a set of points to represent particle hits in a 2D plane
        hit_coords = [
            [-3.0, 1.5, 0], [-3.8, 1.0, 0], [-2.5, 2.2, 0], [-2.0, 0.8, 0],
            [2.5, -1.0, 0], [1.8, -0.5, 0], [3.2, -1.5, 0], [2.2, -2.0, 0],
            [0.2, 1.0, 0], [-1.0, -2.0, 0] # Noise hits
        ]
        
        # Initial hits: Show them as small purple dots
        dots = VGroup(*[
            Dot(point=coord, color=PURPLE, radius=0.08)
            for coord in hit_coords
        ])
        
        self.play(Create(dots))
        self.wait(0.5)

        # Condensation points (hits that will have high beta)
        # We'll pick indices 0 and 4 as the centers of two particles
        cp1_idx = 0
        cp2_idx = 4
        
        # Animation: Growing size and changing color based on beta value
        # High beta = Yellow and Large. Low beta = remains Purple and Small.
        self.play(
            dots[cp1_idx].animate.scale(2.5).set_color(YELLOW),
            dots[cp2_idx].animate.scale(2.5).set_color(YELLOW),
            run_time=1.5
        )

        # Gravity Wells: Represented by concentric rings around high-beta dots
        wells = VGroup()
        for idx in [cp1_idx, cp2_idx]:
            center_pos = dots[idx].get_center()
            # Create several rings to simulate a mesh/gradient effect
            for r in [0.4, 0.8, 1.2]:
                ring = Circle(radius=r, color=YELLOW, stroke_width=1.5)
                ring.move_to(center_pos)
                ring.set_opacity(0.3 / r) # Fades out as it gets larger
                wells.add(ring)
        
        self.play(FadeIn(wells))
        self.wait(0.5)

        # Attraction: Pull neighboring dots toward the condensation points
        # Each dot is pulled toward its nearest high-beta neighbor
        pull_animations = []
        cp1_pos = dots[cp1_idx].get_center()
        cp2_pos = dots[cp2_idx].get_center()
        
        for i, dot in enumerate(dots):
            if i != cp1_idx and i != cp2_idx:
                current_pos = dot.get_center()
                # Manual distance calculation to avoid interpolate/linalg if problematic
                dist1 = np.sqrt(np.sum((current_pos - cp1_pos)**2))
                dist2 = np.sqrt(np.sum((current_pos - cp2_pos)**2))
                
                # Determine nearest center
                if dist1 < dist2:
                    target = cp1_pos
                    dist = dist1
                else:
                    target = cp2_pos
                    dist = dist2
                
                # If hit is within a reasonable distance, pull it toward the center
                if dist < 4.0:
                    # Move 70% of the way to the center
                    new_pos = current_pos + (target - current_pos) * 0.7
                    pull_animations.append(dot.animate.move_to(new_pos))
                    
        if pull_animations:
            self.play(*pull_animations, run_time=2)
        
        self.wait(2)