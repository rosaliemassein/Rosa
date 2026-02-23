from manim import *

class IterativeClustering(Scene):
    def construct(self):
        dots = [Dot(radius=0.1).shift(RIGHT * (2 * i + 1) / 3 + UP * (2 * j + 1) / 3) for i in range(3) for j in range(3)]
        self.add(*dots)

        def find_closest_dots(dots):
            min_distance = float('inf')
            closest_pair = None
            for i, dot1 in enumerate(dots):
                for j, dot2 in enumerate(dots[i + 1:], start=i + 1):
                    distance = dot1.get_center()[0] - dot2.get_center()[0] + dot1.get_center()[1] - dot2.get_center()[1]
                    if distance < min_distance:
                        min_distance = distance
                        closest_pair = (dot1, dot2)
            return closest_pair

        seed_dots, _ = find_closest_dots(dots)
        seed_dots.set_color(YELLOW)

        search_circle = Circle(radius=0.2, color=BLUE).move_to(dots[0].get_center())
        self.add(search_circle)

        closest_dots, _ = find_closest_dots(dots)
        closest_dot = closest_dots[0]
        closest_dot.set_color(YELLOW)

        self.play(FadeIn(search_circle))
        self.wait(1)
        self.play(Transform(search_circle, Circle(radius=0.3, color=BLUE).move_to(closest_dot.get_center())))
        closest_dot.set_color(YELLOW)
        self.wait(1)

        # Repeat the process for 2 more clusters
        for _ in range(2):
            seed_dots, _ = find_closest_dots(dots)
            seed_dots.set_color(YELLOW)

            search_circle = Circle(radius=0.2, color=BLUE).move_to(seed_dots[0].get_center())
            self.add(search_circle)

            closest_dots, _ = find_closest_dots(dots)
            closest_dot = closest_dots[0]
            closest_dot.set_color(YELLOW)

            self.play(FadeIn(search_circle))
            self.wait(1)
            self.play(Transform(search_circle, Circle(radius=0.3, color=BLUE).move_to(closest_dot.get_center())))
            closest_dot.set_color(YELLOW)
            self.wait(1)

        self.wait(2)