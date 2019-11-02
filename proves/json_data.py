import json 
import csv

    

def store_upload_data(Tm,Wm,Hm,Mm,date):
    #jsondata.append({ 'Temperature':Tm, 'Humidity':Hm, 'Moisture':Mm, 'Date:':date })
    #with open('data.json', 'a') as outfile:
        #json.dump(jsondata, outfile)
    with open('data_log.csv','a') as datalog:
        data_writer = csv.writer(datalog)
        data_writer.writerow([str(date),str(Wm),str(Mm),str(Tm),str(Hm)])
    datalog.close

jsondata = [ { 'Temperature':23, 'Humidity':45, 'Moisture':50, 'Date':'' } ]
print ('DATA:',jsondata)
store_upload_data(Tm,Wm,Hm,Mm,date)


Tm = 30
Hm = 60
Mm = 4
Wm = 0
date = datetime.datetime.now().replace(microsecond=0)
print(date)

