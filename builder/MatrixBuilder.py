from builder.MatrixBook import *
from builder.MyDialog import *
import os
from builder.utils import CUR_DIR


class MatrixBuilder:
    def __init__(self, master):
        self.master = master


        # Canvas Initialization
        w = 600
        h = 600
        matx_canvas = tk.Canvas(self.master, width=w, height=h, bg='white')
        matx_canvas.grid(row=0, column=0, rowspan=2, padx=20, pady=20)
        self.master.update_idletasks() # Another Strange Magic Solution
        self.matx_book = MatrixBook(self, matx_canvas, 20, 20)

        # Control Frame Initialization
        self.matx_control = tk.Frame(self.master)
        self.matx_control.grid(row=0, column=1)

        row_label = tk.Label(self.matx_control, text="Row: ", font='Helvetica 8 bold')
        col_label = tk.Label(self.matx_control, text="Col: ", font='Helvetica 8 bold')
        name_label = tk.Label(self.matx_control, text="Name: ", font='Helvetica 8 bold')
        self.row_entry = tk.Entry(self.matx_control, width=20)
        self.col_entry = tk.Entry(self.matx_control, width=20)
        self.name_entry = tk.Entry(self.matx_control, width=20)
        row_label.grid(row=0, column=0)
        col_label.grid(row=1, column=0)
        name_label.grid(row=2, column=0)
        self.row_entry.grid(row=0, column=1)
        self.col_entry.grid(row=1, column=1)
        self.name_entry.grid(row=2, column=1)

        butt_custom = tk.Button(self.matx_control, text='ADD the custom matrix', command=self.create_custom_matx)
        butt_delete = tk.Button(self.matx_control, text='DELETE selected matrix', command=self.delete_button)
        butt_zoom_in = tk.Button(self.matx_control, text='Zoom In', command=lambda: self.matx_book.zoom(self.matx_book.scale_factor + 5))
        butt_zoom_out = tk.Button(self.matx_control, text='Zoom Out', command=lambda: self.matx_book.zoom(self.matx_book.scale_factor - 5))
        butt_custom.grid(row=3, column=0, pady=5, columnspan=2)
        butt_delete.grid(row=4, column=0, pady=5, columnspan=2)
        butt_zoom_in.grid(row=5, column=0, pady=5)
        butt_zoom_out.grid(row=5, column=1, pady=5, padx=2)

        # Group Frame Initialization
        self.group_frame = tk.Frame(self.master)
        self.group_frame.grid(row=1, column=1)

        self.group_listbox = tk.Listbox(self.group_frame)
        self.group_listbox.pack()

        butt_add_group = tk.Button(self.group_frame, text='Add Current Group', command=self.add_current_group)
        butt_delete_group = tk.Button(self.group_frame, text='Delete Group', command=self.delete_group)
        butt_select_group = tk.Button(self.group_frame, text='Activate Group', command=self.select_group)
        butt_add_group.pack()
        butt_delete_group.pack()
        butt_select_group.pack()

        # Status bar initialization
        self.status = tk.Label(self.master, text='Hello there, Welcome!', bd=1, relief=tk.SUNKEN)
        self.status.grid(row=100, column=0)

        # Menu initialization
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

        # Bindings for the Builder
        master.bind('<Configure>', self.resize_canvas)


    def add_current_group(self):
        if self.matx_book.current_group is None:
            return

        new_name = self.ask_user('group')
        if not new_name or self.matx_book.group_list.contains(new_name):
            if new_name is not None:
                self.update_status('Please Input a valid group name, Duplicate Names and Empty String is not allowed.')
            return
        self.matx_book.current_group.set_name(new_name)
        self.matx_book.group_list.add_group(self.matx_book.current_group)
        self.group_listbox.insert(0, self.matx_book.current_group.get_name())

    def delete_group(self):
        self.matx_book.group_list.delete_group(self.group_listbox.get(tk.ANCHOR))
        self.group_listbox.delete(tk.ANCHOR)

    def select_group(self):
        self.matx_book.change_group(self.group_listbox.get(tk.ANCHOR))

    def resize_canvas(self, e):
        new_width = self.master.winfo_width() - 250
        new_height = self.master.winfo_height() - 100
        self.matx_book.get_canvas().config(width=new_width, height=new_height)

    def get_dimension_entry(self):
        row = self.row_entry.get()
        col = self.col_entry.get()

        if not(row.isdigit()) or not (col.isdigit()):
            self.update_status('Please input valid arguments for row and column entries.')
            return None
        return int(row), int(col)

    def get_name_entry(self):
        name = self.name_entry.get()
        if len(name.split()) > 1:
            self.update_status('Name cannot contain any whitespace.')
            return None
        elif len(name.split()) == 0:
            self.update_status('Please provide a name for your sub-matrix.')
            return None

        return name

    """ Some other user widgets. """
    def create_custom_matx(self, dim=None, name=None, grid_pos=None):
        if not dim:
            dim = self.get_dimension_entry()
            if dim is None:
                return
        if not name:
            name = self.get_name_entry()
        if not grid_pos:
            pos = (self.matx_book.get_canvas().winfo_width() // 2, self.matx_book.get_canvas().winfo_height() // 2)
            grid_pos = self.matx_book.pos_to_grid(pos)

        pos = self.matx_book.grid_to_pos(grid_pos)
        self.matx_book.add_custom_matrix(dim, pos, name)

        self.update_status(f'Total matrix: {len(self.matx_book.matrix_list)}')

    def delete_button(self):
        self.matx_book.delete_matrix(self.matx_book.pressed_matrix)

    def reset(self, size=None):
        if not size:
            size = self.ask_user('reset')
            if not size:
                return
        row_size, col_size = int(size[0]), int(size[1])

        self.matx_book.delete_matrix(self.matx_book.matrix_list)
        self.matx_book.get_canvas().delete('all')

        self.matx_book = MatrixBook(self, self.matx_book.get_canvas(), int(row_size), int(col_size))

        new_dim = self.matx_book.get_dimension()
        self.update_status(f'Reset Successful! Current Matrix Size is: ({new_dim[0]}, {new_dim[1]})')

    def resize(self, size=None):
        query_output = size
        if not query_output:
            query_output = self.ask_user('resize')

        if not query_output or not query_output[0] or not query_output[1]:
            return

        row, col = query_output
        self.matx_book.row = int(row)
        self.matx_book.col = int(col)
        self.matx_book.draw_grid()

        new_dim = self.matx_book.get_dimension()
        self.update_status(f'Resize Successful! Current Matrix Size is: ({new_dim[0]}, {new_dim[1]})')

    def ask_user(self, input_type):
        dialog_pop = None
        if input_type == 'save' or input_type == 'load' or input_type == 'export' or input_type == 'group':
            dialog_pop = NameDialog(self.master, input_type)
        elif input_type == 'resize' or input_type == 'reset':
            dialog_pop = RowColDialog(self.master, input_type)

        self.master.wait_window(dialog_pop.pop)
        return dialog_pop.query_output

    def update_status(self, new_msg):
        self.status.config(text=new_msg)


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

        file_dir = os.path.join(CUR_DIR, f'Saved_Matrix/{file_name}.txt')
        f = open(file_dir, 'w')
        f.write(f'{matrix_book.row} {matrix_book.col}\n')
        f.write(matx_data)
        f.close()

        self.update_status(f'Save Successful! Current matrix saved as: {file_name}.txt')

    def load_matrix(self, file_name=None):
        if not file_name:
            file_name = self.ask_user('load')
            if not file_name:
                return

        file_dir = os.path.join(CUR_DIR, f'Saved_Matrix/{file_name}.txt')
        with open(file_dir, 'r') as f:
            row, col = f.readline().split()
            self.reset((int(row), int(col)))

            f_line = f.readline()
            while len(f_line) > 0:
                name, pos_x, pos_y, row, col = f_line.split()
                dim = (int(row), int(col))
                pos = (int(pos_x), int(pos_y))
                self.create_custom_matx(dim, name, pos)

                f_line = f.readline()

        self.update_status(f'Load Successful! Current matrix is from: {file_name}.txt')

    def export_matrix(self, format_type):
        name = self.ask_user('export')
        if name is None:
            return

        if format_type == 'numpy':
            self.export_numpy_matrix(name)
        elif format_type == 'coo':
            self.export_coo_matrix(name)

        self.update_status(f'Export Successful!')

    # output file requires ** string ==(to)==> numpy ** array dictionary
    def export_numpy_matrix(self, def_name='matrix_func'):
        result_code = f'import numpy as np\n\n\n'
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

        file_dir = os.path.join(CUR_DIR, f'output/{def_name}.py')
        with open(file_dir, 'w') as f:
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

        file_dir = os.path.join(CUR_DIR, f'output/{def_name}.py')
        with open(file_dir, 'w') as f:
            f.write(result_code)

    def index_helper(self, index_str):
        result = index_str
        if result[0] == '-':
            result = result[1:]
        if result[-2:] == '.T':
            result = result[:-2]

        return result
