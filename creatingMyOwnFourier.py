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
        vectors = self.get_rotating_vectors()
        self.add(vectors)
        self.wait(5)
        
    def get_freqs(self):
        all_freqs = list(range(self.dicc['n_vectors']//2, -self.dicc['n_vectors']//2, -1))
        all_freqs.sort(key=abs)
        return all_freqs
    
    def get_coefficients(self):
        return [i*.1 for i in range(self.dicc['n_vectors'])]
    
    def get_rotating_vector(self, position, coef, freq):
        vector = Vector(RIGHT, **self.dicc['config_vector'])
        vector.scale(coef)
        vector.shift(position)
        vector.add_updater(lambda v, dt: self.update_vector(v, dt, freq))  # Actualiza el vector con una frecuencia dada
        return vector
    
    def update_vector(self, vector, dt, freq):
        vector.rotate(TAU * freq * dt / self.dicc['n_vectors'], about_point=vector.get_start())  # Rota el vector con una frecuencia dada

    def get_rotating_vectors(self, coefs=None, freqs=None):
        vectors = VGroup()
        start_position = ORIGIN
        if freqs is None:
            freqs = self.get_freqs()
        if coefs is None:
            coefs = self.get_coefficients()
        for coef, freq in zip(coefs, freqs):
            vector = self.get_rotating_vector(start_position, coef, freq)
            vectors.add(vector)
            start_position = vector.get_end()
        return vectors
