from manim import *
import numpy as np
import random

class IterativeClustering(Scene):
    def construct(self):
        # 1. Create a cloud of 27 Dot objects scattered randomly
        random.seed(42)
        dots = VGroup(*[
            Dot(point=[random.uniform(-5, 5), random.uniform(-3, 3), 0]) 
            for _ in range(27)
        ])
        self.add(dots)
        
        available_indices = list(range(27))
        cluster_colors = [RED, BLUE, GREEN]
        
        for cluster_idx in range(3):
            current_color = cluster_colors[cluster_idx]
            
            # 2. Highlight the two dots with the shortest distance (highest similarity)
            min_dist = float('inf')
            seed_pair = (None, None)
            
            # Find the closest pair among unassigned dots
            for i in range(len(available_indices)):
                for j in range(i + 1, len(available_indices)):
                    idx1 = available_indices[i]
                    idx2 = available_indices[j]
                    d = np.linalg.norm(dots[idx1].get_center() - dots[idx2].get_center())
                    if d < min_dist:
                        min_dist = d
                        seed_pair = (idx1, idx2)
            
            idx1, idx2 = seed_pair
            ring1 = Circle(radius=0.25, color=YELLOW).move_to(dots[idx1].get_center())
            ring2 = Circle(radius=0.25, color=YELLOW).move_to(dots[idx2].get_center())
            
            self.play(Create(ring1), Create(ring2))
            self.play(
                dots[idx1].animate.set_color(current_color), 
                dots[idx2].animate.set_color(current_color)
            )
            
            cluster_indices = [idx1, idx2]
            available_indices.remove(idx1)
            available_indices.remove(idx2)
            
            # 3. Animate a 'search' circle expanding from this pair
            seed_center = (dots[idx1].get_center() + dots[idx2].get_center()) / 2
            search_circle = Circle(radius=0.1, color=YELLOW, stroke_width=2).move_to(seed_center)
            self.add(search_circle)
            
            # 4. Greedily pull in the next most similar unassigned proposal until cluster size is 9
            while len(cluster_indices) < 9:
                best_next_idx = -1
                min_dist_to_center = float('inf')
                
                for idx in available_indices:
                    d = np.linalg.norm(dots[idx].get_center() - seed_center)
                    if d < min_dist_to_center:
                        min_dist_to_center = d
                        best_next_idx = idx
                
                # Animate circle expansion to the next closest dot
                self.play(
                    search_circle.animate.set_radius(min_dist_to_center),
                    run_time=0.5
                )
                self.play(
                    dots[best_next_idx].animate.set_color(current_color),
                    run_time=0.2
                )
                
                cluster_indices.append(best_next_idx)
                available_indices.remove(best_next_idx)
            
            # Fade out search visuals for this cluster
            self.play(FadeOut(search_circle), FadeOut(ring1), FadeOut(ring2))

        self.wait(2)