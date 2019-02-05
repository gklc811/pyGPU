import pandas as pd
import numpy as np
from itertools import permutations
import matplotlib.pyplot as plt
from mpld3._server import serve
import mpld3

pd.set_option('display.max_columns', 500)

df = pd.read_csv('./data/desktop_stats.csv')
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
print(nd.head())

# get the permutation of two column
perm = permutations(np.delete(nd.columns.values, 0), 2)
for i in list(perm):
    print(i)

# find the correlation - plot

nd.plot(x="period", y=['System1_[°C]', 'Total_CPU_Usage_[%]'], kind="bar")

# firstgraph
x = [1, 2, 3]
y = [2, 3, 4]
fig1 = plt.figure()
plt.xlabel("xlabel 1")
plt.ylabel("ylabel 1")
plt.title("Plot 1")
plt.legend()
plt.bar(x, y, label='label for bar', color='b')

# secondgraph
x = [1, 2, 3]
y = [5, 3, 1]
fig2 = plt.figure()
plt.xlabel("xlabel 2")
plt.ylabel("ylabel 2")
plt.title("Plot 2")
plt.bar(x, y, color='r')

# create html for both graphs
html1 = mpld3.fig_to_html(fig1)
html2 = mpld3.fig_to_html(fig2)
# serve joined html to browser
serve(html1 + html2)
# render a html/PDF  report
