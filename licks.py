"""
Description
-----------
    reads the lickometer files
    filters the noise
    counts the number of licks

Authors
-------
    amelia douglass
    hakan kucukdereli
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter

curDirPath =  os.path.dirname(os.path.realpath(__file__))
os.chdir(curDirPath)
print "Working directory is set to ", os.getcwd()
#fileName = "data\Kissykissylicklick\mCherry\\6910_test_adlib.csv"
fileName = "data\Kissykissylicklick\mCherry\\6862_test_adlib.csv"

def getLicks(fileName, CH, th_low, th_high, save= False):
    lickData = pd.read_csv(fileName, sep= ' ', header= 0, error_bad_lines= False)

    lickData = lickData[lickData.CH0 <= 255]
    lickData = lickData[lickData.CH0 > -1]
    lickData = lickData[np.isfinite(lickData['TimeStamp']) & lickData['TimeStamp'] < lickData.TimeStamp.loc[-1:]]
    #lickData = lickData.reindex(np.arange(0, len(lickData.TimeStamp)))
    lickData.index = np.arange(0, len(lickData.TimeStamp))

    #print(lickData.CH0)
    #print(lickData.TimeStamp)
    #plt.plot(lickData.index, lickData.CH0)
    #plt.show()

    lickDigi = pd.DataFrame(lickData)
    lickDigi.CH0[lickData.CH0 < 240] = 0.0
    lickDigi.CH0[lickData.CH0 >= 240] = 1.0

    #lickDigi['Event'] = pd.DataFrame(np.zeros(len(lickDigi.TimeStamp)), index= lickDigi.index)
    lickDigi['Start'] = pd.DataFrame(np.zeros(len(lickDigi.TimeStamp)), index= lickDigi.index)
    lickDigi['End'] = pd.DataFrame(np.zeros(len(lickDigi.TimeStamp)), index= lickDigi.index)
    lickDigi.Start = lickDigi.TimeStamp[lickDigi.CH0[lickDigi.index] > lickDigi.CH0[lickDigi.index-1]]
    lickDigi.End = lickDigi.TimeStamp[lickDigi.CH0[lickDigi.index] > lickDigi.CH0[lickDigi.index+1]]

    #lickTimes.Start = lickDigi.Start[np.isfinite(lickData['Start'])]
    #lickTimes.End = lickDigi.End[np.isfinite(lickData['End'])]

    lickStart = np.array(lickDigi.Start[np.isfinite(lickData['Start'])])
    lickEnd = np.array(lickDigi.End[np.isfinite(lickData['End'])])

    lickTimes = pd.DataFrame({'Start' : np.array(lickDigi.Start[np.isfinite(lickData['Start'])]), 'End' : np.array(lickDigi.End[np.isfinite(lickData['End'])])})
    lickTimes['Duration'] = lickTimes.End - lickTimes.Start

    # filter for fast licks
    lickTimes = lickTimes[lickTimes.Duration > th_low]

    if(save):
        lickDigi.to_csv(fileName + "_.csv", sep= ',')
    else:
        pass

    return lickDigi, lickTimes

th_low= 6.0
th_high= 200000.0

dirName = '.\data\Kissykissylicklick\NpHR\\'
files = os.listdir(dirName)
for file in files:
    lickDigi, lickTimes = getLicks(dirName+file, CH = 0, th_low= th_low, th_high= th_high)

    #lickDigi.to_csv("data\lickdata.csv", sep= ',')

    lickTimes.Duration[lickTimes.Duration < th_high].hist(bins= 100)
    #lickTimes.Start[lickTimes.Duration < threshold_high].hist(bins= 100)
    plt.show()
