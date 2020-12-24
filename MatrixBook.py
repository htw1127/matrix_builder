import tkinter as tk
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
        self.matrix_canvas.bind('<Button-3>', self.press_RMB)
        self.matrix_canvas.focus_force()

    def draw_grid(self, scale):
        for l in self.grid_line_list:
            self.matrix_canvas.delete(l)

        for r in range(self.row + 1):
            row_line_len = scale * self.col
            line = self.matrix_canvas.create_line(self.offset[0], self.offset[1] + r*scale, self.offset[0] + row_line_len, self.offset[1] + r*scale, fill='gray')
            self.grid_line_list.append(line)

        for c in range(self.col + 1):
            col_line_len = scale * self.row
            line = self.matrix_canvas.create_line(self.offset[0] + c*scale, self.offset[1], self.offset[0] + c*scale, self.offset[1] + col_line_len, fill='gray')
            self.grid_line_list.append(line)

        for m in self.matrix_list:
            m.raise_matrix()

    """
    matrix_canvas: canvas for MyMatrix's
    pressed_matrix: List of pressed MyMatrix; sub list of shape list
    shape_list: list of all MyMatrix
    
    is_multi_selecting: boolean for if the program is in the middle of selecting
    selection_box: temporary rectangle for the BLUE Selection Box
    selection_box_anchor: box's anchor
    """
    def __init__(self, main_window, canvas, row=60, col=60):
        self.main_window = main_window

        self.matrix_canvas = canvas
        self.pressed_matrix = []
        self.matrix_list = []
        self.grid_line_list = []
        self.is_selecting = False
        self.offset = (0, 0)
        self.is_moving_offset = False
        self.offset_anchor = None

        self.is_multi_selecting = False
        self.selection_box = None
        self.selection_box_anchor = None

        self.row = row
        self.col = col
        self.scale_factor = min(canvas.winfo_height() // row, canvas.winfo_width() // col)

        self.canvas_bind()
        self.draw_grid(self.scale_factor)

    def get_dimension(self):
        return self.row, self.col

    def get_canvas(self):
        return self.matrix_canvas

    def add_custom_matrix(self, dim, pos, name=None):
        grid_pos = self.pos_to_grid(pos)
        pos = self.grid_to_pos(grid_pos)
        if not name:
            name = f'M{len(self.matrix_list)}'

        result_matx = MyMatrix(self.scale_factor, dim, pos, grid_pos, self.matrix_canvas, name)
        self.matrix_list.insert(0, result_matx)

    def set_pressed_matrix(self, matx, anchor=None):
        if not (matx in self.pressed_matrix):
            self.pressed_matrix.append(matx)
            matx.pressed_config()
        lst = self.matrix_list
        lst.insert(0, lst.pop(lst.index(matx)))

        for m in self.pressed_matrix:
            m.set_anchor(anchor)

    def set_released_matrix(self, matx):
        if matx in self.pressed_matrix:
            self.pressed_matrix.remove(matx)
        matx.anchor = None
        matx.released_config()

    def release_all_matrix(self):
        while len(self.pressed_matrix) > 0:
            self.set_released_matrix(self.pressed_matrix[0])

    def in_shape_range(self, pos, matrix):
        x1, y1, x2, y2 = self.matrix_canvas.coords(matrix.shape)
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
        copy_grid_pos = self.pos_to_grid((matx.pos[0] + offset, matx.pos[1] + offset))
        copy_pos = self.grid_to_pos(copy_grid_pos)

        result = MyMatrix(self.scale_factor, matx.dimension, copy_pos, copy_grid_pos, self.matrix_canvas, matx.text)
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

        self.main_window.update_status(f'Total matrix: {len(self.matrix_list)}')

    def create_transpose(self):
        for m in self.pressed_matrix:
            if '.T' == m.text[-2:]:
                self.add_custom_matrix((m.dimension[1], m.dimension[0]), m.pos, m.text[:-2])
            else:
                self.add_custom_matrix((m.dimension[1], m.dimension[0]), m.pos, m.text + '.T')

        self.delete_matrix(self.pressed_matrix)

    def create_negate(self):
        for m in self.pressed_matrix:
            if '-' == m.text[0]:
                self.add_custom_matrix(m.dimension, m.pos, m.text[1:])
            else:
                self.add_custom_matrix(m.dimension, m.pos, '-' + m.text)

        self.delete_matrix(self.pressed_matrix)

    def rename_matrix(self):
        self.pressed_matrix[0].rename(self.main_window.get_name_entry())

    def resize_matrix(self):
        self.pressed_matrix[0].resize(self.main_window.get_dimension_entry())

    def zoom(self, scale, pivot=(0, 0)):
        if scale is None or scale <= 0:
            print('Please input value scale input!')
            return

        self.matrix_canvas.delete('all')

        fine_grid_pos = ((pivot[0] - self.offset[0]) / self.scale_factor, (pivot[1] - self.offset[1]) / self.scale_factor)
        temp = scale - self.scale_factor
        diff = (fine_grid_pos[0] * temp, fine_grid_pos[1] * temp)
        self.offset = (self.offset[0] - diff[0], self.offset[1] - diff[1])
        self.scale_factor = scale

        self.draw_grid(scale)

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
            self.zoom(self.scale_factor + 5, (e.x, e.y))
        elif e.delta < 0:
            self.zoom(self.scale_factor - 5, (e.x, e.y))

    def pressed_delete(self, e):
        self.delete_matrix(self.pressed_matrix)

    def press_RMB(self, e):
        selected = None
        for m in self.matrix_list:
            if self.in_shape_range((e.x, e.y), m):
                selected = m
                break

        # When the background is chosen
        if selected is None:
            self.release_all_matrix()
            canvas_menu = tk.Menu(self.matrix_canvas, tearoff=False)
            canvas_menu.add_command(label='zoom in', command=lambda: self.zoom(self.scale_factor + 5, (e.x_root, e.y_root)))
            canvas_menu.add_command(label='zoom out', command=lambda: self.zoom(self.scale_factor - 5, (e.x_root, e.y_root)))
            canvas_menu.tk_popup(e.x_root, e.y_root)
            return

        # When the matrix is chosen
        if not (selected in self.pressed_matrix):
            self.release_all_matrix()
            self.set_pressed_matrix(selected)

        canvas_menu = tk.Menu(self.matrix_canvas, tearoff=False)
        canvas_menu.add_command(label='Transpose', command=self.create_transpose)
        canvas_menu.add_command(label='Negate', command=self.create_negate)
        canvas_menu.add_command(label='Delete', command=lambda: self.delete_matrix(self.pressed_matrix))
        if len(self.pressed_matrix) == 1:
            canvas_menu.add_command(label='Rename', command=self.rename_matrix)
            canvas_menu.add_command(label='Resize', command=self.resize_matrix)

        canvas_menu.tk_popup(e.x_root, e.y_root)

    def press_LMB(self, e):
        self.matrix_canvas.focus_force()
        for matx in self.matrix_list:
            press_pos = (e.x, e.y)
            if self.in_shape_range(press_pos, matx):
                self.set_pressed_matrix(matx, press_pos)
                return

    def release_LMB(self, e):
        self.follow_grid()

        # Check if the user is NOT in the middle of selection by pressing CTRL
        if not self.is_selecting and not self.is_multi_selecting and not self.is_moving_offset:
            for m in self.pressed_matrix:
                m.set_anchor(None)
                m.released_config()
                for m2 in self.matrix_list:
                    if m2 is m:
                        continue
                    x1, y1, x2, y2 = self.matrix_canvas.coords(m.shape)
                    x10, y10, x20, y20 = self.matrix_canvas.coords(m2.shape)

                    if self.is_overlap((x1, y1), (x2, y2), (x10, y10), (x20, y20)):
                        m.error_highlight()

            for m in self.pressed_matrix:
                if m.grid_pos is None:
                    continue
                elif m.grid_pos[0] < 0 or m.grid_pos[1] < 0:
                    m.error_highlight()
                elif m.grid_pos[0] + m.dimension[1] > self.col or m.grid_pos[1] + m.dimension[0] > self.row:
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
                    self.set_pressed_matrix(m)


            self.is_multi_selecting = False
            self.matrix_canvas.delete(self.selection_box)
            self.selection_box = None

        # Check if the user was moving the screen
        if self.is_moving_offset:
            self.is_moving_offset = False
            self.offset_anchor = None

    def ctrl_v(self, e):
        new_pressed_matx = self.pressed_matrix[:]
        self.release_LMB(e)

        for matx in new_pressed_matx:
            temp = self.copy_matx(matx)
            self.set_pressed_matrix(temp)

    def ctrl_press_LMB(self, e):
        self.is_selecting = True

        for matx in self.matrix_list:
            press_pos = (e.x, e.y)
            if self.in_shape_range(press_pos, matx):
                if matx in self.pressed_matrix:
                    self.set_released_matrix(matx)
                else:
                    self.set_pressed_matrix(matx)
                return

        # If there is not any box clicked, assume in multiple selection mode.
        self.is_multi_selecting = True
        self.selection_box = self.matrix_canvas.create_rectangle(e.x, e.y, e.x, e.y, fill='skyblue', stipple='gray25')
        self.selection_box_anchor = (e.x, e.y)

    def ctrl_release(self, e):
        self.is_selecting = False

    def move(self, e):
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

        if self.is_selecting or self.is_moving_offset or self.is_multi_selecting:
            return

        for m in self.pressed_matrix:
            if m.anchor:
                m.move_matrix((e.x, e.y))

    def on_resize(self, e):
        new_width = e.width - 400
        new_height = e.height - 200
        self.matrix_canvas.config(width=new_width, height=new_height)


