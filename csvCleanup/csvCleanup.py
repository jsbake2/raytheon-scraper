#!/usr/bin/python
import time
import csv
import re
import locations
from locations import parser
import clearances
from clearances import clearance as clear
from sys import argv
#  clearance,description,title,reqid,applink,location,clearanceAndJunk
#csvFile = 'csvWork.csv'
csvFile = 'raytheonTotal.csv'
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

wr.writerow(['title', 'apply_url', 'job_description', 'location', 'company_name', 'company_description', 'company_website', 'company_logo', 'company_facebook', 'company_twitter', 'company_linkedin', 'company_google', 'career_id', 'deployment', 'travel', 'job_lat', 'job_lon', 'company_benefits', 'job_category', 'clearance', 'keywords'])

with open(csvFile, 'rb') as mycsv:
  data=csv.reader(mycsv, dialect='mydialect')
  for row in data:
    clearance = row[0]
    desc      = row[1]
    title     = row[2]
    req       = row[3]
    app       = row[4]
    loc       = row[5]
    clearX    = row[6]
    if not re.match("location|^$", loc):
      location,lat,lon=parser.loc(loc,"raytheon")
    else:
      location,lat,lon = "error","error","error"
    fullLocation = "test"
    clearance =  clear.clear(clearance)
# FINISHED LOCATION #
    if not re.match("None", clearance):
      wr.writerow([title, app, desc, location, "Raytheon", "Raytheon Intelligence, Information and Services delivers innovative technology to make the world a safer place. Our expertise in cyber, analytics and automation allow us to reach beyond what others think is possible to underpin national security and give our global customers unique solutions to solve the most pressing modern challenges -- from cybersecurity to automated operations, and from high-consequence training to clear insight from large volumes of data. IIS operates at nearly 550 sites in 80 countries, and is headquartered in Dulles, VA. The business area generated approximately $6 billion in 2015 revenues. As a global business, our leaders must have the ability to understand, embrace and operate in a multicultural world -- in the marketplace and the workplace. We strive to hire people who reflect our communities and embrace diversity and inclusion to advance our culture, develop our employees, and grow our business.", "http://www.raytheon.com/", "https://clearedcareers.com/wp-content/uploads/Raytheon-1.gif", "Raytheon Facebook", "Raytheon Twitter", "Raytheon Linkedin", "Raytheon Google", req, "deployment", "travel", lat, lon, 'a:16:{i:0;s:17:"Medical Insurance";i:1;s:16:"Dental Insurance";i:2;s:16:"Vision Insurance";i:3;s:17:"Prescription Plan";i:4;s:14:"Life Insurance";i:5;s:21:"Short Term Disability";i:6;s:20:"Long Term Disability";i:7;s:32:"Accidental Death & Dismemberment";i:8;s:22:"Paid Vacation/Time Off";i:9;s:13:"Paid Holidays";i:10;s:24:"Paid New Parent Time Off";i:11;s:4:"401K";i:12;s:20:"Education Assistance";i:13;s:18:"Technical Training";i:14;s:22:"Flexible Work Schedule";i:15;s:23:"Others - Please inquire";}', "need category", clearance, "keywords"])
