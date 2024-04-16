from manim import *

class FourierScene(Scene):
    dicc={
        'config_vector': {
            'stroke_width': 0.3,
            'max_tip_length_to_length_ratio': 0.1,
            'buff': 0,
        },
        'n_vectors': 10,
    }
    def construct(self):
        vectors= self.get_rotating_vectors()
        self.add(vectors)
        self.wait(5)
    def get_freqs(self):
        return list(range(self.dicc['n_vectors']//2, -self.dicc['n_vectors']//2, -1))
    def get_coefficients(self):
        return [i*.1 for i in range(self.dicc['n_vectors'])]
    def get_rotating_vector(self, position, coef, freq):
        vector= Vector(RIGHT, **self.dicc['config_vector'])
        vector.scale(coef)
        vector.rotate(TAU*freq/self.dicc['n_vectors'], about_point=position)
        vector.shift(position)
        return vector
    def get_rotating_vectors(self,coefs=None, freqs=None):
        vectors= VGroup()
        last_vector_end= ORIGIN
        if freqs is None:
            freqs= self.get_freqs()
        if coefs is None:
            coefs= self.get_coefficients()
        for coef, freq in zip(coefs, freqs):
            vector= self.get_rotating_vector(last_vector_end, coef, freq)
            vectors.add(vector)
            last_vector_end= vector.get_end()
        return vectors