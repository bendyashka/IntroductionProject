import tkinter as tk
from tkinter import ttk, messagebox
import requests

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("400x200")

        self.label_from_currency = tk.Label(root, text="To Currency:")
        self.label_from_currency.grid(row=2, column=0, padx=10, pady=10)

        self.currency_from_var = tk.StringVar()
        self.currency_from_combobox = ttk.Combobox(root, textvariable=self.currency_from_var)
        self.currency_from_combobox['values'] = self.get_currency_list()
        self.currency_from_combobox.grid(row=0, column=1, padx=10, pady=10)

        self.label_amount = tk.Label(root, text="Amount:")
        self.label_amount.grid(row=1, column=0, padx=10, pady=10)

        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)

        self.label_to_currency = tk.Label(root, text="From Currency:")
        self.label_to_currency.grid(row=0, column=0, padx=10, pady=10)

        self.currency_to_var = tk.StringVar()
        self.currency_to_combobox = ttk.Combobox(root, textvariable=self.currency_to_var)
        self.currency_to_combobox['values'] = self.get_currency_list()
        self.currency_to_combobox.grid(row=2, column=1, padx=10, pady=10)

        self.buy_button = tk.Button(root, text="Buy", command=lambda: self.show_result('buy'))
        self.buy_button.grid(row=3, column=0, pady=10)

        self.sell_button = tk.Button(root, text="Sell", command=lambda: self.show_result('sell'))
        self.sell_button.grid(row=3, column=1, pady=10)

    def get_currency_list(self):
        return ['USD', 'EUR', 'CNY', 'RUB', 'KGS']

    def exchange_currencies(self, amount, from_currency, to_currency, operation):
        url = "https://mbank.cbk.kg/svc-biz-ib-cbk-currencies/v1/unauthorized-api/private/currencies/exchange-rates"
        response = requests.get(url)
        data = response.json()['rates']

        if operation == 'buy2':
            rate_key = 'buy'
        elif operation == 'sell':
            rate_key = 'sell'
        else:
            return None

        try:
            from_currency_rate = next(currency['to'][0][rate_key] for currency in data if currency['currency'] == to_currency)
        except StopIteration:
            from_currency_rate = next(currency[rate_key] for currency in data if currency['currency'] == to_currency)

        try:
            to_currency_rate = next(currency['to'][0][rate_key] for currency in data if currency['currency'] == from_currency)
        except StopIteration:
            to_currency_rate = next(currency[rate_key] for currency in data if currency['currency'] == from_currency)

        if from_currency_rate is None or to_currency_rate is None:
            return None

        converted_amount = amount / from_currency_rate * to_currency_rate

        return round(converted_amount, 2)

    def show_result(self, operation):
        try:
            amount = float(self.amount_entry.get())
            from_currency = self.currency_from_var.get()
            to_currency = self.currency_to_var.get()

            converted_amount = self.exchange_currencies(amount, from_currency, to_currency, operation)

            if converted_amount is not None:
                result_str = f"{amount} {from_currency} is equal to {converted_amount} {to_currency} ({operation.capitalize()})"
                messagebox.showinfo("Conversion Result", result_str)
            else:
                messagebox.showerror("Error", "Invalid currency selection")

        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = CurrencyConverterApp(root)
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}") 