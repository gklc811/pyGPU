import pandas as pd
import numpy as np
from itertools import permutations, repeat
import matplotlib.pyplot as plt
import mpld3
import json
from jinja2 import Environment, FileSystemLoader
import os
from multiprocessing import Pool, cpu_count

root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'templates')
env = Environment(loader=FileSystemLoader(templates_dir))
template = env.get_template('index.html')

pd.set_option('display.max_columns', 500)

df = pd.read_csv('../data/desktop_stats.csv')
df['period'] = df['Date'].astype(str) + " " + df['Time'].astype(str)

# Get columns and rename
x = df.columns.values
nd = df
for i in x:
    nd = nd.rename(columns={i: i.replace(" ", "_").replace("#", "")})

# choose certain columns
nd = nd[['period', 'Total_CPU_Usage_[%]', 'CPU_Package_[°C].1', 'CPU_Package_Power_[W]', 'System1_[°C]', 'PCH_[°C]',
         'PCIEX16_[°C]', 'VRM_MOS_[°C]', 'EC_TEMP1/System2_[°C]', 'CPU_[RPM]', 'System_1_[RPM]',
         'System_2_(VRM)_[RPM]', 'System_3_[RPM]', 'Drive_Temperature_[°C]', 'GPU_Temperature_[°C]', 'GPU_Fan_[RPM]',
         'GPU_Power_[W]', 'GPU_D3D_Usage_[%]']]

# nd = nd[['period', 'Total_CPU_Usage_[%]', 'CPU_Package_[°C].1', 'CPU_Package_Power_[W]']]

# get the permutation of two column
perm = permutations(np.delete(nd.columns.values, 0), 2)
combination_dict = {}
for i in list(perm):
    ar = list(i)
    ar = sorted(ar)
    combination_dict[ar[0] + "_" + ar[1]] = ar


def plotfig(key, combination_dict, nd):
    jsdict = {}
    fig, ax = plt.subplots()
    cor = nd[combination_dict[key][0]].corr(nd[combination_dict[key][1]])
    nd.plot(x="period", y=combination_dict[key], kind="line", title="correlation factor : " + str(cor), ax=ax, fig=fig)
    jsdict[list(combination_dict.keys()).index(key)] = json.dumps(mpld3.fig_to_dict(fig), skipkeys=True)
    plt.close(fig)
    return jsdict


if __name__ == '__main__':
    print("Main called")
    processes = cpu_count()
    print(processes)
    pool = Pool(processes)
    # find the correlation - plot

    test = pool.starmap_async(plotfig,
                              zip(list(combination_dict.keys()), repeat(combination_dict), repeat(nd)))
    jsdict = {}
    pool.close()
    pool.join()
    if (test.ready()):
        for x in test.get():
            jsdict.update(x)
    names = []
    values = []

    for key in jsdict:
        names.append(key)
        values.append(jsdict[key])

    parent_dict = [jsdict]

    filename = os.path.join(root, 'html', 'index.html')
    with open(filename, 'w') as fh:
        fh.write(template.render(
            h1="Hello Jinja2",
            show_one=True,
            show_two=False,
            parent_dict=parent_dict
        ))
