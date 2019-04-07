from tkinter import *


class Draw():

    @staticmethod
    def figs(figures):
        root = Tk()
        width_canvas = max([f.finish_point.y for f in figures]) + 1
        height_canvas = max([f.finish_point.x for f in figures]) + 1
        koef = 30
        c = Canvas(root, width=width_canvas*koef, height=height_canvas*koef, bg='white')
        c.pack()

        #рисую сетку
        for x in range(width_canvas + 1):
            c.create_line(x*koef, 0, x*koef, height_canvas*koef)

        for y in range(height_canvas + 1):
            c.create_line(0, y*koef, width_canvas*koef, y*koef)

        colors = ['pale green', "tomato", "SkyBlue1", "DarkOliveGreen1", "wheat1", "powder blue", "orange", "gray44", "gold"]

        #рисуем фигуры
        for i, f in enumerate(figures):
            c.create_rectangle(f.start_point.y*koef, f.start_point.x*koef,
                               (f.finish_point.y + 1) * koef, (f.finish_point.x + 1)*koef,  fill=colors[i], width=3)
            c.create_oval(f.start_point.y*koef - 5, f.start_point.x*koef - 5,
                          f.start_point.y * koef + 5, f.start_point.x * koef + 5, fill=colors[i])
            c.create_text((f.start_point.y + (f.finish_point.y - f.start_point.y + 1)/2)*koef,
                          (f.start_point.x + (f.finish_point.x - f.start_point.x + 1) / 2)*koef,
                          text=f.name, font="Verdana 10")
        c.pack()
        root.mainloop()
