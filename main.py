import tkinter as tk

from Application import Application
from lib import *

if __name__ == '__main__':
    root = tk.Tk()
    root.title('paint')
    center_window(root)
    Application(master=root)
    root.mainloop()
    print('terminated')
