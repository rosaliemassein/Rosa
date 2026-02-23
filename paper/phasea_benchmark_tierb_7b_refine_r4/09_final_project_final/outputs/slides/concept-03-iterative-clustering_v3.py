from manim import *
import numpy as np

class IterativeClustering(Scene):
    def construct(self):
        # Define a local linear rate function to avoid identifier errors
        def linear_fn(t):
            return t
        
        # 1. Create a cloud of 27 dot objects scattered randomly
        dots = VGroup(*[
            Dot(point=[np.random.uniform(-5, 5), np.random.uniform(-3, 3), 0], radius=0.08)
            for _ in range(27)
        ])
        self.play(Create(dots))
        self.wait(1)

        assigned_indices = []
        cluster_colors = [BLUE, GREEN, RED]

        for cluster_idx in range(3):
            current_color = cluster_colors[cluster_idx]
            
            # Find the two most similar (shortest distance) unassigned dots to seed the cluster
            unassigned = [i for i in range(27) if i not in assigned_indices]
            
            if len(unassigned) < 2:
                break
                
            best_pair = (unassigned[0], unassigned[1])
            min_dist = np.linalg.norm(dots[unassigned[0]].get_center() - dots[unassigned[1]].get_center())
            
            for i in range(len(unassigned)):
                for j in range(i + 1, len(unassigned)):
                    idx_a, idx_b = unassigned[i], unassigned[j]
                    dist = np.linalg.norm(dots[idx_a].get_center() - dots[idx_b].get_center())
                    if dist < min_dist:
                        min_dist = dist
                        best_pair = (idx_a, idx_b)
            
            idx1, idx2 = best_pair
            
            # Highlight the seed pair with bright rings
            ring1 = Circle(radius=0.18, color=YELLOW, stroke_width=4).move_to(dots[idx1])
            ring2 = Circle(radius=0.18, color=YELLOW, stroke_width=4).move_to(dots[idx2])
            
            self.play(Create(ring1), Create(ring2))
            self.play(
                dots[idx1].animate.set_color(current_color),
                dots[idx2].animate.set_color(current_color)
            )
            self.play(FadeOut(ring1), FadeOut(ring2))
            
            current_cluster = [idx1, idx2]
            assigned_indices.extend([idx1, idx2])
            
            # 2. Greedily pull in the next most similar unassigned dots until cluster size is 9
            while len(current_cluster) < 9:
                unassigned = [i for i in range(27) if i not in assigned_indices]
                if not unassigned:
                    break
                    
                next_dot_idx = -1
                min_dist_to_cluster = float('inf')
                
                # Find unassigned dot closest to any member of the existing cluster
                for u_idx in unassigned:
                    for c_idx in current_cluster:
                        dist = np.linalg.norm(dots[u_idx].get_center() - dots[c_idx].get_center())
                        if dist < min_dist_to_cluster:
                            min_dist_to_cluster = dist
                            next_dot_idx = u_idx
                
                # Search circle expanding from the cluster centroid to the next dot
                cluster_points = [dots[i].get_center() for i in current_cluster]
                centroid = np.mean(cluster_points, axis=0)
                target_pos = dots[next_dot_idx].get_center()
                final_radius = np.linalg.norm(target_pos - centroid)
                
                search_circle = Circle(radius=0.01, color=current_color, stroke_width=2).move_to(centroid)
                self.add(search_circle)
                
                # Animate search circle expansion
                self.play(
                    search_circle.animate.set_width(max(0.01, final_radius * 2)),
                    rate_func=linear_fn,
                    run_time=0.4
                )
                
                # Dot changes color when "touched" by the circle
                self.play(
                    dots[next_dot_idx].animate.set_color(current_color),
                    FadeOut(search_circle),
                    run_time=0.2
                )
                
                current_cluster.append(next_dot_idx)
                assigned_indices.append(next_dot_idx)
            
            self.wait(0.5)

        # Final state: Three distinct colored sets
        self.wait(2)