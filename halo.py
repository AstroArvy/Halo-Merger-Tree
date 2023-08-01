import tkinter as tk
import os
import tkinter
import tkinter.messagebox
import customtkinter
import customtkinter as ctk
from RangeSlider.RangeSlider import RangeSliderH 
from tkinter import messagebox
from tkinter import filedialog
#from tkinter import *
#import threading
#import time
from tkinter import Button, Tk, HORIZONTAL
from tkinter.ttk import Progressbar

from CTkRangeSlider import *

import panel as pn
import math

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


#App functions

def show_value(value):
    print(value)    

def halo_guide():
    from os import startfile
    startfile(".\halo_guide.txt")

def bh_guide():
    from os import startfile
    startfile("blackholes_guide.txt")

def on_click():
    messagebox.showerror('Create Halos', 'Success!! Halos are being created in the directory!')
    
def create_subfolder():
    source_path = filedialog.askdirectory(title='Save location Directory')
    path = os.path.join(source_path, 'halos')
    os.makedirs(path)

def open_subfolder():
    source_path = filedialog.askdirectory(title='Save location Directory')
    path = os.path.join(source_path, 'halos')
    print(path)
    return (path)
 
        
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Halo merger history")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2,3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Binary Merger Tree", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Halo Guide", command=halo_guide)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Black Holes Guide", command=bh_guide)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        #self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        #self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")


        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=850, height=500)

        self.tabview.grid(row=0, column=1, columnspan=4,rowspan=3, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.tabview.add("Halos")
        self.tabview.add("Black Holes")

        self.tabview.tab("Halos").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Black Holes").grid_columnconfigure(0, weight=0)


        #Halos Tab
        hVar1 = tk.DoubleVar(value=6)  #left handle variable
        hVar2 = tk.DoubleVar(value=14)  #right handle variable
        
        
        range_slider = CTkRangeSlider(self.tabview.tab("Halos"), variables=[hVar1,hVar2], width = 360, from_=6, to=14)
        range_slider.place(x=440, y=28)
        
        self.halo_label1 = customtkinter.CTkLabel(self.tabview.tab("Halos"), text="Halo mass range at z=0 in Log10:", font=customtkinter.CTkFont(size=15))
        self.halo_label1.place(x=20, y=20)
        

        self.halo_label1_5 = customtkinter.CTkLabel(self.tabview.tab("Halos"), text="to", font=customtkinter.CTkFont(size=15))
        self.halo_label1_5.place(x=350, y=20)


        self.entry1 = customtkinter.CTkEntry(self.tabview.tab("Halos"), placeholder_text="from", textvariable=hVar1, width=50)
        self.entry1.place(x=290, y=20)

        self.entry11 = customtkinter.CTkEntry(self.tabview.tab("Halos"), placeholder_text="to", textvariable=hVar2, width=50)
        self.entry11.place(x=370, y=20)


        self.halo_label2 = customtkinter.CTkLabel(self.tabview.tab("Halos"), text="Minimum Halo Mass (Mlim):", font=customtkinter.CTkFont(size=15))
        self.halo_label2.place(x=20, y=80)

        self.entry2 = customtkinter.CTkEntry(self.tabview.tab("Halos"), placeholder_text="for example '2e6'", width=130)
        self.entry2.place(x=290, y=80)

        self.halo_label3 = customtkinter.CTkLabel(self.tabview.tab("Halos"), text="Redshift:", font=customtkinter.CTkFont(size=15))
        self.halo_label3.place(x=20, y=140)

        self.entry31 = customtkinter.CTkEntry(self.tabview.tab("Halos"), placeholder_text="initial", width=70)
        self.entry31.place(x=290, y=140)

        self.halo_label31 = customtkinter.CTkLabel(self.tabview.tab("Halos"), text="to", font=customtkinter.CTkFont(size=15))
        self.halo_label31.place(x=380, y=140)

        self.entry32 = customtkinter.CTkEntry(self.tabview.tab("Halos"), placeholder_text="final", width=70)
        self.entry32.place(x=410, y=140)
        
        self.halo_label4 = customtkinter.CTkLabel(self.tabview.tab("Halos"), text="Number of time steps:", font=customtkinter.CTkFont(size=15))
        self.halo_label4.place(x=20, y=200)

        self.entry4 = customtkinter.CTkEntry(self.tabview.tab("Halos"), placeholder_text="for example '200'", width=130)
        self.entry4.place(x=290, y=200)

        self.halo_label5 = customtkinter.CTkLabel(self.tabview.tab("Halos"), text="Number of Halos at initial z:", font=customtkinter.CTkFont(size=15))
        self.halo_label5.place(x=20, y=260)
 
        self.entry5 = customtkinter.CTkEntry(self.tabview.tab("Halos"), placeholder_text="for example '1000'", width=130)
        self.entry5.place(x=290, y=260)


        self.halo_button_1 = customtkinter.CTkButton(self.tabview.tab("Halos"), text="Save location", command=create_subfolder, width=100, height=30)
        self.halo_button_1.place(relx=0.50, rely=0.77, anchor='center')

        
        self.halo_button_2 = customtkinter.CTkButton(self.tabview.tab("Halos"), text="Create Halos",width=200, height=50, command = self.run_halos)
        self.halo_button_2.place(relx=0.50, rely=0.87, anchor='center')

        self.bar = ctk.CTkProgressBar(master=self.tabview.tab("Halos"), orientation='horizontal', mode='determinate', width=300)
    
        # Set default starting point to 0
        self.bar.set(0)

        #Black holes tab
 
        self.main_label = customtkinter.CTkLabel(master=self, text="For any queries or comments, please contact the developer!", fg_color="transparent", text_color=("gray10", "#DCE4EE"),font=("Times italic", 12))
        self.main_label.grid(row=4, column=4, sticky='se', padx=(0,10), pady=(0,10)) 

        self.main_label = customtkinter.CTkLabel(master=self, text="Developed by Aryan Bansal", fg_color="transparent", text_color=("gray10", "#DCE4EE"), font=("Times italic", 12))
        self.main_label.grid(row=4, column=1, sticky='sw', padx=(10,0), pady=(0,10)) 

        

        self.bh_label1 = customtkinter.CTkLabel(self.tabview.tab("Black Holes"), text="Power-law index of Mass relation at final redshift z:", font=customtkinter.CTkFont(size=15))
        self.bh_label1.place(x=20, y=20)

        self.bh_entry1 = customtkinter.CTkEntry(self.tabview.tab("Black Holes"), placeholder_text="for example '1.65'", width=130)
        self.bh_entry1.place(x=450, y=20)

        self.bh_label2 = customtkinter.CTkLabel(self.tabview.tab("Black Holes"), text="Mass loss in each merger due to gravitational waves in %:", font=customtkinter.CTkFont(size=15))
        self.bh_label2.place(x=20, y=70)

        self.bh_entry2 = customtkinter.CTkEntry(self.tabview.tab("Black Holes"), placeholder_text="for example '15'", width=130)
        self.bh_entry2.place(x=450, y=70)

        self.bh_label3 = customtkinter.CTkLabel(self.tabview.tab("Black Holes"), text="number of halo time steps:", font=customtkinter.CTkFont(size=15))
        self.bh_label3.place(x=20, y=120)

        self.bh_entry3 = customtkinter.CTkEntry(self.tabview.tab("Black Holes"), placeholder_text="for example '200'", width=130)
        self.bh_entry3.place(x=450, y=120)

        self.bh_label4 = customtkinter.CTkLabel(self.tabview.tab("Black Holes"), text="Minimum Halo Mass:", font=customtkinter.CTkFont(size=15))
        self.bh_label4.place(x=20, y=170)

        self.bh_entry4 = customtkinter.CTkEntry(self.tabview.tab("Black Holes"), placeholder_text="for example '2e6'", width=130)
        self.bh_entry4.place(x=450, y=170)

        self.bh_label5 = customtkinter.CTkLabel(self.tabview.tab("Black Holes"), text="Number of initial halo samples at z=0:", font=customtkinter.CTkFont(size=15))
        self.bh_label5.place(x=20, y=220)

        self.bh_entry5 = customtkinter.CTkEntry(self.tabview.tab("Black Holes"), placeholder_text="for example '1000'", width=130)
        self.bh_entry5.place(x=450, y=220)

        #self.bh_label6 = customtkinter.CTkLabel(self.tabview.tab("Black Holes"), text="Final redshift:", font=customtkinter.CTkFont(size=15))
        #self.bh_label6.place(x=20, y=270)

        self.bh_label6 = customtkinter.CTkLabel(self.tabview.tab("Black Holes"), text="Redshift:", font=customtkinter.CTkFont(size=15))
        self.bh_label6.place(x=20, y=270)

        self.bh_entry61 = customtkinter.CTkEntry(self.tabview.tab("Black Holes"), placeholder_text="initial", width=70)
        self.bh_entry61.place(x=450, y=270)

        self.bh_label61 = customtkinter.CTkLabel(self.tabview.tab("Black Holes"), text="to", font=customtkinter.CTkFont(size=15))
        self.bh_label61.place(x=540, y=270)

        self.bh_entry62 = customtkinter.CTkEntry(self.tabview.tab("Black Holes"), placeholder_text="final", width=70)
        self.bh_entry62.place(x=570, y=270)

        #self.bh_entry6 = customtkinter.CTkEntry(self.tabview.tab("Black Holes"), placeholder_text="for example '6'", width=130)
        #self.bh_entry6.place(x=450, y=270)

        self.bh_button_1 = customtkinter.CTkButton(self.tabview.tab("Black Holes"), text="Halo folder location", command=open_subfolder, width=100, height=30)
        self.bh_button_1.place(relx=0.41, rely=0.77, anchor='center')
        
        self.bh_button_2 = customtkinter.CTkButton(self.tabview.tab("Black Holes"), text="Blackhole save location", command=open_subfolder, width=100, height=30)
        self.bh_button_2.place(relx=0.59, rely=0.77, anchor='center')
        
        self.bh_button_3 = customtkinter.CTkButton(self.tabview.tab("Black Holes"), text="Assign Black Holes", command=on_click, width=200, height=50)
        self.bh_button_3.place(relx=0.50, rely=0.87, anchor='center')

        global z0,zf,samples,steps,Mlim,Mmin,Mmax
        z0 = self.entry31.get()
        zf = self.entry32.get()
        samples = self.entry5.get()
        steps = self.entry4.get()
        Mlim = self.entry2.get()
        Mmin = self.entry1.get()
        Mmax = self.entry11.get()
        
        
        
    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
    
        
    def run_halos(self):
        
        with open("halo_create.py", mode='rt', encoding='utf-8') as f:
            z0 = self.entry31.get()
            zf = self.entry32.get()
            samples = self.entry5.get()
            steps = self.entry4.get()
            Mlim = self.entry2.get()
            Mmin = self.entry1.get()
            Mmax = self.entry11.get()
            
            read_data = f.read()
            read_data = read_data.split("\n")
            
            read_data[37]='z0=%s'%z0
            read_data[38]='zf=%s'%zf
            read_data[39]='samples=%s'%samples
            read_data[40]='steps=%s'%steps
            read_data[41]='Mlim=%s'%Mlim
            read_data[42]='Mmin=%s'%Mmin
            read_data[43]='Mmax=%s'%Mmax
            
            f.close()
        with open("Halo_create.py", mode='w', encoding='utf-8') as f:
            read_data = "\n".join(read_data) 
            for i in range(len(read_data)):
                f.write(read_data[i])

        os.system('python halo_create.py')

def final():
    print(z0)
if __name__ == "__main__":
    app = App()
    app.mainloop()
