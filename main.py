from MatrixBook import *

class MyDialog:
    def __init__(self, parent, input_type):
        self.parent = parent
        self.pop = Toplevel(parent)
        self.pop.title("Input Query")
        self.pop.geometry("300x130")

        self.intro_frame = Frame(self.pop)
        self.intro_frame.pack(pady=3)
        self.query_frame = Frame(self.pop)
        self.query_frame.pack(pady=3)
        self.choice_frame = Frame(self.pop)
        self.choice_frame.pack(pady=3)

        self.welcome_msg = Label(self.intro_frame)
        head_text = ''
        if input_type == 'resize':
            head_text = 'Please Input Dimension of Resize Matrix.'
        elif input_type == 'reset':
            head_text = 'Please Input Dimension of Reset Matrix.'
        elif input_type == 'save':
            head_text = 'Please Input the Name of this Matrix.'
        elif input_type == 'load':
            head_text = 'Please Input the Name of the Matrix to Load.'
        self.welcome_msg.config(text=head_text)
        self.welcome_msg.pack()

        done = Button(self.choice_frame, text='Done', command=lambda: self.user_input('done'))
        cancel = Button(self.choice_frame, text='Cancel', command=lambda: self.user_input('cancel'))
        done.grid(row=0, column=0, pady=10, padx=2)
        cancel.grid(row=0, column=1, pady=10, padx=2)

        self.query_output = None

    def user_input(self, choice):
        pass


class RowColDialog(MyDialog):
    def __init__(self, parent, input_type):
        super().__init__(parent, input_type)

        pop_label_row = Label(self.query_frame, text="Row: ", font='Helvetica 8 bold')
        pop_label_col = Label(self.query_frame, text="Col: ", font='Helvetica 8 bold')
        self.pop_entry_row = Entry(self.query_frame, width=15)
        self.pop_entry_col = Entry(self.query_frame, width=15)

        pop_label_row.grid(row=0, column=0)
        pop_label_col.grid(row=1, column=0)
        self.pop_entry_row.grid(row=0, column=1)
        self.pop_entry_col.grid(row=1, column=1)

        self.pop_entry_row.focus()

    def user_input(self, choice):
        if choice == 'done':
            row = self.pop_entry_row.get()
            col = self.pop_entry_col.get()
            self.query_output = (row, col)

        self.pop.destroy()


class NameDialog(MyDialog):
    def __init__(self, parent, input_type):
        super().__init__(parent, input_type)

        label_name = Label(self.query_frame, text="Name: ", font='Helvetica 8 bold')
        self.entry_name = Entry(self.query_frame, width=15)

        label_name.grid(row=0, column=0)
        self.entry_name.grid(row=0, column=1)

        self.entry_name.focus()

    def user_input(self, choice):
        if choice == 'done':
            self.query_output = self.entry_name.get()

        self.pop.destroy()


class MatrixBuilder:
    def __init__(self, master):
        self.master = master

        w = 600
        h = 600
        self.matx_canvas = Canvas(self.master, width=w, height=h, bg='white')
        self.matx_canvas.grid(row=0, column=0, rowspan=50, padx=20, pady=20)
        self.matx_book = MatrixBook(self.matx_canvas, 20, 20)

        """ Create canvas where user can interact with GUI. """
        row_label = Label(self.master, text="Row: ", font='Helvetica 8 bold')
        col_label = Label(self.master, text="Col: ", font='Helvetica 8 bold')
        name_label = Label(self.master, text="Name: ", font='Helvetica 8 bold')
        self.row_entry = Entry(self.master, width=20)
        self.col_entry = Entry(self.master, width=20)
        self.name_entry = Entry(self.master, width=20)
        row_label.grid(row=0, column=1)
        col_label.grid(row=1, column=1)
        name_label.grid(row=2, column=1)
        self.row_entry.grid(row=0, column=2)
        self.col_entry.grid(row=1, column=2)
        self.name_entry.grid(row=2, column=2)

        butt_custom = Button(self.master, text='ADD the CUSTOM matrix!', command=self.create_custom_matx)
        butt_std = Button(self.master, text='ADD the DEFAULT matrix!', command=self.create_default_matx)
        butt_delete = Button(self.master, text='DELETE Selected matrix!!!', command=self.delete_button)
        butt_zoom_in = Button(self.master, text='Zoom In', command=lambda: self.matx_book.zoom(self.matx_book.scale_factor + 5))
        butt_zoom_out = Button(self.master, text='Zoom Out', command=lambda: self.matx_book.zoom(self.matx_book.scale_factor - 5))
        butt_custom.grid(row=3, column=1, pady=5, columnspan=2)
        butt_std.grid(row=4, column=1, pady=5, columnspan=2)
        butt_delete.grid(row=5, column=1, pady=5, columnspan=2)
        butt_zoom_in.grid(row=6, column=1, pady=5)
        butt_zoom_out.grid(row=6, column=2, pady=5, padx=2)

        self.status = Label(self.master, text='Hello there, Welcome!', bd=1, relief=SUNKEN)
        self.status.grid(row=100, column=0)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        edit_menu = Menu(menu, tearoff=False)
        menu.add_cascade(label='Edit', menu=edit_menu)
        edit_menu.add_command(label='Resize', command=self.resize)
        edit_menu.add_command(label='Reset', command=self.reset)

        file_menu = Menu(menu, tearoff=False)
        menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_cascade(label='Save', command=self.save_matrix)
        file_menu.add_cascade(label='Load', command=self.load_matrix)
        file_menu.add_cascade(label='Python File', command=self.python_save_matrix)

    """ Some other user widgets. """
    def create_default_matx(self):
        self.create_custom_matx((2, 2))

        self.status.config(text=f'total matrix: {len(self.matx_book.matrix_list)}')

    def create_custom_matx(self, dim=None, name=None, grid_pos=None):
        if not dim:
            dim = (int(self.row_entry.get()), int(self.col_entry.get()))
        if not name:
            name = self.name_entry.get()
        if not grid_pos:
            ## todo: generalize pos?
            pos = (300, 200)
            grid_pos = self.matx_book.pos_to_grid(pos)

        dim = (int(dim[0]), int(dim[1]))
        pos = self.matx_book.grid_to_pos(grid_pos)
        self.matx_book.add_custom_matrix(dim, name, pos)

        self.status.config(text=f'total matrix: {len(self.matx_book.matrix_list)}')

    def delete_button(self):
        self.matx_book.delete_matrix(self.matx_book.pressed_matrix)

        self.status.config(text=f'total matrix: {len(self.matx_book.matrix_list)}')

    def reset(self, size=None):
        if not size:
            size = self.ask_user('reset')
            if not size:
                return
        row_size, col_size = int(size[0]), int(size[1])

        self.matx_book.delete_matrix(self.matx_book.matrix_list)
        self.matx_book.matrix_canvas.delete('all')

        self.matx_book = MatrixBook(self.matx_canvas, int(row_size), int(col_size))

    def resize(self, size=None):
        query_output = size
        if not query_output:
            query_output = self.ask_user('resize')

        if not query_output or not query_output[0] or not query_output[1]:
            return

        row, col = query_output
        self.matx_book.row = int(row)
        self.matx_book.col = int(col)
        self.matx_book.draw_grid(self.matx_book.scale_factor)

    def ask_user(self, input_type):
        dialog_pop = None
        if input_type == 'save' or input_type == 'load':
            dialog_pop = NameDialog(self.master, input_type)
        elif input_type == 'resize' or input_type == 'reset':
            dialog_pop = RowColDialog(self.master, input_type)

        self.master.wait_window(dialog_pop.pop)
        return dialog_pop.query_output

    """
    File I/O methods below
    *** NOTE ***
    Format of the savings
    NAME Y_POS X_POS HEIGHT(row) WIDTH(col)
    """
    def save_matrix(self, file_name=None):
        if not file_name:
            file_name = self.ask_user('save')
            if not file_name:
                return

        matrix_book = self.matx_book
        matx_data = ''
        for matx in matrix_book.matrix_list:
            pos_x, pos_y = matx.grid_pos
            row, col = matx.dimension

            matx_data += f'{matx.text} {pos_x} {pos_y} {row} {col}\n'

        f = open(f'Saved_Matrix/{file_name}.txt', 'w')
        f.write(f'{matrix_book.row} {matrix_book.col}\n')
        f.write(matx_data)
        f.close()

    def load_matrix(self, file_name=None):
        if not file_name:
            file_name = self.ask_user('load')
            if not file_name:
                return

        with open(f'Saved_Matrix/{file_name}.txt', 'r') as f:
            row, col = f.readline().split()
            self.reset((int(row), int(col)))

            f_line = f.readline()
            while len(f_line) > 0:
                name, pos_x, pos_y, row, col = f_line.split()
                dim = (int(row), int(col))
                pos = (int(pos_x), int(pos_y))
                self.create_custom_matx(dim, name, pos)

                f_line = f.readline()

    # output file requires string to numpy array dictionary
    def python_save_matrix(self, def_name='matrix_func'):
        result_code = f'def {def_name}(matrix_dict):\n'
        result_code+= f'\tresult = np.zeros(({self.matx_book.row}, {self.matx_book.col}))\n'
        result_code+= f'\n'

        for m in self.matx_book.matrix_list:
            slicing = f'{m.grid_pos[1]}:{m.grid_pos[1] + m.dimension[0]},{m.grid_pos[0]}:{m.grid_pos[0] + m.dimension[1]}'
            result_code += f'\tresult[{slicing}] = matrix_dict[\'{m.text}\']\n'

        result_code+= f'\n'
        result_code+= f'\treturn result\n'

        with open(f'output/{def_name}.py', 'w') as f:
            f.write(result_code)





def main():
    root = Tk()
    root.title('Matrix Builder')
    root.geometry("1000x700")
    main_window = MatrixBuilder(root)
    root.mainloop()


if __name__ == '__main__':
    main()


