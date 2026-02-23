from manim import *

class MultiStageVerificationLoop(Scene):
    def construct(self):
        # 1. Setup Layout Components
        planning_stage = VGroup(
            RoundedRectangle(height=1.5, width=2.5, corner_radius=0.1, color=BLUE),
            Text("Planning", font_size=24)
        ).to_edge(LEFT, buff=1.0)

        gate_x_positions = [-1, 1, 3]
        gate_names = ["ReqVer", "ExecVer", "ImpVer"]
        
        gates = VGroup()
        labels = VGroup()
        for x, name in zip(gate_x_positions, gate_names):
            g = Line(UP * 1.5, DOWN * 1.5, color=WHITE).move_to(RIGHT * x)
            l = Text(name, font_size=20).next_to(g, UP)
            gates.add(g)
            labels.add(l)

        deployment = VGroup(
            Star(color=YELLOW, fill_opacity=1).scale(0.5),
            Text("Deployment", font_size=20).shift(DOWN * 0.8)
        ).to_edge(RIGHT, buff=1.0)

        formula = MathTex(
            r"\mathcal{M}^{\star} = \mathcal{A}_{o}(I^{\star}) \text{ s.t. } \mathrm{ImpVer}(\mathcal{M}^{\star}) = \text{Pass}",
            font_size=32
        ).to_edge(DOWN, buff=0.8)

        self.add(planning_stage, gates, labels, deployment, formula)

        # 2. Plan Object (a small square)
        plan = Square(side_length=0.4, color=BLUE, fill_opacity=1)
        plan.move_to(planning_stage.get_center())
        self.add(plan)

        # 3. Animation Logic: The Gate Loop
        
        # --- Stage 1: ReqVer Gate Fail Loop ---
        # Move square to the first gate
        target_pos_1 = RIGHT * gate_x_positions[0] + LEFT * 0.3
        self.play(plan.animate.move_to(target_pos_1))
        
        # Fail the gate: Turn Red and draw feedback arrow
        self.play(plan.animate.set_color(RED))
        
        # Use Arrow with path_arc to replace CurvedArrow
        back_arrow = Arrow(
            plan.get_bottom(), 
            planning_stage[0].get_bottom(), 
            path_arc=PI/2, 
            color=RED
        )
        
        self.play(Create(back_arrow))
        self.play(
            plan.animate.move_to(planning_stage.get_center()),
            FadeOut(back_arrow),
            run_time=1
        )
        self.play(plan.animate.set_color(BLUE))

        # --- Stage 2: Successful progression through all gates ---
        
        # Gate 1: ReqVer Pass
        self.play(plan.animate.move_to(RIGHT * gate_x_positions[0] + LEFT * 0.3))
        self.play(plan.animate.set_color(GREEN))
        self.wait(0.2)
        
        # Gate 2: ExecVer Pass
        self.play(plan.animate.move_to(RIGHT * gate_x_positions[1] + LEFT * 0.3))
        self.play(plan.animate.set_color(GREEN))
        self.wait(0.2)
        
        # Gate 3: ImpVer Pass
        self.play(plan.animate.move_to(RIGHT * gate_x_positions[2] + LEFT * 0.3))
        self.play(plan.animate.set_color(GREEN))
        self.wait(0.2)
        
        # 4. Final Deployment
        self.play(plan.animate.move_to(deployment[0].get_center()))
        
        # Success effect
        self.play(
            deployment[0].animate.scale(1.4).set_color(GREEN),
            FadeOut(plan),
            run_time=0.8
        )
        self.play(Indicate(deployment[1], color=GREEN))
        
        self.wait(2)