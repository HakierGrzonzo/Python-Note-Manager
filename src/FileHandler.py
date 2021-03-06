import json, os, sys, codecs
from datetime import datetime, date


def today(divider = '.'):
	"returns current date as string in DD.MM.YYYY format"
	date = datetime.now()
	datestr = str(date.day) + divider + str(date.month) + divider + str(date.year)
	return datestr


def properties(Title, Type, Date, Author):
	"Template for Folder.properties. Type field is depracated."
	data = {
		"Title":	Title,
		"Type" :	Type,
		"Date" :	Date,
		"Author":	Author
		}
	return data


class Folder(object):
	"""
		Represents phisical folder on a computer with a .json file containing
		metadata. It contains:
			.parent - updirectory
			.dir - path
			.files - list of filenames
			.folders - list of folders in folder #NOTE: Folder with names
			ending with .assets are ignored
	"""
	def __init__(self, dir, MakeNew = False, properties = None, parent = None):
		"""
			dir - path to folder
			MakeNew - Can create new folder
			properties - dict with metadata
			parent - folder updirectory
		"""
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
		"""Scan for files and folders"""
		self.files = list()
		self.folders = list()

		for r, d, f in os.walk(self.dir):
			for folder in d:
				try:
					if not folder.endswith('.assets'):
						self.folders.append(Folder(self.dir + '/' + folder + '/', parent = self))
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
		"""For sorting the list of folders by date"""
		d1, m1, y1 = [int(x) for x in self.properties['Date'].split('/')]
		d2, m2, y2 = [int(x) for x in other.properties['Date'].split('/')]
		return date(y1, m1, d1) < date(y2, m2, d2)

def MakeTemplate(template, folder, extension = '.md'):
	"""Substitute the fields in template and copy it to the target folder"""
	templateDir = os.path.expanduser('~/PNO/templates/')
	try:
		templateFile = codecs.open(templateDir + template + extension, 'r', 'utf-8')
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
			target = folder.dir + '/' + 'note' + extension
			targetFile = codecs.open(target, 'w+', 'utf-8')
			targetFile.write(text)
			folder.Scan()
			targetFile.close()
		except Exception as e:
			raise e
