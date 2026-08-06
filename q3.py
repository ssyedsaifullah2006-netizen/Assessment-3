import csv
import os
dataset = [
    {"Investor ID": "INV001", "Stock Symbol": "TCS", "Quantity": 100, "Buy Price": 3200, "Current Price": 3650, "Sector": "IT", "Dividend Received": 5000},
    {"Investor ID": "INV002", "Stock Symbol": "INFY", "Quantity": 150, "Buy Price": 1400, "Current Price": 1550, "Sector": "IT", "Dividend Received": 3000},
    {"Investor ID": "INV003", "Stock Symbol": "HDFCBANK", "Quantity": 200, "Buy Price": 1500, "Current Price": 1450, "Sector": "Banking", "Dividend Received": 4000},
    {"Investor ID": "INV001", "Stock Symbol": "RELIANCE", "Quantity": 80, "Buy Price": 2400, "Current Price": 2700, "Sector": "Energy", "Dividend Received": 2500},
    {"Investor ID": "INV004", "Stock Symbol": "SUNPHARMA", "Quantity": 120, "Buy Price": 900, "Current Price": 980, "Sector": "Healthcare", "Dividend Received": 1500},
    {"Investor ID": "INV005", "Stock Symbol": "SBIN", "Quantity": 250, "Buy Price": 620, "Current Price": 700, "Sector": "Banking", "Dividend Received": 3500}
]
REPORT_FILE = "portfolio_report.csv"
def main():
    print("=" * 65)
    print("SMART STOCK PORTFOLIO AND RISK MANAGEMENT SYSTEM")
    print("=" * 65)
    # 1. Investment Value
    print("\n1. INVESTMENT VALUE")
    for stock in dataset:
        stock["Investment Value"] = stock["Quantity"] * stock["Buy Price"]
        print(f"{stock['Stock Symbol']} : Rs.{stock['Investment Value']}")
    # 2. Current Value
    print("\n2. CURRENT VALUE")
    for stock in dataset:
        stock["Current Value"] = stock["Quantity"] * stock["Current Price"]
        print(f"{stock['Stock Symbol']} : Rs.{stock['Current Value']}")
    # 3. Profit / Loss
    print("\n3. PROFIT / LOSS")
    for stock in dataset:
        stock["Profit"] = (stock["Current Value"] -
                           stock["Investment Value"] +
                           stock["Dividend Received"])
        print(f"{stock['Stock Symbol']} : Rs.{stock['Profit']}")
    # 4. Percentage Return
    print("\n4. PERCENTAGE RETURN")
    for stock in dataset:
        stock["Return %"] = round(
            (stock["Profit"] / stock["Investment Value"]) * 100, 2)
        print(f"{stock['Stock Symbol']} : {stock['Return %']}%")
    # 5. Best Performing Stock
    print("\n5. BEST PERFORMING STOCK")
    best = max(dataset, key=lambda x: x["Return %"])
    print(f"{best['Stock Symbol']} : {best['Return %']}%")
    # 6. Worst Performing Stock
    print("\n6. WORST PERFORMING STOCK")
    worst = min(dataset, key=lambda x: x["Return %"])
    print(f"{worst['Stock Symbol']} : {worst['Return %']}%")
    # 7. Sector-wise Exposure
    print("\n7. SECTOR-WISE EXPOSURE")
    sector_exposure = {}
    for stock in dataset:
        sector = stock["Sector"]
        sector_exposure[sector] = sector_exposure.get(
            sector, 0) + stock["Current Value"]
    for sector, value in sector_exposure.items():
        print(f"{sector} : Rs.{value}")
    # 8. Rank Investors by Portfolio Return
    print("\n8. INVESTOR RANKING")
    investor_returns = {}
    for stock in dataset:
        investor = stock["Investor ID"]
        investor_returns[investor] = investor_returns.get(
            investor, 0) + stock["Profit"]
    ranking = sorted(investor_returns.items(),
                     key=lambda x: x[1],
                     reverse=True)
    for i, investor in enumerate(ranking, 1):
        print(f"{i}. {investor[0]} : Rs.{investor[1]}")
    # 9. Generate Portfolio Report
    print("\n9. GENERATING PORTFOLIO REPORT")
    headers = [
        "Investor ID",
        "Stock Symbol",
        "Sector",
        "Investment Value",
        "Current Value",
        "Profit",
        "Return %"
    ]
    with open(REPORT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for stock in dataset:
            writer.writerow({
                "Investor ID": stock["Investor ID"],
                "Stock Symbol": stock["Stock Symbol"],
                "Sector": stock["Sector"],
                "Investment Value": stock["Investment Value"],
                "Current Value": stock["Current Value"],
                "Profit": stock["Profit"],
                "Return %": stock["Return %"]
            })
    print(f"Report saved as '{REPORT_FILE}'")
    # 10. Read Report
    print("\n10. READING PORTFOLIO REPORT")
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(row)
    else:
        print("Report file not found.")

if __name__ == "__main__":
    main()
