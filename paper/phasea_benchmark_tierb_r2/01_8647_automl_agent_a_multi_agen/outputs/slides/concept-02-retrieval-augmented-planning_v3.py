from manim import *

class RetrievalAugmentedPlanning(Scene):
    def construct(self):
        # 1. Formula at the top
        formula = MathTex(r"\mathbf{P} = \mathcal{A}_{mgr}(\mathrm{RAP}(R))").to_edge(UP, buff=0.5)
        self.add(formula)

        # 2. Agent Manager (Central Icon)
        manager_circle = Circle(radius=1.0, color=BLUE, fill_opacity=0.3)
        manager_text = Text("Agent\nManager", font_size=24).move_to(manager_circle.get_center())
        manager = VGroup(manager_circle, manager_text).move_to(ORIGIN)

        # 3. Knowledge Base (Cloud Icon on the left)
        # Constructing a cloud-like shape from circles
        c1 = Circle(radius=0.5, color=GREY, fill_opacity=0.8).shift(LEFT * 0.4)
        c2 = Circle(radius=0.6, color=GREY, fill_opacity=0.8).shift(UP * 0.3)
        c3 = Circle(radius=0.5, color=GREY, fill_opacity=0.8).shift(RIGHT * 0.4)
        kb_icon = VGroup(c1, c2, c3).scale(0.8).shift(LEFT * 4.5)
        kb_text = Text("Knowledge\nBase", font_size=20).move_to(kb_icon.get_center())
        kb = VGroup(kb_icon, kb_text)

        # 4. Knowledge Arrow
        kb_arrow = Arrow(kb.get_right(), manager.get_left(), color=BLUE, buff=0.2)
        kb_label = Text("Knowledge", font_size=20, color=BLUE).next_to(kb_arrow, UP, buff=0.1)

        # Initial display
        self.play(FadeIn(kb), FadeIn(manager))
        self.play(GrowArrow(kb_arrow), FadeIn(kb_label))
        self.wait(0.5)

        # 5. Parallel Plans (Icons on the right)
        # Plan A: Transformer (represented by a square with grid lines)
        plan_a_icon = VGroup(Square(side_length=1, color=YELLOW), Line(LEFT, RIGHT).scale(0.4), Line(UP, DOWN).scale(0.4))
        # Plan B: CNN (represented by a triangle/pyramid)
        plan_b_icon = Triangle(color=GREEN).scale(0.6)
        # Plan C: Other strategy (represented by a hexagon)
        plan_c_icon = RegularPolygon(n=6, color=PURPLE).scale(0.5)

        plan_icons = [plan_a_icon, plan_b_icon, plan_c_icon]
        plan_labels = ["Plan A\n(Transformer)", "Plan B\n(CNN)", "Plan C\n(Other)"]
        
        plans = VGroup()
        arrows_to_plans = VGroup()

        for i, (icon, label_text) in enumerate(zip(plan_icons, plan_labels)):
            # Position plan units
            plan_unit = VGroup(icon, Text(label_text, font_size=18).next_to(icon, RIGHT, buff=0.2))
            plan_unit.move_to(RIGHT * 4 + UP * (1.5 - i * 1.5))
            plans.add(plan_unit)
            
            # Create branching arrow
            arr = Arrow(manager.get_right(), plan_unit.get_left(), buff=0.1, color=WHITE)
            arrows_to_plans.add(arr)

        # 6. Animation: Branching Out
        # Instead of ImageMobjects, we transform the concept of the manager's output into multiple plans
        self.play(
            LaggedStart(
                *[GrowArrow(arr) for arr in arrows_to_plans],
                lag_ratio=0.2
            ),
            LaggedStart(
                *[FadeIn(p, shift=RIGHT) for p in plans],
                lag_ratio=0.2
            )
        )
        self.wait(1)

        # 7. Narration Text (Summary)
        narration_box = Rectangle(height=1.2, width=12, fill_color=BLACK, fill_opacity=0.8, stroke_width=0).to_edge(DOWN, buff=0)
        narration = Text(
            "RAP queries external knowledge to generate multiple diverse plans in parallel.",
            font_size=24,
            color=WHITE
        ).move_to(narration_box.get_center())

        self.play(FadeIn(narration_box), Write(narration))
        self.wait(3)