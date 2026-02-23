from manim import *
import numpy as np

class IterativeClustering(Scene):
    def construct(self):
        # Setup: Generate 27 random points
        np.random.seed(42)  # For consistent layout
        points = [
            np.array([np.random.uniform(-5, 5), np.random.uniform(-3, 3), 0])
            for _ in range(27)
        ]
        dots = VGroup(*[Dot(point=p, radius=0.08) for p in points])
        self.add(dots)

        unassigned_indices = list(range(27))
        cluster_colors = [YELLOW, BLUE, RED]

        # Iterate to create 3 clusters of 9
        for cluster_idx in range(3):
            # 1. Find the two closest unassigned dots to seed the cluster
            min_dist = float('inf')
            seed_pair = [0, 1]

            for i in range(len(unassigned_indices)):
                for j in range(i + 1, len(unassigned_indices)):
                    idx1 = unassigned_indices[i]
                    idx2 = unassigned_indices[j]
                    dist = np.linalg.norm(dots[idx1].get_center() - dots[idx2].get_center())
                    if dist < min_dist:
                        min_dist = dist
                        seed_pair = [idx1, idx2]

            current_color = cluster_colors[cluster_idx]
            
            # Highlight the seed pair
            seed_dots = VGroup(dots[seed_pair[0]], dots[seed_pair[1]])
            bright_ring = Circle(radius=0.2, color=WHITE, stroke_width=2).move_to(dots[seed_pair[0]].get_center())
            bright_ring2 = Circle(radius=0.2, color=WHITE, stroke_width=2).move_to(dots[seed_pair[1]].get_center())
            
            self.play(
                Create(bright_ring),
                Create(bright_ring2),
                seed_dots.animate.set_color(current_color),
                run_time=0.8
            )

            # Move seed indices to cluster and remove from unassigned
            cluster_indices = [seed_pair[0], seed_pair[1]]
            unassigned_indices.remove(seed_pair[0])
            unassigned_indices.remove(seed_pair[1])

            # 2. Greedily pull in next closest until cluster size is 9
            search_circle = Circle(radius=0.01, color=current_color, stroke_opacity=0.5)
            search_circle.move_to(VGroup(*[dots[i] for i in cluster_indices]).get_center())
            self.add(search_circle)

            while len(cluster_indices) < 9:
                cluster_vg = VGroup(*[dots[i] for i in cluster_indices])
                center = cluster_vg.get_center()

                # Find closest unassigned dot to the current cluster centroid
                closest_dist = float('inf')
                closest_idx = -1

                for u_idx in unassigned_indices:
                    d = np.linalg.norm(dots[u_idx].get_center() - center)
                    if d < closest_dist:
                        closest_dist = d
                        closest_idx = u_idx

                # Animate the search circle expanding to "touch" the next dot
                self.play(
                    search_circle.animate.set_width(2 * closest_dist).move_to(center),
                    run_time=0.4
                )
                self.play(
                    dots[closest_idx].animate.set_color(current_color),
                    run_time=0.2
                )

                cluster_indices.append(closest_idx)
                unassigned_indices.remove(closest_idx)

            # Cleanup search visuals for this cluster
            self.play(
                FadeOut(search_circle),
                FadeOut(bright_ring),
                FadeOut(bright_ring2),
                run_time=0.5
            )

        self.wait(2)