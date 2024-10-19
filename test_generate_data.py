import random
import csv

def generator_data(count):
    data = []
    for _ in range(count):
        row = ["metal-HUD: " + str(random.randint(150, 200)), 0, round(random.uniform(150, 200), 2)]
        for _ in range(162):
            row.append(round(random.uniform(100, 120), 2))
        data.append(row)
    
    with open('output2.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

    # print(data)

generator_data(1)
print("완료!")
