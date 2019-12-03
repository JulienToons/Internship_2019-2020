'''
Julien Owhadi
11/12/2019

'''

# ======================== IMPORT LIBRARIES ========================
import matplotlib.pyplot as plt
import numpy as np
import csv
import math
from scipy.signal import find_peaks

# ======================== CREATE FUNCTIONS ========================
toNum = lambda entry, ver=0: float(entry[0].split(",")[ver]) # returns the needed value (row like intensity or ppm)
                                                             # from an index (column) in the excel sheet

# ========================  OPEN DATA FILE AS A DICTIONARY OF INDEXES ========================

# OPEN .csv FILE DATA AS A MULTIDIMENSIONAL LIST:
with open('nanoparticle_scattering_data_rev.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile, delimiter=' ', quotechar='|'))

    references = [] # a dictionary composed of particle concentration, start index, and end index for comprehensibility
    temp_ppm = toNum(data[1])
    previous_index = 1
    for i in range(1,len(data)):
        row = data[i]
        if temp_ppm != toNum(row):
            references.append({'ppm': toNum(row), 'start': previous_index,'end': i})
            temp_ppm = toNum(row)
            previous_index = i
references.append({'ppm': toNum(row), 'start': previous_index,'end': i})
references.pop(0)


# ========================  CREATE REFERENCES & SET VARIABLES ========================

x_index = 1 # associated row in excel sheet
y_index = 4 # associated row in excel sheet

# ========================  PLOT GRAPH 1: LINES & PEAKS ========================
peaks = [None] * len(references)
for lineCounter, line in enumerate(references): # lineCounter represents the index attached to each element (line) in references

    if toNum(data[line['start']], 0) == 50 or True: # can set True to False if you only want to plot the line with ppm = 50ppm

        plt.plot([(toNum(data[i],x_index)) for i in range(line['start'],line['end'])],
                 [(toNum(data[i],y_index)) for i in range(line['start'],line['end'])],
                 label=line['ppm']) # plot lines

        peaks[lineCounter],_ = find_peaks(list(map(lambda el: toNum(el, x_index) , data[line['start']:line['end']])),
                           list(map(lambda el: toNum(el, y_index), data[line['start']:line['end']])),
                            prominence = .8) # find peaks

        color = [.2,.8,.9] # set color in RGB from [0-1 * 3]
        peaks.append(line['start']) # plot the initial peaks/'plateau'
        for peak_index in peaks[lineCounter]: # plot the rest of the peaks
            plt.plot(toNum(data[peak_index + line['start']], x_index),
                     toNum(data[peak_index+ line['start']], y_index), "*", color = color)


# ========================  LABEL GRAPH ========================

plt.xlabel('q (1/A)')
plt.ylabel('I_bkgd_subtracted(q) (mean background-subtracted intensity [a.u.])')

plt.title('q (1/A) v.s. I_background_subtracted(q) for SiO2 NP in H2O')

plt.legend(title="concentration(ppm)")

ax = plt.gca()

ax.set_xscale('log')
ax.set_yscale('log')

plt.show()
