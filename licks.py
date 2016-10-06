import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter

curDirPath =  os.path.dirname(os.path.realpath(__file__))
os.chdir(curDirPath)
print "Working directory is set to ", os.getcwd()
fileName = "8055_adlibtest_.csv"

CH = 0

lickData = pd.read_csv(fileName, sep= ' ', header= 0, error_bad_lines= False)
lickData = lickData[lickData.CH0 <= 255]
lickData = lickData[np.isfinite(lickData['TimeStamp']) & lickData['TimeStamp'] < lickData.TimeStamp.loc[-1:]]
lickData = lickData.reindex(np.arange(0, len(lickData.TimeStamp)))
#print(lickData.CH0)
#print(lickData.TimeStamp)
#plt.plot(lickData.index, lickData.CH0)
#plt.show()
print lickData.TimeStamp.tail(1)
print lickData.CH0[lickData.index] > lickData.CH0[lickData.index-1]
#for line in lickData.TimeStamp:
#    pass
