from tkinter import *


class MyMatrix:
    def draw_matrix(self, scale, row, col, x_pos, y_pos):
        width = col * scale
        height = row * scale
        self.shape = self.canvas.create_rectangle(x_pos, y_pos, x_pos + width, y_pos + height)

        x1, y1, x2, y2 = self.canvas.coords(self.shape)
        offset_x = (x2 - x1) // 2
        offset_y = (y2 - y1) // 2
        self.text_shape = self.canvas.create_text(x1 + offset_x, y1 + offset_y, text=self.text)


    """
    Redo this comment.
    """
    def __init__(self, scale, dimension, pos, canvas, text=None):
        self.scale = scale
        self.dimension = dimension
        self.pos = pos
        self.grid_pos = None
        self.canvas = canvas
        self.text = text
        self.anchor = None

        self.shape = None
        self.text_shape = None
        self.draw_matrix(scale, dimension[0], dimension[1], pos[0], pos[1])

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


    def normal_highlight(self):
        self.released_config()

    def error_highlight(self):
        self.canvas.itemconfig(self.shape, fill='red')
        self.canvas.itemconfig(self.text_shape, fill="black")

    def pressed_config(self):
        self.canvas.itemconfig(self.shape, fill='black')
        self.canvas.itemconfig(self.text_shape, fill="white")

    def released_config(self):
        self.canvas.itemconfig(self.shape, fill='white')
        self.canvas.itemconfig(self.text_shape, fill='black')







