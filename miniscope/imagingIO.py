import os
import numpy as np
import pandas as pd

def loopMice(mice, behType):
    """
        Gathers file paths for imaging data and behaviour time stamps
    """
    fileList = pd.DataFrame({'Mouse':[], 'Session':[], 'Data':[], 'Behaviour':[]})
    for mus,sess in mice:
        dataPath = "J:\\Hakan Kucukdereli\\Miniscope_Behaviour_MPIN\\" + str(mus) + "_" + str(behType) + "_Test\\Filtered_32-bit_2X2\\ICs_" + str(sess) + "\\M" + str(mus) + "_recording_ICs.csv"
        behPath = "J:\\Hakan Kucukdereli\\Miniscope_Behaviour_MPIN\\" + str(mus) + "_" + str(behType) + "_Behaviour\\" + str(mus) + "_" + str(behType) + "_Behaviour.csv"
        musList = pd.DataFrame({ 'Mouse' : mus, 'Session' : sess, 'Data' : dataPath, 'Behaviour' : behPath, 'Type' : behType }, index=[mus], dtype=object)
        fileList = fileList.append(musList)

    return fileList

def loadData(mice, behType):
    """
        Gets the names of files of all the mice and returns it as a list.
    """
    # Get the file names
    fileList = loopMice(mice, behType)

    # Load the data
    dataList = {}
    for mus, sess in mice:
        data = pd.read_csv(fileList['Data'].loc[mus], delimiter= ",", skip_blank_lines= True, error_bad_lines= False)

        # Organize the data a little bit
        # Get the frame rate of the recording
        fs = get_fs(data['Time (s)'])
        # Rearrange the time axis and set the index
        data['Time (s)'] = np.arange(0.00, len(data.index)*fs, fs)
        data = data.set_index(data['Time (s)'])

        dataList[mus] = data.drop('Time (s)', 1)

    return dataList

def loadBeh(filePath, behType):
    """
    """
    # load the data from csv
    behData = pd.read_csv(filePath, delimiter= ",", skip_blank_lines= True, error_bad_lines= False)

    eventTypes1 = ['Right_Poke', 'Right_Cue', 'Success_Reward', 'Left_Poke', 'Left_Cue', 'Miss_Reward']
    eventTypes2 = ['Food_Contact', 'Eat_Start', 'Eat_End']

    for eventType in behData.columns:
        if behType == 'FR1':
            offset = behData['Trials_Start'].iloc[0]
            if eventType in eventTypes1:
                behData[eventType] = (behData[eventType] - offset)/1000
            elif eventType in eventTypes2:
                behData[eventType] = (behData[eventType]) /1000
                behData['Bout_Duration'] = behData['Eat_End'] - behData['Eat_Start']
        else:
            behData[eventType] = behData[eventType]
            behData['Bout_Duration'] = behData['Eating_End'] - behData['Eating_Start']

    return behData

def getBeh(mice, behList, behType):
    """
    """
    eventList = {}
    for mus, sess in mice:
        eventList[mus] = loadBeh(behList[mus], behType)

    return eventList

def get_fs(time):
    """
    """
    fs = time.values[1] - time.values[0]

    return fs
