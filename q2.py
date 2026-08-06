import csv
import os

dataset = [
    {"Train Number": "T101", "Route": "Chennai-Bangalore", "Total Seats": 500, "Booked Seats": 450, "Waiting List": 30, "Ticket Fare": 600, "Cancellation Count": 20, "Distance": 350},
    {"Train Number": "T102", "Route": "Delhi-Mumbai", "Total Seats": 700, "Booked Seats": 680, "Waiting List": 60, "Ticket Fare": 1200, "Cancellation Count": 30, "Distance": 1400},
    {"Train Number": "T103", "Route": "Hyderabad-Chennai", "Total Seats": 400, "Booked Seats": 180, "Waiting List": 0, "Ticket Fare": 800, "Cancellation Count": 10, "Distance": 700},
    {"Train Number": "T104", "Route": "Kolkata-Patna", "Total Seats": 300, "Booked Seats": 290, "Waiting List": 40, "Ticket Fare": 500, "Cancellation Count": 15, "Distance": 600},
    {"Train Number": "T105", "Route": "Mumbai-Goa", "Total Seats": 450, "Booked Seats": 180, "Waiting List": 5, "Ticket Fare": 900, "Cancellation Count": 5, "Distance": 590}
]
REPORT_FILE = "reservation_report.csv"
def main():
    print("=" * 65)
    print("SMART RAILWAY RESERVATION AND REVENUE OPTIMIZATION SYSTEM")
    print("=" * 65)
    # 1. Occupancy Ratio
    print("\n1. OCCUPANCY RATIO")
    for train in dataset:
        train["Occupancy Ratio"] = round(
            (train["Booked Seats"] / train["Total Seats"]) * 100, 2)
        print(f"{train['Train Number']} ({train['Route']}): {train['Occupancy Ratio']}%")
    # 2. Actual Revenue
    print("\n2. ACTUAL REVENUE AFTER CANCELLATIONS")
    for train in dataset:
        actual_passengers = train["Booked Seats"] - train["Cancellation Count"]
        train["Revenue"] = actual_passengers * train["Ticket Fare"]
        print(f"{train['Train Number']}: Rs.{train['Revenue']}")
    # 3. High Demand / Overbooked Trains
    print("\n3. HIGH DEMAND / OVERBOOKED TRAINS")
    found = False
    for train in dataset:
        if train["Waiting List"] > 20 or train["Booked Seats"] > train["Total Seats"]:
            print(f"{train['Train Number']} - {train['Route']}")
            found = True
    if not found:
        print("No high demand trains.")
    # 4. Revenue per Kilometer
    print("\n4. REVENUE PER KILOMETER")
    for train in dataset:
        train["Revenue per KM"] = round(
            train["Revenue"] / train["Distance"], 2)
        print(f"{train['Train Number']}: Rs.{train['Revenue per KM']} per km")
    # 5. Route with Maximum Revenue
    print("\n5. ROUTE WITH MAXIMUM REVENUE")
    highest = max(dataset, key=lambda x: x["Revenue"])
    print(f"{highest['Route']} -> Rs.{highest['Revenue']}")
    # 6. Occupancy Below 50%
    print("\n6. TRAINS WITH OCCUPANCY BELOW 50%")
    low = False
    for train in dataset:
        if train["Occupancy Ratio"] < 50:
            print(f"{train['Train Number']} - {train['Route']}")
            low = True
    if not low:
        print("No trains below 50% occupancy.")
    # 7. Sort by Revenue
    print("\n7. TRAINS SORTED BY REVENUE")
    sorted_trains = sorted(dataset,
                           key=lambda x: x["Revenue"],
                           reverse=True)
    for i, train in enumerate(sorted_trains, 1):
        print(f"{i}. {train['Train Number']} - Rs.{train['Revenue']}")
    # 8. Reservation Analytics Report
    print("\n8. RESERVATION ANALYTICS REPORT")
    headers = [
        "Train Number",
        "Route",
        "Occupancy Ratio",
        "Revenue",
        "Revenue per KM"
    ]
    with open(REPORT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for train in sorted_trains:
            writer.writerow({
                "Train Number": train["Train Number"],
                "Route": train["Route"],
                "Occupancy Ratio": train["Occupancy Ratio"],
                "Revenue": train["Revenue"],
                "Revenue per KM": train["Revenue per KM"]
            })
    print(f"Report saved as '{REPORT_FILE}'")
    # 9. Read Report
    print("\n9. READING REPORT")
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(row)
    else:
        print("Report file not found.")
    # 10. Top Three Revenue Trains
    print("\n10. TOP THREE REVENUE GENERATING TRAINS")
    with open(REPORT_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for i, row in enumerate(rows[:3], 1):
            print(f"{i}. {row['Train Number']} | {row['Route']} | Revenue: Rs.{row['Revenue']}")


if __name__ == "__main__":
    main()
