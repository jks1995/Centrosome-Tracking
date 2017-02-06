import imageJake
import toolbox
import filters
from tkinter import *

def main():
    root = Tk()
    tb = toolbox.toolbox()
    tb.launch_toolbox(root)
    root.mainloop()

if __name__ == "__main__":
    main()
