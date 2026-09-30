#!/usr/bin/env python3
"""Запуск конвертера валют с GUI"""

import tkinter as tk
from tkinter import messagebox
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RATES_FILE = os.path.join(SCRIPT_DIR, "rates.json")
if not os.path.exists(RATES_FILE):
    RATES_FILE = os.path.join(os.getcwd(), "rates.json")


def load_rates():
    if not os.path.exists(RATES_FILE):
        messagebox.showerror("Ошибка", f"Файл {RATES_FILE} не найден!")
        return {}
    try:
        with open(RATES_FILE, "r", encoding="utf-8") as f:
            rates = json.load(f)
            return rates
    except json.JSONDecodeError:
        messagebox.showerror("Ошибка", "Невалидный JSON в rates.json")
        return {}


class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Конвертер валют")
        self.root.resizable(False, False)

        self.rates = load_rates()
        currencies = list(self.rates.keys()) if self.rates else ["USD", "EUR", "RUB", "GBP"]

        tk.Label(root, text="Сумма:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.amount_entry = tk.Entry(root, width=15)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)
        self.amount_entry.insert(0, "100")

        tk.Label(root, text="Из:").grid(row=1, column=0, sticky="w", padx=10)
        self.from_var = tk.StringVar(value="USD")
        tk.OptionMenu(root, self.from_var, *currencies).grid(row=1, column=1, sticky="w", padx=10)

        tk.Label(root, text="В:").grid(row=2, column=0, sticky="w", padx=10, pady=(0, 10))
        self.to_var = tk.StringVar(value="RUB")
        tk.OptionMenu(root, self.to_var, *currencies).grid(row=2, column=1, sticky="w", padx=10, pady=(0, 10))

        tk.Button(root, text="Конвертировать", command=self.convert, width=20).grid(row=3, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
        self.result_label.grid(row=4, column=0, columnspan=2, pady=(0, 10))

    def convert(self):
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите число.")
            return

        from_c = self.from_var.get()
        to_c = self.to_var.get()

        if from_c not in self.rates or to_c not in self.rates:
            messagebox.showerror("Ошибка", "Валюта не найдена в курсах.")
            return

        if self.rates[from_c] == 0:
            messagebox.showerror("Ошибка", f"Курс {from_c} равен 0.")
            return

        result = amount / self.rates[from_c] * self.rates[to_c]
        self.result_label.config(text=f"{amount:.2f} {from_c} = {result:.2f} {to_c}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()