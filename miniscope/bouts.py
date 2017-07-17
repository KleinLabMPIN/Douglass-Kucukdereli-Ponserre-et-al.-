import pandas as pd
import numpy as np
from imagingIO import loopMice, loadData, getBeh
from events import find_nearest, getEvents
from statistics import getBoutMeans, getStats

def getBouts(mice, dataList, eventStart, eventEnd, baseEvent, base, behType, trials, baselining=False):
    """
        Use this one for fixed baseline length.
    """
    eventsData = pd.DataFrame()
    for mus, sess in mice:

        for i in range(trials[0], trials[1]+1):
            ind1, nearest1 = find_nearest(dataList[mus].index.values, eventStart[mus].loc[i])
            ind2, nearest2 = find_nearest(dataList[mus].index.values, eventEnd[mus].loc[i])
            ind3, nearest3 = find_nearest(dataList[mus].index.values, baseEvent[mus].loc[i])
            eventStart[mus].loc[i] = nearest1
            eventEnd[mus].loc[i] = nearest2
            baseEvent[mus].loc[i] = nearest3

        fs = dataList[mus].index[1] - dataList[mus].index[0]
        newTime = np.arange(base, 10000, fs)

        for col in dataList[mus].columns:
            if not col == 'Time (s)':
                data = dataList[mus][col]
                for j in range(trials[0], trials[1]+1):
                    startT = eventStart[mus].loc[j]
                    endT = eventEnd[mus].loc[j]
                    baseT = baseEvent[mus].loc[j]

                    slicedData = pd.DataFrame()

                    if baselining:
                        if base < 0:
                            basedFF = data.loc[baseT+base:baseT+0.0001].mean()
                        elif base > 0:
                            basedFF = data.loc[baseT:baseT+base+0.0001].mean()
                    elif not baselining:
                        basedFF = 0.0

                    if base < 0:
                        slicePre = data.loc[baseT+base:baseT].values - basedFF
                        slicePost = data.loc[startT:endT].values - basedFF
                        dataSlice = np.concatenate((slicePre, slicePost), axis=0)
                        slicedData['Fluoro'] = dataSlice
                        slicedData['New_Time'] = newTime[0:len(dataSlice)]
                        #slicedData['New_Time'] = np.linspace(base,((len(dataSlice)-1)*fs)+base,len(dataSlice))
                    elif base > 0:
                        dataSlice = data.loc[startT+base:endT+0.0001].values - basedFF
                        slicedData['Fluoro'] = dataSlice
                        slicedData['New_Time'] = np.linspace(base,((len(dataSlice)-1)*fs)+base,len(dataSlice))

                    slicedData['Cell'] = col
                    slicedData['Event'] = j
                    eventsData = eventsData.append(slicedData)

    print "\n", len(mice), " mice were loaded."

    if baselining:
        print "\nBaseline was set", base, "sec before the event."
    elif not baselining:
        print "\nTraces were not baselined."

    return eventsData

def getBouts_(mice, dataList, eventStart, eventEnd, baseEvent, base, behType, trials, baselining=False):
    """
        Use this one for varying baseline length.
    """
    eventsData = pd.DataFrame()
    for mus, sess in mice:

        for i in range(trials[0], trials[1]+1):
            ind1, nearest1 = find_nearest(dataList[mus].index.values, eventStart[mus].loc[i])
            ind2, nearest2 = find_nearest(dataList[mus].index.values, eventEnd[mus].loc[i])
            ind3, nearest3 = find_nearest(dataList[mus].index.values, baseEvent[mus].loc[i])
            ind4, nearest4 = find_nearest(-dataList[mus].index.values, base[mus].loc[i])
            eventStart[mus].loc[i] = nearest1
            eventEnd[mus].loc[i] = nearest2
            baseEvent[mus].loc[i] = nearest3
            base[mus].loc[i] = nearest4

        fs = dataList[mus].index[1] - dataList[mus].index[0]

        for col in dataList[mus].columns:
            if not col == 'Time (s)':
                data = dataList[mus][col]
                for j in range(trials[0], trials[1]+1):
                    startT = eventStart[mus].loc[j]
                    endT = eventEnd[mus].loc[j]
                    baseT = baseEvent[mus].loc[j]

                    slicedData = pd.DataFrame()
                    newTime = np.arange(base[mus].loc[j], 10000, fs)

                    if baselining:
                        if base[mus].loc[j] < 0:
                            basedFF = data.loc[baseT+base[mus].loc[j]:baseT+0.0001].mean()
                        elif base[mus].loc[j] > 0:
                            basedFF = data.loc[baseT:baseT+base[mus].loc[j]+0.0001].mean()
                    elif not baselining:
                        basedFF = 0.0

                    if base[mus].loc[j] < 0:
                        slicePre = data.loc[baseT+base[mus].loc[j]:baseT].values - basedFF
                        slicePost = data.loc[startT:endT].values - basedFF
                        dataSlice = np.concatenate((slicePre, slicePost), axis=0)
                        slicedData['Fluoro'] = dataSlice
                        slicedData['New_Time'] = newTime[0:len(dataSlice)]
                        #slicedData['New_Time'] = np.linspace(base,((len(dataSlice)-1)*fs)+base,len(dataSlice))
                    elif base[mus].loc[j] > 0:
                        print "Oh, no!"
                        dataSlice = data.loc[startT+base[mus].loc[j]:endT+0.0001].values - basedFF
                        slicedData['Fluoro'] = dataSlice
                        slicedData['New_Time'] = np.linspace(base,((len(dataSlice)-1)*fs)+base[mus].loc[j],len(dataSlice))

                    slicedData['Cell'] = col
                    slicedData['Event'] = j
                    eventsData = eventsData.append(slicedData)

    print "\n", len(mice), " mice were loaded."

    if baselining:
        print "\nBaseline was set", base.mean().mean(), "sec before the event."
    elif not baselining:
        print "\nTraces were not baselined."

    return eventsData

def getBoutDur(mice, eventType, behType, trials):
    """
        DEPRICATED: Needs major revision!
    """
    print "DEPRICATED: Needs major revision!"
    # Load the data
    dataList = loadData(mice)

    # Load the events
    fileList = loopMice(mice, behType)
    eventList = getBeh(mice, fileList['Behaviour'], behType)

    durationData = pd.DataFrame()
    for mus, sess in mice:
        # Find the events
        boutDur = np.array([])
        startList = eventList[mus][eventType[0]].dropna().values
        endList = eventList[mus][eventType[1]].dropna().values
        for i in range(trials[0]-1, trials[1]):
            ind, start = find_nearest(dataList[mus].index.values, startList[i])
            ind, end = find_nearest(dataList[mus].index.values, endList[i])
            boutDur = np.append(boutDur, end-start)

        durationData[mus] = boutDur

    durationData.set_index(np.arange(trials[0], trials[1]+1), inplace=True)

    return durationData

def markBouts(mice, dataList, eventType, behType, trials, base, dff=True, baseline=False):
    """
        DEPRICATED: Use getBouts instead.
    """
    print "DEPRICATED: Use getBouts instead."
    fileList = loopMice(mice, behType)
    eventList = getBeh(mice, fileList['Behaviour'], behType)

    eventsData = pd.DataFrame()
    for mus, sess in mice:

        # Find the events
        eventTimes1 = np.array([])
        eventTimes2 = np.array([])
        startTimes = eventList[mus][eventType[0]].dropna().reset_index(drop=True)
        endTimes = eventList[mus][eventType[1]].dropna().reset_index(drop=True)
        for i, event in enumerate(startTimes):
            ind1, nearest1 = find_nearest(dataList[mus].index.values, startTimes.loc[i])
            ind2, nearest2 = find_nearest(dataList[mus].index.values, endTimes.loc[i])
            eventTimes1 = np.append(eventTimes1, nearest1)
            eventTimes2 = np.append(eventTimes2, nearest2)

        fs = dataList[mus].index[1] - dataList[mus].index[0]
        for col in dataList[mus].columns:
            if not col == 'Time (s)':
                data = dataList[mus][col]
                for i, event in enumerate(eventTimes1[trials[0]-1:trials[1]]):
                    start = eventTimes1[i]
                    end = eventTimes2[i]

                    slicedData = pd.DataFrame()

                    if baseline:
                        basedFF = data.loc[start+base:start+0.0001].mean()
                    elif not baseline:
                        basedFF = 0.0

                    slicedData['Fluoro'] = data.loc[start+base:end+0.0001].values - basedFF
                    slicedData['Cell'] = col
                    slicedData['Event'] = i+1
                    if len(data.loc[start+base:end+0.0001].values - basedFF) == len(np.arange(base,end-start+0.0001,fs)):
                        slicedData['New_Time'] = np.arange(base,end-start+0.0001,fs)
                    if len(data.loc[start+base:end+0.0001].values - basedFF) < len(np.arange(base,end-start+0.0001,fs)):
                        slicedData['New_Time'] = np.arange(base,end-start,fs)

                    eventsData = eventsData.append(slicedData)

    print "\n", len(mice), " mice were loaded."
    if behType == 'FR1':
        for mus, sess in mice:
            print "Mouse number", mus, " had ", eventList[mus]['Right_Count'].max(), " total rewards."

    if baseline:
        print "\nBaseline was set", baseline, "sec before the event."
    elif not baseline:
        print "\nTraces were not baselined."

    return eventsData
