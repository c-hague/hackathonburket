import json
import pandas as pd
import matplotlib.pyplot as plt
import config
import os

files = os.listdir('tmp/')

for file in files:
    if not file.startswith('trial'):
        continue

    with open('tmp/' + file) as f:
        data = json.load(f)

        topics = {}
        for item in data:
            if item['topic'] not in topics.keys():
                topics[item['topic']] = []
            topics[item['topic']].append(item)
        volume = pd.DataFrame(topics[config.SUB_VOLUME])
        plt.plot(volume['time'] - volume['time'].min(), volume['volume'])
        mass = pd.DataFrame(topics[config.SUB_MASS])
        plt.plot(mass['time'] - mass['time'].min(), mass['mass'] - mass['mass'].min())
        if mass['mass'][mass.shape[0] - 1] - mass['mass'][0] > 0:
            plt.savefig('tmp/plot_{0}.png'.format(file[:-5]))
        plt.clf()
