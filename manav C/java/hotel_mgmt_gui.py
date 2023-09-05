from tkinter import *
import random
import time
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter import *

def system():
    root = Tk()
    root.geometry("1700x800")
    root.title("APNA DHABA")


    def Database():
        global connectn, cursor
        connectn = sqlite3.connect("Restaurant.db")
        cursor = connectn.cursor()
        
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS Restaurantrecords(ordno text,piz text,bur text,ice text, dr text, ct text,sb text)")

    
    orderno = StringVar()
    pizza = StringVar()
    burger = StringVar()
    icecream = StringVar()
    drinks = StringVar()
    cost = StringVar()
    subtotal = StringVar()
    

    
    def tottal():
    
        order = (orderno.get())
        pi = float(pizza.get())
        bu = float(burger.get())
        ice = float(icecream.get())
        dr = float(drinks.get())



        costpi = pi * 240
        costbu = bu * 125
        costice = ice * 80
        costdr = dr * 60
        costofmeal = (costpi + costbu + costice + costdr)
       
        sub = (costpi + costbu + costice + costdr)
        
        overall = str(  sub)

        cost.set(costofmeal)
        
        subtotal.set(sub)
        

    def reset():
        orderno.set("")
        pizza.set("")
        burger.set("")
        icecream.set("")
        drinks.set("")
        cost.set("")
        subtotal.set("")
        
    def exit():
        root.destroy()

   
    topframe = Frame(root, bg="white", width=1600, height=50)
    topframe.pack(side=TOP)
    leftframe = Frame(root, width=900, height=700)
    leftframe.pack(side=LEFT)

    rightframe = Frame(root, width=400, height=700)
    rightframe.pack(side=RIGHT)

    def DisplayData():
        Database()
        my_tree.delete(*my_tree.get_children())
        cursor = connectn.execute("SELECT * FROM Restaurantrecords")
        fetch = cursor.fetchall()
        for data in fetch:
            my_tree.insert('', 'end', values=(data))
        cursor.close()
        connectn.close()

    style = ttk.Style()
    style.configure("Treeview",
                    foreground="black",
                    rowheight=40,
                    fieldbackground="white"
                    )
    style.map('Treeview',
              background=[('selected', 'lightblue')])

    
    my_tree = ttk.Treeview(rightframe)
    my_tree['columns'] = ("ordno", "piz", "bur", "ice", "dr", "ct", "sb")

    horizontal_bar = ttk.Scrollbar(rightframe, orient="horizontal")
    horizontal_bar.configure(command=my_tree.xview)
    my_tree.configure(xscrollcommand=horizontal_bar.set)
    horizontal_bar.pack(fill=X, side=BOTTOM)

    vertical_bar = ttk.Scrollbar(rightframe, orient="vertical")
    vertical_bar.configure(command=my_tree.yview)
    my_tree.configure(yscrollcommand=vertical_bar.set)
    vertical_bar.pack(fill=Y, side=RIGHT)

    my_tree.column("#0", width=0, minwidth=0)
    my_tree.column("ordno", anchor=CENTER, width=80, minwidth=25)
    my_tree.column("piz", anchor=CENTER, width=60, minwidth=25)
    my_tree.column("bur", anchor=CENTER, width=50, minwidth=25)
    my_tree.column("ice", anchor=CENTER, width=80, minwidth=25)
    my_tree.column("dr", anchor=CENTER, width=50, minwidth=25)
    my_tree.column("ct", anchor=CENTER, width=50, minwidth=25)
    my_tree.column("sb", anchor=CENTER, width=100, minwidth=25)
    

   
    my_tree.heading("ordno", text="Order No", anchor=CENTER)
    my_tree.heading("piz", text="Pizza", anchor=CENTER)
    my_tree.heading("bur", text="Burger", anchor=CENTER)
    my_tree.heading("ice", text="Ice cream", anchor=CENTER)
    my_tree.heading("dr", text="Drinks", anchor=CENTER)
    my_tree.heading("ct", text="Cost", anchor=CENTER)
    my_tree.heading("sb", text="Subtotal", anchor=CENTER)
    

    my_tree.pack()
    DisplayData()

    
    def add():
        Database()
       
        orders = orderno.get()
        pizzas = pizza.get()
        burgers = burger.get()
        ices = icecream.get()
        drinkss = drinks.get()
        costs = cost.get()
        subtotals = subtotal.get()
        
        if orders == "" or pizzas == "" or burgers == "" or ices == "" or drinkss == "" or costs == "" or subtotals == "" :
            messagebox.showinfo("Warning", "Please fill the empty field!!!")
        else:
            connectn.execute(
                'INSERT INTO Restaurantrecords (ordno, piz, bur , ice ,dr ,ct ,sb ) VALUES (?,?,?,?,?,?,?)',
                (orders, pizzas, burgers, ices, drinkss, costs, subtotals))
            connectn.commit()
            messagebox.showinfo("Message", "Stored successfully")
        
        DisplayData()
        connectn.close()

    
    def DisplayData():
        Database()
        my_tree.delete(*my_tree.get_children())
        cursor = connectn.execute("SELECT * FROM Restaurantrecords")
        fetch = cursor.fetchall()
        for data in fetch:
            my_tree.insert('', 'end', values=(data))
        cursor.close()
        connectn.close()

    def Delete():
        Database()
        if not my_tree.selection():
            messagebox.showwarning("Warning", "Select data to delete")
        else:
            result = messagebox.askquestion('Confirm', 'Are you sure you want to delete this record?',
                                            icon="warning")
        if result == 'yes':
            curItem = my_tree.focus()
            contents = (my_tree.item(curItem))
            selecteditem = contents['values']
            my_tree.delete(curItem)
            cursor = connectn.execute("DELETE FROM Restaurantrecords WHERE ordno= %d" % selecteditem[0])
            connectn.commit()
            cursor.close()
            connectn.close()

    
    localtime = time.asctime(time.localtime(time.time()))
    
    main_lbl = Label(topframe, font=('Calibri', 25, 'bold'), text="Restaurant Management System", fg="Blue",
                   anchor=W)
    main_lbl.grid(row=0, column=0)
    main_lbl = Label(topframe, font=('Calibri', 15,), text=localtime, fg="lightgreen", anchor=W)
    main_lbl.grid(row=1, column=0)

    
    ordlbl = Label(leftframe, font=('Calibri', 16, 'bold'), text="Order No.", fg="black", bd=5, anchor=W).grid(row=1,
                                                                                                             column=0)
    ordtxt = Entry(leftframe, font=('Calibri', 16, 'bold'), bd=6, insertwidth=4, justify='right',
                   textvariable=orderno).grid(row=1, column=1)
    
    pizlbl = Label(leftframe, font=('Calibri', 16, 'bold'), text="Pizza", fg="black", bd=5, anchor=W).grid(row=2,
                                                                                                         column=0)
    piztxt = Entry(leftframe, font=('Calibri', 16, 'bold'), bd=6, insertwidth=4, justify='right',
                   textvariable=pizza).grid(row=2, column=1)
    
    burlbl = Label(leftframe, font=('Calibri', 16, 'bold'), text="Burger", fg="black", bd=5, anchor=W).grid(row=3,
                                                                                                          column=0)
    burtxt = Entry(leftframe, font=('Calibri', 16, 'bold'), bd=6, insertwidth=4, justify='right',
                   textvariable=burger).grid(row=3, column=1)

    
    icelbl = Label(leftframe, font=('Calibri', 16, 'bold'), text="Ice Cream", fg="black", bd=5, anchor=W).grid(row=4,
                                                                                                             column=0)
    icetxt = Entry(leftframe, font=('Calibri', 16, 'bold'), bd=6, insertwidth=4, justify='right',
                   textvariable=icecream).grid(row=4, column=1)
    
    drinklbl = Label(leftframe, font=('Calibri', 16, 'bold'), text="Drinks", fg="black", bd=5, anchor=W).grid(row=5,
                                                                                                            column=0)
    drinktxt = Entry(leftframe, font=('Calibri', 16, 'bold'), bd=6, insertwidth=4, justify='right',
                     textvariable=drinks).grid(row=5, column=1)
    
    costlbl = Label(leftframe, font=('Calibri', 16, 'bold'), text="Cost", bd=5, anchor=W).grid(row=6, column=0)
    costtxt = Entry(leftframe, font=('Calibri', 16, 'bold'), bd=6, insertwidth=4, justify='right',
                    textvariable=cost).grid(row=6, column=1)
    
    sublbl = Label(leftframe, font=('Calibri', 16, 'bold'), text="Subtotal", bd=5, anchor=W).grid(row=7, column=0)
    subtxt = Entry(leftframe, font=('Calibri', 16, 'bold'), bd=6, insertwidth=4, justify='right',
                   textvariable=subtotal).grid(row=7, column=1)
   
    


    totbtn = Button(leftframe, font=('Calibri', 16, 'bold'), text="Total", bg="Lightgrey", fg="black", bd=3, padx=5, pady=5,
                    width=6, command=tottal).grid(row=6, column=3)

    resetbtn = Button(leftframe, font=('Calibri', 16, 'bold'), text="Reset", bg="lightgrey", fg="black", bd=3, padx=5,
                      pady=5, width=6, command=reset).grid(row=4, column=3)

    exitbtn = Button(leftframe, font=('Calibri', 16, 'bold'), text="Exit The System", bg="lightgrey", fg="black", bd=3, padx=5,
                     pady=5, width=12, command=exit).grid(row=6, column=2)

    addbtn = Button(leftframe, font=('Calibri', 16, 'bold'), text="Add", bg="lightgrey", fg="black", bd=3, padx=5, pady=5,
                    width=6, command=add).grid(row=2, column=3)

    deletebtn = Button(leftframe, font=('Calibri', 16, 'bold'), text="Delete Record", bg="lightgrey", fg="black", bd=3,
                       padx=5, pady=5, width=12, command=Delete).grid(row=4, column=2)


    
    def menu():
        roott = Tk()
        roott.title("Price Menu")
        roott.geometry("300x300")
        lblinfo = Label(roott, font=("Calibri", 20, "bold"), text="ITEM LIST", fg="black", bd=10)
        lblinfo.grid(row=0, column=0)
        lblprice = Label(roott, font=("Calibri", 20, "bold"), text="Prices", fg="black", bd=10)
        lblprice.grid(row=0, column=3)
        lblpizza = Label(roott, font=("Calibri", 20, "bold"), text="Pizza", fg="Blue", bd=10)
        lblpizza.grid(row=1, column=0)
        lblpricep = Label(roott, font=("Calibri", 20, "bold"), text="240/-", fg="blue", bd=10)
        lblpricep.grid(row=1, column=3)
        lblburger = Label(roott, font=("Calibri", 20, "bold"), text="Burger", fg="Blue", bd=10)
        lblburger.grid(row=3, column=0)
        lblpriceb = Label(roott, font=("Calibri", 20, "bold"), text="125/-", fg="blue", bd=10)
        lblpriceb.grid(row=3, column=3)
        lblicecream = Label(roott, font=("Calibri", 20, "bold"), text="Ice-Cream", fg="Blue", bd=10)
        lblicecream.grid(row=4, column=0)
        lblpricei = Label(roott, font=("Calibri", 20, "bold"), text="80/-", fg="blue", bd=10)
        lblpricei.grid(row=4, column=3)
        lbldrinks = Label(roott, font=("Calibri", 20, "bold"), text="Drinks", fg="Blue", bd=10)
        lbldrinks.grid(row=5, column=0)
        lblpriced = Label(roott, font=("Calibri", 20, "bold"), text="60/-", fg="blue", bd=10)
        lblpriced.grid(row=5, column=3)
        roott.mainloop()

   
    menubtn = Button(leftframe, font=('Calibri', 16, 'bold'), text="Menu Card", bg="lightgrey", fg="black", bd=3, padx=6,
                     pady=6, width=12, command=menu).grid(row=2, column=2)

    root.mainloop()

system()