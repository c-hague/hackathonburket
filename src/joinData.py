import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

with open('src/data.json') as f:
    data = json.load(f)

newData = []
for row in data:
    found = False
    for otherRow in newData:
        if abs(row['time'] - otherRow['time']) < .05:
            otherRow.update(row)
            found = True
            break
    if not found:
        newData.append(row)

df = pd.DataFrame(newData)
del df['topic']

df.to_csv('data.csv')

plt.plot(df['time'], df['flow'])
plt.figure()
plt.plot(df['time'], df['mass'])
plt.show()
