import json, os, sys
from datetime import *


class Page(object):
	"""
		Page class consists of:
			* Dictonary to keep track of metadata
			* List of files in Page folder
		Page folder is a working directory for users as it contains the actual files with notes
	"""
	def __init__(self, dir, MakeNew = False, properties = None):
		super(Page, self).__init__()
		self.dir = dir
		if MakeNew:
			os.mkdir(self.dir)

		try:
			if MakeNew:
				self.properties = properties
				json.dump(self.properties, open(self.dir + 'properties.json', 'w+'))

			else:
				self.properties = json.load(open(dir+'properties.json','r'))

			if self.properties['Type'] == 'Page':
				self.Files = list()

				for r, d, f in os.walk(self.dir):
					for file in f:
						self.Files.append(self.dir + file)

			else:
				raise TypeError('SubSection folder expected, got: ' + self.properties['Type'])

		except Exception as e:
			raise e

	def __lt__(self, other):
		y1, m1, d1 = [int(x) for x in self.properties['Date'].split('/')]
		y2, m2, d2 = [int(x) for x in other.properties['Date'].split('/')] 
		return date(y1, m1, d1) < date(y2, m2, d2)
		

class SubSection(object):
	"""simmilar to Notebook() class"""
	def __init__(self, dir, MakeNew = False, properties = None):
		super(subSection, self).__init__()
		self.dir = dir
		if MakeNew:
			os.mkdir(self.dir)

		try:
			if MakeNew:
				self.properties = properties
				json.dump(self.properties, open(self.dir + 'properties.json', 'w+'))

			else:
				self.properties = json.load(open(dir+'properties.json','r'))

			if self.properties['Type'] == 'SubSection':
				self.pages = list()

				for r, d, f in os.walk(self.dir):
					for folder in d:
						self.pages.append(Page(self.dir + folder + '/'))

			else:
				raise TypeError('SubSection folder expected, got: ' + self.properties['Type'])

		except Exception as e:
			raise e
	def SortSelf(self):
		self.pages.sort()
	def __lt__(self, other):
		y1, m1, d1 = [int(x) for x in self.properties['Date'].split('/')]
		y2, m2, d2 = [int(x) for x in other.properties['Date'].split('/')] 
		return date(y1, m1, d1) < date(y2, m2, d2)

class Section(object):
	"""simmilar to Notebook() class"""
	def __init__(self, dir, MakeNew = False, properties = None):
		super(Section, self).__init__()
		self.dir = dir

		if MakeNew:
			os.mkdir(self.dir)

		try:
			if MakeNew:
				self.properties = properties
				json.dump(self.properties, open(self.dir + 'properties.json', 'w+'))

			else:
				self.properties = json.load(open(dir+'properties.json','r'))

			if self.properties['Type'] == 'Section':
				self.subsections = list()

				for r, d, f in os.walk(self.dir):
					for folder in d:
						try:
							self.subsections.append(SubSection(self.dir + folder + '/'))
						except Exception as e:
							pass

			else:
				raise TypeError('Section folder expected, got: ' + self.properties['Type'])

		except Exception as e:
			raise e
	def SortSelf(self):
		self.subsections.sort()
	def __lt__(self, other):
		y1, m1, d1 = [int(x) for x in self.properties['Date'].split('/')]
		y2, m2, d2 = [int(x) for x in other.properties['Date'].split('/')] 
		return date(y1, m1, d1) < date(y2, m2, d2)

class Notebook(object):
	"""
		Notebook class consists of:
			* Dictonary to keep track of metadata
			* List of sections in Notebook folder
	"""
	def __init__(self, dir, MakeNew = False, properties = None):
		super(Notebook, self).__init__()
		self.dir = dir

		if MakeNew:
			os.mkdir(self.dir)

		try:
			if MakeNew:
				self.properties = properties
				self.file = open(self.dir + 'properties.json', 'w+')
				json.dump(properties, self.file)

			else:
				self.properties = json.load(open(dir+'properties.json','r'))

			if self.properties['Type'] == 'Notebook':
				self.sections = list()

				for r, d, f in os.walk(self.dir):
					for folder in d:
						try:
							self.sections.append(Section(self.dir + folder + '/'))
						except Exception as e:
							pass

			else:
				raise TypeError('Notebook folder expected, got: ' + self.properties['Type'])

		except Exception as e:
			raise e
	def SortSelf(self):
		self.sections.sort()
	def __lt__(self, other):
		y1, m1, d1 = [int(x) for x in self.properties['Date'].split('/')]
		y2, m2, d2 = [int(x) for x in other.properties['Date'].split('/')] 
		return date(y1, m1, d1) < date(y2, m2, d2)

	def __del__(self):
		self.file = open(self.dir + 'properties.json', 'w+')
		json.dump(properties, self.file)
		self.file.close()
		
		

def properties(Title, Type, Date, Author):
	data = {
		"Title" : 	Title,
		"Type" : 	Type,
		"Date" : 	Date,
		"Author" : 	Author
	}
	return data

if __name__ == '__main__':
	NotebookDir = '/home/admin/Desktop/zeszyt/'
	Note = Notebook(NotebookDir)
	print(Note.sections)