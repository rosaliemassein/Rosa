from manim import *

class RetrievalAugmentedPlanning(Scene):
    def construct(self):
        # 1. Search Bar at the top
        search_rect = Rectangle(width=6, height=0.7, color=WHITE).to_edge(UP, buff=0.5)
        search_label = Text("Search:", font_size=24).next_to(search_rect, LEFT)
        search_bar = VGroup(search_rect, search_label)
        
        keyword = Text("Image Classification", font_size=28).move_to(search_rect.get_center())
        
        self.play(Create(search_bar))
        self.play(AddTextLetterByLetter(keyword))
        self.wait(0.5)

        # 2. Documents flying in from the "cloud" (top of screen)
        # Create small rectangles representing documents with lines inside
        docs = VGroup()
        for i in range(3):
            doc_body = Rectangle(width=0.9, height=1.2, fill_opacity=0.2, color=GRAY)
            doc_lines = VGroup(*[Line(LEFT*0.3, RIGHT*0.3, stroke_width=1) for _ in range(5)]).arrange(DOWN, buff=0.1)
            doc = VGroup(doc_body, doc_lines).move_to(UP * 5 + (i-1)*RIGHT*3)
            docs.add(doc)
            
        self.play(
            LaggedStart(
                *[doc.animate.move_to(UP * 1 + (i-1)*RIGHT*2.5) for i, doc in enumerate(docs)],
                lag_ratio=0.3,
                run_time=2
            )
        )
        self.wait(0.5)

        # 3. Root of the Tree: Parsed Requirement
        root_circle = Circle(radius=0.7, color=YELLOW).shift(DOWN * 1.5)
        root_text = Text("Parsed\nRequirement", font_size=18).move_to(root_circle.get_center())
        root = VGroup(root_circle, root_text)

        # 4. Transform Documents into Plans
        plan_a = Text("Plan A", font_size=24).move_to(UP * 1 + LEFT * 3)
        plan_b = Text("Plan B", font_size=24).move_to(UP * 1)
        plan_c = Text("Plan C", font_size=24).move_to(UP * 1 + RIGHT * 3)
        plans = VGroup(plan_a, plan_b, plan_c)

        self.play(
            Create(root),
            ReplacementTransform(docs[0], plan_a),
            ReplacementTransform(docs[1], plan_b),
            ReplacementTransform(docs[2], plan_c),
            run_time=2
        )

        # 5. Create Branches
        branch_a = Line(root.get_top(), plan_a.get_bottom(), buff=0.1)
        branch_b = Line(root.get_top(), plan_b.get_bottom(), buff=0.1)
        branch_c = Line(root.get_top(), plan_c.get_bottom(), buff=0.1)
        branches = VGroup(branch_a, branch_b, branch_c)

        self.play(Create(branches))
        self.wait(0.5)

        # 6. Highlight the most "successful" branch (Plan B)
        highlight_circle = Circle(radius=0.6, color=GOLD).move_to(plan_b.get_center())
        self.play(
            branch_b.animate.set_stroke(color=YELLOW, width=8),
            plan_b.animate.set_color(YELLOW).scale(1.2),
            Create(highlight_circle),
        )
        self.play(Indicate(plan_b), Flash(plan_b, color=YELLOW))
        
        # 7. Add Formula at the bottom
        formula = MathTex(r"\mathbf{P} = \mathcal{A}_{mgr}(\mathrm{RAP}(R))").to_edge(DOWN, buff=0.4)
        self.play(Write(formula))
        
        self.wait(3)