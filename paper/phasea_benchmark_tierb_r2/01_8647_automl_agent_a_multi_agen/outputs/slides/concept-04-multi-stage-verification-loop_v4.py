from manim import *

class ConceptVerificationLoop(Scene):
    def construct(self):
        # 1. Setup Gates and Labels
        gate_x_positions = [-2.5, 0, 2.5]
        gate_names = ["ReqVer", "ExecVer", "ImpVer"]
        gates = VGroup()
        gate_labels = VGroup()

        for x, name in zip(gate_x_positions, gate_names):
            line = Line(2 * UP, 2 * DOWN, color=GREY)
            line.move_to(x * RIGHT)
            label = Text(name, font_size=24).next_to(line, UP)
            gates.add(line)
            gate_labels.add(label)

        # Start and end positions
        planning_point = 5.5 * LEFT
        deployment_point = 5.5 * RIGHT
        
        planning_label = Text("Planning", font_size=24).move_to(planning_point + 2.5 * UP)

        # Deployment Icon
        deploy_box = Square(side_length=1.0, color=BLUE, fill_opacity=0.3)
        deploy_text = Text("Deploy", font_size=18).move_to(deploy_box)
        deploy_icon = VGroup(deploy_box, deploy_text).move_to(deployment_point)
        deploy_label = Text("Deployment", font_size=24).next_to(deploy_icon, UP)

        self.add(gates, gate_labels, planning_label, deploy_icon, deploy_label)

        # 2. The 'Plan' Object
        plan_square = Square(side_length=0.5, color=WHITE, fill_opacity=1)
        plan_inner_text = Text("Plan", font_size=16, color=BLACK)
        plan = VGroup(plan_square, plan_inner_text).move_to(planning_point)

        # 3. Animation Logic
        self.play(FadeIn(plan))

        # First pass: Gate 1
        self.play(plan.animate.move_to(gate_x_positions[0] * RIGHT))
        self.play(plan_square.animate.set_color(GREEN))
        self.wait(0.2)

        # Hit Gate 2 and Fail
        self.play(plan.animate.move_to(gate_x_positions[1] * RIGHT))
        self.play(plan_square.animate.set_color(RED))
        
        # Feedback Loop Arrow (Using Arrow with path_arc to avoid CurvedArrow identifier)
        loop_arrow = Arrow(
            start=gate_x_positions[1] * RIGHT + 0.5 * UP,
            end=planning_point + 0.5 * UP,
            path_arc=-1.2,
            color=RED
        )
        self.play(Create(loop_arrow))
        
        # Loop back to Planning
        self.play(
            plan.animate.move_to(planning_point),
            FadeOut(loop_arrow),
            plan_square.animate.set_color(WHITE)
        )
        self.wait(0.5)

        # Second run: Success through all gates
        for pos in gate_x_positions:
            self.play(plan.animate.move_to(pos * RIGHT))
            self.play(plan_square.animate.set_color(GREEN))
            self.wait(0.1)

        # Final move to deployment
        self.play(plan.animate.move_to(deployment_point))
        self.play(FadeOut(plan))
        
        # Flash the deployment icon
        circles = VGroup(*[Circle(radius=r, color=BLUE).move_to(deployment_point) for r in [0.6, 0.8, 1.0]])
        self.play(FadeIn(circles, scale=1.5), FadeOut(circles), run_time=0.5)

        # 4. Narrator Text and Formula
        formula = MathTex(
            r"\mathcal{M}^{\star} = \mathcal{A}_{o}(I^{\star}) \text{ s.t. } \mathrm{ImpVer}(\mathcal{M}^{\star}) = \text{Pass}"
        ).scale(0.85).to_edge(DOWN, buff=0.8)

        # Voiceover summary
        narration = Text(
            "Three-stage verification gate ensures deployment-ready reliability.",
            font_size=20
        ).next_to(formula, UP, buff=0.4)

        self.play(Write(narration))
        self.play(Write(formula))
        self.wait(3)