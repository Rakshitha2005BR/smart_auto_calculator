import math
import re

# === SAFE SCIENTIFIC FUNCTIONS ===
safe_functions = {
    'sin': lambda x: math.sin(math.radians(x)),  # angle in degrees
    'cos': lambda x: math.cos(math.radians(x)),
    'tan': lambda x: math.tan(math.radians(x)),
    'log': math.log10,
    'ln': math.log,
    'sqrt': math.sqrt,
    'pow': math.pow,
    'pi': math.pi,
    'e': math.e,
    '__builtins__': {}
}

# === STATIC CURRENCY RATES (1 INR = base) ===
currency_rates = {
    "USD": 83.0,
    "EUR": 90.5,
    "GBP": 105.3,
    "INR": 1.0
}

# === DETECT SCIENTIFIC EXPRESSIONS ===
def is_scientific_expression(expr):
    sci_keywords = ['sin', 'cos', 'tan', 'log', 'ln', 'sqrt', 'pi', 'e', 'pow', '^']
    return any(key in expr.lower() for key in sci_keywords)

# === DETECT CURRENCY EXPRESSIONS ===
def is_currency_expression(expr):
    pattern = r'^\s*(\d+(?:\.\d+)?)\s+([A-Za-z]{3})\s+to\s+([A-Za-z]{3})\s*$'
    return re.match(pattern, expr.strip(), re.IGNORECASE)

# === CURRENCY CONVERSION ===
def convert_currency(expr):
    match = is_currency_expression(expr)
    if not match:
        return "❌ Invalid format. Use like: 100 USD to INR"

    amount = float(match.group(1))
    from_curr = match.group(2).upper()
    to_curr = match.group(3).upper()

    if from_curr not in currency_rates or to_curr not in currency_rates:
        return f"❌ Unsupported currency: {from_curr} or {to_curr}"

    in_inr = amount * currency_rates[from_curr]
    converted = in_inr / currency_rates[to_curr]

    return round(converted, 2)

# === EVALUATE NORMAL OR SCIENTIFIC EXPRESSION ===
def evaluate_expression(expr):
    try:
        expr = expr.replace('^', '**')  # replace ^ with Python power
        if is_scientific_expression(expr):
            print("🔬 Scientific Mode (auto)")
            result = eval(expr, {"__builtins__": None}, safe_functions)
        else:
            print("🧮 Normal Mode (default)")
            result = eval(expr, {"__builtins__": None}, {})
        return round(result, 5)
    except Exception as e:
        return f"❌ Error: {e}"

# === MAIN CALCULATOR LOOP ===
def run_calculator():
    print("=== Smart Auto Calculator ===")
    print("Supports: Normal | Scientific | Currency Conversion")
    print("Examples:")
    print("  ➤ 12 + 5")
    print("  ➤ sin(30), log(1000), sqrt(64)")
    print("  ➤ 100 USD to INR\n")
    print("Type 'exit' to quit.\n")

    while True:
        expr = input("Enter expression: ").strip()

        if expr.lower() == 'exit':
            print("👋 Goodbye!")
            break

        if not expr:
            continue

        if is_currency_expression(expr):
            print("💱 Currency Conversion Mode")
            result = convert_currency(expr)
        else:
            result = evaluate_expression(expr)

        print(f"Result: {result}\n")

# === RUN ===
if __name__ == "__main__":
    run_calculator()
