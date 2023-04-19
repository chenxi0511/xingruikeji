import csv

# 从csv文件中读取数据并存储为一个列表
data = []
with open('fyx_chinamoney.csv', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        data.append(row)

# 将列表拆分为多个批次并输出
batch_size = 80
num_batches = (len(data) + batch_size - 1) // batch_size  # 向上取整
for i in range(num_batches):
    batch_data = data[i*batch_size : (i+1)*batch_size]
    print(f'Batch {i+1}:')
    for row in batch_data:
        print(row)
    print('\n')
