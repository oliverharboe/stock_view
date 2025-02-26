import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import datetime

class UserView:
    def __init__(self, master=None):
        self.m = tk.Tk()
        self.m.title("Aktie Data")
        self.m.geometry("800x600")
        self.current_stock = None

    def startview(self):
        # Ryd tidligere indhold
        for widget in self.m.winfo_children():
            widget.destroy()
            
        # Hovedramme
        main_frame = Frame(self.m, padx=20, pady=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Overskrift - Første brugergrænseflade
        Label(main_frame, text="Aktie overblik", font='Helvetica 18 bold').pack(pady=10)
        
        # Indre ramme med kant
        inner_frame = Frame(main_frame, relief=RIDGE, borderwidth=2, padx=20, pady=20)
        inner_frame.pack(fill=BOTH, expand=True, padx=100, pady=10)
        
        # Ticker kode input
        ticker_frame = Frame(inner_frame)
        ticker_frame.pack(fill=X, pady=20)
        self.ticker_entry = Entry(ticker_frame, font=('Helvetica', 11))
        self.ticker_placeholder = "Indtast Ticker kode"
        self.ticker_entry.insert(0, self.ticker_placeholder)
        self.ticker_entry.pack(fill=X, ipady=20)
        
        # Kurs input
        kurs_frame = Frame(inner_frame)
        kurs_frame.pack(fill=X, pady=10)
        self.kurs_entry = Entry(kurs_frame, font=('Helvetica', 11))
        self.kurs_placeholder = "Indtast kurs, aktien er købt til"
        self.kurs_entry.insert(0, self.kurs_placeholder)
        self.kurs_entry.pack(fill=X, ipady=8)
        
        # Antal aktier input
        antal_frame = Frame(inner_frame)
        antal_frame.pack(fill=X, pady=10)
        self.antal_entry = Entry(antal_frame, font=('Helvetica', 11))
        self.antal_placeholder = "Indtast antal aktier"
        self.antal_entry.insert(0, self.antal_placeholder)
        self.antal_entry.pack(fill=X, ipady=8)
        
        # Beskrivelsestekst
        description_frame = Frame(inner_frame)
        description_frame.pack(fill=X, pady=10)
        Label(description_frame, text="Tryk på den nedstående knap\nfor at finde de ønskede\ninformationer", 
              justify=CENTER).pack()
        
        # Find informationer knap
        button_frame = Frame(inner_frame)
        button_frame.pack(pady=15)
        find_button = Button(button_frame, text="Find informationer", 
                             command=self.find_information, relief=RIDGE,
                             borderwidth=1, padx=15, pady=5)
        find_button.pack()
        
        # Ryd fokus, når brugeren klikker i feltet
        self.ticker_entry.bind("<FocusIn>", self.clear_placeholder)
        self.kurs_entry.bind("<FocusIn>", self.clear_placeholder)
        self.antal_entry.bind("<FocusIn>", self.clear_placeholder)
    
    def clear_placeholder(self, event):
        """Fjerner placeholder-tekst, når brugeren klikker på feltet"""
        if event.widget == self.ticker_entry and event.widget.get() == self.ticker_placeholder:
            event.widget.delete(0, END)
        elif event.widget == self.kurs_entry and event.widget.get() == self.kurs_placeholder:
            event.widget.delete(0, END)
        elif event.widget == self.antal_entry and event.widget.get() == self.antal_placeholder:
            event.widget.delete(0, END)
    
    def find_information(self):
        try:
            self.current_stock = self.controller.getdata(self.ticker_entry.get())
            self.current_stock['buy_price'] = float(self.kurs_entry.get())
            self.current_stock['amount'] = int(self.antal_entry.get())
            self.showaktie()
        except Exception as e:
            messagebox.showerror("Fejl", f"Der opstod en fejl: {e}")
    
    def showaktie(self):
        # Ryd tidligere indhold
        for widget in self.m.winfo_children():
            widget.destroy()
            
        if not self.current_stock:
            messagebox.showerror("Fejl", "Ingen aktie-information tilgængelig")
            self.startview()
            return
            
        # Hovedramme
        main_frame = Frame(self.m, padx=20, pady=20)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Overskrift - Anden brugergrænseflade
        Label(main_frame, text="DIN udvikling", font='Helvetica 18 bold').pack(pady=10)
        
        # Indre ramme med kant
        inner_frame = Frame(main_frame, relief=RIDGE, borderwidth=2, padx=20, pady=20)
        inner_frame.pack(fill=BOTH, expand=True, padx=100, pady=10)
        
        # Aktie overblik overskrift
        Label(inner_frame, text="Aktie overblik", font='Helvetica 16 bold').pack(pady=10)
        
        # Information om aktien
        info_frame = Frame(inner_frame)
        info_frame.pack(fill=X, pady=5)
        
        # Ticker kode
        Label(info_frame, text=f"Aktie: {self.current_stock.get('name')}", anchor="w").pack(fill=X, pady=2)

        # Tid
        Label(info_frame, text=f"Tid: {self.current_stock.get('time')}", anchor="w").pack(fill=X, pady=2)
        
        # Kurs købt til
        Label(info_frame, text=f"Kurs købt til: {self.current_stock.get('buy_price', 0):.0f} $USD", anchor="w").pack(fill=X, pady=2)
        
        # Antal aktier
        Label(info_frame, text=f"Antal aktier: {self.current_stock.get('amount', 0)}", anchor="w").pack(fill=X, pady=2)
        
        # Nuværende kurs pr. aktie
        Label(info_frame, text=f"Nuværende kurs pr. aktie:", anchor="w").pack(fill=X, pady=2)
        Label(info_frame, text=f"{self.current_stock.get('price', 0):.0f} $USD", anchor="w").pack(fill=X, pady=2)
        
        # Samlede værdi
        samlet_vaerdi = self.current_stock.get('price') * self.current_stock.get('amount', 0)
        Label(info_frame, text=f"Samlede værdi:", anchor="w").pack(fill=X, pady=2)
        Label(info_frame, text=f"{samlet_vaerdi:.0f} $USD", anchor="w").pack(fill=X, pady=2)
        
        # Vækst i procent
        kurs_kobt = self.current_stock.get('buy_price', 0)
        if kurs_kobt > 0:
            vaekst_procent = ((self.current_stock.get("price") / kurs_kobt) - 1) * 100
        else:
            vaekst_procent = 0
        Label(info_frame, text=f"Vækst i procent: {vaekst_procent:.2f}%", anchor="w").pack(fill=X, pady=2)
        
        # Fortjeneste
        fortjeneste = (float(self.current_stock.get("price")) - float(self.current_stock.get("buy_price"))) * self.current_stock.get("amount")
        Label(info_frame, text=f"Fortjeneste:", anchor="w").pack(fill=X, pady=2)
        Label(info_frame, text=f"{fortjeneste:.0f} $USD", anchor="w").pack(fill=X, pady=2)
        
        # Opdater knap
        button_frame = Frame(inner_frame)
        button_frame.pack(pady=15)
        opdater_button = Button(button_frame, text="Opdater", 
                                command=self.refresh, relief=RIDGE,
                                borderwidth=3, padx=20, pady=10)
        opdater_button.pack()
    
    def refresh(self):
        # Her kunne du hente opdaterede data; vi simulerer en opdatering ved at vise samme skærm
        self.showaktie()
    
    def setController(self, controller):
        self.controller = controller
    
    def run(self):
        self.startview()
        self.m.mainloop()


