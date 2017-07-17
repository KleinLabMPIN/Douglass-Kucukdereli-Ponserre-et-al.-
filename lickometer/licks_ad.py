# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 19:32:28 2015

@author: douglass
"""
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt
from collections import Counter
from operator import sub
import glob

curDirPath =  os.path.dirname(os.path.realpath(__file__))
os.chdir(curDirPath)
print "Working directory is set to ", os.getcwd()
fileName = "data\Kissykissylicklick\NpHR\8055__test_adlib.csv"

# variables
value1 = list()
time1 = list()
event1 = list()

value2 = list()
time2 = list()
event2 = list()

acqt = 0 # sampling rate in ms

#separate into Lick1 and Lick2
#with open('P:/Amygdala/Behaviour/Optogenetics/Htr nHR Licks/Grp1_Day7/test2.csv') as f:
        #animal = csv.reader(f, delimiter=' ', skipinitialspace=False)
        #for row in animal:
            #print(row)
            #if len(row) > 1:
               #value1.append(int(row[1]))

#data = glob.glob('P:/Amygdala/Behaviour/Optogenetics/Htr nHR Licks/Grp1_Day12/8076_FRtest.csv')
#print data[0]
CH = 0
herro = np.genfromtxt(fileName, delimiter = ' ', usecols= CH)
print herro

plt.plot(herro)
plt.show()

# function detecting the begining and end of each bout

def boutsDetect(value1, acqt, choice):

	bouts = []

	if choice == "begin":
		print("Begining of the bouts: ")
		i = 0
		for i in range(0, len(herro)-1):
			if herro[i] == 0:
				if herro[i+1] > 0:
					bouts.append(i*acqt)

	elif choice == "end":
		print("Ending of the bouts: ")
		i = 0
		for i in range(0, len(herro)-1):
			if herro[i] > 0:
				if herro[i+1] == 0:
					bouts.append(i*acqt)

	else:
		print("Wrong choice!")

	return bouts

# counts the number of licks
def boutsCount(boutsBegin):
    return len(boutsDetect(boutsBegin, 1, "begin"))

# digitizing the data
threshold = 240
boutDigi = []

for i in range(0, len(herro)):
	if herro[i] >= threshold:
		boutDigi.append(1)
	else:
		boutDigi.append(0)

#bout duration
bout_starts = list(boutsDetect(boutDigi, 1, "begin"))
bout_ends = list(boutsDetect(boutDigi, 1, "end"))
#print "Beginning of bouts:" + str(bout_starts)
#print "End of bouts:" + str(bout_ends)

boutDuration = map(sub,bout_ends, bout_starts)
#print len(boutDuration)

longLicks = list()
Licks = list()

for value in boutDuration:
    if value > 9 and value < 63:
        Licks.append(value)

    if value > 63:
        longLicks.append(value)

ammendedValue = list()

for value in longLicks:
    ammendedValue.append(float(value/42))
    print("Ammended Value:" + str(len(ammendedValue)))
    totalAmmended = sum(ammendedValue)
    totalLicks = totalAmmended + len(Licks)
    print("Total number of licks:" + str(totalLicks))

#print "Total number of licks: " + str(len(boutDuration)

# data analysis
#print(boutDigi)
#boutDur = (boutsDetect(boutDigi, acqt, "begin"), boutsDetect(boutDigi, acqt, "end"))



# calculate the total bout duration. not very representative...
#boutDurTotal = np.sum(boutDur)
#print("Total bout duration: " + str(boutDurTotal) + "ms.")



# plotting the graphs
beginTime = 0
#beginTime = 111000
endTime = len(herro)
#endTime= 115000

plt.figure(1)
plt.plot(range(0, len(herro)), herro, "r")
plt.axis(ymin = 0, ymax = 300, xmin = beginTime, xmax = endTime)

plt.figure(2)
plt.plot(range(0, len(herro)), boutDigi, "b")
plt.axis(ymin = 0, ymax = 2,  xmin = beginTime, xmax = endTime)

plt.show()
