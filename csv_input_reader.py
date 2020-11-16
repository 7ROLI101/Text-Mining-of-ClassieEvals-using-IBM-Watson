import csv
import os

valuable = []
needs_improvement = []

with os.scandir('./Sample_Class_CSV_Files') as it:
    for entry in it:
        print(entry.name)
    file = input("Select a file you want to use: ")

with open('./Sample_Class_CSV_Files/' + file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["TYPE"] == "Valuable":
            valuable.append(row["COMMENT"])
        elif row["TYPE"] == "Needs Improvement":
            needs_improvement.append(row["COMMENT"])

for i in valuable:
    print(i)
    print("\n")

print("\n")

for j in needs_improvement:
    print(j)
    print("\n")
print("\n")
