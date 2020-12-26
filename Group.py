

class Group:
    def __init__(self, dimension, grid_pos, canvas, name):
        self.dimension = dimension
        self.grid_pos = grid_pos
        self.canvas = canvas
        self.name = name

        self.shape = None

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name
