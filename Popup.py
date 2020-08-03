from tkinter import *

from lib import *


class Popup(Toplevel):

    def __init__(self, msg, flag, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        center_window(self, 600, 400)
        self.tuple_list = []
        self.msg = msg
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.frm_form = Frame(master=self)
        self.set_frm_form(flag)
        self.frm_bottom_btn = Frame(master=self)
        self.set_bottom_btn()

    def set_frm_form(self, flag):
        self.frm_form.grid(row=0, column=0, sticky='nsew', padx=10, pady=8)
        if flag == 'add':
            name_list = ['x0', 'y0', 'x1', 'y1', 'x2', 'y2']
            lbl_type = Label(master=self.frm_form, text='type')
            lbl_type.grid(row=len(name_list), column=0, sticky='e')
            var = StringVar(self.frm_form)
            var.set('line')
            menu = OptionMenu(self.frm_form, var, 'line', 'oval', 'rectangle', 'polygon')
            menu.grid(row=len(name_list), column=1, sticky='w')
            self.tuple_list.append((lbl_type, var))
        elif flag == 'config':
            name_list = ['outline color', 'fill color', 'move to', 'xscale', 'yscale', 'rotate angle']
        else:
            name_list = []
        for i, name in enumerate(name_list):
            lbl = Label(master=self.frm_form, text=name)
            lbl.grid(row=i, column=0, sticky='e')
            ent = Entry(master=self.frm_form)
            ent.grid(row=i, column=1, sticky='w')
            self.tuple_list.append((lbl, ent))

    def set_bottom_btn(self):
        def ok():
            for my_tuple in self.tuple_list:
                self.msg[my_tuple[0]['text']] = my_tuple[1].get()
            self.destroy()

        self.frm_bottom_btn.grid(row=1, column=0, sticky='se', pady=10)
        self.frm_bottom_btn.rowconfigure(0, weight=1, minsize=2)
        self.frm_bottom_btn.columnconfigure([0, 1], weight=1)
        btn_cancel = Button(master=self.frm_bottom_btn, text='cancel', width=6,
                            command=lambda: self.destroy())
        btn_cancel.grid(row=0, column=0, sticky='nse', padx=5, pady=2)
        btn_ok = Button(master=self.frm_bottom_btn, text='ok', width=6,
                        command=ok)
        btn_ok.grid(row=0, column=1, sticky='nse', padx=5, pady=2)
