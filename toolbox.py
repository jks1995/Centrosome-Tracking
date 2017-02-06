from tkinter import *
from tkinter import filedialog
import os
from PIL import Image
import numpy as np
import filters
import imageJake as ij
import roi

class toolbox():

    def __init__(self):
        self.start_coords = []
        self.end_coords = []
        self.curr_img = 0
        self.img_dir = None
        self.pic_list = {}
        self.c_list = {}
        self.root = None
        self.flt = filters.filters()
        self.thresh_max=255
        self.zoom_val = 1

    def launch_toolbox(self, master, default = None):

        toolbox = master

        toolbox.title("imageJake - toolbox")
        if default == None:
            file_picker = Button(toolbox, text = "Select Images", command = self.dir_select).grid(row = 0, column = 0, columnspan = 2)

        pic_change_label = Label(toolbox, text = "Change Picture").grid(row = 1, column = 0, columnspan = 2)
        previous_b = Button(toolbox, text = "Prev", command = lambda: self.new_pic("p")).grid(row = 2, column = 0)
        next_b = Button(toolbox, text = "Next", command = lambda: self.new_pic("n")).grid(row = 2, column = 1)

        thresh_label = Label(toolbox, text="Threshold").grid(row=3,column=0, columnspan=2)
        self.thresh_min_scale = Scale(toolbox, label = "Min", from_=0, to=255, command=self.update_min_thresh, resolution=1)
        self.thresh_min_scale.grid(row=5,column=0)
        self.thresh_max_scale = Scale(toolbox, label = "Max", from_=0, to=255,command=self.update_max_thresh,resolution=1)
        self.thresh_max_scale.set(255)
        self.thresh_max_scale.grid(row=5, column=1)

        filters_button = Button(toolbox, text="Apply Filters", command= self.update_filters).grid(row=6, column=0, columnspan=2)

        gauss_label = Label(toolbox, text="Gauss STDev:").grid(row=7, column = 0)
        fft_label = Label(toolbox, text="FFT Mulitple:").grid(row=8, column = 0)
        self.gauss_entry = Entry(toolbox)
        self.gauss_entry.grid(row=7, column = 1)
        self.fft_entry = Entry(toolbox)
        self.fft_entry.grid(row=8, column = 1)

        mean_label = Label(toolbox, text="Mean Exclusion").grid(row=9, column=0)
        self.mean_entry = Entry(toolbox)
        self.mean_entry.grid(row=9,column=1)

        self.zoom_scale = Scale(toolbox, label = "Zoom", from_=1, to=3, resolution=.05, orient=HORIZONTAL, command=self.update_zoom)
        self.zoom_scale.grid(row=10, column=0, columnspan=2)
        reset_button =  Button(toolbox, text="Reset", command=self.reset).grid(row=11,column=0,columnspan=2)

        self.roi_button = Button(toolbox, text="Draw Roi", command=self.draw_roi)
        self.roi_button.grid(row=12,column=0)
        set_roi_button = Button(toolbox, text="Set Roi", command=self.set_roi).grid(row=12,column=1)

        self.im = ij.imageJake(default, Toplevel())


        try: #used for roi's
            self.im.set_image(default)
            self.c_list[0] = default
            self.im.zoom(4)
        except Exception as e:
            print(e)
            pass
        return 0


    def dir_select(self):
        # returns dir name
        self.img_dir = filedialog.askdirectory()
        count = 0
        for subdir, dirs, files in os.walk(self.img_dir):
            for file in files:
                im = Image.open(self.img_dir + "/" + file)
                data = np.asarray(im)
                data.flags.writeable = True
                self.pic_list[count] = data
                count+=1
        self.c_list = self.pic_list.copy()
        self.im.update_size(self.c_list[0].shape)
        self.im.set_image(self.c_list[self.curr_img])
        return 0

    def new_pic(self, sender):

        if self.img_dir == None:
            return 0
        if self.curr_img == len(self.pic_list):
            self.curr_img = 0
        elif sender == "n":
            self.curr_img+=1
        else:
            if self.curr_img == 0:
                return 0
            self.curr_img-=1

        self.update_filters()
        self.update_zoom(self.zoom_val)
        return 0

    def update_max_thresh(self, val):
        self.thresh_max = int(val)
        self.update_filters()
        return 0

    def update_min_thresh(self, val):
        self.thresh_min = int(val)
        self.update_filters()
        return 0

    def update_zoom(self, val):
        self.zoom_val = val
        self.im.zoom(self.zoom_scale.get())
        return 0

    def reset(self):
        self.thresh_max_scale.set(255)
        self.thresh_min_scale.set(0)
        self.c_list = self.pic_list.copy()
        self.im.set_image(self.c_list[self.curr_img])
        return 0

    def draw_roi(self):
        self.roi_button.configure(bg='red')
        self.im.delete_roi()
        self.im.get_canvas().bind("<Button-1>", self.getstart)
        self.im.get_canvas().bind("<B1-Motion>", self._rectangle)
        self.im.get_canvas().bind("<ButtonRelease-1>", self.release)
        self.ROI = self.im.get_canvas().create_rectangle(0, 0, 0, 0, outline = "red")
        return 0

    def set_roi(self):
        self.roi_button.configure(background='white')
        self.im.get_canvas().unbind("<Button-1>")
        self.im.get_canvas().unbind("<B1-Motion>")
        self.im.get_canvas().unbind("<ButtonRelease-1>")
        c = self.get_roi_corners(self.start_coords, self.end_coords)
        im = self.update_filters_im(self.c_list[self.curr_img])
        r = roi.roi(Toplevel(), im[c[2]:c[3], c[0]:c[1]])
        return 0

    def _rectangle(self, event):
        x0, y0 = self.start_coords
        x1,y1 = (event.x, event.y)

        self.im.delete_roi()
        self.im.draw_roi({'s': self.start_coords, 'e':[event.x, event.y]})
        return 0

    def getstart(self, event):
        self.start_coords = []
        self.start_coords.append(event.x)
        self.start_coords.append(event.y)
        np.asarray(self.start_coords)
        return 0

    def release(self, event):
        if self.img_dir == None :
            return 0
        self.end_coords = []
        self.end_coords.append(event.x)
        self.end_coords.append(event.y)
        np.asarray(self.end_coords)
        return 0

    def update_filters(self):
        try:
            im = self.flt.apply_filter(self.c_list[self.curr_img], self.fft_entry.get(), self.gauss_entry.get(), self.thresh_max, self.thresh_min, self.mean_entry.get())
            self.im.set_image(im)
            self.update_zoom(self.zoom_val)
            return 0
        except KeyError:
            return 0

    def update_filters_im(self, im):
        try:
            return self.flt.apply_filter(im, self.fft_entry.get(), self.gauss_entry.get(), self.thresh_max, self.thresh_min, self.mean_entry.get())
        except KeyError:
            return 0

    def get_roi_corners(self, s_coords, e_coords):

        coords = []

        if( s_coords[0] < e_coords[0] ):
            coords.append(s_coords[0])
            coords.append(e_coords[0])
        else:
            coords.append(e_coords[0])
            coords.append(s_coords[0])

        if( s_coords[1] < e_coords[1] ):
            coords.append(s_coords[1])
            coords.append(e_coords[1])
        else:
            coords.append(e_coords[1])
            coords.append(s_coords[1])

        return coords
