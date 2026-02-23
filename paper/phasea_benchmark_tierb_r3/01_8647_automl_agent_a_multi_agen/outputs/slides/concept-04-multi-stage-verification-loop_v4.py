from manim import *

class MultiStageVerificationLoop(Scene):
    def construct(self):
        # 1. Title and Formula Setup
        title = Text("Three-Stage Verification Gate", font_size=36).to_edge(UP)
        formula = MathTex(
            r"\mathcal{M}^{\star} = \mathcal{A}_{o}(I^{\star}) \text{ s.t. } \mathrm{ImpVer}(\mathcal{M}^{\star}) = \text{Pass}",
            font_size=30
        ).next_to(title, DOWN)
        
        self.play(Write(title), Write(formula))

        # 2. Layout: Gates, Labels, and Deployment Icon
        gate_positions = [LEFT * 2.5, ORIGIN, RIGHT * 2.5]
        gate_names = ["ReqVer", "ExecVer", "ImpVer"]
        gates = VGroup()
        labels = VGroup()

        for pos, name in zip(gate_positions, gate_names):
            line = Line(UP * 1.5, DOWN * 1.5, color=WHITE).move_to(pos)
            label = Text(name, font_size=24).next_to(line, UP)
            gates.add(line)
            labels.add(label)

        planning_pos = LEFT * 5 + UP * 0.5
        planning_label = Text("Planning", font_size=24).move_to(planning_pos)
        
        deployment_icon = VGroup(
            RegularPolygon(n=6, color=GOLD),
            Text("Deploy", font_size=18)
        ).scale(0.5).move_to(RIGHT * 5)

        self.play(
            Create(gates), 
            Write(labels), 
            Write(planning_label), 
            Create(deployment_icon)
        )
        self.wait(1)

        # 3. The Plan Object (Small Square)
        plan = Square(side_length=0.4, fill_opacity=1, color=YELLOW).move_to(LEFT * 5)
        self.play(Create(plan))

        # 4. Animation Sequence: First Attempt (Fail at ExecVer)
        # Move to Gate 1: Request Verification
        self.play(plan.animate.move_to(gate_positions[0]))
        self.play(plan.animate.set_color(GREEN)) # Success
        
        # Move to Gate 2: Execution Verification
        self.play(plan.animate.move_to(gate_positions[1]))
        self.play(plan.animate.set_color(RED)) # Fail
        
        # Loop back to Planning stage using Arrow with path_arc
        fail_arrow = Arrow(
            plan.get_top(), 
            planning_label.get_bottom(), 
            path_arc=-1.5, 
            color=RED,
            buff=0.2
        )
        self.play(Create(fail_arrow))
        self.play(plan.animate.move_to(LEFT * 5).set_color(YELLOW))
        self.play(FadeOut(fail_arrow))
        self.wait(0.5)
        
        # 5. Animation Sequence: Second Attempt (Full Success)
        # Gate 1
        self.play(plan.animate.move_to(gate_positions[0]))
        self.play(plan.animate.set_color(GREEN))
        
        # Gate 2
        self.play(plan.animate.move_to(gate_positions[1]))
        self.play(plan.animate.set_color(GREEN))
        
        # Gate 3: Implementation Verification
        self.play(plan.animate.move_to(gate_positions[2]))
        self.play(plan.animate.set_color(GREEN))
        
        # Deployment
        self.play(plan.animate.move_to(deployment_icon.get_center()))
        self.play(Indicate(deployment_icon, color=GREEN, scale_factor=1.3))
        
        self.wait(2)