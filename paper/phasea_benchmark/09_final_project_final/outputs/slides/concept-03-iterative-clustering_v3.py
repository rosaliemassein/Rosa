from manim import *
import numpy as np

class ConceptIterativeClustering(Scene):
    def construct(self):
        # Narration setup
        narration_text = Text(
            "Iterative Clustering: Grouping by Thematic Cohesion",
            font_size=24
        ).to_edge(UP)
        self.add(narration_text)

        # 1. Generate a cloud of 27 Dot objects scattered randomly
        # We set a seed for consistent layout
        np.random.seed(42)
        dots = VGroup(*[
            Dot(point=[np.random.uniform(-5, 5), np.random.uniform(-3, 2), 0]) 
            for _ in range(27)
        ])
        self.add(dots)
        self.wait(1)

        unassigned = list(dots)
        cluster_colors = [RED, BLUE, GREEN]
        
        # We need to create 3 clusters of 9 dots each
        for cluster_idx in range(3):
            # A. Find the two most similar (shortest distance) dots among unassigned
            min_dist = float('inf')
            seed_pair = (None, None)
            
            for i in range(len(unassigned)):
                for j in range(i + 1, len(unassigned)):
                    d1, d2 = unassigned[i], unassigned[j]
                    dist = np.linalg.norm(d1.get_center() - d2.get_center())
                    if dist < min_dist:
                        min_dist = dist
                        seed_pair = (d1, d2)
            
            s1, s2 = seed_pair
            current_cluster = [s1, s2]
            unassigned.remove(s1)
            unassigned.remove(s2)
            
            color = cluster_colors[cluster_idx]
            
            # Highlight the seed pair with a ring
            seed_midpoint = (s1.get_center() + s2.get_center()) / 2
            # Initial ring encompasses the pair
            ring = Circle(radius=min_dist/2 + 0.2, color=color, stroke_width=2)
            ring.move_to(seed_midpoint)
            
            self.play(
                s1.animate.set_color(color),
                s2.animate.set_color(color),
                Create(ring),
                run_time=0.8
            )
            
            # B. Greedily pull in the next most similar unassigned dots until cluster size is 9
            while len(current_cluster) < 9:
                # Calculate the centroid of the current cluster for the 'search' expansion
                centroid = np.mean([d.get_center() for d in current_cluster], axis=0)
                
                # Find the unassigned dot closest to the cluster centroid
                next_dot = min(unassigned, key=lambda d: np.linalg.norm(d.get_center() - centroid))
                new_radius = np.linalg.norm(next_dot.get_center() - centroid) + 0.1
                
                # Animate the 'search' circle expanding
                search_circle = Circle(radius=new_radius, color=color, stroke_width=1, stroke_opacity=0.5)
                search_circle.move_to(centroid)
                
                self.play(
                    Transform(ring, search_circle),
                    run_time=0.4
                )
                
                self.play(
                    next_dot.animate.set_color(color),
                    run_time=0.2
                )
                
                current_cluster.append(next_dot)
                unassigned.remove(next_dot)
            
            # Fade out the search ring before starting the next cluster
            self.play(FadeOut(ring), run_time=0.5)

        # Final state wait
        self.wait(2)