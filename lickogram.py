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
from licks import getLicks

if __name__ == "__main__":

    if(os.path.dirname(os.path.realpath(__file__)) != os.getcwd()):
        curDirPath =  os.path.dirname(os.path.realpath(__file__))
        os.chdir(curDirPath)
        print "Working directory is set to ", os.getcwd()

    th_low= 12.0
    th_high= 140.0

    dirName = ('.\\data\\lickdata\NpHR\\', '.\\data\\lickdata\mCherry\\')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
    labelList = []
    count = 1
    for j in (0,1):
        files = os.listdir(dirName[j])
        for file in files:
            print(file)
            #lickDigi, lickTimes = getLicks(dirName + file, CH = 0, th_low= th_low, th_high= th_high)
            lickData, lickTimes = getLicks(dirName[j] + file, CH = 0, th_low= th_low, th_high= th_high)

            colors = ('#0070C0', '#BCBEC0')
            yVal = np.ones(len(lickTimes.Start))*count
            ax.plot((lickTimes.Start, lickTimes.End), (yVal, yVal), color= colors[j], linewidth= 20, solid_capstyle= 'butt')

            labelList.append(file)
            count += 1
    ax.set_ylim([0, count])
    ax.set_yticks(np.arange(1, count, 1))
    ax.set_yticklabels(labelList)
    ax.set_ylabel('NpHR         mCherry')
    ax.set_xlim([0, 900000])
    ax.set_xticks(np.arange(1, 900000, 900000/10))
    ax.set_xlabel('Time (sec)')

    plt.tight_layout()
    plt.show()

        #print(lickTimes[550:600])

        #lickDigi.to_csv("data\lickdata.csv", sep= ',')
        #print(max(lickTimes.Duration))
        #lickTimes.Duration[lickTimes.Duration < th_high].hist(bins= max(lickTimes.Duration)/10)
        #lickTimes.Start[lickTimes.Duration < th_high].hist(bins= 100)
        #plt.show()
