from MatrixBook import *
from MyDialog import *


class MatrixBuilder:
    def __init__(self, master):
        self.master = master

        w = 600
        h = 600
        self.matx_canvas = tk.Canvas(self.master, width=w, height=h, bg='white')
        self.matx_canvas.grid(row=0, column=0, rowspan=50, padx=20, pady=20)
        self.matx_book = MatrixBook(self.matx_canvas, 20, 20)

        """ Create canvas where user can interact with GUI. """
        row_label = tk.Label(self.master, text="Row: ", font='Helvetica 8 bold')
        col_label = tk.Label(self.master, text="Col: ", font='Helvetica 8 bold')
        name_label = tk.Label(self.master, text="Name: ", font='Helvetica 8 bold')
        self.row_entry = tk.Entry(self.master, width=20)
        self.col_entry = tk.Entry(self.master, width=20)
        self.name_entry = tk.Entry(self.master, width=20)
        row_label.grid(row=0, column=1)
        col_label.grid(row=1, column=1)
        name_label.grid(row=2, column=1)
        self.row_entry.grid(row=0, column=2)
        self.col_entry.grid(row=1, column=2)
        self.name_entry.grid(row=2, column=2)

        butt_custom = tk.Button(self.master, text='ADD the CUSTOM matrix!', command=self.create_custom_matx)
        butt_std = tk.Button(self.master, text='ADD the DEFAULT matrix!', command=self.create_default_matx)
        butt_delete = tk.Button(self.master, text='DELETE Selected matrix!!!', command=self.delete_button)
        butt_zoom_in = tk.Button(self.master, text='Zoom In', command=lambda: self.matx_book.zoom(self.matx_book.scale_factor + 5))
        butt_zoom_out = tk.Button(self.master, text='Zoom Out', command=lambda: self.matx_book.zoom(self.matx_book.scale_factor - 5))
        butt_custom.grid(row=3, column=1, pady=5, columnspan=2)
        butt_std.grid(row=4, column=1, pady=5, columnspan=2)
        butt_delete.grid(row=5, column=1, pady=5, columnspan=2)
        butt_zoom_in.grid(row=6, column=1, pady=5)
        butt_zoom_out.grid(row=6, column=2, pady=5, padx=2)

        self.status = tk.Label(self.master, text='Hello there, Welcome!', bd=1, relief=tk.SUNKEN)
        self.status.grid(row=100, column=0)

        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        edit_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label='Edit', menu=edit_menu)
        edit_menu.add_command(label='Resize', command=self.resize)
        edit_menu.add_command(label='Reset', command=self.reset)

        file_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_cascade(label='Save', command=self.save_matrix)
        file_menu.add_cascade(label='Load', command=self.load_matrix)

        file_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label='Export', menu=file_menu)
        file_menu.add_cascade(label='Numpy', command=lambda: self.export_matrix('numpy'))
        file_menu.add_cascade(label='Sparse (COO)', command=lambda: self.export_matrix('coo'))

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
            pos = (300, 200)
            grid_pos = self.matx_book.pos_to_grid(pos)

        dim = (int(dim[0]), int(dim[1]))
        pos = self.matx_book.grid_to_pos(grid_pos)
        self.matx_book.add_custom_matrix(dim, pos, name)

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
        if input_type == 'save' or input_type == 'load' or input_type == 'export':
            dialog_pop = NameDialog(self.master, input_type)
        elif input_type == 'resize' or input_type == 'reset':
            dialog_pop = RowColDialog(self.master, input_type)

        self.master.wait_window(dialog_pop.pop)
        return dialog_pop.query_output

    """
    File I/O methods below
    *** NOTE ***
    Format of the savings
    NAME X_POS Y_POS HEIGHT(row) WIDTH(col)
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

    def export_matrix(self, format_type):
        name = self.ask_user('export')
        if name is None:
            return

        if format_type == 'numpy':
            self.export_numpy_matrix(name)
        elif format_type == 'coo':
            self.export_coo_matrix(name)

    # output file requires ** string ==(to)==> numpy ** array dictionary
    def export_numpy_matrix(self, def_name='matrix_func'):
        result_code = f'import numpy as np\n\n'
        result_code+= f'def {def_name}(matrix_dict):\n'
        result_code+= f'\tresult = np.zeros(({self.matx_book.row}, {self.matx_book.col}))\n'
        result_code+= f'\n'

        for m in self.matx_book.matrix_list:
            rhs = ''
            index = m.text
            if index[0] == '-':
                index = index[1:]
            if index[-2:] == '.T':
                index = index[:-2]

            if m.text[0] == '-':
                rhs = f'-1 * matrix_dict[\'{index}\']'
            else:
                rhs = f'matrix_dict[\'{index}\']'
            if m.text[-2:] == '.T':
                rhs += '.T'

            lhs = ''
            slicing = f'{m.grid_pos[1]}:{m.grid_pos[1] + m.dimension[0]}, {m.grid_pos[0]}:{m.grid_pos[0] + m.dimension[1]}'
            lhs = f'result[{slicing}]'

            result_code += f'\t{lhs} = {rhs}\n'

        result_code += f'\n'
        result_code += f'\treturn result\n'

        with open(f'output/{def_name}.py', 'w') as f:
            f.write(result_code)

    def export_coo_matrix(self, def_name='matrix_func'):
        result_code = f'import numpy as np\n'
        result_code+= f'from scipy import sparse\n\n'
        result_code+= f'def {def_name}(matrix_dict):\n'
        result_code+= f'\trow_indices = list()\n'
        result_code+= f'\tcol_indices = list()\n'
        result_code+= f'\tvalues = list()\n'

        for m in self.matx_book.matrix_list:
            for r in range(m.dimension[0]):
                for c in range(m.dimension[1]):
                    index = self.index_helper(m.text)
                    value = ''
                    if m.text[-2:] == '.T':
                        value += f'matrix_dict[\'{index}\'][{c}, {r}]'
                    else:
                        value += f'matrix_dict[\'{index}\'][{r}, {c}]'
                    if m.text[0] == '-':
                        value = '-1 * ' + value

                    result_code+= f'\trow_indices.append({m.grid_pos[1] + r})\n'
                    result_code+= f'\tcol_indices.append({m.grid_pos[0] + c})\n'
                    result_code+= f'\tvalues.append({value})\n\n'


        result_code+= f'\treturn sparse.coo_matrix((np.array(values), (np.array(row_indices), np.array(col_indices))), shape=({self.matx_book.row}, {self.matx_book.col}))\n'

        with open(f'output/{def_name}.py', 'w') as f:
            f.write(result_code)

    def index_helper(self, index_str):
        result = index_str
        if result[0] == '-':
            result = result[1:]
        if result[-2:] == '.T':
            result = result[:-2]

        return result
