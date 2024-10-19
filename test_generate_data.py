import random
import csv

def generator_data(count):
    data = []
    for _ in range(count):
        row = ["metal-HUD: " + str(random.randint(100000, 3000000)), 0, round(random.uniform(10000, 30000), 2)]
        for _ in range(162):
            row.append(round(random.uniform(40, 1400), 2))
        data.append(row)
    
    with open('output1.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

    # print(data)

generator_data(10000)
print("완료!")
