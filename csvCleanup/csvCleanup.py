import time
import csv
import re
from sys import argv
#  clearance,description,title,reqid,applink,location,clearanceAndJunk
#csvFile = 'csvWork.csv'
csvFile = 'raytheonTotal.csv'
geoFile = 'geoInfo.csv'
geoDict = {}
outFile = 'raytheonFinal.csv'

# Open CSV output stream
output = open(outFile, 'wb')
wr = csv.writer(output, quoting=csv.QUOTE_ALL)

csv.register_dialect(
  'mydialect',
  delimiter=',',
  quotechar='"',
  doublequote=True,
  skipinitialspace=True,
  lineterminator='\r\n',
  quoting=csv.QUOTE_MINIMAL)

with open(geoFile, 'rb') as geocsv:
  geodata=csv.reader(geocsv, dialect='mydialect')
  for row in geodata:
    geoDict[row[0]]=(row[1]+","+row[2]) 

with open(csvFile, 'rb') as mycsv:
  data=csv.reader(mycsv, dialect='mydialect')
  for row in data:
    clear  = row[0]
    desc   = row[1]
    title  = row[2]
    req    = row[3]
    app    = row[4]
    loc    = row[5]
    clearX = row[6]
    location = ""
    ll = []

# LOCATION WORK #
    # Multi-location job cleanup
    loc = re.sub("United Kingdom United Kingdom", "United Kingdom", loc)
    if (loc.count('-') > 1):
      locA = loc.split(" ")
      if (re.match('^\s*\w\w\s*$',locA[3])):
        location=(locA[2]+", "+locA[0])
      elif (re.match('^\s*\w\w\s*$',locA[4])):
        location=(locA[2]+" "+locA[3]+", "+locA[0])
      elif (re.match('-', locA[2])):
        location=(locA[3]+", "+locA[0]+" "+locA[1])
      elif (re.match('-', locA[5])):
        location=(locA[2]+" "+locA[3]+" "+locA[4]+", "+locA[0])
      elif (re.match('-', locA[6])):
        location=(locA[2]+" "+locA[3]+" "+locA[4]+" "+locA[5]+", "+locA[0])
    # State / City cleanup
    elif (re.match('Afghanistan', loc)):
      location = 'Afghanistan'
    elif (re.match('Iraq', loc)):
      location = 'Iraq'
    elif (re.match('Kuwait', loc)):
      location = 'Kuwait'
    elif (re.match("^(\w{2}) - (.+)$",loc)):  
      location = re.sub("^(\w{2}) - (.+)$", r"\2, \1", loc)
    # Country cleanup
    else:
      location = re.sub("^(.+) - (.+)$", r"\2, \1", loc)
    location = re.sub(' Canada, Canada', ', Canada',location)
    location = re.sub(' Marshall Islands,| Saudi Arabia,', ',',location)
    if (re.match('TX - El Paso',loc)):
      location = 'El Paso, TX'
    # Cleaning up extraneous whitespace
    location = re.sub("^\s+|\s+$","",location)
    # Looking up LAT/LON from geo dictionary
    if (geoDict.has_key(location)):
      latlon=geoDict[location]
      ll=re.split(',', latlon)
      lat=(ll[0])
      lon=(ll[1])
    elif(re.match("location",location)):
      lat=('LAT')
      lon=('LON')
    else:
      lat=('NOT_FOUND')
      lon=('NOT_FOUND')
    fullLocation = loc
    row[5]=location
# FINISHED LOCATION #
  
    wr.writerow([title, desc, clear, app, req, location, lat, lon, "Raytheon", "http://www.raytheon.com/", 'a:16:{i:0;s:17:"Medical Insurance";i:1;s:16:"Dental Insurance";i:2;s:16:"Vision Insurance";i:3;s:17:"Prescription Plan";i:4;s:14:"Life Insurance";i:5;s:21:"Short Term Disability";i:6;s:20:"Long Term Disability";i:7;s:32:"Accidental Death & Dismemberment";i:8;s:22:"Paid Vacation/Time Off";i:9;s:13:"Paid Holidays";i:10;s:24:"Paid New Parent Time Off";i:11;s:4:"401K";i:12;s:20:"Education Assistance";i:13;s:18:"Technical Training";i:14;s:22:"Flexible Work Schedule";i:15;s:23:"Others - Please inquire";}', "https://clearedcareers.com/wp-content/uploads/Raytheon-1.gif", "Raytheon Intelligence, Information and Services delivers innovative technology to make the world a safer place. Our expertise in cyber, analytics and automation allow us to reach beyond what others think is possible to underpin national security and give our global customers unique solutions to solve the most pressing modern challenges -- from cybersecurity to automated operations, and from high-consequence training to clear insight from large volumes of data. IIS operates at nearly 550 sites in 80 countries, and is headquartered in Dulles, VA. The business area generated approximately $6 billion in 2015 revenues. As a global business, our leaders must have the ability to understand, embrace and operate in a multicultural world -- in the marketplace and the workplace. We strive to hire people who reflect our communities and embrace diversity and inclusion to advance our culture, develop our employees, and grow our business.", "########",fullLocation ])
