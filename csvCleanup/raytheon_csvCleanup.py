#!/usr/bin/python
import time
import csv
import re
import locations
from locations import parser
import clearances
from clearances import clearance as clear
from sys import argv
import companyinfo
from companyinfo import infofiller
import datetime
import categories
from categories import category
#  clearance,description,title,reqid,applink,location,clearanceAndJunk
#csvFile = 'csvWork.csv'
csvFile = 'raytheonTotal.csv'
outFile = 'raytheonFinal.csv'

# Open CSV output stream
logDate= datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
companyName = 'Raytheon'
output = open('/home/jbaker/Desktop/'+companyName+'_'+logDate+'_'+outFile, 'wb')

wr = csv.writer(output, quoting=csv.QUOTE_ALL)

csv.register_dialect(
  'mydialect',
  delimiter=',',
  quotechar='"',
  doublequote=True,
  skipinitialspace=True,
  lineterminator='\r\n',
  quoting=csv.QUOTE_MINIMAL)

wr.writerow(['title', 'apply_url', 'job_description', 'location', 'company_name', 'company_description', 'company_website', 'company_logo', 'company_facebook', 'company_twitter', 'company_linkedin', 'career_id', 'deployment', 'travel', 'job_lat', 'job_lon', 'company_benefits', 'job_category', 'clearance', 'keywords','author'])

infoComp,infoDesc,infoSite,infoLogo,infoFace,infoTwit,infoLinked,infoBeni,author=companyinfo.infofiller(companyName)

with open(csvFile, 'rb') as mycsv:
  data=csv.reader(mycsv, dialect='mydialect')
  for row in data:
    keyw = ""
    locKey = ''
    clearance = row[0]
    desc      = row[1]
    title     = row[2]
    req       = row[3]
    appUrl    = row[4]
    loc       = row[5]
    clearX    = row[6]
    if not re.match("location|^$", loc):
      location,lat,lon,locKey=parser.loc(loc,"raytheon")
    else:
      location,lat,lon = "error","error","error"
    clearance,clKey =  clear.clear(clearance)
    for i in clKey:
      keyw=keyw+' '+i
    keyw=re.sub('^ ','',keyw)    
    keyWords = keyw + ' ' + locKey
    job_category = category(title,title)
    if re.match('Other', job_category):
      job_category = category(desc,title)
# FINISHED LOCATION #
    if not re.match("None|^$", clearance):
      wr.writerow([title, appUrl, desc, location, infoComp, infoDesc, infoSite, infoLogo, infoFace, infoTwit, infoLinked, req, 'UNKNOWN', 'UNKNOWN', lat, lon, infoBeni, job_category, clearance, keyWords, author])
