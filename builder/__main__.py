from builder.MatrixBuilder import *
import os
from builder.utils import CUR_DIR


def main():
    if not os.path.exists(os.path.join(CUR_DIR, 'Saved_Matrix')):
        os.makedirs(os.path.join(CUR_DIR, 'Saved_Matrix'))
    if not os.path.exists(os.path.join(CUR_DIR, 'output')):
        os.makedirs(os.path.join(CUR_DIR, 'output'))

    root = tk.Tk()
    root.title('Matrix Builder')
    root.geometry("900x700+10+10")
    file_dir = os.path.join(os.path.dirname(__file__), 'logo.ico')
    root.wm_iconbitmap(bitmap=file_dir)

    main_window = MatrixBuilder(root)
    root.mainloop()


if __name__ == '__main__':
    main()


