import math


def center_window(root, width=900, height=800):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


def calculate_center(*args):
    print(args)
    return (args[0] + args[2]) / 2, (args[1] + args[3]) / 2


def calculate_rotate(center, angle, *args):
    cos_val = math.cos(math.radians(angle))
    sin_val = math.sin(math.radians(angle))
    x_trans = lambda x, y: (x - center[0]) * cos_val - (y - center[1]) * sin_val + center[0]
    y_trans = lambda x, y: (x - center[0]) * sin_val + (y - center[1]) * cos_val + center[1]
    r = []
    for i in range(0, len(args), 2):
        r.append(x_trans(args[i], args[i + 1]))
        r.append(y_trans(args[i], args[i + 1]))
    return r


if __name__ == '__main__':
    print(calculate_center(0, 0, 1, 1))
