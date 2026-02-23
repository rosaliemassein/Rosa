from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Create the Agent Manager (Central Icon)
        agent_manager_rect = RoundedRectangle(height=1.5, width=2.5, color=WHITE, fill_opacity=0.1)
        agent_manager_text = Text("Agent Manager", font_size=24)
        agent_manager = VGroup(agent_manager_rect, agent_manager_text).move_to(ORIGIN)
        
        # 2. Create the Knowledge Base (Cloud Icon on the left)
        kb_cloud = VGroup(
            Circle(radius=0.4, color=BLUE, fill_opacity=0.5).shift(LEFT * 0.3),
            Circle(radius=0.5, color=BLUE, fill_opacity=0.5).shift(UP * 0.2),
            Circle(radius=0.4, color=BLUE, fill_opacity=0.5).shift(RIGHT * 0.3),
            Circle(radius=0.3, color=BLUE, fill_opacity=0.5).shift(DOWN * 0.1)
        ).move_to(LEFT * 5)
        kb_text = Text("Knowledge Base", font_size=20, color=BLUE).next_to(kb_cloud, DOWN)
        knowledge_base = VGroup(kb_cloud, kb_text)

        # 3. Knowledge Retrieval Arrow
        retrieval_arrow = Arrow(knowledge_base.get_right(), agent_manager.get_left(), color=BLUE, buff=0.2)
        knowledge_label = Text("Knowledge", font_size=18).next_to(retrieval_arrow, UP)

        # 4. Branching Paths (Plans A, B, C)
        branch_end_a = RIGHT * 3 + UP * 2
        branch_end_b = RIGHT * 3
        branch_end_c = RIGHT * 3 + DOWN * 2
        
        arrow_a = Arrow(agent_manager.get_right(), branch_end_a, color=GREEN)
        arrow_b = Arrow(agent_manager.get_right(), branch_end_b, color=YELLOW)
        arrow_c = Arrow(agent_manager.get_right(), branch_end_c, color=RED)
        
        # ML Strategy Icons/Labels
        plan_a_icon = Square(side_length=0.4, color=GREEN)
        plan_a_text = Text("Plan A: Transformer", font_size=20)
        plan_a = VGroup(plan_a_icon, plan_a_text).arrange(RIGHT).next_to(branch_end_a, RIGHT)
        
        plan_b_icon = Circle(radius=0.2, color=YELLOW)
        plan_b_text = Text("Plan B: Standard CNN", font_size=20)
        plan_b = VGroup(plan_b_icon, plan_b_text).arrange(RIGHT).next_to(branch_end_b, RIGHT)
        
        plan_c_icon = Triangle(color=RED).scale(0.2)
        plan_c_text = Text("Plan C: Hybrid Model", font_size=20)
        plan_c = VGroup(plan_c_icon, plan_c_text).arrange(RIGHT).next_to(branch_end_c, RIGHT)

        # 5. Formula
        formula = MathTex(r"\mathbf{P} = \mathcal{A}_{mgr}(\mathrm{RAP}(R))")
        formula.to_edge(DOWN, buff=0.5)

        # --- ANIMATION SEQUENCE ---
        
        # Show Manager and Knowledge Base
        self.play(Create(agent_manager), FadeIn(knowledge_base))
        self.wait(0.5)
        
        # Animate Knowledge Retrieval
        self.play(GrowArrow(retrieval_arrow), Write(knowledge_label))
        self.wait(0.5)
        
        # Branching out (Transforming the knowledge flow into the central branch first)
        self.play(
            ReplacementTransform(retrieval_arrow.copy(), arrow_b),
            FadeOut(knowledge_label)
        )
        
        # Parallel Branching from the central branch to top and bottom
        self.play(
            ReplacementTransform(arrow_b.copy(), arrow_a),
            ReplacementTransform(arrow_b.copy(), arrow_c)
        )
        
        # Show Plan Strategy Icons and Descriptions
        self.play(
            FadeIn(plan_a, shift=RIGHT),
            FadeIn(plan_b, shift=RIGHT),
            FadeIn(plan_c, shift=RIGHT)
        )
        self.wait(1)
        
        # Display the final formula
        self.play(Write(formula))
        self.wait(3)