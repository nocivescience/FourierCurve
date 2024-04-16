from manim import *
import itertools as it
class ArrowScene(Scene):
    dic={
        'arrow_config': {
            'color': RED,
            'buff': 1,
            'stroke_width': 1,
            'max_tip_length_to_length_ratio': 0.1,
        },
    }
    def construct(self):
        dot1 = Dot(3*RIGHT, color=RED)
        dot2 = Dot(2*UP, color=BLUE)
        arrow = Arrow(dot1.get_center(), dot2.get_center(), **self.dic['arrow_config'])
        self.play(*(map(Create, [dot1, dot2, arrow])))
        self.wait()