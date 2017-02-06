from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import toolbox as tb

class roi():

    first_corner = {}
    second_corner = {}

    def __init__(self, master, im):
        self.coords = {'s':[], 'e':[]}

        root = master
        root.title("imageJake - ROI")

        tbox = tb.toolbox()
        tbox.launch_toolbox(master, im)
