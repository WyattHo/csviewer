import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import font
from tkinter import ttk

import main


def open_dir(stringvar: tk.StringVar):
    dir_name = filedialog.askopenfilename(title='Choose the directory')
    stringvar.set(dir_name)


def read_csv(
        treeview_read: ttk.Treeview, stringvar: tk.StringVar, 
        scrollbar_ver_left: tk.Scrollbar, scrollbar_hor_left: tk.Scrollbar):
    # Clear items first
    for item in treeview_read.get_children():
        treeview_read.delete(item)

    # Read csv
    tgtfile_name = stringvar.get()
    with open(tgtfile_name, 'r') as f:
        csv_data = csv.DictReader(f)
        fieldnames = csv_data.fieldnames
        treeview_read['columns'] = fieldnames

        # Analyze best-fit width for each field
        max_widths = {}
        for fieldname in fieldnames:
            max_widths[fieldname] = len(fieldname)

        for row_idx, row_data in enumerate(csv_data):
            for fieldname in fieldnames:
                data_width = len(row_data[fieldname])

                if data_width > max_widths[fieldname]:
                    max_widths[fieldname] = data_width

        # Set fields
        for fieldname in fieldnames:
            treeview_read.column(fieldname, anchor=tk.W, width=10*max_widths[fieldname], stretch=0)
            treeview_read.heading(fieldname, text=fieldname, anchor=tk.W)

        # Reset scrollbars
        scrollbar_ver_left.config(command=treeview_read.yview)
        scrollbar_hor_left.config(command=treeview_read.xview)
        
        # The entire file has been iterated at the first time,
        # so it is needed to seek to the beginning.
        f.seek(0)
        next(csv_data)

        # Insert values
        for row_idx, row_data in enumerate(csv_data):
            values = [row_data[fieldName] for fieldName in fieldnames]
            treeview_read.insert(parent='', index=row_idx, values=values, tags=str(row_idx))


def draw():
    ...


def clear():
    ...


def main():
    root = tk.Tk()
    root.title('PlotCSV')
    root.resizable(width=0, height=0)
    root.configure()

    font_label = font.Font(family='Helvetica', size=10)
    font_btn = font.Font(family='Helvetica', size=10)
    
    # frame up
    frame_up = tk.LabelFrame(root, text='Choose the csv file')
    frame_up.grid(row=0, column=0, padx=5, pady=5, ipadx=1, ipady=1, sticky=tk.W)
    frame_up['font'] = font_label
    
    frame_up_up = tk.Frame(frame_up)
    frame_up_up.grid(row=0, column=0)

    frame_up_right = tk.Frame(frame_up)
    frame_up_right.grid(row=0, column=1, rowspan=2)

    stringvar = tk.StringVar()
    tgtdir_entry = tk.Entry(frame_up_up, width=50, textvariable=stringvar)
    tgtdir_entry.grid(row=0, column=0, padx=5, pady=5)

    choose_btn = tk.Button(frame_up_right, text='Choose', command=lambda: open_dir(stringvar), width=6)
    choose_btn.grid(row=0, column=0, padx=5, pady=5, ipadx=1, ipady=1)
    choose_btn['font'] = font_btn


    # frame down
    frame_dw = tk.LabelFrame(root, text='Working area')
    frame_dw.grid(row=1, column=0, padx=5, pady=5)
    frame_dw.propagate(0)
    frame_dw['font'] = font_label
    
    # frame down left 1
    frame_dw_left_1 = tk.Frame(frame_dw, width=250, height=300)
    frame_dw_left_1.grid(row=0, column=0, padx=5, pady=5)
    frame_dw_left_1.propagate(0)

    scrollbar_ver_left = tk.Scrollbar(frame_dw_left_1)
    scrollbar_ver_left.pack(side=tk.RIGHT, fill=tk.Y)

    scrollbar_hor_left = tk.Scrollbar(frame_dw_left_1, orient='horizontal')
    scrollbar_hor_left.pack(side=tk.BOTTOM, fill=tk.X)

    treeview_read = ttk.Treeview(
        frame_dw_left_1, 
        yscrollcommand=scrollbar_ver_left.set, 
        xscrollcommand=scrollbar_hor_left.set,
        height=15
    )
    
    treeview_read.pack(fill='both')
    treeview_read.propagate(0)

    scrollbar_ver_left.config(command=treeview_read.yview)
    scrollbar_hor_left.config(command=treeview_read.xview)
    treeview_read['columns'] = ('1', )
    treeview_read['show'] = 'headings'

    treeview_read.column('1')
    treeview_read.heading('1', text='')
    
    # frame down left 2
    frame_dw_left_2 = tk.Frame(frame_dw)
    frame_dw_left_2.grid(row=1, column=0)
    frame_dw_left_2.propagate(0)

    read_btn = tk.Button(
        frame_dw_left_2, 
        text='Read', 
        command=lambda: read_csv(treeview_read, stringvar, scrollbar_ver_left, scrollbar_hor_left), 
        width=6
    )
    read_btn.grid(row=0, column=0, padx=5, pady=5, ipadx=1, ipady=1)
    read_btn['font'] = font_btn

    # frame down right 1
    frame_dw_right_1 = tk.Frame(frame_dw, width=250, height=300)
    frame_dw_right_1.grid(row=0, column=1, padx=5, pady=5)
    frame_dw_right_1.propagate(0)

    scrollbar_ver_right = tk.Scrollbar(frame_dw_right_1)
    scrollbar_ver_right.pack(side=tk.RIGHT, fill=tk.Y)

    scrollbar_hor_right = tk.Scrollbar(frame_dw_right_1, orient='horizontal')
    scrollbar_hor_right.pack(side=tk.BOTTOM, fill=tk.X)

    treeview_draw = ttk.Treeview(
        frame_dw_right_1, 
        yscrollcommand=scrollbar_ver_right.set, 
        xscrollcommand=scrollbar_hor_right.set,
        height=15
    )

    treeview_draw.pack(fill='both')
    treeview_draw.propagate(0)

    scrollbar_ver_right.config(command=treeview_draw.yview)
    scrollbar_hor_right.config(command=treeview_draw.xview)
    treeview_draw['columns'] = ('1', )
    treeview_draw['show'] = 'headings'

    treeview_draw.column('1')
    treeview_draw.heading('1', text='')

    # frame down right 2
    frame_dw_right_2 = tk.Frame(frame_dw)
    frame_dw_right_2.grid(row=1, column=1)

    used_indices = []
    clear_state = False
    draw_btn = tk.Button(frame_dw_right_2, text='Draw', command=lambda: draw(), width=6)
    draw_btn.grid(row=0, column=0, padx=5, pady=5, ipadx=1, ipady=1)
    draw_btn['font'] = font_btn
    
    clear_btn = tk.Button(frame_dw_right_2, text='Clear', command=lambda: clear(), width=6)
    clear_btn.grid(row=0, column=1, padx=5, pady=5, ipadx=1, ipady=1)
    clear_btn['font'] = font_btn
    
    root.mainloop()
    

if __name__ == '__main__':
    main()
