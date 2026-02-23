from manim import *

class MultiStageVerificationLoop(Scene):
    def construct(self):
        # Define the gates
        req_ver = Rectangle(height=2, width=1.5).next_to(LEFT, UR)
        exec_ver = Rectangle(height=2, width=1.5).next_to(req_ver, RIGHT)
        imp_ver = Rectangle(height=2, width=1.5).next_to(exec_ver, RIGHT)
        gates = [req_ver, exec_ver, imp_ver]
        for gate in gates:
            gate.set_fill(BLUE, opacity=0.5)

        # Define the deployment icon
        deployment = ImageMobject("img-2.jpeg").next_to(imp_ver, RIGHT * 3)

        # Define the plan object
        plan = Square(side_length=0.5).next_to(req_ver, DOWN)

        # Animation steps
        self.play(Create(gates[0]), Write(MathTex(r"ReqVer")))
        self.play(Create(plan))
        self.wait(1)
        plan_fail = True
        for gate in gates:
            if plan_fail:
                self.play(plan.animate.scale(1.2).set_color(RED), run_time=0.5)
                self.play(plan.animate.scale(1 / 1.2).set_color(BLUE), run_time=0.5)
                plan_fail = False
            self.play(plan.animate.next_to(gate, UP))
            self.wait(1)
        if not plan_fail:
            self.play(plan.animate.next_to(deployment, UP))
            self.wait(1)
        else:
            self.play(FadeOut(plan), run_time=0.5)

        # Label the stages
        req_ver_label = MathTex(r"ReqVer").next_to(req_ver, UP)
        exec_ver_label = MathTex(r"ExecVer").next_to(exec_ver, UP)
        imp_ver_label = MathTex(r"ImpVer").next_to(imp_ver, UP)
        self.play(Create(req_ver_label), Create(exec_ver_label), Create(imp_ver_label))
        self.wait(2)