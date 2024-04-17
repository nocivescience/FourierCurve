from manim import *
class VectorScene(Scene):
    dicc={
        'vector_config': {
            'buff': 0,
            'max_tip_length_to_length_ratio': .2,
            'stroke_width': .2
        }
    }
    def construct(self):
        vector = self.get_vector_rotating()
        vector2 = self.get_vector_rotating_2()
        self.add(vector, vector2)
        self.wait(5)
    def get_vector_rotating(self):
        vector=self.vector = Vector(RIGHT, **self.dicc['vector_config'])
        vector.add_updater(lambda v, dt: self.update_vector(v, dt))
        return vector
    def update_vector(self, vector, dt):
        vector.rotate(TAU * dt / 2, about_point=vector.get_start())
        return vector
    def get_vector_rotating_2(self):
        vector = Vector(RIGHT, **self.dicc['vector_config'])
        mob = self.vector
        vector.add_updater(lambda v, dt: self.update_vector_2(v, mob, dt))
        return vector
    def update_vector_2(self, vector, mob, dt):
        vector.move_to(mob.get_end(), vector.get_start())
        vector.rotate(TAU * dt / 2, about_point=vector.get_start())
        return vector, mob