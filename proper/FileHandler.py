import json, os, sys
from datetime import *

dayfirst=True


def properties(Title, Type, Date, Author): 
	data = {
		"Title":	Title,
		"Type" :	Type,
		"Date" :	Date,
		"Author":	Author
		} 
	return data

class Folder(object):
	"""docstring for Folder"""
	def __init__(self, dir, MakeNew = False, properties = None, parent = None):
		super(Folder, self).__init__()
		self.parent = parent
		self.dir = dir
		self.MakeNew = MakeNew
		if MakeNew:
			if properties == None:
				raise ValueError('specify properties while making new folder!')
			try:
				os.mkdir(self.dir)
			except FileExistsError:
				self.MakeNew = False
			self.properties = properties
			propertiesFile = open(dir+'/properties.json', 'w+')
			json.dump(properties, propertiesFile)
			propertiesFile.close()
		else:
			propertiesFile = open(dir+'/properties.json', 'r')
			self.properties = json.load(propertiesFile)
			propertiesFile.close()
		self.files = list()
		self.folders = list()
		self.Scan()

	def Scan(self):
		self.files = list()
		self.folders = list()
		for r, d, f in os.walk(self.dir):
			for folder in d:
				self.folders.append(Folder(self.dir + '/' + folder + '/'))
			for file in f:
				if not file == 'properties.json':
					self.files.append(file)
		self.files.sort()
		self.folders.sort()

	def __lt__(self, other):
		d1, m1, y1 = [int(x) for x in self.properties['Date'].split('/')]
		d2, m2, y2 = [int(x) for x in other.properties['Date'].split('/')] 
		return date(y1, m1, d1) < date(y2, m2, d2)

		
