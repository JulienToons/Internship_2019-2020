'''
Julien Owhadi
11/12/2019

'''

# ======================== IMPORT LIBRARIES ========================
import matplotlib.pyplot as plt
from statistics import mean
import numpy as np
import csv
import math
from scipy.signal import find_peaks

# ======================== CREATE VARIABLES & FUNCTIONS ========================
toNum = lambda entry, ver=0: float(entry[0].split(",")[ver]) # returns the needed value (row like intensity or ppm)
                                                             # from an index (column) in the excel sheet
x_index = 1 # associated row in excel sheet
y_index = 4 # associated row in excel sheet

f1, ax1 = plt.subplots(1)
f2, ax2 = plt.subplots(2,1)

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


# ========================  PLOT GRAPH 1: LINES & PEAKS ========================
peaks = [None] * len(references)
for lineCounter, line in enumerate(references): # lineCounter represents the index attached to each element (line) in references

    if toNum(data[line['start']], 0) == 50 or True: # can set True to False if you only want to plot the line with ppm = 50ppm

        ax1.plot([(toNum(data[i],x_index)) for i in range(line['start'],line['end'])],
                 [(toNum(data[i],y_index)) for i in range(line['start'],line['end'])],
                 label=line['ppm']) # plot lines

        temp,_ = find_peaks(#list(map(lambda el: toNum(el, x_index) , data[line['start']:line['end']])),
                           list(map(lambda el: toNum(el, y_index), data[line['start']:line['end']])),
                            prominence = .8) # find peaks
        peaks[lineCounter] = list(temp)
        color = [.2,.8,.9] # set color in RGB from [0-1 * 3]
        peaks[lineCounter].append(0) # add the initial peaks/'plateau'
        for peak_index in peaks[lineCounter]: # plot the peaks
            ax1.plot(toNum(data[peak_index + line['start']], x_index),
                     toNum(data[peak_index+ line['start']], y_index), "*", color = color)
            peak_index = peak_index + line['start']

# ========================  LABEL GRAPH 1 ========================
'''
plt.xlabel('q (1/A)')
plt.ylabel('I_bkgd_subtracted(q) (mean background-subtracted intensity [a.u.])')

plt.title('q (1/A) v.s. I_background_subtracted(q) for SiO2 NP in H2O')

plt.legend(title="concentration(ppm)")

ax = plt.gca()

ax.set_xscale('log')
ax.set_yscale('log')
'''
ax1.set_xlabel('q (1/A)')
ax1.set_ylabel('Intensity [a.u.]\n(mean background-subtracted)')

ax1.set_title('q (1/A) v.s. bkdg-sub\nintensity for SiO2 NP in H2O')

ax1.legend("concentration(ppm)", loc="upper right")
ax1.legend()
#f1.suptitle('test title', fontsize=20)

ax1.set_xscale('log')
ax1.set_yscale('log')
plt.show()

# ========================  CREATE GRAPH 2 ========================
'''numberOfPeaksShown = 2

for i in range(numberOfPeaksShown):
    temp_label = "Peak " + str(i) if (i == 0) else "Plateau"

    try:
        I_by_peak = peaks[:,i]
        ax2[0].plot([line['ppm'] for line in references],
                 [(toNum(data[i], y_index)) for i in I_by_peak],
                 label=temp_label)
    except:
        I_by_peak = []
        temp_xaxis = []
        for r in peaks:
            try:
                I_by_peak.append(toNum(data[r[i]], y_index))
                temp_xaxis.append(references[i]['ppm'])
            except:
                print("-")
        print(temp_xaxis)
        print(I_by_peak)
        ax2[0].plot(temp_xaxis, I_by_peak,label=temp_label)
'''
def best_fit_slope_and_intercept(xs, ys):
    m = (((mean(xs) * mean(ys)) - mean(xs * ys)) /
         ((mean(xs) * mean(xs)) - mean(xs * xs)))

    b = mean(ys) - m * mean(xs)

    return m, b
def abline(slope, intercept):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    ax2[0].plot(x_vals, y_vals, '--')

for (i in range(peaks)):
    value=map(lambda x:x[i], peaks)
    # plt.plot(concentrations, value)

    m, b = best_fit_slope_and_intercept(concentration, value)
    abline(m,b)

ax2[0].set_xlabel('Concentration (ppm)')
ax2[0].set_ylabel('Intensity [a.u.]\n(mean background-subtracted)')
ax2[0].set_title('Concentration vs Mean bkd-sub. Intensity')
ax2[0].legend()

plt.show()