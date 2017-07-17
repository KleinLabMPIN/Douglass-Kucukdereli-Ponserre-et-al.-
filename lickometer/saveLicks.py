import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from licks import getLicks

## change the wd to dir containing the script
curpath = os.path.dirname(os.path.realpath(__file__))
os.chdir(curpath)

# load the data from csv
th_low= 8.0
th_high= 90.0

dirName = '.\\data\lickdata\\NpHR\\'
fileList = []
sumList = []
files = os.listdir(dirName)
for file in files:
    lickData, lickTimes = getLicks(dirName + file, CH = 0, th_low= th_low, th_high= th_high)
    fileList.append(file)
    sum = lickTimes.Count.sum()
    sumList.append(sum)
nphr = pd.DataFrame({'Animals' : fileList, 'Sum' : sumList})
print nphr

dirName = '.\\data\\lickdata\\mCherry\\'
fileList = []
sumList = []
files = os.listdir(dirName)
for file in files:
    lickData, lickTimes = getLicks(dirName + file, CH = 0, th_low= th_low, th_high= th_high)
    fileList.append(file)
    sum = lickTimes.Count.sum()
    sumList.append(sum)
mcherry = pd.DataFrame({'Animals' : fileList, 'Sum' : sumList})
print mcherry

data = pd.DataFrame({'mCherry_Animals' : mcherry.Animals, 'mCherry' : mcherry.Sum, 'NpHR_Animals' : nphr.Animals, 'NpHR' : nphr.Sum})
data.to_csv(".\\data\\lickdata\\fresubin_data.csv", sep= ',')
