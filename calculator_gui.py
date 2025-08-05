import tkinter as tk
from tkinter import ttk
from calci import evaluate_expression

# ==== Currency Rates ====
currency_rates = {
    "INR": 1.0,
    "USD": 0.012,
    "EUR": 0.011,
    "JPY": 1.82,
    "GBP": 0.0093
}

# ==== Core Functions ====
def convert_currency():
    try:
        input_value = screen_var.get().strip()
        if not input_value:
            input_value = "1"
            screen_var.set("1")
        amount = float(input_value)
        from_curr = from_currency.get()
        to_curr = to_currency.get()
        rate = currency_rates[to_curr] / currency_rates[from_curr]
        converted = round(amount * rate, 4)
        add_to_history(f"{amount} {from_curr} → {converted} {to_curr}")
        screen_var.set(str(converted))
    except:
        screen_var.set("Error")

def calculate():
    try:
        expression = screen.get()
        result = evaluate_expression(expression)
        add_to_history(f"{expression} = {result}")
        screen_var.set(result)
    except:
        screen_var.set("Error")

def on_click(event):
    text = event.widget["text"]
    if text == "=":
        calculate()
    elif text == "C":
        screen_var.set("")
    else:
        screen_var.set(screen_var.get() + text)

def add_to_history(entry):
    history_list.insert(tk.END, entry)

def toggle_history():
    global history_visible
    if history_visible:
        history_frame.pack_forget()
        history_visible = False
    else:
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        history_visible = True

# ==== GUI Setup ====
root = tk.Tk()
root.title("Smart Calculator with Toggle History")
root.geometry("500x750")
root.configure(bg="#222")

# ==== Entry Display ====
screen_var = tk.StringVar()
screen = tk.Entry(root, textvar=screen_var, font="Arial 24", bd=10, relief=tk.RIDGE, justify=tk.RIGHT)
screen.pack(fill=tk.BOTH, ipadx=8, ipady=20, padx=10, pady=10)

# ==== Bind Enter Globally ====
root.bind("<Return>", lambda event: calculate())

# ==== Buttons ====
button_frame = tk.Frame(root, bg="#333")
button_frame.pack(fill=tk.BOTH, expand=True)

buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"],
    ["C", "(", ")", "^"]
]

for row_values in buttons:
    row = tk.Frame(button_frame, bg="#333")
    row.pack(expand=True, fill="both")
    for btn_text in row_values:
        button = tk.Button(
            row, text=btn_text, font="Arial 18", relief=tk.FLAT,
            bg="#444", fg="white", activebackground="#666", activeforeground="white"
        )
        button.pack(side="left", expand=True, fill="both", padx=2, pady=2)
        button.bind("<Button-1>", on_click)

# ==== Currency Conversion ====
currency_frame = tk.Frame(root, bg="#222")
currency_frame.pack(fill=tk.BOTH, padx=10, pady=10)

tk.Label(currency_frame, text="From", fg="white", bg="#222", font="Arial 12").grid(row=0, column=0)
tk.Label(currency_frame, text="To", fg="white", bg="#222", font="Arial 12").grid(row=0, column=1)

from_currency = ttk.Combobox(currency_frame, values=list(currency_rates.keys()), font="Arial 12", width=10, state="readonly")
from_currency.set("INR")
from_currency.grid(row=1, column=0, padx=5)

to_currency = ttk.Combobox(currency_frame, values=list(currency_rates.keys()), font="Arial 12", width=10, state="readonly")
to_currency.set("USD")
to_currency.grid(row=1, column=1, padx=5)

convert_btn = tk.Button(
    currency_frame, text="Convert", font="Arial 14 bold",
    bg="orange", fg="black", relief=tk.RAISED, command=convert_currency
)
convert_btn.grid(row=2, column=0, columnspan=2, pady=10, ipadx=20)

# ==== History Toggle Icon ====
history_icon_btn = tk.Button(root, text="🕘", font="Arial 18", bg="#111", fg="white", command=toggle_history)
history_icon_btn.pack(pady=5)

# ==== History Frame ====
history_visible = False  # Start with history hidden

history_frame = tk.Frame(root, bg="#222")

history_scrollbar = tk.Scrollbar(history_frame)
history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

history_list = tk.Listbox(
    history_frame, height=8, font="Arial 12", bg="#111", fg="white",
    yscrollcommand=history_scrollbar.set
)
history_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
history_scrollbar.config(command=history_list.yview)

# ==== Run Application ====
root.mainloop()
