# -*- coding: UTF-8 -*-

from tkinter.scrolledtext import ScrolledText

import os 
os.environ['HDF5_DISABLE_VERSION_CHECK']='2'
from tkinter import *
from tkinter import filedialog

import json
from functools import reduce
import numpy as np
from tkinter import ttk
#import pandas as pd
from PIL import ImageTk, Image

from math import sqrt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import threading
from tkinter.ttk import Separator,Scrollbar,Treeview,Progressbar,Combobox
import pydot
import graphviz
import Back_end_scrap



def gui_post():
    global js_posts
    js_posts=Back_end_scrap.scarp_post(page_name.get(),date_range_min.get(),date_range_max.get())

    text.delete('1.0', END)

    for posts_fb in js_posts:

        text.insert(END, json.dumps(posts_fb, indent=3, ensure_ascii=False))
    
    progress_bar.stop()
        

def seaarch_post():
    text_se.delete('1.0', END)
    

    if posts_search.get()=="Most Liked Post":

        maxpost = max(js_posts, key=lambda x:x['Likes'])
        text_se.insert(END, json.dumps(maxpost, indent=3, ensure_ascii=False))
    elif posts_search.get()=="Most Shared Post":
        maxpost = max(js_posts, key=lambda x:x['Shares'])
        text_se.insert(END, json.dumps(maxpost, indent=3, ensure_ascii=False))
    elif posts_search.get()=="Most Commented Post":
        maxpost = max(js_posts, key=lambda x:x['Comments'])
        text_se.insert(END, json.dumps(maxpost, indent=3, ensure_ascii=False))
        
def start_progressbar():
    global tread1
    progress_bar.start()
    tread1 = threading.Thread(target=gui_post, args=())
    tread1.start()
    master.after(20, check_foo_thread)
    

def check_foo_thread():
    if tread1.is_alive():
        master.after(20, check_foo_thread)
    else:
        progress_bar.stop()
          
    
    
master = Tk()
master.title("Scrap Facebook")

lab_par=Label(master, text="Scrap Facebook Posts",fg="salmon4",font='Helvetica 16 bold')
lab_par.grid(row=0, column=1,pady=13,columnspan=50)

##### PAge name
lab_page=Label(master, text="Enter Page name",fg="salmon4",font='Helvetica 11 bold')
lab_page.grid(row=1, column=3)

page_name= StringVar()
page_en = Entry(master,width=20, textvariable=page_name)
page_en.grid(row=1, column=4)
#### enter a range of date 

lab_date=Label(master, text="Enter a range of dates(YYYY-MM-DD)",fg="salmon4",font='Helvetica 11 bold')
lab_date.grid(row=2, column=3)

date_range_min= StringVar()
date_rg = Entry(master,width=20, textvariable=date_range_min)
date_rg.grid(row=2, column=4)

date_range_max= StringVar()
date_rg1 = Entry(master,width=20, textvariable=date_range_max)
date_rg1.grid(row=2, column=6)
##### 


    ###### ***** Create BUTTON run script *** ########
Button(master, text="Start Scraping",bg="cyan", width=20,font='Helvetica 10 bold',command=start_progressbar).grid(row=2, column=12,pady=5)
    
################ ************** Progress Bar ***************** ###########################################

progress_bar = Progressbar(master, orient='horizontal',  length=700, mode='indeterminate')
progress_bar.grid(row=9, column=1,pady=13,columnspan=10) 



################ ************** Output ***************** ###########################################


lab_output=Label(master, text="Output:",fg="salmon4",font='Helvetica 10 bold')
lab_output.grid(row=49, column=1)

vsb = Scrollbar(master,orient="vertical")
text = Text(master,width=110, height=16, spacing1=3,
                            yscrollcommand=vsb.set,bd=3,bg="light cyan" )
vsb.config(command=text.yview)
vsb.grid(row=50, column=0)
text.grid(row=50, column=1,columnspan=10,sticky='nwse')
#,state=DISABLED
################ ************** Search  ***************** ###########################################

lab_search=Label(master, text="Search:",fg="salmon4",font='Helvetica 14 bold')
lab_search.grid(row=60, column=1)

posts_search = StringVar()
number_chosen = ttk.Combobox(master,state="readonly",width=30, textvariable=posts_search)
number_chosen['values'] = ("Most Liked Post", "Most Shared Post", "Most Commented Post")
number_chosen.grid(row=60, column=1,columnspan=10,pady=18)                       # <= Combobox in column 1
number_chosen.current(0)

    ###### ***** Create BUTTON run script *** ########
Button(master, text="Search",bg="cyan", width=20,font='Helvetica 10 bold',command=seaarch_post).grid(row=60, column=7,columnspan=10,pady=5)
  
#### create a text 

text_se = Text(master,width=15, height=8, spacing1=3,bd=3,bg="light cyan" )
text_se.grid(row=68, column=3,columnspan=20,sticky='nwse')

master.geometry("%dx%d+0+0" % (1080,750))
#master.config(bg='blue')
master.mainloop()