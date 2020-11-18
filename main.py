from MatrixBook import *
from utils import *

root = Tk()
root.title('Matrix')
root.geometry("1000x700")

w = 600
h = 600
x = w // 2
y = h // 2
matx_canvas = Canvas(root, width=w, height=h, bg='white')
matx_canvas.grid(row=0, column=0, rowspan=20, padx=20, pady=20)
matx_book = MatrixBook(matx_canvas, 20, 20)

""" Create canvas where user can interact with GUI. """
matx_book.add_matrix()


row_entry = Entry(root, width=20)
col_entry = Entry(root, width=20)
name_entry = Entry(root, width=20)
row_entry.grid(row=0, column=1)
col_entry.grid(row=1, column=1)
name_entry.grid(row=2, column=1)



""" Some other user widgets. """
def create_std_matx():
    matx_book.add_matrix()

    global status
    status.config(text=f'total matrix: {len(matx_book.matrix_list)}')

def create_custom_matx():
    row_size = row_entry.get()
    col_size = col_entry.get()
    if not row_size.isdigit() or not col_size.isdigit():
        print('Please input the valid format of row and cols!!!')
        return

    matx_book.add_custom_matrix(int(row_size), int(col_size), name_entry.get())

    global status
    status.config(text=f'total matrix: {len(matx_book.matrix_list)}')

def save_button():
    save_matrix(matx_book, 'temp')

    global status
    status.config(text=f'Saved!!')

def delete_button():
    matx_book.delete_matrix(matx_book.pressed_matrix)

    global status
    status.config(text=f'total matrix: {len(matx_book.matrix_list)}')

def reset_button():
    row_size = row_entry.get()
    col_size = col_entry.get()
    if not row_size.isdigit() or not col_size.isdigit():
        print('Please input the valid format of row and cols!!!')
        return

    global matx_book
    matx_book.delete_matrix(matx_book.matrix_list)
    matx_book.matrix_canvas.delete('all')

    matx_book = MatrixBook(matx_canvas, int(row_size), int(col_size))


butt_custom = Button(root, text='ADD the CUSTOM matrix!', command=create_custom_matx)
butt_std = Button(root, text='ADD the DEFAULT matrix!', command=create_std_matx)
butt_save = Button(root, text='SAVE your matrix data!!!', command=save_button)
butt_delete = Button(root, text='DELETE Selected Matrix!!!', command=delete_button)
butt_resize = Button(root, text='RESET your big Matrix!!!', command=reset_button)
butt_custom.grid(row=3, column=1, pady=5, padx=5)
butt_std.grid(row=4, column=1, pady=5, padx=5)
butt_save.grid(row=5, column=1, pady=5, padx=5)
butt_delete.grid(row=6, column=1, pady=5, padx=5)
butt_resize.grid(row=7, column=1, pady=5, padx=5)

status = Label(root, text='Hello there, Welcome!', bd=1, relief=SUNKEN)
status.grid(row=100, column=0)

root.mainloop()

