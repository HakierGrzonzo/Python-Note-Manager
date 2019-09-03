import FileHandler as fh
from datetime import *
import os

author = 'HakierGrzonzo'
currentFolder = None
NoteDir = os.path.expanduser('~/PNO/Notebooks/')
TemplateDir = os.path.expanduser('~/PNO/templates')

def initialize():
	try:
		os.mkdir(NoteDir)
	except Exception as e:
		pass
	try:
		os.mkdir(TemplateDir)
	except Exception as e:
		pass

def today():
	date = datetime.now()
	datestr = str(date.day) + '/' + str(date.month) + '/' + str(date.year)
	return datestr

def DoNew(command):
	"""Syntax: new {type of folder} {title}"""
	global currentFolder
	global NoteDir

	split = command[1].split(' ', 1)

	command = [command[0], split[0], split[1]]

	if command[1] == 'page':
		path = 'page' + str(len(currentFolder.folders))
	else:
		path = command[2]

	if not len(command) >=  3:
		print('Invalid syntax, use: new {type of folder} {title}')

	else: 
		properties = fh.properties(command[2], command[1], today(), author)

		if currentFolder == None:
			dir = NoteDir + path 
		else:
			dir = currentFolder.dir + '/' + path

		try:
			currentFolder = fh.Folder(dir, MakeNew = True, properties = properties, parent = currentFolder)
			if not currentFolder.parent == None:
				currentFolder.parent.Scan()

			print('succesfuly created ' + command[1] + ' named: ' + command[2])

		except Exception as e:
			raise e
		
def DoOpen(command):
	global currentFolder
	global NoteDir

	previousFolder = currentFolder
	try:
		if currentFolder == None:
			currentFolder = fh.Folder(NoteDir + command[1])
		else:
			currentFolder = fh.Folder(previousFolder.dir + '/' + command[1], parent = previousFolder)
	except Exception as e:
		currentFolder = previousFolder
		if type(e) == FileNotFoundError:
			print('specified object does not exist')
			print(e)
		else:
			raise e

def getPosition():
	global currentFolder
	if currentFolder == None:
		return None
	else:
		folder = currentFolder
		folderList = list()
		while True:
			folderList.append(folder.properties['Title'])
			if not folder.parent == None:
				folder = folder.parent
			else:
				break
		folderList.reverse()
		return folderList

def ShellString():
	position = getPosition()
	if not position == None:
		string = str()
		for folder in position:
			string = string + folder + '/'
		return string
	else:
		return str()

def DoList():
	global currentFolder
	if len(currentFolder.folders) > 0:
		print('Folders: ')
		for folder in currentFolder.folders:
			print('  ' + folder.properties['Title'])
	if len(currentFolder.files) > 0:
		print('Files: ')
		for file in currentFolder.files:
			print('  ' + file)

def DoMake(command):
	global currentFolder
	fh.MakeTemplate(command[1] + '.tex', currentFolder)

def main():
	global currentFolder
	while True:
		command = input(ShellString()+': ')
		if command == 'exit':
			break
		command = command.split(' ', 1)
		command[0].lower
		if command[0] == 'new':
			DoNew(command)
		elif command[0] == 'open':
			DoOpen(command)
		elif command[0] == '..':
			currentFolder = currentFolder.parent
		elif command[0] == 'list':
			DoList()
		elif command[0] == 'make':
			DoMake(command)
		else:
			print('Invalid command')



if __name__ == '__main__':
	initialize()
	print('Python Note Organizer:')
	main()
	print('exited succesfuly!')
