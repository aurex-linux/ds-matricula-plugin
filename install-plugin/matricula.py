import datastore
import sh


class matricula(datastore.datastore_plugin):
	def import_csv(self, username, userpass, filestream):
		import_csv_command = sh.Command("/usr/share/ds-matricula-plugin/matricula-common-scripts/1-itaca2mysql")
		# set a temporary file and pathname
		if self._put_file(filepath, fname, filestream):
		


