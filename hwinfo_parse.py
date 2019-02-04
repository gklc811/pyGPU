import pandas as pd
import seaborn as sns
import numpy as np

pd.set_option('display.max_columns', 500)

df = pd.read_csv('./data/desktop_stats.csv')

print(df.head())

# Get columns
# choose certain columns
# get the first two column
# find the correlation - plot
# render a html/PDF  report
