from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from scipy import ndimage

class filters():

    def __init__(self):
        thresh_max = 255
        thresh_min = 0
        last_min=0
        last_max=255

    def apply_filter(self, im, fft, gauss, _max, _min, _mean):
        f = im.copy()
        try:
            #f = self.pic_list[self.curr_img].copy()
            try:
                f_val=float(fft)
                f = np.fft.fft(f)
                av_f = f_val*np.mean(abs(f))
                f[abs(f) < av_f] = 0
                f = np.fft.ifft(f).real.astype(np.uint8)
            except ValueError:
                print("No fft")

            try:
                g_val = float(gauss)
                f = ndimage.gaussian_filter(f, g_val)
                f.astype(np.uint8)
            except ValueError:
                print("No Gauss")

            f[f>_max]=0
            f[f<_min]=0

            try:
                print(np.mean(f))
                change = f.copy()
                change = np.ma.masked_where(change==0, change)
                mean = np.mean(change)
                f_mean = float(_mean) * mean
                f[f<f_mean] = 0
            except ValueError:
                print("No Mean")

            return f

        except (KeyError, ValueError):
            return 0
