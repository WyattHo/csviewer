import tkinter as tk
from tkinter import font
from tkinter import filedialog
from tkinter import ttk

from kernel import Treeview, Notebook


class MyApp:
    PADS = {
        'padx': 5, 'pady': 5,
        'ipadx': 1, 'ipady': 1,
    }
    ROOT_MINSIZE = {
        'width': 400, 'height': 400
    }

    # typesetting
    def __init__(self):
        self.root = self.initialize_main_window()
        self.font_label = font.Font(family='Helvetica', size=10)
        self.font_btn = font.Font(family='Helvetica', size=10)
        self.create_frame_for_csv_names()
        self.create_frame_for_csv_data()
        self.create_frame_for_curve_settings()
        self.create_frame_for_axes_settings()
        self.root.mainloop()

    def initialize_main_window(self) -> tk.Tk:
        root = tk.Tk()
        root.title('PlotCSV')
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=5)
        root.state('zoomed')
        root.minsize(**self.ROOT_MINSIZE)
        root.configure()
        return root

    def create_frame_for_csv_names(self) -> ttk.Treeview:
        frame = tk.LabelFrame(self.root, text='Choose CSV files')
        frame.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW, **self.PADS)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame['font'] = self.font_label

        subframe = tk.Frame(frame)
        subframe.grid(row=0, column=0, sticky=tk.NSEW)
        columns = ('CSV ID', 'CSV Path')
        self.treeview_csv_names = Treeview(
            subframe, columns, 5)

        subframe = tk.Frame(frame)
        subframe.grid(row=0, column=1)
        button = tk.Button(
            subframe,
            text='Choose',
            command=lambda: self.open_files(),
            width=6
        )
        button.grid(row=0, column=0, **self.PADS)
        button['font'] = self.font_btn

    def create_frame_for_csv_data(self):
        frame = tk.LabelFrame(self.root, text='Review CSV data')
        frame.grid(row=1, column=0, sticky=tk.NSEW, **self.PADS)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame['font'] = self.font_label

        self.notebook_csv_data = Notebook(frame)
        self.notebook_csv_data.grid(
            row=0, column=0, columnspan=2, sticky=tk.NSEW
        )
        tab = self.notebook_csv_data.create_new_tab(tabname='1')
        Treeview(tab, columns=('',), height=25)

        button = tk.Button(
            frame,
            text='Import',
            command=lambda: self.import_csv(),
            width=6
        )
        button.grid(row=1, column=0, **self.PADS)
        button['font'] = self.font_btn

        button = tk.Button(
            frame,
            text='Clear',
            command=lambda: self.clear_csv_data_notebook(),
            width=6
        )
        button.grid(row=1, column=1, **self.PADS)
        button['font'] = self.font_btn

    def create_frame_for_curve_settings(self):
        frame = tk.LabelFrame(self.root, text='Curve settings')
        frame.grid(row=1, column=1, sticky=tk.NSEW, **self.PADS)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        self.notebook_curve_settings = Notebook(frame)
        self.notebook_curve_settings.grid(
            row=1, column=0, columnspan=2, sticky=tk.NSEW)
        self.notebook_curve_settings.initialize_notebook_for_curve_settings(MyApp.PADS)

        label = tk.Label(frame, text='Curve numbers')
        label.grid(row=0, column=0, **self.PADS)

        self.spinbox = tk.Spinbox(
            frame, from_=1, to=20, width=3,
            command=lambda: self.adjust_curve_settings_tabs()
        )
        self.spinbox.grid(row=0, column=1, **self.PADS)

    def create_frame_for_axes_settings(self):
        frame = tk.LabelFrame(self.root, text='Axes settings')
        frame.grid(row=1, column=2, sticky=tk.NSEW, **self.PADS)
        button = tk.Button(
            frame,
            text='Draw',
            command=lambda: self.draw(),
            width=6
        )
        button.grid(row=0, column=0, **self.PADS)
        button['font'] = self.font_btn

    # actions
    def open_files(self):
        self.treeview_csv_names.clear()
        filenames = filedialog.askopenfilenames(
            title='Choose csv files',
            filetypes=[('csv files', '*.csv')]
        )
        self.treeview_csv_names.insert_csv_names(filenames)
        self.treeview_csv_names.adjust_column_width()

    def import_csv(self):
        try:
            if not self.treeview_csv_names.get_children():
                raise Exception('No CSV file chosen.')
        except Exception as e:
            tk.messagebox.showerror(title='Error', message=e)
        else:
            self.notebook_csv_data.remove_tabs()
            csv_data_all = self.treeview_csv_names.collect_all_csv_data()
            for csv_idx, csv_data in csv_data_all.items():
                tab = self.notebook_csv_data.create_new_tab(csv_idx)
                treeview_csv_data = Treeview(
                    tab, list(csv_data.columns), 25
                )
                treeview_csv_data.insert_csv_data(csv_data)
                treeview_csv_data.adjust_column_width()

    def clear_csv_data_notebook(self):
        self.notebook_csv_data.remove_tabs()
        tab = self.notebook_csv_data.create_new_tab(tabname='1')
        Treeview(tab, columns=('',), height=25)

    def adjust_curve_settings_tabs(self):
        exist_num = len(self.notebook_curve_settings.tabs())
        tgt_num = int(self.spinbox.get())
        if tgt_num > exist_num:
            for tab_idx in range(exist_num, tgt_num):
                tab = self.notebook_curve_settings.create_new_tab(tabname=str(tab_idx + 1))
                Notebook.fill_curve_setting_widgets(tab, self.PADS)
        elif tgt_num < exist_num:
            tab_idx = self.notebook_curve_settings.index('end') - 1
            self.notebook_curve_settings.forget(tab_idx)

    def draw(self):
        ...


if __name__ == '__main__':
    MyApp()
