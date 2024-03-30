# Standard library imports
import sys

# local .py 
from app import crud, models 
from app.database import engine
from sqlalchemy import text

# GUI Imports
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import customtkinter

from app.schemas import ArtCreate

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
            self.toplevel_window = Article(self)  # create window if its None or destroyed
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
        self.counter : int= 0      
        # header
        self.title_label = customtkinter.CTkLabel(self, text='Inventar', fg_color='transparent', font=self.header_font)
        self.title_label.pack(padx=20, pady=20, anchor=customtkinter.CENTER)

        self.table_inv = InventoryTable(self)
        self.table_inv.pack(padx=20, pady=20, anchor=customtkinter.CENTER, fill='x')

        # Close the window
        self.new_button = customtkinter.CTkButton(self, text="Schließen", command=self.close)
        self.new_button.pack(pady=40)
    
    def close(self):
        self.destroy()

class InventoryTable(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.counter : int = 0
        
        self.table_inv : ttk.Treeview = ttk.Treeview(self, columns=("Name", "Anzahl", "Ort"))
        self.table_inv.heading("#0", text="Artikel")
        self.table_inv.heading("Name", text="Bezeichnung")
        self.table_inv.heading("Anzahl", text="Anzahl")
        self.table_inv.heading("Ort", text="Ort")

        self.table_inv.pack(anchor=tk.CENTER, fill="both") 
        self.get_inventory_data()

    def get_inventory_data(self):
        records : Article = crud.get_inv_entries()
        for record in records:
            self.counter += 1
            #print("Record " + str(self.counter) + ":", record)
            self.table_inv.insert("", "end", text=record.article_number, values=(record.name, record.stock, record.location))        

class Article(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.header_font = customtkinter.CTkFont(family="Helvetica", size=18, weight="bold", slant="roman", underline=False, overstrike=False)
        
        self.title("Artikel")
        self.geometry("950x550")
        self.minsize(900, 450)
        self.maxsize(1000, 1000)   
  
        # header
        self.title_label = customtkinter.CTkLabel(self, text='Artikelübersicht', fg_color='transparent', font=self.header_font)
        self.title_label.pack(padx=20, pady=20, anchor=customtkinter.CENTER)

        self.art_frame = ArtTable(master=self)
        self.art_frame.pack(padx=20, pady=10, anchor=tk.CENTER, fill="both") 


        #data boxes
        self.data_frame = ArtDataFrame(master=self)
        self.data_frame.pack(fill="x", expand="yes", padx=20, pady=10)

        self.button_frame = ArtButtonFrame(master=self)
        self.button_frame.pack(fill="x", expand="yes", padx=20, pady=10)
        

        child_id = self.art_frame.table_art.get_children()[0]
        self.art_frame.table_art.focus(child_id)
        self.art_frame.table_art.selection_set(child_id)
        self.art_frame.focus()
        self.art_frame.table_art.bind('<<TreeviewSelect>>', self.selected_record) 
        
    def close(self):
        self.destroy()

    def selected_record(self, event):   
        tree = event.widget
        selection = [tree.item(item)["text"] for item in tree.selection()]
        print("selected items:", selection)
     
        """self.selected_item = self.art_frame.table_art.selection_get()
        print('selected' + self.selected)
        if self.selected != '' :
	        # Grab record values
            self.values = self.art_frame.item(self.selected, 'values')
            print(self.values)
            self.data_frame.art_entry.insert(0, self.values[0])
            self.data_frame.name_entry.insert(0, self.values[1])
            self.data_frame.add_entry.insert(0, self.values[2])
            self.data_frame.prod_entry.insert(0, self.values[3])
            self.data_frame.sp_entry.insert(0, self.values[4])
            self.data_frame.pp_entry.insert(0, self.values[5])"""
        
class ArtTable(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        #table style
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.counter = 0   
        
        # table config
        self.table_art = ttk.Treeview(self, selectmode="extended", columns=("Artikel", "Name", "Zusatz", "Hersteller", "VK", "EK"))
        self.style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")

        #Column settings
        self.table_art.column("#0", width=0, stretch=False)
        self.table_art.column("Artikel", width=60)
        self.table_art.column("Hersteller", width=100)
        self.table_art.column("VK", anchor="e", width=20)
        self.table_art.column("EK", anchor="e", width=20)
    
        self.table_art.heading("#0", text="ID", anchor="w" )
        self.table_art.heading("Artikel", anchor="w", text="Artikel")
        self.table_art.heading("Name", anchor="w",text="Name")
        self.table_art.heading("Zusatz", anchor="w",text="Zusatz")
        self.table_art.heading("Hersteller", anchor="center", text="Hersteller")
        self.table_art.heading("VK", anchor="center",text="VK")
        self.table_art.heading("EK", anchor="center",text="EK")
        
        self.get_art_data()
        #self.table_art.bind("")#, master.selected_record())
        self.table_art.pack(fill="both")
                    
    def get_art_data(self):
        records = crud.get_art_entries()
        for record in records:
            self.counter += 1
            #print("Record " + str(self.counter) + ":", record)
            self.table_art.insert("", "end", text=record.id, values=(record.article_number, record.name, record.additional_information, record.producer, record.purchase_price, record.selling_price))
    
class ArtDataFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.art_label = customtkinter.CTkLabel(self, text="Artikel-Nr.")
        self.art_label.grid(row=0, column=0, padx=10, pady=10)
        self.art_entry = customtkinter.CTkEntry(self)
        self.art_entry.grid(row=0, column=1, padx=10, pady=10)

        self.name_label = customtkinter.CTkLabel(self, text="Name")
        self.name_label.grid(row=0, column=2, padx=10, pady=10)
        self.name_entry = customtkinter.CTkEntry(self)
        self.name_entry.grid(row=0, column=3, padx=10, pady=10)

        self.add_label = customtkinter.CTkLabel(self, text="Zusatz")
        self.add_label.grid(row=0, column=4, padx=10, pady=10)
        self.add_entry = customtkinter.CTkEntry(self)
        self.add_entry.grid(row=0, column=5, padx=10, pady=10)

        self.prod_label = customtkinter.CTkLabel(self, text="Hersteller")
        self.prod_label.grid(row=1, column=0, padx=10, pady=10)
        self.prod_entry = customtkinter.CTkEntry(self)
        self.prod_entry.grid(row=1, column=1, padx=10, pady=10)

        self.sp_label = customtkinter.CTkLabel(self, text="VK")
        self.sp_label.grid(row=1, column=2, padx=10, pady=10)
        self.sp_entry = customtkinter.CTkEntry(self)
        self.sp_entry.grid(row=1, column=3, padx=10, pady=10)

        self.pp_label = customtkinter.CTkLabel(self, text="EK")
        self.pp_label.grid(row=1, column=4, padx=10, pady=10)
        self.pp_entry = customtkinter.CTkEntry(self)
        self.pp_entry.grid(row=1, column=5, padx=10, pady=10)
        
class ArtButtonFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.update_button = customtkinter.CTkButton(self, text="Eintrag aktualisieren")#, command=update_record)
        self.update_button.grid(row=0, column=0, padx=10, pady=10)

        self.add_button = customtkinter.CTkButton(self, text="Eintrag hinzufügen", command=self.add_record)
        self.add_button.grid(row=0, column=1, padx=10, pady=10)

        self.remove_one_button = customtkinter.CTkButton(self, text="Eintrag löschen", command=self.remove_one)
        self.remove_one_button.grid(row=0, column=2, padx=10, pady=10)

        self.move_up_button = customtkinter.CTkButton(self, text="Move Up", command=self.up)
        self.move_up_button.grid(row=1, column=0, padx=10, pady=10)

        self.move_down_button = customtkinter.CTkButton(self, text="Move Down", command=self.down)
        self.move_down_button.grid(row=1, column=1, padx=10, pady=10)

        self.select_record_button = customtkinter.CTkButton(self, text="Einträge bereinigen", command=self.clear_entries)
        self.select_record_button.grid(row=1, column=2, padx=10, pady=10)
        
        self.close_button = customtkinter.CTkButton(self, text="Fenster schließen", fg_color="red", command=master.close)
        self.close_button.grid(row=1, column=4, padx=10, sticky="ew")
    
    def add_record(self):
        art : ArtCreate = ArtCreate()
           
    def remove_all(self):
        pass
    
    def remove_one(self):
        pass
    
    def remove_many(self):
        pass
    
    def up(self):
        pass
    
    def down(self):
        pass
    
    def clear_entries(Self):
        pass
    

# Main Function
if __name__ == "__main__":
#    if len(crud.get_inv_entries()) > 0:
#    crud.add_test_data(art='420', name='not69', loc='HOME', stock=1.25)
#    if len(crud.get_art_entries()) > 0:
#    crud.add_art_entry(art='123456', name='Test', info='additional Info', ek=69.69, vk=420.69)
    app = App()
    app.mainloop()
