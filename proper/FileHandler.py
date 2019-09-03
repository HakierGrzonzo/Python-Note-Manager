import json, os, sys, codecs
from datetime import *


def today(divider = '.'):
	date = datetime.now()
	datestr = str(date.day) + divider + str(date.month) + divider + str(date.year)
	return datestr


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

		if self.dir[len(self.dir) - 1] == '/':
			self.dir = self.dir[:len(self.dir) - 1]

		self.MakeNew = MakeNew

		if MakeNew:
			if properties == None:
				raise ValueError('specify properties while making new folder!')
			try:
				os.mkdir(self.dir)
			except FileExistsError:
				self.MakeNew = False

			self.properties = properties
			propertiesFile = open(self.dir+'/properties.json', 'w+')
			json.dump(properties, propertiesFile)
			propertiesFile.close()

		else:
			propertiesFile = open(self.dir+'/properties.json', 'r')
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
				try:
					self.folders.append(Folder(self.dir + '/' + folder + '/'))
				except:
					raise TypeError('Could not load folder : ' + folder)

			for file in f:
				if not file == 'properties.json':
					self.files.append(file)

			#Stop os.walk in the top directory
			break

		self.files.sort()
		self.folders.sort()

	def __lt__(self, other):
		d1, m1, y1 = [int(x) for x in self.properties['Date'].split('/')]
		d2, m2, y2 = [int(x) for x in other.properties['Date'].split('/')] 
		return date(y1, m1, d1) < date(y2, m2, d2)

def MakeTemplate(template, folder):

	templateDir = os.path.expanduser('~/PNO/templates/')
	try:
		templateFile = codecs.open(templateDir + template, 'r', 'utf-8')
		text = templateFile.read()
		templateFile.close()
		text = text.replace('<date>', today())
		text = text.replace('<title>', folder.properties['Title'])

		if not folder.parent == None:
			text = text.replace('<subsection>', folder.parent.properties['Title'])

			if not folder.parent.parent == None:
				text = text.replace('<section>', folder.parent.parent.properties['Title'])
			else:
				text = text.replace('<section>', ' ')

		else:
			text.replace('<subsection>', ' ')
		success = True

	except Exception as e:
		if type(e) == FileNotFoundError:
			print('Did not find the specified file')
			success = False
		else:
			success = False
			raise e

	if success == True:
		try:
			target = folder.dir + '/' + 'note' + '.tex'
			targetFile = codecs.open(target, 'w+', 'utf-8')
			targetFile.write(text)
			folder.Scan()
			targetFile.close()
			print('success')
		except Exception as e:
			raise e
