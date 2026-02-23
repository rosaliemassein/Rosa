from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Setup Formula (using Text for robustness against LaTeX errors)
        formula = Text("A_mgr → {A_p, A_d, A_m, A_o}", font_size=24).to_edge(UP)
        self.add(formula)

        # 2. Central Node: Agent Manager
        manager_center = UP * 2
        manager_circle = Circle(radius=0.6, color=GREEN, fill_opacity=0.2)
        manager_circle.move_to(manager_center)
        manager_label = Text("Agent Manager", color=GREEN, font_size=20).next_to(manager_circle, UP)
        manager_group = VGroup(manager_circle, manager_label)

        # 3. Sub-nodes: Specialized Agents
        agent_names = ["Prompt Agent", "Data Agent", "Model Agent", "Operation Agent"]
        agent_colors = [RED, ORANGE, BLUE, YELLOW]
        agent_x_positions = [-4.5, -1.5, 1.5, 4.5]
        
        agent_nodes = VGroup()
        arrows = VGroup()
        
        for i in range(4):
            agent_pos = [agent_x_positions[i], -0.5, 0]
            circle = Circle(radius=0.5, color=agent_colors[i], fill_opacity=0.2)
            circle.move_to(agent_pos)
            label = Text(agent_names[i], color=agent_colors[i], font_size=18).next_to(circle, DOWN)
            node = VGroup(circle, label)
            agent_nodes.add(node)
            
            # Connect Manager to Agents
            arrow = Arrow(
                start=manager_circle.get_bottom(),
                end=circle.get_top(),
                buff=0.1,
                color=GREY,
                stroke_width=3
            )
            arrows.add(arrow)

        # 4. Building the Hierarchy
        self.play(GrowFromCenter(manager_group))
        self.wait(0.5)
        self.play(
            LaggedStart(*[Create(arrow) for arrow in arrows], lag_ratio=0.2),
            LaggedStart(*[GrowFromCenter(node) for node in agent_nodes], lag_ratio=0.2)
        )
        self.wait(1)

        # 5. User Instruction pulse
        user_node = VGroup(
            Dot(color=WHITE).move_to(LEFT * 5 + DOWN * 3),
            Text("User", font_size=20).move_to(LEFT * 5 + DOWN * 3.4)
        )
        self.play(FadeIn(user_node))
        
        instruction_pulse = Dot(color=WHITE).move_to(user_node[0].get_center())
        pulse_label = Text("User Instruction", font_size=16).next_to(instruction_pulse, UP)
        
        self.play(FadeIn(instruction_pulse), Write(pulse_label))
        self.play(
            instruction_pulse.animate.move_to(manager_circle.get_center()),
            pulse_label.animate.move_to(manager_circle.get_center() + RIGHT * 1.5),
            run_time=1.5
        )
        self.play(FadeOut(instruction_pulse), FadeOut(pulse_label))
        self.play(manager_circle.animate.scale(1.2).set_fill(opacity=0.5), run_time=0.2)
        self.play(manager_circle.animate.scale(1/1.2).set_fill(opacity=0.2), run_time=0.2)

        # 6. Task Pulses from Manager to Agents
        task_texts = [
            "Ask for task", 
            "Data Parsing", 
            "Model Design", 
            "Execution"
        ]

        for i in range(4):
            task_dot = Dot(color=agent_colors[i]).move_to(manager_circle.get_center())
            task_label = Text(task_texts[i], font_size=14, color=agent_colors[i]).next_to(agent_nodes[i], DOWN * 2)
            
            self.play(
                task_dot.animate.move_to(agent_nodes[i][0].get_center()),
                Write(task_label),
                run_time=0.8
            )
            self.play(FadeOut(task_dot))

        self.wait(2)