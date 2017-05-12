from forecastiopy import *
import csv
import os
import pandas as pd
import datetime
import time

apikey = 'enter your key here'
 
Boulder = [40.014984, -105.270546, 1451631600]
Boulder_Time = 1451631600
 
fio = ForecastIO.ForecastIO(apikey,
                            latitude=Boulder[0],
                            longitude=Boulder[1],
                            time=str(Boulder[2])) 
print 'Latitude', fio.latitude, 'Longitude', fio.longitude
print 'Timezone', fio.timezone
print fio.get_url() # You might want to see the request url
print

req_list = {}
b_mth = '5/'
for b_day in range(1,31):
    dt = datetime.datetime(2016, 5, b_day, 0, 0)
    req_list[b_mth + str(b_day) + '/2016'] = int((time.mktime(dt.timetuple())))
sortedReqList = sorted(req_list.items())
    
columns = ['Date', 'Hour', 'apparentTemperature', 'cloudCover', 'humidity', 'temperature', 'time', 'visibility', 'windSpeed']
index = ['Row']
dF = pd.DataFrame(columns = columns, index = index)
dF1= pd.DataFrame(columns = columns, index = index)
csv_file = "C:\Temp\Boulder_May_Hourly_2016_Forecast.csv"
for req_day in sortedReqList:
    Boulder_Time = req_day[1]
    fio = ForecastIO.ForecastIO(apikey,
                            latitude=Boulder[0],
                            longitude=Boulder[1],
                            time=str(Boulder_Time))

    if fio.has_hourly() is True:
        hourly = FIOHourly.FIOHourly(fio)
        print 'Hourly'
        print 'Summary:' #, hourly.summary
        print 'Icon:' #, hourly.icon
        print
        for hour in xrange(0, hourly.hours()):
            for item in hourly.get_hour(hour).keys():
                 dF['Date'] = req_day[0]
                dF['Hour'] = int(hour)
                if item == 'time':
                    dF[str(item)] = hourly.get_hour(hour)[item]
                if item == 'cloudCover':
                    dF[str(item)] = hourly.get_hour(hour)[item]
                if item == 'temperature':
                    dF[str(item)] = hourly.get_hour(hour)[item]
                if item == 'apparentTemperature':
                    dF[str(item)] = hourly.get_hour(hour)[item]
                if item == 'windSpeed':
                    dF[str(item)] = hourly.get_hour(hour)[item]
                if item == 'humidity':
                    dF[str(item)] = hourly.get_hour(hour)[item]
                if item == 'visibility':
                    dF[str(item)] = hourly.get_hour(hour)[item]
            dF1 = dF1.append(dF)   
    else:
        print 'No Hourly data'

#csv_file = "C:\Temp\Jan2015.csv"
dF1.to_csv(csv_file, sep=',')

new_dF = pd.read_csv(csv_file,index_col=0)
print new_dF
