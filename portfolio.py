import csv
import os
from datetime import datetime

PORTFOLIO_FILE = "portfolio_summary.csv"

# Dictionary to store portfolio positions
portfolio = {}

print("=" * 45)
print("       INVESTMENT PORTFOLIO TRACKER")
print("=" * 45)

while True:
    ticker = input("\nEnter stock ticker (or 'done' to finish): ").strip().upper()

    if ticker == "DONE":
        break

    if not ticker:
        print("Ticker cannot be empty.")
        continue

    if ticker in portfolio:
        print("Ticker already exists. Enter each ticker only once.")
        continue

    try:
        buy_price = float(input("Enter buy price per share: "))
        quantity = int(input("Enter number of shares: "))
        current_price = float(input("Enter current price per share: "))

        if buy_price <= 0 or current_price < 0 or quantity <= 0:
            print("Buy price and quantity must be positive; current price cannot be negative.")
            continue

        portfolio[ticker] = {
            "buy_price": buy_price,
            "quantity": quantity,
            "current_price": current_price,
        }

    except ValueError:
        print("Invalid input. Please enter numeric values.")

if not portfolio:
    print("\nNo stocks were entered. Exiting program.")
    raise SystemExit

total_invested = 0.0
total_market_value = 0.0
rows_to_save = []

print("\n" + "=" * 91)
print("PORTFOLIO SUMMARY")
print("=" * 91)
print(
    f"{'Ticker':<10}{'Buy Price':>12}{'Quantity':>10}"
    f"{'Current Price':>15}{'Invested':>14}{'Market Value':>16}"
    f"{'Gain/Loss %':>14}"
)
print("-" * 91)

for ticker, stock in portfolio.items():
    buy_price = stock["buy_price"]
    quantity = stock["quantity"]
    current_price = stock["current_price"]

    invested = buy_price * quantity
    market_value = current_price * quantity
    gain_loss = market_value - invested
    percentage = (gain_loss / invested) * 100

    total_invested += invested
    total_market_value += market_value

    print(
        f"{ticker:<10}{buy_price:>12.2f}{quantity:>10}"
        f"{current_price:>15.2f}{invested:>14.2f}"
        f"{market_value:>16.2f}{percentage:>13.2f}%"
    )

    rows_to_save.append([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ticker,
        buy_price,
        quantity,
        current_price,
        invested,
        market_value,
        gain_loss,
        percentage,
    ])

total_gain_loss = total_market_value - total_invested
total_percentage = (total_gain_loss / total_invested) * 100

print("-" * 91)
print(f"Total invested capital: ${total_invested:.2f}")
print(f"Current market value:   ${total_market_value:.2f}")
print(f"Total gain/loss:        ${total_gain_loss:.2f}")
print(f"Overall return:          {total_percentage:.2f}%")

# Append each run's holdings to the CSV file, adding the header only once.
file_exists = os.path.exists(PORTFOLIO_FILE) and os.path.getsize(PORTFOLIO_FILE) > 0

with open(PORTFOLIO_FILE, "a", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)

    if not file_exists:
        writer.writerow([
            "Date", "Ticker", "Buy Price", "Quantity", "Current Price",
            "Invested Capital", "Market Value", "Gain/Loss", "Gain/Loss %",
        ])

    writer.writerows(rows_to_save)

print(f"\nSaved portfolio details to: {PORTFOLIO_FILE}")
print("Note: Current prices are entered manually; they are not live market quotes.")
