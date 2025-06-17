import csv

try:
    with open("log.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Time", "Event"])
    print("log.csv created with headers.")
except PermissionError:
    print("Permission error: Close the file if it's open in another app.")
