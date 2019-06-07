#!/usr/bin/python
import tkinter
window = tkinter.Tk()
# to rename the title of the window
window.title("Cortical Lesion Finder")
# pack is used to show the object in the window
label = tkinter.Label(window, text = "Please enter your dicom files.").pack()
window.mainloop()
