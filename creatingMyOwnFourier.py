from manim import *
class FourierScene(Scene):
    dicc={
        'config_vector': {
            'stroke_width': .2,
            'max_tip_length_to_length_ratio': 0.1,
            'buff':0
        },
    }
    def construct(self):
        pass
    def create_vectors(self):
        vectors= VGroup()
        return vectors
    def create_vectors_path(self, vectors):
        vector=Arrow(RIGHT, **self.dicc['config_vector'])
        vectors.add(vector)
        return vectors