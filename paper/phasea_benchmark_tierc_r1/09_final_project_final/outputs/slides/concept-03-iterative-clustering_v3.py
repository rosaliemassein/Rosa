from manim import *
import numpy as np

class IterativeClusteringConcept(Scene):
    def construct(self):
        # 1. Setup random dots
        np.random.seed(42)
        dots = VGroup()
        for _ in range(27):
            pos = [np.random.uniform(-5, 5), np.random.uniform(-3, 2), 0]
            dots.add(Dot(pos, color=GRAY, radius=0.08))
        
        self.add(dots)
        
        available_dots = list(dots.submobjects)
        cluster_colors = [RED, GREEN, YELLOW]
        
        # 2. Iterative Clustering Process
        for cluster_idx in range(3):
            # Find the two most similar (closest) dots in the available pool
            min_dist = float('inf')
            pair = (None, None)
            
            for i in range(len(available_dots)):
                for j in range(i + 1, len(available_dots)):
                    d = np.linalg.norm(available_dots[i].get_center() - available_dots[j].get_center())
                    if d < min_dist:
                        min_dist = d
                        pair = (available_dots[i], available_dots[j])
            
            dot1, dot2 = pair
            current_cluster = [dot1, dot2]
            available_dots.remove(dot1)
            available_dots.remove(dot2)
            
            # Highlight seed pair
            seed_color = cluster_colors[cluster_idx]
            ring = Circle(radius=0.2, color=WHITE, stroke_width=2).move_to(
                (dot1.get_center() + dot2.get_center()) / 2
            )
            
            self.play(
                dot1.animate.set_color(seed_color),
                dot2.animate.set_color(seed_color),
                Create(ring)
            )
            
            # Search circle
            search_circle = Circle(radius=0.1, color=seed_color, stroke_width=1, fill_opacity=0.1).move_to(ring.get_center())
            self.add(search_circle)

            # Greedily pull in 7 more dots (total 9)
            for _ in range(7):
                centroid = np.mean([d.get_center() for d in current_cluster], axis=0)
                
                # Find next closest unassigned dot to the centroid
                next_dot = min(available_dots, key=lambda d: np.linalg.norm(d.get_center() - centroid))
                dist_to_next = np.linalg.norm(next_dot.get_center() - centroid)
                
                # Animate search circle expanding and pulling in dot
                self.play(
                    search_circle.animate.set_radius(dist_to_next).move_to(centroid),
                    run_time=0.4
                )
                self.play(
                    next_dot.animate.set_color(seed_color),
                    run_time=0.2
                )
                
                current_cluster.append(next_dot)
                available_dots.remove(next_dot)
            
            # Fade out search tools for this cluster
            self.play(FadeOut(ring), FadeOut(search_circle))

        self.wait(1)
        
        # 3. Final Narration
        voice_text = Text(
            "This iterative approach ensures each group of nine proposals has\n"
            "the highest possible thematic cohesion, making it easier to find\n"
            "a single panel of reviewers who can cover the whole batch.",
            t2c={"thematic cohesion": BLUE},
            line_spacing=0.8
        ).scale(0.5).to_edge(DOWN)
        
        self.play(Write(voice_text))
        self.wait(3)

def get_dist(m1, m2):
    return np.linalg.norm(m1.get_center() - m2.get_center())