# from driver.pixels_driver import HUD
from tkinter import ttk
import tkinter as tk
from driver.core.hud import HUD
import time
global running
global landNumber
global travel_button  


hud = HUD()

def start_travel():
    global running
    global landNumber
    global travel_button  

    land_num = landNumber.get()
    running = True
    travel_button.config(state=tk.DISABLED)
    hud.travel_bookmark(land_num)
    print('must be started with landnumber{}'.format(land_num))
    travel_button.config(state=tk.NORMAL)

root = tk.Tk()
root.title('Travel Machine')
landNumber = tk.IntVar(value=1043)
running = False


tk.Label(root,text='Land Number: ').grid(row=4,column=0,padx=10,pady=5)
tk.Entry(root,textvariable=landNumber).grid(row=4,column=1,padx=10,pady=5)
travel_button = tk.Button(root,text='Travel',command=start_travel)
travel_button.grid(row=7,column=0,padx=10,pady=10)
root.mainloop()




