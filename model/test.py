import csv  

f_data = 0
t_data = 0

with open(file= "./training_dataset/True.csv", mode= "r") as file:
    csv_file = csv.reader(file)
    for row in csv_file:
        t_data += 1

with open(file= "./training_dataset/Fake.csv", mode= "r") as file:
    csv_file = csv.reader(file)
    for row in csv_file:
        f_data += 1

print(t_data, f_data)
