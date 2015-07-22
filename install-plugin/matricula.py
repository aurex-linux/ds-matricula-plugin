import datastore
import sh
import csv
import tempfile
import os

class matricula(datastore.datastore_plugin):
	def _csv2xml(self, csvFile, xmlFile):
		# FB - 201010107
		# First row of the csv file must be header!
		# Most of the code was downloaded from: http://code.activestate.com/recipes/577423-convert-csv-to-xml/
		# License: MIT License
		# Copyright 2010: FB36 (http://code.activestate.com/recipes/users/4172570/)
		try:
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
		except:
			return False
		return True

	def import_csv(self, username, userpass, filestream):
		retCode = True
		import_xml_command = sh.Command("/usr/share/ds-matricula-plugin/matricula-common-scripts/1-itaca2mysql")
		# set a temporary filename
		TMP_CSV = tempfile.mkstemp()[1]
		TMP_CSV2 = tempfile.mkstemp()[1]
		if self._put_file(TMP_CSV, filestream):
			TMP_XML = tempfile.mkstemp()[1]
			sh.sed(sh.iconv("-f", "ISO-8859-15", "-t", "UTF-8", TMP_CSV), "-e", "1{s%[[:blank:]]%%g;s%\.%%g;s%[ñÑ]%n%g;s%.*%\L&%}", _out=TMP_CSV2)

			if self._csv2xml(TMP_CSV2, TMP_XML):
				try:
					import_xml_command(TMP_XML)
				except ErrorReturnCode:
					# some error happened
					retCode = False

			os.remove(TMP_XML)
		os.remove(TMP_CSV)
		os.remove(TMP_CSV2)
		return retCode

	def delete_from_ldap(self):
		retCode = True
		delete_from_ldap_command = sh.Command("/usr/share/ds-matricula-plugin/matricula-common-scripts/2-delete_from_ldap")
		try:
			delete_from_ldap_command("-y")
		except ErrorReturnCode:
			# some error happened
			retCode = False
		return retCode

	def add_to_ldap(self):
		retCode = True
		add_to_ldap_command = sh.Command("/usr/share/ds-matricula-plugin/matricula-common-scripts/3-add_to_ldap")
		try:
			add_to_ldap_command("-y")
		except ErrorReturnCode:
			# some error happened
			retCode = False
		return retCode

