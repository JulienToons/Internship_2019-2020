'''
Julien Owhadi
11/12/2019
'''

# import libraries
import matplotlib.pyplot as plt
import numpy as np
import csv
import math
from scipy.signal import find_peaks as find_peaks

# returns the needed value (row like intensity or ppm) from an index (column) in the excel sheet
toNum = lambda entry, ver=0: float(entry[0].split(",")[ver])


# ========================  OPEN FILE ========================

# OPEN .csv FILE DATA AS A MULTIDIMENSIONAL LIST:
with open('nanoparticle_scattering_data_rev.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile, delimiter=' ', quotechar='|'))

    references = [] # a dictionary composed of particle concentration, start index, and end index for comprehensibility
    temp_ppm = toNum(data[1])
    previous_index = 1
    for i in range(1,len(data)):
        row = data[i]
        # print(', '.join(row))
        if temp_ppm != toNum(row):
            references.append({'ppm': toNum(row), 'start': previous_index,'end': i})
            temp_ppm = toNum(row)
            previous_index = i
references.append({'ppm': toNum(row), 'start': previous_index,'end': i})
references.pop(0)


# ========================  CREATE REFERENCES & SET VARIABLES ========================

x_index = 1 # associated row in excel sheet
y_index = 4 # associated row in excel sheet

# ========================  PLOT LINES ========================

for line in references:
    if toNum(data[line['start']], 0) == 50:
        plt.plot([(toNum(data[i],x_index)) for i in range(line['start'],line['end'])],
                 [(toNum(data[i],y_index)) for i in range(line['start'],line['end'])],
                 label=line['ppm'])


# ========================  PLOT PEAKS ========================

for line in references:
    if toNum(data[line['start']], 0) == 50: # plot peaks for only the desired lines/data
        peaks,_ = find_peaks(#list(map(lambda el: toNum(el, x_index), data[line['start']:line['end']])),
                           list(map(lambda el: toNum(el, y_index), data[line['start']:line['end']])),
                            prominence = .35)
        print(peaks)

        color = [.2,.8,.9]

        plt.plot(toNum(data[line['start']], x_index),
                 toNum(data[line['start']], y_index), "*", color=color)
        for peak_index in peaks:
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