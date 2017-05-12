# make sure there is a connection to Google's server
import requests
try:
  response = requests.get('http://www.google.com')
except:
  print('Can\'t connect to Google\'s server')
  raw_input('Press any key to exit.')
  quit()

# use the Google Maps API
import googlemaps
import json
import csv

with open('data/Boulder_Bike_Kiosks_Details.csv', 'r') as f:
    reader = csv.reader(f)
    Bike_list = list(reader)
f.close()
result1 = []
result2 = []
result = []

with open("data/Boulder_Bike_Kiosks_Distances_Durations.csv", "w", newline='') as f:
  writer = csv.writer(f)
  colNames = ["Checkout_Kiosk", "Checkout_Kiosk_Latitude", "Checkout_Kiosk_Longitude",
      "Return_Kiosk", "Return_Kiosk_Latitude", "Return_Kiosk_Longitude",
      "Distance_Checkout_Return", "Duration_Checkout_Return",
      "Distance_Return_Checkout", "Duration_Return_Checkout", "Average_Distance",
      "Average_Duration"]
  writer.writerow(colNames)
  for KioskRow in Bike_list[1:1805]:
    origins = KioskRow[1] + "," + KioskRow[2]
    destinations = KioskRow[4] + "," + KioskRow[5]
    gmaps = googlemaps.Client(key='Enter your key here')
    matrix = gmaps.distance_matrix(origins, destinations, mode="bicycling", units="imperial", avoid="highways")
    print(matrix)
    cycling_distance = matrix['rows'][0]['elements'][0]['distance']['value']
    cycling_time = matrix['rows'][0]['elements'][0]['duration']['value']
    print(KioskRow)
    result1 = KioskRow + [format(cycling_distance*0.0006213, '.2f'), format(cycling_time/60,'2f')]
    origins = KioskRow[4] + "," + KioskRow[5]
    destinations = KioskRow[1] + "," + KioskRow[2]
    gmaps = googlemaps.Client(key='Enter your key here')
    matrix = gmaps.distance_matrix(origins, destinations, mode="bicycling", units="imperial", avoid="highways")
    print(matrix)
    cycling_distance = matrix['rows'][0]['elements'][0]['distance']['value']
    cycling_time = matrix['rows'][0]['elements'][0]['duration']['value']
    result2 = [format(cycling_distance*0.0006213, '.2f'), format(cycling_time/60,'2f')]
    result = result1 + result2
    print(result)
    writer.writerow(result)
  f.close()
