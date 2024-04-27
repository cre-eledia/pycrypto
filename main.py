from tkinter import *
from tkinter import messagebox, Menu
import requests
import json
import base64
import sqlite3
import os
from dotenv import load_dotenv

pycrypto = Tk()
pycrypto.title("Mein Crypto-Portfolio")

icon = PhotoImage(file='btc.png')
pycrypto.iconphoto(False, icon)

con = sqlite3.connect('coin.db')
cursorObj = con.cursor()

cursorObj.execute(
    'CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY, symbol TEXT, amount INTEGER, price REAL)')
con.commit()


def refresh():
    # empty the window
    for widget in pycrypto.winfo_children():
        widget.destroy()
    app_header()
    my_portfolio()
    app_navigation()


def app_navigation():
    def clear_all():
        cursorObj.execute('DELETE FROM coin')
        con.commit()
        messagebox.showinfo("Erfolg", "Portfolio wurde gelöscht")
        refresh()
    menu = Menu(pycrypto)
    pycrypto.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label="Datei", menu=filemenu)
    filemenu.add_command(label="Portfolio löschen", command=clear_all)
    filemenu.add_command(label="Aktualisieren", command=refresh)
    filemenu.add_command(label="Schließen", command=pycrypto.quit)


def my_portfolio():
    base_url = 'https://pro-api.coinmarketcap.com/v1/'
    load_dotenv()
    CMC_PRO_API_KEY = os.getenv('CMC_PRO_API_KEY')
    endpoint = 'cryptocurrency/listings/latest?start=1&limit=500&convert=EUR'
    url = f'{base_url}{endpoint}&CMC_PRO_API_KEY={CMC_PRO_API_KEY}'
    request = requests.get(url)
    api = json.loads(request.content)

    def font_color(amount):
        if amount > 0:
            return "green"
        elif amount < 0:
            return "red"
        else:
            return "black"

    cursorObj.execute('SELECT * FROM coin')
    coins = cursorObj.fetchall()

    def insert_coin(symbol, amount, price):
        cursorObj.execute('INSERT INTO coin(symbol, amount, price) VALUES(?, ?, ?)',
                          (symbol, amount, price))
        con.commit()
        messagebox.showinfo("Erfolg", "Coin wurde hinzugefügt")
        refresh()

    def delete_coin(id):
        cursorObj.execute('DELETE FROM coin WHERE id=?', (id,))
        con.commit()
        messagebox.showinfo("Erfolg", "Coin wurde gelöscht")
        # refresh the page after deleting a coin
        refresh()

    def update_coin(id, symbol, amount, price):
        cursorObj.execute('UPDATE coin SET symbol=?, amount=?, price=? WHERE id=?',
                          (symbol, amount, price, id))
        con.commit()
        messagebox.showinfo("Erfolg", "Coin wurde aktualisiert")
        refresh()

    total_pl = 0
    total_current_value = 0
    total_amount_paid = 0
    current_row = 0

    for coin in coins:
        for i in range(0, 500):
            if coin[1] == api['data'][i]['symbol']:
                total_paid = coin[2] * coin[3]
                current_value = coin[2] * \
                    api['data'][i]['quote']['EUR']['price']
                pl_percoin = api['data'][i]['quote']['EUR']['price'] - \
                    coin[3]
                total_pl_coin = pl_percoin * coin[2]
                total_pl += total_pl_coin
                total_current_value += current_value
                total_amount_paid += total_paid

                portfolio_id = Label(pycrypto, text=coin[0], bg="#F3F4F6", fg="black",
                                     font="Helvetica 12", padx="2", pady="2", borderwidth=2, relief="groove")
                portfolio_id.grid(row=current_row+1, column=0,
                                  sticky=N + S + E + W)

                name = Label(pycrypto, text=api['data'][i]['symbol'], bg="white",
                             fg="black", font="Helvetica 12", padx="2", pady="2", borderwidth=2, relief="groove")
                name.grid(row=current_row+1, column=1, sticky=N + S + E + W)

                price = Label(pycrypto, text="{0:.2f}".format(api['data'][i]['quote']['EUR']['price']), bg="#F3F4F6",
                              fg="black", font="Helvetica 12", padx="2", pady="2", borderwidth=2, relief="groove")
                price.grid(row=current_row+1, column=2, sticky=N + S + E + W)

                amount = Label(pycrypto, text=coin[2], bg="white",
                               fg="black", font="Helvetica 12", padx="2", pady="2", borderwidth=2, relief="groove")
                amount.grid(row=current_row+1, column=3, sticky=N + S + E + W)

                total_paid = Label(pycrypto, text="{0:.2f}".format(total_paid), bg="#F3F4F6",
                                   fg="black", font="Helvetica 12", padx="2", pady="2", borderwidth=2, relief="groove")
                total_paid.grid(row=current_row+1, column=4,
                                sticky=N + S + E + W)

                current_value = Label(pycrypto, text="{0:.2f}".format(current_value), bg="white",
                                      fg="black", font="Helvetica 12", padx="2", pady="2", borderwidth=2, relief="groove")
                current_value.grid(row=current_row+1,
                                   column=5, sticky=N + S + E + W)

                pl_percoin = Label(pycrypto, text="{0:.2f}".format(pl_percoin), bg="#F3F4F6",
                                   fg=font_color(float(pl_percoin)), font="Helvetica 12", padx="2", pady="2", borderwidth=2, relief="groove")
                pl_percoin.grid(row=current_row+1, column=6,
                                sticky=N + S + E + W)

                total_pl_coin = Label(pycrypto, text="{0:.2f}".format(total_pl_coin), bg="white",
                                      fg=font_color(float(total_pl_coin)), font="Helvetica 12", padx="2", pady="2", borderwidth=2, relief="groove")
                total_pl_coin.grid(row=current_row+1,
                                   column=7, sticky=N + S + E + W)
                current_row += 1

    # insert symbol entry field
    symbol_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    symbol_txt.grid(row=current_row+3, column=1)
    # insert amount entry field
    amount_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_txt.grid(row=current_row+3, column=3)
    # insert price entry field
    price_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    price_txt.grid(row=current_row+3, column=2)
    # insert add coin Button
    add_coin = Button(pycrypto, text="Coin hinzufügen", bg="#142E54", fg="white", font="Helvetica 12",
                      padx="2", pady="2", borderwidth=2, relief="groove", command=lambda: insert_coin(symbol_txt.get(), amount_txt.get(), price_txt.get()))
    add_coin.grid(row=current_row+3, column=0, sticky=N + S + E + W)
    # update coin entry fields
    portid_update = Entry(pycrypto, borderwidth=2, relief="groove")
    portid_update.grid(row=current_row+4, column=0)
    symbol_update = Entry(pycrypto, borderwidth=2, relief="groove")
    symbol_update.grid(row=current_row+4, column=1)
    amount_update = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_update.grid(row=current_row+4, column=3)
    price_update = Entry(pycrypto, borderwidth=2, relief="groove")
    price_update.grid(row=current_row+4, column=2)
    # update coin Button
    update_coin_btn = Button(pycrypto, text="Coin aktualisieren", bg="#142E54", fg="white", font="Helvetica 12", padx="2", pady="2", borderwidth=2, relief="groove",
                             command=lambda: update_coin(portid_update.get(), symbol_update.get(), amount_update.get(), price_update.get()))
    update_coin_btn.grid(row=current_row+4, column=4, sticky=N + S + E + W)
    # delete coin entry field
    portid_delete = Entry(pycrypto, borderwidth=2, relief="groove")
    portid_delete.grid(row=current_row+5, column=0)
    # insert delete coin Button
    delete_coin_btn = Button(pycrypto, text="Coin löschen", bg="#142E54", fg="white", font="Helvetica 12",
                             padx="2", pady="2", borderwidth=2, relief="groove", command=lambda: delete_coin(portid_delete.get()))
    delete_coin_btn.grid(row=current_row+5, column=4, sticky=N + S + E + W)
    # sum up all columns values on last row
    total_am_paid = Label(pycrypto, text="{0:.2f}".format(total_amount_paid), bg="#F3F4F6", fg="black",
                          font="Helvetica 12", padx="2", pady="2", borderwidth=2, relief="groove")
    total_am_paid.grid(row=current_row+2, column=4, sticky=N + S + E + W)
    total_pl_coin = Label(pycrypto, text="{0:.2f}".format(total_pl), bg="white",
                          fg=font_color(float(total_pl)), font="Helvetica 12", padx="2", pady="2", borderwidth=2, relief="groove")
    total_pl_coin.grid(row=current_row+2, column=7, sticky=N + S + E + W)

    total_current_value_coins = Label(pycrypto, text="{0:.2f}".format(total_current_value),
                                      bg="white",  fg="black", font="Helvetica 12", padx="2", pady="2", borderwidth=2, relief="groove")
    total_current_value_coins.grid(
        row=current_row+2, column=5, sticky=N + S + E + W)
    api = ""
    # refresh button
    refresh_btn = Button(pycrypto, text="Aktualisieren", bg="#142E54", fg="white",
                         font="Helvetica 12", padx="2", pady="2", borderwidth=2, relief="groove", command=refresh)
    refresh_btn.grid(row=current_row+6, column=7, sticky=N + S + E + W)


def app_header():
    portfolio_id = Label(pycrypto, text="ID", bg="#142E54", padx="5", pady="5",
                         borderwidth=2, relief="groove", fg="white", font="Helvetica 12 bold")
    portfolio_id.grid(row=0, column=0, sticky=N + S + E + W)
    name = Label(pycrypto, text="Name", bg="#142E54", padx="5", pady="5", borderwidth=2, relief="groove",
                 fg="white", font="Helvetica 12 bold")
    name.grid(row=0, column=1, sticky=N + S + E + W)

    name = Label(pycrypto, text="Preis EUR", bg="#142E54", padx="5", pady="5", borderwidth=2, relief="groove",
                 fg="white", font="Helvetica 12 bold")
    name.grid(row=0, column=2, sticky=N + S + E + W)

    name = Label(pycrypto, text="Coins", bg="#142E54", padx="5", pady="5", borderwidth=2, relief="groove",
                 fg="white", font="Helvetica 12 bold")
    name.grid(row=0, column=3, sticky=N + S + E + W)

    name = Label(pycrypto, text="Gesamteinkaufspreis EUR", bg="#142E54", padx="5", pady="5", borderwidth=2, relief="groove",
                 fg="white", font="Helvetica 12 bold")
    name.grid(row=0, column=4, sticky=N + S + E + W)

    name = Label(pycrypto, text="Aktueller Wert EUR", bg="#142E54", padx="5", pady="5", borderwidth=2, relief="groove",
                 fg="white", font="Helvetica 12 bold")
    name.grid(row=0, column=5, sticky=N + S + E + W)

    name = Label(pycrypto, text="G/V je Coin EUR", bg="#142E54", padx="5", pady="5", borderwidth=2, relief="groove",
                 fg="white", font="Helvetica 12 bold")
    name.grid(row=0, column=6, sticky=N + S + E + W)

    name = Label(pycrypto, text="G/V EUR", bg="#142E54", padx="5", pady="5", borderwidth=2, relief="groove",
                 fg="white", font="Helvetica 12 bold")
    name.grid(row=0, column=7, sticky=N + S + E + W)


app_header()
app_navigation()
my_portfolio()
pycrypto.mainloop()
cursorObj.close()
con.close()
