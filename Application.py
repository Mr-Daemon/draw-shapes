from tkinter import *

from Popup import Popup
from lib import *


class Application(Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.msg = dict()
        self.flag = True
        self.item = None
        self.item_bbox = None
        self.sidebar_btns = []
        self.pack(fill=BOTH, expand=True)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.frm_sidebar = Frame(master=self, relief=SUNKEN, borderwidth=2)
        self.set_sidebar()
        self.canvas = Canvas(master=self, relief=SUNKEN, borderwidth=2)
        self.set_canvas()

    def set_sidebar(self):
        def add():
            if self.flag:
                self.flag = False
                self.msg.clear()
                popup_window = Popup(master=self, msg=self.msg, flag='add')
                self.wait_window(popup_window)
                self.flag = True
                if self.msg:
                    self.render_add_msg()

        def config():
            if self.flag:
                self.flag = False
                self.msg.clear()
                popup_window = Popup(master=self, msg=self.msg, flag='config')
                self.wait_window(popup_window)
                self.flag = True
                if self.msg:
                    self.render_config_msg()

        def delete():
            self.canvas.delete(self.item, self.item_bbox)

        self.frm_sidebar.grid(row=0, column=0, sticky='nsew', ipady=5, padx=2, pady=2)
        self.frm_sidebar.columnconfigure(0, weight=1, minsize=80)
        materials = [('add', add), ('config', config), ('delete', delete)]
        for i, material in enumerate(materials):
            btn = Button(master=self.frm_sidebar, text=material[0], command=material[1])
            btn.grid(row=i, column=0, sticky='ew', padx=5, pady=5)
            self.sidebar_btns.append(btn)
        self.sidebar_btns[1]['state'] = 'disabled'
        self.sidebar_btns[2]['state'] = 'disabled'

    def set_canvas(self):
        def on_click(event):
            print(f'onclick: {event}')
            if self.item:
                print(f'delete {self.item_bbox}')
                self.canvas.delete(self.item_bbox)
            items = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
            if not items or items[0] == self.item_bbox:
                self.sidebar_btns[1]['state'] = 'disabled'
                self.sidebar_btns[2]['state'] = 'disabled'
                self.item = None
                self.item_bbox = None
                return
            self.item = items[0]
            self.create_bbox()
            self.sidebar_btns[1]['state'] = 'normal'
            self.sidebar_btns[2]['state'] = 'normal'

        def drag(event):
            if self.item_bbox:
                self.canvas.delete(self.item_bbox)
                self.create_bbox()
            self.canvas.moveto(self.item, event.x, event.y)

        self.canvas.tag_bind('tag', '<B1-Motion>', drag)
        self.canvas.grid(row=0, column=1, sticky='nsew')
        options = {
            'outline': 'black',
            'fill': 'white',
            'activefill': 'black',
            'tag': 'tag',
        }
        self.canvas.create_polygon(10, 60, 60, 10, 110, 60, 60, 110, **options)
        self.canvas.create_oval(150, 150, 300, 400, **options)
        self.canvas.bind('<Button-1>', on_click)

    def render_add_msg(self):
        graph_type = self.msg.pop('type')
        options = {
            'outline': 'black',
            'fill': 'white',
            'activefill': 'black',
            'tag': 'tag',
        }
        coordinate = list(self.msg.values())
        if graph_type == 'line':
            options = {'fill': 'black', 'activefill': 'blue'}
            self.canvas.create_line(*(coordinate[:4]), **options)
        elif graph_type == 'oval':
            self.canvas.create_oval(*(coordinate[:4]), **options)
        elif graph_type == 'rectangle':
            self.canvas.create_rectangle(*(coordinate[:4]), **options)
        elif graph_type == 'polygon':
            self.canvas.create_polygon(*coordinate, **options)

    def render_config_msg(self):
        print(self.msg)
        if self.msg['outline color']:
            self.canvas.itemconfigure(self.item, outline=self.msg['outline color'])
        if self.msg['fill color']:
            self.canvas.itemconfigure(self.item, fill=self.msg['fill color'])
        if self.msg['move to']:
            coordinate = tuple(filter(None, self.msg['move to'].split(',')))
            self.canvas.moveto(self.item, coordinate[0], coordinate[1])
        xscale = {True: self.msg['xscale'], False: 1}[bool(self.msg['xscale'])]
        yscale = {True: self.msg['yscale'], False: 1}[bool(self.msg['yscale'])]
        self.canvas.scale(self.item, self.canvas.bbox(self.item)[0], self.canvas.bbox(self.item)[1], float(xscale),
                          float(yscale))
        if self.msg['rotate angle']:
            rotate_angle = float(self.msg['rotate angle'])
            old_coords = self.canvas.coords(self.item)
            print(self.canvas.bbox(self.item))
            new_coords = calculate_rotate(calculate_center(*self.canvas.bbox(self.item)), rotate_angle, *old_coords)
            options = {
                'outline': self.canvas.itemcget(self.item, 'outline'),
                'fill': self.canvas.itemcget(self.item, 'fill'),
                'activefill': self.canvas.itemcget(self.item, 'activefill'),
            }
            self.canvas.delete(self.item)
            self.item = self.canvas.create_polygon(*new_coords, **options)
        self.canvas.delete(self.item_bbox)
        self.create_bbox()

    def create_bbox(self, event=None):
        self.item_bbox = self.canvas.create_rectangle(*self.canvas.bbox(self.item), **{'outline': 'red'})
