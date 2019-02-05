import pandas as pd
import numpy as np
from itertools import permutations
import matplotlib.pyplot as plt
from mpld3._server import serve
import mpld3
import json
from jinja2 import Environment, FileSystemLoader
import os

root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'templates')
env = Environment(loader=FileSystemLoader(templates_dir))
template = env.get_template('index.html')

pd.set_option('display.max_columns', 500)

df = pd.read_csv('../data/desktop_stats.csv')
df['period'] = df['Date'].astype(str) + " " + df['Time'].astype(str)

print(df.head())

# Get columns and rename
x = df.columns.values
nd = df
for i in x:
    nd = nd.rename(columns={i: i.replace(" ", "_").replace("#", "")})
print(nd.head())

# choose certain columns
nd = nd[['period', 'Total_CPU_Usage_[%]', 'CPU_Package_[°C].1', 'CPU_Package_Power_[W]', 'System1_[°C]', 'PCH_[°C]',
         'PCIEX16_[°C]', 'VRM_MOS_[°C]', 'EC_TEMP1/System2_[°C]', 'CPU_[RPM]', 'System_1_[RPM]', 'System_2_(VRM)_[RPM]',
         'System_2_(VRM)_[RPM]', 'System_3_[RPM]', 'Drive_Temperature_[°C]', 'GPU_Temperature_[°C]', 'GPU_Fan_[RPM]',
         'GPU_Power_[W]', 'GPU_D3D_Usage_[%]']]

# nd = nd[['period', 'Total_CPU_Usage_[%]', 'CPU_Package_[°C].1', 'CPU_Package_Power_[W]']]
print(nd.head())

# get the permutation of two column
perm = permutations(np.delete(nd.columns.values, 0), 2)
combination_dict = {}
for i in list(perm):
    ar = list(i)
    ar = sorted(ar)
    combination_dict[ar[0] + "_" + ar[1]] = ar

jsdict = {}
# find the correlation - plot
for key in combination_dict:
    print(combination_dict[key])
    fig, ax = plt.subplots()
    nd.plot(x="period", y=combination_dict[key], kind="line", ax=ax, fig=fig)
    jsdict[list(combination_dict.keys()).index(key)] = json.dumps(mpld3.fig_to_dict(fig), skipkeys=True)
    plt.close(fig)

names = []
values = []
for key in jsdict:
    print(jsdict[key])
    names.append(key)
    values.append(jsdict[key])

parent_dict = [jsdict]
print(parent_dict)

filename = os.path.join(root, 'html', 'index.html')
with open(filename, 'w') as fh:
    fh.write(template.render(
        h1="Hello Jinja2",
        show_one=True,
        show_two=False,
        parent_dict=parent_dict
    ))
