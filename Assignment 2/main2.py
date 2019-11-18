'''
Julien Owhadi
11/12/2019
'''

# import libraries
import matplotlib.pyplot as plt
import numpy as np
import csv
import math

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

alphaDistance = math.fabs(.07) # interval boundaries: will set automatically later on
mysterious_manipulator = .7
mergeDistance = .01
peak_qualifier = .1

# ========================  PLOT LINES ========================

for line in references:
    if toNum(data[line['start']], 0) == 50:
        plt.plot([(toNum(data[i],x_index)) for i in range(line['start'],line['end'])],
                 [(toNum(data[i],y_index)) for i in range(line['start'],line['end'])],
                 label=line['ppm'])


# ========================  PLOT PEAKS ========================

for line in references:
    if toNum(data[line['start']], 0) == 50: # plot peaks for only the desired lines/data
        peakValues = []

        # 1. g(x) = Sum from -alpha to alpha of f(x + d)*h(d)*delta(d)
        for i in range(line['start'], line['end']):
            temp_x = toNum(data[i],x_index)

            # define interval boundaries
            left = max( toNum(data[line['start']],x_index), temp_x - alphaDistance)
            right = min( toNum(data[line['end']],x_index) , temp_x + alphaDistance)

            leftIndex = line['start']
            rightIndex = line['end']

            for counter in range(i - 1, line['start'], -1):
                if toNum(data[counter], x_index) <= left:
                    leftIndex = counter + 1
                    break

            for counter in range(i+1, line['end']):
                if toNum(data[counter],x_index) >= right:
                    leftIndex = counter -1
                    break

            value = 0
            for counter in range(leftIndex,rightIndex):
                temp_difference = math.fabs(toNum(data[i], x_index) - toNum(data[counter], x_index))

                mysterious_value = 1 # h(x)
                mysterious_value = (1- 2*temp_difference/(alphaDistance*mysterious_manipulator) if temp_difference < mysterious_manipulator * alphaDistance
                                    else temp_difference/(alphaDistance*(1-mysterious_manipulator)) -1 if temp_difference < alphaDistance
                                    else 0)

                value += mysterious_value * toNum(data[counter], y_index) * temp_difference/alphaDistance

            peakValues.append(value)

            '''
            #### print(leftIndex-rightIndex)
            #### print()

            # compute linear regression formula form y = ax^2 + bx + c
            try:
                a,b,c = np.polyfit([toNum(data[m],x_index) for m in range(leftIndex,rightIndex)],   \
                               [toNum(data[m],y_index) for m in range(leftIndex,rightIndex)], 2)
            except:
                print("FAILED POLY-FIT")
                continue

            # find coordinates of the peak
            px = -b / (2 * a)
            py = a*px*px + b*px + c
            # DEBUGGER: print("a is {}\nb/2a is {}".format(a,b/(2*a)))

            # add to peaks if peak is in boundaries     ******** maybe store how far from middle???
            if (a<0 and  left <= -b/(2*a) <= right):
                # DEBUGGER: print("ADDED")
                peaks.append(i)                       # ******** maybe store x coordinate & y instead of the index???
            '''

        peaks = []

        # 2. Qualify Peaks
        for i in range(len(peakValues)):
            if(peakValues[i] >= peak_qualifier):
                peaks.append(line['start'] + i)

        # 3. 'Merge' almost-repetitive (close x values) list of peaks
        '''
        finalPeaks = []
        for i in range(0,len(peaks)-1):  # should be double for loop
            temp = []

            # create a list "temp" that contains close x values
            for l in range(i, len(peaks)-1):
                if (math.fabs(toNum(data[peaks[l]],x_index) - toNum(data[peaks[i]], x_index)) <= merIntDist):
                    temp.append(l)

            # remove all indexes other than the one that contains the highest y value
            highestVal = toNum(data[peaks[temp[0]]],y_index)
            while len(temp) > 1:
                if(highestVal < toNum(data[peaks[temp[1]]],y_index)):
                    temp.pop(0)
                else:
                    temp.pop(1)
            finalPeaks.append(peaks[temp[0]])
        # DEBUGGER: print(peaks)
        '''

        # 4. Plot the peaks
        for peak_index in peaks:
            plt.plot(toNum(data[peak_index], x_index), toNum(data[peak_index], y_index), "*y")


# ========================  LABEL GRAPH ========================

plt.xlabel('q (1/A)')
plt.ylabel('I_bkgd_subtracted(q) (mean background-subtracted intensity [a.u.])')

plt.title('q (1/A) v.s. I_background_subtracted(q) for SiO2 NP in H2O')

plt.legend(title="concentration(ppm)")

ax = plt.gca()

ax.set_xscale('log')
ax.set_yscale('log')

plt.show()