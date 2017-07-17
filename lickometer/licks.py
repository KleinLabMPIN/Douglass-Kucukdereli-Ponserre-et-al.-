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

def getLicks(fileName, CH, th_low, th_high, save= False):
    '''
    Parameters
    ----------
        fileName, CH, th_low, th_high
    Other Parameters
    ----------------
        save= False
    Return
    ------
        lickDigi, lickTimes
    '''

    lickData = pd.DataFrame({'CH0' : np.genfromtxt(fileName, delimiter = ' ', skip_header= 1, usecols= CH)})
    lickData.CH0[lickData.CH0 > 255] = np.nan

    # create the time axis
    lickData['Time'] = np.arange(0, len(lickData.CH0))*2

    # digitize the data
    lickData['Digi'] = np.zeros(len(lickData.CH0))
    lickData.Digi[lickData.CH0 < 240] = 0.0
    lickData.Digi[lickData.CH0 >= 240] = 1.0

    # find the lick start and end
    lickData['Start'] = pd.DataFrame(lickData.Time[lickData.Digi[lickData.index] > lickData.Digi[lickData.index-1]], index= lickData.index)
    lickData['End'] = pd.DataFrame(lickData.Time[lickData.Digi[lickData.index] > lickData.Digi[lickData.index+1]], index= lickData.index)

    # create the new frame with lick TimeStamp
    lickTimes = pd.DataFrame({'Start' : np.array(lickData.Start[np.isfinite(lickData['Start'])]), 'End' : np.array(lickData.End[np.isfinite(lickData['End'])])})
    lickTimes['Duration'] = lickTimes.End - lickTimes.Start
    lickTimes['Count'] = pd.DataFrame(np.zeros(len(lickTimes.Duration)))

    # filter for fast licks
    lickTimes = lickTimes[lickTimes.Duration > th_low]
    lickTimes.Count[lickTimes.Duration > th_low] = 1

    # extrapolate the long licks
    lickTimes.Count[lickTimes.Duration > th_high] = np.rint(lickTimes.Duration[lickTimes.Duration > th_high] / th_high)

    if(save):
        lickData.to_csv(fileName + "_.csv", sep= ',')
    else:
        pass

    you ='mustnt'
    if you == 'must':
        #plt.plot(lickData.Time, lickData.Digi)
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
        colors = ('#BCBEC0', '#0070C0')
        yVal = np.ones(len(lickTimes.Start))
        ax.plot((lickTimes.Start, lickTimes.End), (yVal, yVal), color= colors[0], linewidth= 15, solid_capstyle= 'butt')
        ax.set_ylim([0.9, 1.1])
        plt.show()

    return lickData, lickTimes


if __name__ == "__main__":

    if(os.path.dirname(os.path.realpath(__file__)) != os.getcwd()):
        curDirPath =  os.path.dirname(os.path.realpath(__file__))
        os.chdir(curDirPath)
        print "Working directory is set to ", os.getcwd()

    th_low= 12.0
    th_high= 140.0

    dirName = ('.\\data\\lickdata\NpHR\\', '.\\data\\lickdata\mCherry\\')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 6))
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

            count += 1
    ax.set_ylim([0, count])
    ax.set_yticks(np.arange(1, count, 4))
    ax.set_ylabel('NpHR         mCherry')
    ax.set_xlim([0, 900000])
    ax.set_xticks(np.arange(1, 900000, 900000/10))
    ax.set_xlabel('Time (sec)')

    plt.show()

        #print(lickTimes[550:600])

        #lickDigi.to_csv("data\lickdata.csv", sep= ',')
        #print(max(lickTimes.Duration))
        #lickTimes.Duration[lickTimes.Duration < th_high].hist(bins= max(lickTimes.Duration)/10)
        #lickTimes.Start[lickTimes.Duration < th_high].hist(bins= 100)
        #plt.show()
