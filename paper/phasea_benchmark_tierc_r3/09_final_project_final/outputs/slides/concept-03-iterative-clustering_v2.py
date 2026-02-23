from manim import *
import numpy as np

class ConceptIterativeClustering(Scene):
    def construct(self):
        # 1. Create a cloud of 27 dots
        np.random.seed(42)  # For reproducibility
        dot_points = []
        while len(dot_points) < 27:
            p = np.array([np.random.uniform(-5, 5), np.random.uniform(-3, 2), 0])
            # Ensure dots aren't exactly on top of each other
            if all(np.linalg.norm(p - existing) > 0.4 for existing in dot_points):
                dot_points.append(p)
        
        dots = VGroup(*[Dot(point=p, color=GRAY) for p in dot_points])
        self.add(dots)

        # Narration setup
        voice_text = Text(
            "Finding most similar proposals to seed clusters...",
            font_size=24
        ).to_edge(UP)
        self.add(voice_text)

        colors = [BLUE, GREEN, ORANGE]
        unassigned_indices = list(range(27))

        for cluster_idx in range(3):
            # 2. Find the two most similar (closest) unassigned dots
            min_dist = float('inf')
            pair = (None, None)
            for i in range(len(unassigned_indices)):
                for j in range(i + 1, len(unassigned_indices)):
                    idx1 = unassigned_indices[i]
                    idx2 = unassigned_indices[j]
                    d = np.linalg.norm(dots[idx1].get_center() - dots[idx2].get_center())
                    if d < min_dist:
                        min_dist = d
                        pair = (idx1, idx2)
            
            idx_a, idx_b = pair
            cluster_members = [idx_a, idx_b]
            unassigned_indices.remove(idx_a)
            unassigned_indices.remove(idx_b)

            cluster_color = colors[cluster_idx]
            
            # Highlight seeds
            seed_highlight = VGroup(
                Circle(radius=0.2, color=YELLOW).move_to(dots[idx_a]),
                Circle(radius=0.2, color=YELLOW).move_to(dots[idx_b])
            )
            self.play(Create(seed_highlight), dots[idx_a].animate.set_color(cluster_color), dots[idx_b].animate.set_color(cluster_color))
            self.remove(seed_highlight)

            # 3. Iteratively pull in next closest until cluster size is 9
            search_circle = Circle(radius=0, color=cluster_color, stroke_opacity=0.5).move_to(
                (dots[idx_a].get_center() + dots[idx_b].get_center()) / 2
            )
            self.add(search_circle)

            for _ in range(7):
                # Find centroid of current cluster to move/expand search circle
                centroid = sum(dots[i].get_center() for i in cluster_members) / len(cluster_members)
                
                # Find next closest unassigned dot to the centroid
                next_dot_idx = -1
                min_d_to_centroid = float('inf')
                for u_idx in unassigned_indices:
                    d = np.linalg.norm(dots[u_idx].get_center() - centroid)
                    if d < min_d_to_centroid:
                        min_d_to_centroid = d
                        next_dot_idx = u_idx
                
                # Animate search circle expanding to touch the next dot
                self.play(
                    search_circle.animate.move_to(centroid).set_width(min_d_to_centroid * 2),
                    run_time=0.5
                )
                
                # Color the dot and add to cluster
                self.play(dots[next_dot_idx].animate.set_color(cluster_color), run_time=0.2)
                cluster_members.append(next_dot_idx)
                unassigned_indices.remove(next_dot_idx)

            self.play(FadeOut(search_circle))

        # Final narration update
        new_text = Text(
            "Iterative clustering ensures thematic cohesion.",
            font_size=24, color=YELLOW
        ).to_edge(UP)
        self.play(Transform(voice_text, new_text))
        self.wait(2)