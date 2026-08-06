import csv
import os
dataset = [
    # Month 1 Records
    {"Product ID": "P001", "Product Name": "Wireless Mouse", "Category": "Electronics", "Opening Stock": 120, "Units Sold": 80, "Units Returned": 5, "Supplier Lead Time": 3, "Unit Cost": 10.0, "Selling Price": 25.0},
    {"Product ID": "P002", "Product Name": "Gaming Keyboard", "Category": "Electronics", "Opening Stock": 90, "Units Sold": 60, "Units Returned": 2, "Supplier Lead Time": 5, "Unit Cost": 20.0, "Selling Price": 55.0},
    {"Product ID": "P003", "Product Name": "Office Chair", "Category": "Furniture", "Opening Stock": 40, "Units Sold": 15, "Units Returned": 1, "Supplier Lead Time": 7, "Unit Cost": 45.0, "Selling Price": 110.0},
    # Month 2 Records
    {"Product ID": "P001", "Product Name": "Wireless Mouse", "Category": "Electronics", "Opening Stock": 110, "Units Sold": 85, "Units Returned": 3, "Supplier Lead Time": 3, "Unit Cost": 10.0, "Selling Price": 25.0},
    {"Product ID": "P002", "Product Name": "Gaming Keyboard", "Category": "Electronics", "Opening Stock": 85, "Units Sold": 65, "Units Returned": 4, "Supplier Lead Time": 5, "Unit Cost": 20.0, "Selling Price": 55.0},
    {"Product ID": "P003", "Product Name": "Office Chair", "Category": "Furniture", "Opening Stock": 38, "Units Sold": 18, "Units Returned": 0, "Supplier Lead Time": 7, "Unit Cost": 45.0, "Selling Price": 110.0},
    # Month 3 Records (Current Active Inventory State)
    {"Product ID": "P001", "Product Name": "Wireless Mouse", "Category": "Electronics", "Opening Stock": 100, "Units Sold": 90, "Units Returned": 4, "Supplier Lead Time": 3, "Unit Cost": 10.0, "Selling Price": 25.0},
    {"Product ID": "P002", "Product Name": "Gaming Keyboard", "Category": "Electronics", "Opening Stock": 80, "Units Sold": 70, "Units Returned": 1, "Supplier Lead Time": 5, "Unit Cost": 20.0, "Selling Price": 55.0},
    {"Product ID": "P003", "Product Name": "Office Chair", "Category": "Furniture", "Opening Stock": 35, "Units Sold": 22, "Units Returned": 2, "Supplier Lead Time": 7, "Unit Cost": 45.0, "Selling Price": 110.0},
    {"Product ID": "P004", "Product Name": "Leather Backpack", "Category": "Apparel", "Opening Stock": 60, "Units Sold": 55, "Units Returned": 5, "Supplier Lead Time": 4, "Unit Cost": 15.0, "Selling Price": 40.0},
    {"Product ID": "P005", "Product Name": "Desk Lamp", "Category": "Furniture", "Opening Stock": 15, "Units Sold": 14, "Units Returned": 0, "Supplier Lead Time": 10, "Unit Cost": 8.0, "Selling Price": 22.0}
]
CSV_FILE = "inventory_report.csv"
def main():
    # Process historical data for Moving Average calculation
    historical_sales = {}
    for row in dataset:
        pid = row["Product ID"]
        historical_sales.setdefault(pid, []).append(row["Units Sold"])

    # Extract the most recent unique records as our current active inventory state
    current_inventory = {}
    for row in dataset:
        current_inventory[row["Product ID"]] = row.copy()

    print("=" * 60)
    print("        SMART RETAIL INVENTORY MANAGEMENT SYSTEM        ")
    print("=" * 60)
    # 1. Calculate current stock
    print("\n1. CURRENT STOCK CALCULATION")
    for p in current_inventory.values():
        p["Current Stock"] = p["Opening Stock"] - p["Units Sold"] + p["Units Returned"]
        print(f"- {p['Product Name']} ({p['Product ID']}): {p['Current Stock']} units")

    # 2. Calculate profit for each product
    print("\n2. PROFIT PER PRODUCT")
    for p in current_inventory.values():
        net_units_sold = p["Units Sold"] - p["Units Returned"]
        p["Profit"] = net_units_sold * (p["Selling Price"] - p["Unit Cost"])
        print(f"- {p['Product Name']}: ${p['Profit']:.2f}")

    # 3. Identify products requiring immediate reorder
    print("\n3. PRODUCTS REQUIRING IMMEDIATE REORDER")
    for p in current_inventory.values():
        # Reorder threshold logic based on safety buffer and lead time demand
        lead_time_demand = (p["Units Sold"] / 30.0) * p["Supplier Lead Time"]
        if p["Current Stock"] <= lead_time_demand + 5:  # buffer added for safety
            print(f"⚠ ALERT: {p['Product Name']} needs reorder! Current Stock: {p['Current Stock']}")

    # 4. Compute inventory turnover ratio
    print("\n4. INVENTORY TURNOVER RATIO")
    for p in current_inventory.values():
        net_units_sold = p["Units Sold"] - p["Units Returned"]
        cogs = net_units_sold * p["Unit Cost"]
        avg_inventory = (p["Opening Stock"] + p["Current Stock"]) / 2
        turnover_ratio = round(cogs / avg_inventory, 2) if avg_inventory > 0 else 0.0
        print(f"- {p['Product Name']}: {turnover_ratio}")

    # 5. Find the highest profit product
    print("\n5. HIGHEST PROFIT PRODUCT")
    highest_profit_p = max(current_inventory.values(), key=lambda x: x["Profit"])
    print(f" {highest_profit_p['Product Name']} with a total profit of ${highest_profit_p['Profit']:.2f}")
    # 6. Calculate category-wise profit
    print("\n6. CATEGORY-WISE PROFIT")
    category_profits = {}
    for p in current_inventory.values():
        cat = p["Category"]
        category_profits[cat] = category_profits.get(cat, 0.0) + p["Profit"]
    for cat, total_profit in category_profits.items():
        print(f"- {cat}: ${total_profit:.2f}")
    # 7. Predict next month demand using moving average logic
    print("\n7. NEXT MONTH DEMAND PREDICTION (MOVING AVERAGE)")
    for pid, p in current_inventory.items():
        sales_history = historical_sales[pid]
        moving_avg = round(sum(sales_history) / len(sales_history), 1)
        print(f"- {p['Product Name']}: Predicted Demand = {moving_avg} units")
    # 8. Sort products by profitability
    print("\n8. PRODUCTS SORTED BY PROFITABILITY")
    sorted_list = sorted(current_inventory.values(), key=lambda x: x["Profit"], reverse=True)
    for idx, p in enumerate(sorted_list, 1):
        print(f" {idx}. {p['Product Name']} (${p['Profit']:.2f})")
    # 9. Export inventory report to CSV
    print("\n9. EXPORTING INVENTORY REPORT TO CSV")
    csv_headers = [
        "Product ID", "Product Name", "Category", "Opening Stock", 
        "Units Sold", "Units Returned", "Supplier Lead Time", 
        "Unit Cost", "Selling Price", "Current Stock", "Profit"
    ]
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()
        for p in sorted_list:
            writer.writerow({k: p[k] for k in csv_headers})
    print(f"[✔] Report saved successfully as '{CSV_FILE}'")
    # 10. Read the CSV and display the top five profitable products
    print("\n10. READING CSV & DISPLAYING TOP 5 PROFITABLE PRODUCTS")
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            csv_rows = list(reader)
            for i, row in enumerate(csv_rows[:5], 1):
                print(f" Rank {i}: {row['Product Name']} | Category: {row['Category']} | Profit: ${float(row['Profit']):.2f}")
    else:
        print("CSV File missing.")

if __name__ == "__main__":
    main()
