from manim import *

class MultiAgentOrchestration(Scene):
    def construct(self):
        # Create the Agent Manager node
        manager_node = Circle(color=BLUE, radius=0.5)
        self.add(manager_node)

        # Draw arrows to the specialized agents
        arrow_p = Arrow(start=manager_node.get_center() + RIGHT * 2, end=manager_node.get_center() + LEFT * 3, buff=0.5)
        arrow_d = Arrow(start=manager_node.get_center() + RIGHT * 2, end=manager_node.get_center(), buff=0.5)
        arrow_m = Arrow(start=manager_node.get_center() + RIGHT * 2, end=manager_node.get_center() + RIGHT * 1.5, buff=0.5)
        arrow_o = Arrow(start=manager_node.get_center() + RIGHT * 2, end=manager_node.get_center() + LEFT * 0.5, buff=0.5)

        # Create and add the specialized agent nodes
        prompt_agent = Circle(color=RED, radius=0.3)
        data_agent = Circle(color=GREEN, radius=0.3)
        model_agent = Circle(color=YELLOW, radius=0.3)
        operation_agent = Circle(color=PURPLE, radius=0.3)
        
        self.add(prompt_agent, data_agent, model_agent, operation_agent)

        # Animate the arrows growing from the manager
        self.play(GrowFromCenter(arrow_p), GrowFromCenter(arrow_d), GrowFromCenter(arrow_m), GrowFromCenter(arrow_o))

        # Narration
        narration = Text("Imagine an AI project as a construction site. Instead of one person trying to build the whole house, AutoML-Agent uses a team of specialized workers. We have an Agent Manager acting as the conductor, delegating tasks to experts in data parsing, preprocessing, model design, and final code generation. This modular approach allows the system to handle the massive complexity of an end-to-end machine learning pipeline without getting overwhelmed.", font_size=24)
        self.play(Write(narration))
        self.wait()

        # Small task pulses flowing from the manager to each specialized agent
        prompt_pulse = Dot(radius=0.1, color=RED)
        data_pulse = Dot(radius=0.1, color=GREEN)
        model_pulse = Dot(radius=0.1, color=YELLOW)
        operation_pulse = Dot(radius=0.1, color=PURPLE)

        # Animate the task pulses
        self.play(FadeIn(prompt_pulse, shift=RIGHT * 2), FadeIn(data_pulse, shift=UP), FadeIn(model_pulse, shift=DOWN * 2), FadeIn(operation_pulse, shift=LEFT))
        self.wait()

        # Final message
        final_message = Text("Understand the roles and hierarchy of the specialized agents within the AutoML-Agent framework.", font_size=24)
        self.play(Write(final_message))