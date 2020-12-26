from MatrixBuilder import *


def main():
    root = tk.Tk()
    root.title('Matrix Builder')
    root.geometry("850x700")
    main_window = MatrixBuilder(root)
    root.mainloop()


if __name__ == '__main__':
    main()


