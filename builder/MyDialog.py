import tkinter as tk


class MyDialog:
    def __init__(self, parent, input_message):
        self.parent = parent
        self.pop = tk.Toplevel(parent)
        self.pop.title("Input Query")
        offset_w = parent.winfo_x() + parent.winfo_width()//2 - 100
        offset_h = parent.winfo_y() + parent.winfo_height()//2 - 100

        self.pop.geometry("300x130+%d+%d" % (offset_w, offset_h))
        self.pop.resizable(width=False, height=False)

        self.intro_frame = tk.Frame(self.pop)
        self.intro_frame.pack(pady=3)
        self.query_frame = tk.Frame(self.pop)
        self.query_frame.pack(pady=3)
        self.choice_frame = tk.Frame(self.pop)
        self.choice_frame.pack(pady=3)

        self.welcome_msg = tk.Label(self.intro_frame)
        self.welcome_msg.config(text=input_message)
        self.welcome_msg.pack()

        done = tk.Button(self.choice_frame, text='Done', command=lambda: self.user_input('done'))
        cancel = tk.Button(self.choice_frame, text='Cancel', command=lambda: self.user_input('cancel'))
        done.grid(row=0, column=0, pady=10, padx=2)
        cancel.grid(row=0, column=1, pady=10, padx=2)

        self.query_output = None

    def user_input(self, choice):
        pass


class RowColDialog(MyDialog):
    def __init__(self, parent, input_type):
        msg = ''
        if input_type == 'resize':
            msg = 'Please Input Dimension of Resize Matrix.'
        elif input_type == 'reset':
            msg = 'Please Input Dimension of Reset Matrix.'
        super().__init__(parent, msg)

        pop_label_row = tk.Label(self.query_frame, text="Row: ", font='Helvetica 8 bold')
        pop_label_col = tk.Label(self.query_frame, text="Col: ", font='Helvetica 8 bold')
        self.pop_entry_row = tk.Entry(self.query_frame, width=15)
        self.pop_entry_col = tk.Entry(self.query_frame, width=15)

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
        msg = ''
        if input_type == 'resize':
            msg = 'Please Input the Name of this Matrix.'
        elif input_type == 'reset':
            msg = 'Please Input the Name of the Matrix to Load.'
        elif input_type == 'export':
            msg = 'Please Input the Name of the Function'
        elif input_type == 'group':
            msg = 'Please Input the Name of the Group'
        super().__init__(parent, msg)

        label_name = tk.Label(self.query_frame, text="Name: ", font='Helvetica 8 bold')
        self.entry_name = tk.Entry(self.query_frame, width=15)

        label_name.grid(row=0, column=0)
        self.entry_name.grid(row=0, column=1)

        self.entry_name.focus()

    def user_input(self, choice):
        if choice == 'done':
            self.query_output = self.entry_name.get()

        self.pop.destroy()

