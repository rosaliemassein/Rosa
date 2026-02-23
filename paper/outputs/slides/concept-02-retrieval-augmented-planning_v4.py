from manim import *

class RetrievalAugmentedPlanningConcept(Scene):
    def construct(self):
        # 1. Search Bar Animation
        search_box = RoundedRectangle(corner_radius=0.1, width=6, height=0.7, color=BLUE_A)
        search_label = Text("Image Classification", font_size=24, color=WHITE).move_to(search_box.get_center())
        search_bar = VGroup(search_box, search_label).to_edge(UP, buff=0.5)

        self.play(Create(search_box))
        self.play(Write(search_label), run_time=1)
        self.wait(0.5)

        # 2. Knowledge Retrieval (Cloud and Docs)
        cloud = VGroup(
            Circle(radius=0.5).shift(LEFT * 0.3),
            Circle(radius=0.7).shift(ORIGIN),
            Circle(radius=0.5).shift(RIGHT * 0.3),
            Rectangle(width=1.2, height=0.6, stroke_width=0, fill_opacity=1).shift(DOWN * 0.2)
        ).set_fill(BLUE_E, opacity=0.3).set_stroke(BLUE_A, 2)
        cloud.to_corner(UR, buff=1)
        cloud_text = Text("Knowledge Cloud", font_size=16).next_to(cloud, DOWN, buff=0.1)

        self.play(FadeIn(cloud), Write(cloud_text))

        # Create document rectangles
        docs = VGroup(*[
            VGroup(
                Rectangle(width=0.5, height=0.7, fill_color=GRAY_B, fill_opacity=0.9, color=WHITE),
                Line(LEFT*0.15, RIGHT*0.15, color=BLACK, stroke_width=1).shift(UP*0.15),
                Line(LEFT*0.15, RIGHT*0.15, color=BLACK, stroke_width=1),
                Line(LEFT*0.15, RIGHT*0.15, color=BLACK, stroke_width=1).shift(DOWN*0.15)
            ) for _ in range(3)
        ])
        
        for doc in docs:
            doc.scale(0.7).move_to(cloud.get_center())

        # Documents flying in
        doc_destinations = [LEFT * 3 + DOWN * 0.5, ORIGIN + DOWN * 0.5, RIGHT * 3 + DOWN * 0.5]
        self.play(
            LaggedStart(
                *[doc.animate.move_to(dest) for doc, dest in zip(docs, doc_destinations)],
                lag_ratio=0.3
            )
        )
        self.wait(0.5)

        # 3. Tree Structure Transition
        root_box = RoundedRectangle(width=3.5, height=0.8, color=TEAL, fill_opacity=0.2)
        root_text = Text("Parsed Requirement", font_size=22)
        root = VGroup(root_box, root_text).to_edge(UP, buff=1.8)

        plan_names = ["Plan A", "Plan B", "Plan C"]
        plan_nodes = VGroup(*[
            VGroup(
                RoundedRectangle(width=2, height=0.7, color=WHITE, fill_opacity=0.1),
                Text(name, font_size=20)
            ) for name in plan_names
        ]).arrange(RIGHT, buff=1).shift(DOWN * 1.5)

        edges = VGroup(*[
            Line(root.get_bottom(), plan.get_top(), color=GRAY_A)
            for plan in plan_nodes
        ])

        # Sequence the transformation
        self.play(
            FadeOut(search_bar),
            FadeOut(cloud),
            FadeOut(cloud_text),
            FadeIn(root)
        )
        
        # Merge transformations and edge creation
        tree_anims = []
        for i in range(3):
            tree_anims.append(ReplacementTransform(docs[i], plan_nodes[i]))
            tree_anims.append(Create(edges[i]))
            
        self.play(LaggedStart(*tree_anims, lag_ratio=0.15))
        self.wait(0.5)

        # 4. Highlight Optimal Path
        success_color = GREEN_B
        # Highlight Plan B (index 1)
        self.play(
            plan_nodes[1].animate.set_color(success_color),
            edges[1].animate.set_color(success_color).set_stroke(width=5),
            run_time=1
        )
        
        # Flash animation
        self.play(Flash(plan_nodes[1].get_center(), color=success_color, line_length=0.3, flash_radius=1.2))
        
        # Glow effect
        glow = plan_nodes[1][0].copy().set_stroke(success_color, 8).set_opacity(0.5)
        self.add(glow)
        self.play(glow.animate.scale(1.2).set_opacity(0), run_time=1)
        self.remove(glow)

        # 5. Final Formula
        formula = MathTex(r"\mathbf{P} = \mathcal{A}_{mgr}(\mathrm{RAP}(R))", font_size=42)
        formula.to_edge(DOWN, buff=0.8)
        formula_box = SurroundingRectangle(formula, color=YELLOW, buff=MED_SMALL_BUFF)
        
        self.play(Write(formula))
        self.play(Create(formula_box))
        
        self.wait(3)