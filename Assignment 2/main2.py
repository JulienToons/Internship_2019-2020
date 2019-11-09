import matplotlib.pyplot as plt
import csv
#
toNum = lambda entry, ver=0: float(entry[0].split(",")[ver])

# OPEN .csv FILE DATA AS A MULTIDIMENSIONAL LIST:
with open('nanoparticle_scattering_data_rev.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile, delimiter=' ', quotechar='|'))

    references = []
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
# PLOT DATA:
for line in references: # math.log10(...
    plt.plot([(toNum(data[i],1)) for i in range(line['start'],line['end'])],                \
             [(toNum(data[i],4)) for i in range(line['start'],line['end'])],    \
             label=line['ppm'])

plt.xlabel('q (1/A)')
plt.ylabel('I_bkgd(q) (mean background-subtracted intensity [a.u.])')


# I am not certain if this title is accurate
plt.title('I(q) v.s. I_bkgd(q) for SiO2 NP in H2O (background-subtracted)')

plt.legend(title="concentration(ppm)")

ax = plt.gca()
ax.set_xscale('log')
ax.set_yscale('log')

plt.show()




