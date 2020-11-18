
from MyMatrix import *

class MatrixBook:

    """
    ==============
    Preliminary Functions which get used in initialization stage of the class.
    ==============
    """
    """
    Binding all the necessary key binds
    """
    def canvas_bind(self):
        self.matrix_canvas.bind('<B1-Motion>', self.move)
        self.matrix_canvas.bind('<ButtonRelease-1>', self.release_LMB)
        self.matrix_canvas.bind('<Button-1>', self.press_LMB)
        self.matrix_canvas.bind('<Control-Button-1>', self.ctrl_press_LMB)
        self.matrix_canvas.bind('<Control-v>', self.ctrl_v)
        self.matrix_canvas.bind('<KeyRelease-Control_L>', self.ctrl_release)
        self.matrix_canvas.bind('<Delete>', self.pressed_delete)
        self.matrix_canvas.bind('<Control-MouseWheel>', self.ctrl_wheel)
        self.matrix_canvas.bind('<Shift-Button-1>', self.shift_LMB)
        self.matrix_canvas.focus_force()

    def draw_grid(self, scale):
        for r in range(self.row + 1):
            row_line_len = scale * self.col
            line = self.matrix_canvas.create_line(self.offset[0], self.offset[1] + r*scale, self.offset[0] + row_line_len, self.offset[1] + r*scale, fill='gray')
            self.grid_line_list.append(line)

        for c in range(self.col + 1):
            col_line_len = scale * self.row
            line = self.matrix_canvas.create_line(self.offset[0] + c*scale, self.offset[1], self.offset[0] + c*scale, self.offset[1] + col_line_len, fill='gray')
            self.grid_line_list.append(line)


    """
    matrix_canvas: canvas for MyMatrix's
    pressed_matrix: List of pressed MyMatrix; sub list of shape list
    shape_list: list of all MyMatrix
    
    is_multi_selecting: boolean for if the program is in the middle of selecting
    selection_box: temporary rectangle for the BLUE Selection Box
    selection_box_anchor: box's anchor
    """
    def __init__(self, canvas, row=60, col=60):
        self.matrix_canvas = canvas
        self.pressed_matrix = []
        self.matrix_list = []
        self.grid_line_list = []
        self.canvas_bind()
        self.is_selecting = False
        self.offset = (0, 0)
        self.is_moving_offset = False
        self.offset_anchor = None

        self.is_multi_selecting = False
        self.selection_box = None
        self.selection_box_anchor = None

        self.row = row
        self.col = col
        self.scale_factor = min(600 // row, 600 // col)

        self.draw_grid(self.scale_factor)

    def add_matrix(self):
        self.add_custom_matrix(2, 2)

    def add_custom_matrix(self, row, col, name=None):
        ## todo: generalize x and y
        x = 300
        y = 200

        if not name:
            name = f'M{len(self.matrix_list)}'

        result_matx = MyMatrix(self.scale_factor, (row, col), (x, y), self.matrix_canvas, name)
        self.matrix_list.append(result_matx)



    def set_pressed_matrix(self, matx, anchor):
        self.pressed_matrix.append(matx)
        matx.pressed_config()
        for m in self.pressed_matrix:
            self.matrix_canvas.tag_raise(m.shape)
            self.matrix_canvas.tag_raise(m.text_shape)
            m.set_anchor(anchor)

    def in_shape_range(self, pos, shape):
        x1, y1, x2, y2 = self.matrix_canvas.coords(shape)
        is_in_y = y1 <= pos[1] <= y2
        is_in_x = x1 <= pos[0] <= x2
        return is_in_x and is_in_y

    def is_overlap(self, l1, r1, l2, r2):
        # If one rectangle is on left side of other
        if l1[0] >= r2[0] or l2[0] >= r1[0]:
            return False

        # If one rectangle is above other
        if l1[1] >= r2[1] or l2[1] >= r1[1]:
            return False

        return True

    def copy_matx(self, matx):
        offset = self.scale_factor
        new_pos = (matx.pos[0] + offset, matx.pos[1] + offset)
        result = MyMatrix(self.scale_factor, matx.dimension, new_pos, self.matrix_canvas, matx.text)
        self.matrix_list.append(result)

        return result

    def pos_to_grid(self, pos):
        x = pos[0] - self.offset[0]
        y = pos[1] - self.offset[1]

        return round(x / self.scale_factor), round(y / self.scale_factor)

    def grid_to_pos(self, grid):
        x = self.offset[0] + grid[0] * self.scale_factor
        y = self.offset[1] + grid[1] * self.scale_factor
        return x, y

    def follow_grid(self):
        for m in self.pressed_matrix:
            m.grid_pos = self.pos_to_grid(m.pos)
            new_x = self.offset[0] + m.grid_pos[0] * self.scale_factor
            new_y = self.offset[1] + m.grid_pos[1] * self.scale_factor

            dx = new_x - m.pos[0]
            dy = new_y - m.pos[1]
            m.replace_matrix(dx, dy)

    def delete_matrix(self, matx_list0):
        matx_list1 = matx_list0[:]
        while len(matx_list1) > 0:
            matx = matx_list1.pop()
            self.matrix_canvas.delete(matx.text_shape)
            self.matrix_canvas.delete(matx.shape)
            self.matrix_list.remove(matx)

            if matx in self.pressed_matrix:
                self.pressed_matrix.remove(matx)

    def zoom(self, scale):
        if not scale:
            print('Please input value scale input!')
            return

        self.matrix_canvas.delete('all')
        self.draw_grid(scale)
        self.scale_factor = scale

        for m in self.matrix_list:
            m.pos = self.grid_to_pos(m.grid_pos)
            m.draw_matrix(scale, m.dimension[0], m.dimension[1], m.pos[0], m.pos[1])



    """
    Below this Line, the functions are related to the key bindings.
    """
    def shift_LMB(self, e):
        self.is_moving_offset = True
        self.offset_anchor = (e.x, e.y)

    def ctrl_wheel(self, e):
        if e.delta > 0:
            self.zoom(self.scale_factor + 5)
        elif e.delta < 0:
            self.zoom(self.scale_factor - 5)

    def pressed_delete(self, e):
        self.delete_matrix(self.pressed_matrix)

    def press_LMB(self, e):
        self.matrix_canvas.focus_force()
        for matx in self.matrix_list:
            press_pos = (e.x, e.y)
            if self.in_shape_range(press_pos, matx.shape):
                self.set_pressed_matrix(matx, press_pos)
                return

        ## If there is not any box clicked, assume in multiple selection mode.
        self.is_multi_selecting = True
        self.selection_box = self.matrix_canvas.create_rectangle(e.x, e.y, e.x, e.y, fill='skyblue', stipple='gray25')
        self.selection_box_anchor = (e.x, e.y)

    def release_LMB(self, e):
        # Check if I am NOT in the middle of selection by pressing CTRL
        if not self.is_selecting:
            self.follow_grid()

            for m in self.matrix_list:
                m.set_anchor(None)
                m.released_config()
                for m2 in self.matrix_list:
                    if m2 is m:
                        continue
                    x1, y1, x2, y2 = self.matrix_canvas.coords(m.shape)
                    x10, y10, x20, y20 = self.matrix_canvas.coords(m2.shape)

                    if self.is_overlap((x1, y1), (x2, y2), (x10, y10), (x20, y20)):
                        m.error_highlight()
                        m2.error_highlight()

            for m in self.matrix_list:
                if m.grid_pos is None:
                    continue
                elif m.grid_pos[0] < 0 or m.grid_pos[1] < 0:
                    m.error_highlight()
                elif m.grid_pos[0] + m.dimension[0] > self.row or m.grid_pos[1] + m.dimension[1] > self.col:
                    m.error_highlight()


            self.pressed_matrix = []

        # Checks if I am in the middle of multi-selecting with the blue selection box
        if self.is_multi_selecting:
            x1, y1, x2, y2 = self.matrix_canvas.coords(self.selection_box)
            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1
            l1 = (x1, y1)
            r1 = (x2, y2)

            for m in self.matrix_list:
                x1, y1, x2, y2 = self.matrix_canvas.coords(m.shape)
                l2 = (x1, y1)
                r2 = (x2, y2)
                if self.is_overlap(l1, r1, l2, r2):
                    self.set_pressed_matrix(m, None)


            self.is_multi_selecting = False
            self.matrix_canvas.delete(self.selection_box)
            self.selection_box = None

        if self.is_moving_offset:
            self.is_moving_offset = False
            self.offset_anchor = None

    def ctrl_v(self, e):
        new_pressed_matx = self.pressed_matrix[:]
        self.release_LMB(e)

        for matx in new_pressed_matx:
            temp = self.copy_matx(matx)
            self.set_pressed_matrix(temp, None)


    def ctrl_press_LMB(self, e):
        self.is_selecting = True

        for matx in self.matrix_list:
            press_pos = (e.x, e.y)
            if self.in_shape_range(press_pos, matx.shape):
                self.set_pressed_matrix(matx, press_pos)
                break

    def ctrl_release(self, e):
        self.is_selecting = False

    def move(self, e):
        if not self.is_selecting:
            for m in self.pressed_matrix:
                if m.anchor:
                    m.move_matrix((e.x, e.y))

        if self.is_multi_selecting:
            x, y = self.selection_box_anchor
            self.matrix_canvas.coords(self.selection_box, x, y, e.x, e.y)

        if self.is_moving_offset:
            dx = e.x - self.offset_anchor[0]
            dy = e.y - self.offset_anchor[1]
            self.offset_anchor = (e.x, e.y)
            self.offset = (self.offset[0] + dx, self.offset[1] + dy)

            for m in self.matrix_list:
                m.replace_matrix(dx, dy)

            for l in self.grid_line_list:
                self.matrix_canvas.move(l, dx, dy)
