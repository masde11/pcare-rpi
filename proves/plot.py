import csv
import numpy as np
import matplotlib.pyplot as plt
import datetime

#plot_data(Tm,Wm,Hm,Mm,date)

Tm = 30
Hm = 60
Mm = 4
Wm = 0
date = datetime.datetime.now().replace(microsecond=0)

data_string = []
with open('data_log.csv','r') as datalog:
    reader = csv.reader(datalog)
    for row in reader: # each row is a list
        data_string.append(row)
datalog.close
print(data_string)
data_num = np.zeros(len(data_string[:,0],4))
for i in range(1,len(data_string[:,0])):
    for j in range(1,4):
        data_num[i,j] = float(data_string[i,j])
        #data_date[i] = data_string[i,0]

print(data_num)
'''fig = plt.figure()
    plt.plot(date,Tm,label="Temperature")
    plt.plot(date,Hm,label="Humidity")
    plt.plot(date,Mm,label="Moisture")
    plt.legend()
    fig.savefig('plot.png')'''