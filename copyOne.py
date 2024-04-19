from manim import *
import itertools as it
class FourierScene(Scene):
    CONFIG={
        'wait_time': 12,
        'vector_config':{
            'max_tip_length_to_length_ratio':.25,
            'tip_length': 0.15,
            'stroke_width': 1.3
        },
        'vector_time':ValueTracker(0),
        'center_point':ORIGIN,
        'n_vectors':10,
        'random_seed':[-1,1],
    }
    def construct(self):
        vectors= self.get_rotating_vectors()
        self.add(vectors)
        self.wait(self.CONFIG['wait_time'])
    def get_freqs(self):
        n=self.CONFIG['n_vectors']
        all_freqs = list(range(n//2,-n//2,-1))
        all_freqs.sort(key=abs)
        return all_freqs
    def get_coefficients(self):
        n=self.CONFIG['n_vectors']
        lista=[i*4 for i in np.random.random(size=n)]
        return lista
    def get_rotating_vectors(self,freqs=None, coeffs=None):
        vectors=VGroup()
        self.center_tracker=VectorizedPoint(self.CONFIG['center_point'])
        if freqs is None:
            freqs=self.get_freqs()
        if coeffs is None:
            coeffs=self.get_coefficients()
        last_vector=None
        for freq, coeff, i in zip(freqs, coeffs, it.count(1)):
            if last_vector:
                center_func= last_vector.get_end
            else:
                center_func=self.center_tracker.get_location
            random=np.random.random()
            if random<.5:
                spin=-1
            else:
                spin=1
            vector=self.get_rotating_vector(coeff/i,freq,center_func,spin=spin)
            vectors.add(vector)
            last_vector=vector
        return vectors
    def get_rotating_vector(self,coeff,freq,center_func, spin):
        vector=Vector(**self.CONFIG['vector_config'])
        vector.coeff=coeff
        vector.freq=freq
        vector.center_func=center_func
        vector.spin=spin
        vector.scale(2)
        vector.add_updater(self.update_vector)
        return vector
    def update_vector(self,vector,dt):
        time=self.CONFIG['vector_time'].get_value()
        vector.set_length(vector.coeff.real)
        vector.rotate(vector.spin*(time+dt)*vector.freq,about_point=vector.get_start())
        vector.shift(vector.center_func()-vector.get_start())