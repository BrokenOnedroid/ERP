# Standard library imports
import sys

# local .py 
from app import crud, models 
from app.database import engine
from sqlalchemy import text

# GUI Imports
import tkinter as tk
from tkinter import ttk
import customtkinter

# creating the db tabels
models.Base.metadata.create_all(bind=engine)

# basic apperance Options
customtkinter.set_appearance_mode("default")
customtkinter.set_default_color_theme("dark-blue") 

# Main Window
class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.header_font = customtkinter.CTkFont(family="Helvetica", size=44, weight="bold", slant="roman", underline=False, overstrike=False)
        self.geometry("400x350")
        self.minsize(400, 350)
        self.title("ERP")
        # self.set_appearance_mode("dark")
        # self.set_default_color_theme("dark-green")
       
        self.title_label = customtkinter.CTkLabel(self, text='Hauptmenü', fg_color='transparent', font=self.header_font)
        self.title_label.pack(padx=20, pady=20, anchor=customtkinter.CENTER)
        
        self.article_menue_button = customtkinter.CTkButton(self, text="Artikelübersicht", command=self.open_article_window)
        self.article_menue_button.pack(padx=20, pady=20)
        
        self.inventory_button = customtkinter.CTkButton(self, text="Inventar", command=self.open_inventar_window)
        self.inventory_button.pack(padx=20, pady=20)

        self.inventory_button = customtkinter.CTkButton(self, text="Beenden", command=self.close_window)
        self.inventory_button.pack(padx=20, pady=20)

        self.toplevel_window = None

    def open_inventar_window(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Inventory(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus_set()  # if window exists focus it
    
    def open_article_window(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Article()  # create window if its None or destroyed
        else:
            self.toplevel_window.focus_set()  # if window exists focus it
    
    def close_window(self):
        self.destroy()

# inventory Windows
class Inventory(customtkinter.CTkToplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.header_font = customtkinter.CTkFont(family="Helvetica", size=18, weight="bold", slant="roman", underline=False, overstrike=False)
        
        self.title("Inventar")
        self.geometry("950x450")
        self.minsize(900, 450)
        self.maxsize(1000, 450) 
        self.counter = 0      
        # header
        self.title_label = customtkinter.CTkLabel(self, text='Inventar', fg_color='transparent', font=self.header_font)
        self.title_label.pack(padx=20, pady=20, anchor=customtkinter.CENTER)

        self.table_Inv = ttk.Treeview(self, columns=("Name", "Anzahl", "Ort"))
        self.table_Inv.heading("#0", text="Artikel")
        self.table_Inv.heading("Name", text="Bezeichnung")
        self.table_Inv.heading("Anzahl", text="Anzahl")
        self.table_Inv.heading("Ort", text="Ort")

        self.table_Inv.pack(padx=20, pady=20, anchor=tk.CENTER, fill='x') 

        # Close the window
        self.new_button = customtkinter.CTkButton(self, text="Schließen", command=self.close)
        self.new_button.pack(pady=40)

        self.get_inventory_data()
    
    def close(self):
        self.destroy()

    def get_inventory_data(self):
        records = crud.get_inv_entries()
        for record in records:
            self.counter += 1
            #print("Record " + str(self.counter) + ":", record)
            self.table_Inv.insert("", "end", text=record.article_number, values=(record.name, record.stock, record.location))

class Article(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.header_font = customtkinter.CTkFont(family="Helvetica", size=18, weight="bold", slant="roman", underline=False, overstrike=False)
        
        self.title("Artikel")
        self.geometry("950x450")
        self.minsize(900, 450)
        self.maxsize(1000, 100)   
        self.counter = 0     
        # header
        self.title_label = customtkinter.CTkLabel(self, text='Artikelübersicht', fg_color='transparent', font=self.header_font)
        self.title_label.pack(padx=20, pady=20, anchor=customtkinter.CENTER)

        #table style
        self.style = ttk.Style()
        self.style.theme_use('default')
        
        # table config
        self.table_Art = ttk.Treeview(self, columns=("Artikel", "Name", "Zusatz", "Hersteller", "VK", "EK"))
        self.style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")

        #Column settings
        self.table_Art.column("#0", width=0, stretch=False)
        self.table_Art.column("Artikel", width=60)
        self.table_Art.column("Hersteller", width=100)
        self.table_Art.column("VK", anchor="e", width=20)
        self.table_Art.column("EK", anchor="e", width=20)
    
        self.table_Art.heading("#0", text="ID", anchor="w" )
        self.table_Art.heading("Artikel", anchor="w", text="Artikel")
        self.table_Art.heading("Name", anchor="w",text="Name")
        self.table_Art.heading("Zusatz", anchor="w",text="Zusatz")
        self.table_Art.heading("Hersteller", anchor="center", text="Hersteller")
        self.table_Art.heading("VK", anchor="center",text="VK")
        self.table_Art.heading("EK", anchor="center",text="EK")

        self.table_Art.pack(padx=20, pady=20, anchor=tk.CENTER, fill='x') 

        #data boxes
        
        self.data_frame = customtkinter.CTkFrame(self)
        self.data_frame.pack(fill="x", expand="yes", padx=20)

        art_label = customtkinter.CTkLabel(self.data_frame, text="Artikel-Nr.")
        art_label.grid(row=0, column=0, padx=10, pady=10)
        art_entry = customtkinter.CTkEntry(self.data_frame)
        art_entry.grid(row=0, column=1, padx=10, pady=10)

        name_label = customtkinter.CTkLabel(self.data_frame, text="Name")
        name_label.grid(row=0, column=2, padx=10, pady=10)
        name_entry = customtkinter.CTkEntry(self.data_frame)
        name_entry.grid(row=0, column=3, padx=10, pady=10)

        add_label = customtkinter.CTkLabel(self.data_frame, text="Zusatz")
        add_label.grid(row=0, column=4, padx=10, pady=10)
        add_entry = customtkinter.CTkEntry(self.data_frame)
        add_entry.grid(row=0, column=5, padx=10, pady=10)

        prod_label = customtkinter.CTkLabel(self.data_frame, text="Hersteller")
        prod_label.grid(row=1, column=0, padx=10, pady=10)
        prod_entry = customtkinter.CTkEntry(self.data_frame)
        prod_entry.grid(row=1, column=1, padx=10, pady=10)

        sp_label = customtkinter.CTkLabel(self.data_frame, text="VK")
        sp_label.grid(row=1, column=2, padx=10, pady=10)
        sp_entry = customtkinter.CTkEntry(self.data_frame)
        sp_entry.grid(row=1, column=3, padx=10, pady=10)

        pp_label = customtkinter.CTkLabel(self.data_frame, text="EK")
        pp_label.grid(row=1, column=4, padx=10, pady=10)
        pp_entry = customtkinter.CTkEntry(self.data_frame)
        pp_entry.grid(row=1, column=5, padx=10, pady=10)

        # button Close the window
        self.new_button = customtkinter.CTkButton(self, text="Schließen", command=self.close)
        self.new_button.pack(pady=40)

        self.get_art_data()

    def close(self):
        self.destroy()

    def get_art_data(self):
        records = crud.get_art_entries()
        for record in records:
            self.counter += 1
            #print("Record " + str(self.counter) + ":", record)
            self.table_Art.insert("", "end", text=record.id, values=(record.article_number, record.name, record.additional_information, record.producer, record.purchase_price, record.selling_price))

        
    # Clear entry boxes
    def clear_entries(self):
	    # Clear entry boxes
	    self.art_entry.delete(0)
        self.name_entry.delete(0)
        self.add_entry.delete(0, END)
	    self.prod_entry.delete(0, END)
	    self.sp_entry.delete(0, END)
	    self.pp_entry.delete(0, END)

    # Select Record
    def select_record(self):
	    # Clear entry boxes
	    self.art_entry.delete(0, END)
	    self.name_entry.delete(0, END)
	    self.prod_entry.delete(0, END)
	    self.address_entry.delete(0, END)
	    self.sp_entry.delete(0, END)
	    self.pp_entry.delete(0, END)

	    # Grab record Number
#	    self.selected = my_tree.focus()
	    # Grab record values
#	    self.values = my_tree.item(selected, 'values')

	    # outpus to entry boxes
	    self.art_entry.insert(0, values[0])
	    self.name_entry.insert(0, values[1])
	    self.ad_entry.insert(0, values[2])
	    self.prod_entry.insert(0, values[3])
	    self.sp_entry.insert(0, values[4])
	    self.pp_entry.insert(0, values[5])

# Main Function
if __name__ == "__main__":
#    if len(crud.get_inv_entries()) > 0:
#    crud.add_test_data(art='420', name='not69', loc='HOME', stock=1.25)
#    if len(crud.get_art_entries()) > 0:
#    crud.add_art_entry(art='123456', name='Test', info='additional Info', ek=69.69, vk=420.69)
    app = App()
    app.mainloop()
