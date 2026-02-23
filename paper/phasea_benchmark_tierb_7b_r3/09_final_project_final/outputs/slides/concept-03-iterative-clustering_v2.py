from manim import *
import numpy as np

class IterativeClustering(Scene):
    def construct(self):
        # Generate a cloud of 27 Dot objects scattered randomly
        np.random.seed(42)
        dots = VGroup(*[
            Dot(point=[np.random.uniform(-5, 5), np.random.uniform(-3, 3), 0])
            for _ in range(27)
        ])
        self.add(dots)

        available_indices = list(range(27))
        colors = [BLUE, GREEN, RED]

        # Process: create 3 clusters of 9 dots each
        for cluster_idx in range(3):
            # 1. Find the two most similar (closest distance) dots in the available pool to seed a cluster
            min_dist = float('inf')
            seed_pair = (None, None)
            
            for i_pos, i_idx in enumerate(available_indices):
                for j_idx in available_indices[i_pos + 1:]:
                    d = np.linalg.norm(dots[i_idx].get_center() - dots[j_idx].get_center())
                    if d < min_dist:
                        min_dist = d
                        seed_pair = (i_idx, j_idx)
            
            idx1, idx2 = seed_pair
            
            # Highlight the seed pair using bright rings
            ring1 = Circle(radius=0.25, color=YELLOW, stroke_width=3).move_to(dots[idx1].get_center())
            ring2 = Circle(radius=0.25, color=YELLOW, stroke_width=3).move_to(dots[idx2].get_center())
            
            self.play(Create(ring1), Create(ring2))
            self.play(
                dots[idx1].animate.set_color(colors[cluster_idx]),
                dots[idx2].animate.set_color(colors[cluster_idx]),
                ring1.animate.set_color(colors[cluster_idx]),
                ring2.animate.set_color(colors[cluster_idx])
            )
            
            # Update the available pool
            available_indices.remove(idx1)
            available_indices.remove(idx2)
            
            # 2. Search circle expands from the midpoint of this pair
            mid_point = (dots[idx1].get_center() + dots[idx2].get_center()) / 2
            search_circle = Circle(radius=min_dist/2, color=colors[cluster_idx], stroke_width=2).move_to(mid_point)
            self.add(search_circle)
            self.play(FadeOut(ring1), FadeOut(ring2))
            
            # 3. Greedily pull in the next closest unassigned dots until cluster size is 9
            # (Already have 2 dots, so we need 7 more)
            for _ in range(7):
                best_d = float('inf')
                best_idx = -1
                best_avail_pos = -1
                
                # Search for the dot closest to the seed center among remaining dots
                for i_avail, d_idx in enumerate(available_indices):
                    dist = np.linalg.norm(dots[d_idx].get_center() - mid_point)
                    if dist < best_d:
                        best_d = dist
                        best_idx = d_idx
                        best_avail_pos = i_avail
                
                # Animate search circle expanding until it touches the next dot
                self.play(
                    search_circle.animate.set_width(2 * best_d),
                    run_time=0.5
                )
                
                # Change the newly captured dot's color to match the cluster
                self.play(dots[best_idx].animate.set_color(colors[cluster_idx]), run_time=0.2)
                
                # Remove from pool
                available_indices.pop(best_avail_pos)
            
            # Finish cluster iteration
            self.play(FadeOut(search_circle))

        self.wait(2)