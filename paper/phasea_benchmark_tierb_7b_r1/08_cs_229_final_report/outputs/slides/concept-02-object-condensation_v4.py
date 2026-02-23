from manim import *
import numpy as np

class ObjectCondensation(Scene):
    def construct(self):
        # 1. Formula Display
        formula = MathTex(r"q_i = \text{arctanh}(\beta_i) + q_{min}")
        formula.to_edge(UP)
        self.add(formula)

        # 2. Manual Grid Creation (avoiding NumberPlane)
        grid = VGroup()
        for x in range(-7, 8):
            grid.add(Line(np.array([x, -4, 0]), np.array([x, 4, 0]), stroke_width=1, stroke_opacity=0.2))
        for y in range(-4, 5):
            grid.add(Line(np.array([-7, y, 0]), np.array([7, y, 0]), stroke_width=1, stroke_opacity=0.2))
        self.add(grid)

        # 3. Setup Dots
        # Condensation points (high beta centers)
        cp_locs = [np.array([-3, 1, 0]), np.array([3, -1, 0])]
        centers = VGroup(*[Dot(p, color=PURPLE, radius=0.1) for p in cp_locs])
        
        # Surrounding hits (low beta)
        hits = VGroup()
        for p in cp_locs:
            for _ in range(12):
                angle = np.random.uniform(0, 2 * np.pi)
                dist = np.random.uniform(1.2, 3.2)
                pos = p + np.array([np.cos(angle) * dist, np.sin(angle) * dist, 0])
                hits.add(Dot(pos, color=PURPLE, radius=0.06))

        # Noise hits
        noise = VGroup(*[
            Dot(np.array([np.random.uniform(-6, 6), np.random.uniform(-3, 3), 0]), 
                color=PURPLE, radius=0.06) for _ in range(8)
        ])

        self.play(FadeIn(hits), FadeIn(centers), FadeIn(noise))
        self.wait(0.5)

        # 4. Growth and Color Change (Simulating Beta increase)
        # We use discrete color steps since interpolate_color was restricted
        center_anims = [c.animate.scale(3.0).set_color(YELLOW) for c in centers]
        hit_anims = [h.animate.set_color(ORANGE).scale(1.2) for h in hits]
        
        self.play(*(center_anims + hit_anims), run_time=2)

        # Charge labels
        labels = VGroup()
        for i in range(len(centers)):
            lbl = MathTex(f"q_{i+1}").scale(0.8).next_to(centers[i], UR, buff=0.1)
            labels.add(lbl)
        self.play(Write(labels))

        # 5. Gravity Wells (Concentric Circles)
        wells = VGroup()
        for c in centers:
            for r in [0.5, 1.0, 1.5, 2.0]:
                circ = Circle(radius=r, color=YELLOW).move_to(c.get_center())
                circ.set_stroke(width=1.5, opacity=1.0 - (r / 2.2))
                wells.add(circ)
        self.play(Create(wells), run_time=1.5)

        # 6. Movement/Pull Animation
        # Define a manual cubic rate function for smooth movement
        def custom_smooth(t):
            return t * t * (3 - 2 * t)

        pull_anims = []
        for h in hits:
            p_current = h.get_center()
            # Find the closer condensation point center
            d0 = np.linalg.norm(p_current - cp_locs[0])
            d1 = np.linalg.norm(p_current - cp_locs[1])
            target_center = cp_locs[0] if d0 < d1 else cp_locs[1]
            
            # Manually calculate a point 70% of the way to the center
            # new_pos = current + alpha * (target - current)
            p_new = p_current + 0.7 * (target_center - p_current)
            pull_anims.append(h.animate.move_to(p_new))

        # Noise moves slightly randomly to simulate jitter/pushing
        for n in noise:
            p_new = n.get_center() + np.array([np.random.uniform(-0.4, 0.4), 0, 0])
            pull_anims.append(n.animate.move_to(p_new))

        self.play(*pull_anims, run_time=3, rate_func=custom_smooth)
        self.wait(2)