from manim import *
class FourierScene(Scene):
    dicc={
        'n_vectors':10,
        'vector_config':{
            'buff':0,
            'max_tip_length_to_length_ratio':0.25,
            'max_stroke_width_to_length_ratio':0.2,
        },
        'center_point':ORIGIN,
    }
    def construct(self):
        self.get_vectors()
    def get_vectors(self):
        vectors= self.get_rotating_vectors()
        self.add(vectors)
        self.wait(3)
    def get_rotating_vectors(self):
        vectors=VGroup()
        for i in range(1,self.dicc['n_vectors']):
            if i>len(vectors)-1:
                break
            vector=self.get_rotating_vector(vectors[i-1])
            vectors.add(vector)
        return vectors
    def get_rotating_vector(self, prev_vector):
        vector= Vector(RIGHT,**self.dicc['vector_config'])
        vector.start=vector.get_start()
        vector.shift(prev_vector.get_end()-vector.start)
        return vector