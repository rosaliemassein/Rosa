from manim import *
import numpy as np

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Setup centers for split-screen view
        left_center = LEFT * 3.5
        right_center = RIGHT * 3.5

        # 2. Draw manual axes for Physical Space (Left)
        l_xaxis = Line(left_center + LEFT * 2, left_center + RIGHT * 2, color=WHITE)
        l_yaxis = Line(left_center + DOWN * 2, left_center + UP * 2, color=WHITE)
        l_label = Text("Physical Space", font_size=24).move_to(left_center + UP * 2.5)

        # 3. Draw manual axes for Learned Space (Right)
        r_xaxis = Line(right_center + LEFT * 2, right_center + RIGHT * 2, color=WHITE)
        r_yaxis = Line(right_center + DOWN * 2, right_center + UP * 2, color=WHITE)
        r_label = Text("Learned Space", font_size=24).move_to(right_center + UP * 2.5)

        # 4. Create formula
        formula = MathTex(
            r"L_V = \frac{1}{N} \sum q_j \sum (\mathbb{1} \check{V}_k + (1-\mathbb{1}) \hat{V}_k)",
            font_size=28
        ).to_edge(DOWN, buff=0.5)

        # 5. Generate dot clusters
        np.random.seed(42)
        num_hits = 15
        
        # Physical hits (Left) - Overlapping clusters
        hits_red_phys = VGroup()
        hits_blue_phys = VGroup()
        for _ in range(num_hits):
            # Cluster A (Red) centered slightly offset
            pos_red = left_center + np.array([np.random.normal(0.2, 0.5), np.random.normal(0.2, 0.5), 0])
            hits_red_phys.add(Dot(point=pos_red, color=RED, radius=0.06))
            
            # Cluster B (Blue) overlapping Cluster A
            pos_blue = left_center + np.array([np.random.normal(-0.2, 0.5), np.random.normal(-0.2, 0.5), 0])
            hits_blue_phys.add(Dot(point=pos_blue, color=BLUE, radius=0.06))

        # Learned hits (Right) - Separated clusters
        hits_red_learn = VGroup()
        hits_blue_learn = VGroup()
        for _ in range(num_hits):
            # Cluster A (Red) pushed to top-right
            pos_red = right_center + np.array([np.random.normal(1.2, 0.3), np.random.normal(1.2, 0.3), 0])
            hits_red_learn.add(Dot(point=pos_red, color=RED, radius=0.06))
            
            # Cluster B (Blue) pushed to bottom-left
            pos_blue = right_center + np.array([np.random.normal(-1.2, 0.3), np.random.normal(-1.2, 0.3), 0])
            hits_blue_learn.add(Dot(point=pos_blue, color=BLUE, radius=0.06))

        # 6. Initial Scene Composition
        self.add(l_xaxis, l_yaxis, l_label, r_xaxis, r_yaxis, r_label, formula)
        self.add(hits_red_phys, hits_blue_phys)
        self.wait(1)

        # 7. Transformation Animation
        # We transform the physical hits into the learned positions
        self.play(
            Transform(hits_red_phys, hits_red_learn),
            Transform(hits_blue_phys, hits_blue_learn),
            run_time=2.5
        )

        # 8. Indicate successful classification with circles
        # Since DashedLine/DashedVMobject was disallowed, we use standard Circles
        circle_red = Circle(radius=0.9, color=RED).move_to(right_center + np.array([1.2, 1.2, 0]))
        circle_blue = Circle(radius=0.9, color=BLUE).move_to(right_center + np.array([-1.2, -1.2, 0]))

        self.play(FadeIn(circle_red), FadeIn(circle_blue))
        self.wait(2)