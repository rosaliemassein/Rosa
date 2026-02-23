from manim import *
import numpy as np

class ConceptAnimation(Scene):
    def construct(self):
        # Narration setup
        voice_text_1 = "Standard clustering methods often fail on sparse data."
        voice_text_2 = "We start by finding the two most similar proposals."
        voice_text_3 = "Then greedily pull in the next most similar proposals."
        
        narrator_label = Text(voice_text_1, font_size=24).to_edge(DOWN)
        self.add(narrator_label)

        # Create 27 randomly scattered Dot objects
        np.random.seed(42)
        dots = VGroup(*[
            Dot(point=[np.random.uniform(-5, 5), np.random.uniform(-3, 3), 0], radius=0.1)
            for _ in range(27)
        ])
        self.play(FadeIn(dots))
        self.wait(1)

        available_dots = list(dots)
        clusters = []
        colors = [RED, BLUE, GREEN]

        for i in range(3):
            cluster_color = colors[i]
            
            # Update narration
            if i == 0:
                self.play(Transform(narrator_label, Text(voice_text_2, font_size=24).to_edge(DOWN)))
            elif i == 1:
                self.play(Transform(narrator_label, Text("Repeating for the next cluster...", font_size=24).to_edge(DOWN)))

            # 1. Find the two most similar (closest) dots in available_dots
            min_dist = float('inf')
            seed_a, seed_b = None, None
            
            for idx_a in range(len(available_dots)):
                for idx_b in range(idx_a + 1, len(available_dots)):
                    d1 = available_dots[idx_a]
                    d2 = available_dots[idx_b]
                    dist = np.linalg.norm(d1.get_center() - d2.get_center())
                    if dist < min_dist:
                        min_dist = dist
                        seed_a, seed_b = d1, d2
            
            current_cluster = [seed_a, seed_b]
            available_dots.remove(seed_a)
            available_dots.remove(seed_b)

            # Highlight initial seed
            seed_center = (seed_a.get_center() + seed_b.get_center()) / 2
            highlight_ring = Circle(radius=min_dist/2 + 0.2, color=YELLOW).move_to(seed_center)
            
            self.play(
                Create(highlight_ring),
                seed_a.animate.set_color(cluster_color),
                seed_b.animate.set_color(cluster_color)
            )

            # 2. Greedily pull in the next 7 dots (total 9)
            while len(current_cluster) < 9:
                target_dot = None
                closest_dist = float('inf')
                reference_point = None

                # Find dot in available_dots closest to ANY dot in the current cluster
                for d in available_dots:
                    for c_dot in current_cluster:
                        dist = np.linalg.norm(d.get_center() - c_dot.get_center())
                        if dist < closest_dist:
                            closest_dist = dist
                            target_dot = d
                            reference_point = c_dot.get_center()

                # Animate search circle expanding from cluster center of mass
                cluster_center = sum([d.get_center() for d in current_cluster]) / len(current_cluster)
                search_circle = Circle(radius=0.1, color=cluster_color, stroke_opacity=0.5).move_to(cluster_center)
                
                # Expansion distance
                dist_to_target = np.linalg.norm(target_dot.get_center() - cluster_center)
                
                self.play(
                    search_circle.animate.set_style(stroke_opacity=0).scale(dist_to_target * 10),
                    target_dot.animate.set_color(cluster_color),
                    run_time=0.4
                )
                
                current_cluster.append(target_dot)
                available_dots.remove(target_dot)
                self.remove(search_circle)

            self.play(FadeOut(highlight_ring))
            clusters.append(current_cluster)

        # Final Narration
        final_text = "Highest thematic cohesion for easier reviewer assignment."
        self.play(Transform(narrator_label, Text(final_text, font_size=24).to_edge(DOWN)))
        
        # Group and emphasize clusters
        all_clusters = VGroup(*[VGroup(*c) for c in clusters])
        self.play(all_clusters.animate.scale(1.1), run_time=1)
        self.play(all_clusters.animate.scale(1/1.1), run_time=1)
        self.wait(2)