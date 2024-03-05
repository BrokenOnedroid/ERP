# Standard library imports
import sys

# GUI Imports
import tkinter as tk
from tkinter import ttk
import customtkinter

customtkinter.set_appearance_mode("dark")
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
        # header
        self.title_label = customtkinter.CTkLabel(self, text='Inventar', fg_color='transparent', font=self.header_font)
        self.title_label.pack(padx=20, pady=20, anchor=customtkinter.CENTER)

        self.table_Inv = ttk.Treeview(self, columns=("Bezeichnung", "Anzahl", "EK", "VK"))
        self.table_Inv.heading("#0", text="Artikel")
        self.table_Inv.heading("Bezeichnung", text="Bezeichnung")
        self.table_Inv.heading("Anzahl", text="Anzahl")
        self.table_Inv.heading("EK", text="EK")
        self.table_Inv.heading("VK", text="VK", )

        self.table_Inv.pack(padx=20, pady=20, anchor=tk.CENTER) 

        # Close the window
        self.new_button = customtkinter.CTkButton(self, text="Close Window", command=self.close)
        self.new_button.pack(pady=40)
    
    def close(self):
        self.destroy()

    def get_inventory_data(self):
        pass

# table for Invetory Data
#class InventoryTable(customtkinter.CTkTabview):
    #def __init__(self, master, **kwargs):
        #super().__init__(master, **kwargs)

        # create Table
        #treeview = ttk.Treeview()
        #treeview.pack()


        # add widgets on tabs
        #self._label = customtkinter.CTkLabel(master=self.tab("Artikelnummer"))
        #self._label.grid(row=0, column=0, padx=20, pady=10)


class Article(customtkinter.CTkToplevel):
    pass

# Main Function
if __name__ == "__main__":
    app = App()
    app.mainloop()
