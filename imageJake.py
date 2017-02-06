from tkinter import *
import os
from PIL import Image, ImageTk
import toolbox
import numpy as np

class imageJake(Frame):

    def __init__(self, default=None, master=None):

        root = master
        root.title("imageJake - Image")

        self.canvas = Canvas(root)
        self.canvas.pack()


        self.im = Image.open(os.getcwd() + '/cell_10000.png')
        self.sz = self.im.size
        self.canvas.config( height = self.sz[1], width = self.sz[0])

        photo = ImageTk.PhotoImage(self.im)
        self.image = self.canvas.create_image(0, 0, anchor = NW, image=photo)
        self.canvas.image = photo

    def get_canvas(self):
        return self.canvas

    def get_image(self):
        return self.canvas.image

    def set_image(self, im):
        self.sz = im.shape
        print(self.sz)
        self.canvas.config(heigh=self.sz[0], width=self.sz[1])
        self.im = Image.fromarray(im)
        img = ImageTk.PhotoImage(Image.fromarray(im))
        self.canvas.itemconfig(self.image, image = img)
        self.canvas.image = img

    def draw_roi(self, coords_dict):
        try:
            s_corner = coords_dict['s']
            e_corner = coords_dict['e']
            self.roi = self.canvas.create_rectangle(s_corner[0], s_corner[1], e_corner[0], e_corner[1], outline = "red")
        except KeyError:
            print('Wrong Dictionary')

    def update_size(self,sz):
        self.canvas.config(height=sz[0],width=sz[1])
        return 0

    def delete_roi(self):
        try:
            self.canvas.delete(self.roi)
        except AttributeError:
            pass

    def zoom(self, x):
        pic = self.get_image()
        self.canvas.config(heigh=int(x*self.sz[0]), width=int(x*self.sz[1]))

        pic = self.im.resize((int(x*self.sz[1]), int(x*self.sz[0])), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(pic)
        self.canvas.itemconfig(self.image, image = img)
        self.canvas.image = img
