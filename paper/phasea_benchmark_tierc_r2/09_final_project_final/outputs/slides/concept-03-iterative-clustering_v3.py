from manim import *
import numpy as np
import math

class IterativeClustering(Scene):
    def construct(self):
        # Setting random seed for reproducibility
        np.random.seed(42)

        # 1. Generate a cloud of 27 Dot objects scattered randomly
        dots = VGroup(*[
            Dot(
                point=[np.random.uniform(-5, 5), np.random.uniform(-3, 3), 0],
                radius=0.1,
                color=BLUE
            ) for _ in range(27)
        ])
        
        self.add(dots)
        self.wait(1)

        cluster_colors = [GREEN, RED, GOLD]
        assigned_indices = set()

        # Iterate to create 3 clusters of 9 dots each
        for cluster_idx in range(3):
            # Find the two most similar (closest) unassigned proposals to seed
            min_dist = float('inf')
            seed_pair = (0, 0)
            
            unassigned_list = [i for i in range(27) if i not in assigned_indices]
            
            # If for some reason we can't find a pair, break
            if len(unassigned_list) < 2:
                break
                
            for i in range(len(unassigned_list)):
                for j in range(i + 1, len(unassigned_list)):
                    idx1 = unassigned_list[i]
                    idx2 = unassigned_list[j]
                    dist = np.linalg.norm(dots[idx1].get_center() - dots[idx2].get_center())
                    if dist < min_dist:
                        min_dist = dist
                        seed_pair = (idx1, idx2)
            
            # Highlight the seed pair with rings
            idx1, idx2 = seed_pair
            current_cluster_indices = [idx1, idx2]
            assigned_indices.update(current_cluster_indices)
            
            highlight_rings = VGroup(
                Circle(radius=0.2, color=WHITE).move_to(dots[idx1]),
                Circle(radius=0.2, color=WHITE).move_to(dots[idx2])
            )
            
            self.play(
                Create(highlight_rings),
                dots[idx1].animate.set_color(cluster_colors[cluster_idx]),
                dots[idx2].animate.set_color(cluster_colors[cluster_idx])
            )

            # Iteratively add dots until cluster size is 9
            # Start search circle from the midpoint of the seed pair
            seed_midpoint = (dots[idx1].get_center() + dots[idx2].get_center()) / 2
            search_circle = Circle(radius=0.1, color=cluster_colors[cluster_idx], stroke_width=2)
            search_circle.move_to(seed_midpoint)
            self.add(search_circle)

            for _ in range(7):
                next_dot_idx = -1
                min_dist_to_cluster = float('inf')
                
                # Find the next closest unassigned dot to ANY dot already in the current cluster (greedy)
                unassigned_remaining = [i for i in range(27) if i not in assigned_indices]
                if not unassigned_remaining:
                    break
                    
                for u_idx in unassigned_remaining:
                    for c_idx in current_cluster_indices:
                        dist = np.linalg.norm(dots[u_idx].get_center() - dots[c_idx].get_center())
                        if dist < min_dist_to_cluster:
                            min_dist_to_cluster = dist
                            next_dot_idx = u_idx
                
                if next_dot_idx == -1:
                    break
                
                # Animate search circle expanding to touch the next closest dot
                # We calculate the distance from the cluster center to the new dot
                cluster_center = VGroup(*[dots[i] for i in current_cluster_indices]).get_center()
                new_radius = np.linalg.norm(dots[next_dot_idx].get_center() - cluster_center)
                
                self.play(
                    search_circle.animate.move_to(cluster_center).set_width(new_radius * 2),
                    run_time=0.4
                )
                
                # Update dot state
                self.play(dots[next_dot_idx].animate.set_color(cluster_colors[cluster_idx]), run_time=0.1)
                current_cluster_indices.append(next_dot_idx)
                assigned_indices.add(next_dot_idx)

            self.play(FadeOut(search_circle), FadeOut(highlight_rings))
            self.wait(0.3)

        self.wait(2)