import zipfile
import sys
import os
import os.path

__author__ = 'Elmer Thomas'
__version__ = '0.1'

class unzip:
	"""Unzip a file to a specified output directory"""
	def __init__(self, input_filename, dir):
		"""Attributes needed for file processing
		
		Keyword arguements:
		input_filename -- file that needs to be unzipped
		dir -- directory where the file is located
		zipped_files -- arroay of the unzipped filenames
		"""
		self.input_filename = input_filename
		self.dir = dir
		self.zipped_files = []

	def extract(self):
		"""Perform the unzip action"""
		unzipped_file = zipfile.ZipFile(self.input_filename)
		"""Write the file(s) to specified directory"""
		for i, name in enumerate(unzipped_file.namelist()):
			file = open(os.path.join(self.dir,name), 'wb')
			self.zipped_files.append(name)
			file.write(unzipped_file.read(name))
			file.flush()
			file.close()

	def get_unzipped_filenames(self):
		return self.zipped_files
