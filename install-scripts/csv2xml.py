#!/usr/bin/env python
# csv2xml.py
# FB - 201010107
# First row of the csv file must be header!
# example CSV file: myData.csv
# id,code name,value
# 36,abc,7.6
# 40,def,3.6
# 9,ghi,6.3
# 76,def,99

#Downloaded from: http://code.activestate.com/recipes/577423-convert-csv-to-xml/
#License: MIT License
#Copyright 2010: FB36 (http://code.activestate.com/recipes/users/4172570/)
import csv
import sys

# check arguments
if len(sys.argv) < 3 :
        print 'Usage: csv2xml.py <inputcsvfile> <ouputxmlfile>'
	sys.exit()

csvFile = sys.argv[1]
xmlFile = sys.argv[2]

csvData = csv.reader(open(csvFile))
xmlData = open(xmlFile, 'w')
xmlData.write('<?xml version="1.0" encoding="UTF-8" ?>' + "\n")
# there must be only one top-level tag
xmlData.write('<csv_data>' + "\n")

rowNum = 0
for row in csvData:
    if rowNum == 0:
        tags = row
        # replace spaces w/ underscores in tag names
        for i in range(len(tags)):
            tags[i] = tags[i].replace(' ', '_')
    else: 
        xmlData.write('<row>' + "\n")
        for i in range(len(tags)):
            xmlData.write('    ' + '<' + tags[i] + '>' \
                          + row[i] + '</' + tags[i] + '>' + "\n")
        xmlData.write('</row>' + "\n")
            
    rowNum +=1

xmlData.write('</csv_data>' + "\n")
xmlData.close()
