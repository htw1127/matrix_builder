import tkinter as tk


class MyMatrix:
    """
    Redo this comment.
    """
    def __init__(self, dimension, pos, grid_pos, canvas, text=None):
        self.dimension = dimension
        self.pos = pos
        self.grid_pos = grid_pos
        self.canvas = canvas
        self.text = text
        self.anchor = None

        self.shape = None
        self.text_shape = None

    def set_anchor(self, new_anchor):
        self.anchor = new_anchor

    def move_matrix(self, pos):
        dx = pos[0] - self.anchor[0]
        dy = pos[1] - self.anchor[1]
        self.canvas.move(self.shape, dx, dy)
        self.canvas.move(self.text_shape, dx, dy)
        self.anchor = (pos[0], pos[1])

        self.pos = (self.pos[0] + dx, self.pos[1] + dy)

    def replace_matrix(self, dx, dy):
        self.canvas.move(self.shape, dx, dy)
        self.canvas.move(self.text_shape, dx, dy)

        self.pos = (self.pos[0] + dx, self.pos[1] + dy)

    def raise_matrix(self):
        self.canvas.tag_raise(self.shape)
        self.canvas.tag_raise(self.text_shape)

    def normal_highlight(self):
        self.released_config()

    def error_highlight(self):
        self.canvas.itemconfig(self.shape, fill='red')
        self.canvas.itemconfig(self.text_shape, fill="black")

    def pressed_config(self):
        self.canvas.itemconfig(self.shape, fill='black')
        self.canvas.itemconfig(self.text_shape, fill="white")
        self.raise_matrix()

    def released_config(self):
        self.canvas.itemconfig(self.shape, fill='white')
        self.canvas.itemconfig(self.text_shape, fill='black')

    def rename(self, new_name):
        self.text = new_name
        self.canvas.delete(self.shape)
        self.canvas.delete(self.text_shape)

    def resize(self, new_dimension):
        self.dimension = new_dimension
        self.canvas.delete(self.shape)
        self.canvas.delete(self.text_shape)

