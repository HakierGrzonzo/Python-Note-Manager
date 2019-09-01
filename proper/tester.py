import FileHandler as fh
from datetime import *

author = 'HakierGrzonzo'
currentFolder = None

def today():
	date = datetime.now()
	datestr = str(date.day) + '/' + str(date.month) + '/' + str(date.year)
	return datestr

def DoNew(command):
	"""Syntax: new {type of folder} {title}"""
	global currentFolder

	if not len(command) >=  3:
		print('Invalid syntax, use: new {type of folder} {title}')

	else: 
		properties = fh.properties(command[2], command[1], today(), author)

		if currentFolder == None:
			if command[2][0] == '/':
				dir = command[2]
			else:
				dir = './' + command[2]
		else:
			dir = currentFolder.dir + '/' + command[2]

		try:
			currentFolder = fh.Folder(dir, MakeNew = True, properties = properties, parent = currentFolder)
			if not currentFolder.parent == None:
				currentFolder.parent.Scan()

			print('succesfuly created ' + command[1] + ' named: ' + command[2])

		except Exception as e:
			raise e
		
def DoOpen(command):
	global currentFolder
	previousFolder = currentFolder
	try:
		if currentFolder == None:
			currentFolder = fh.Folder('./' + command[1])
		else:
			currentFolder = fh.Folder(previousFolder.dir + '/' + command[1], parent = previousFolder)
	except Exception as e:
		currentFolder = previousFolder
		if type(e) == FileNotFoundError:
			print('specified object does not exist')
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

		

def main():
	global currentFolder
	while True:
		command = input(ShellString()+': ')
		if command == 'exit':
			break
		command = command.split(' ')
		command[0].cllower
		if command[0] == 'new':
			DoNew(command)
		elif command[0] == 'open':
			DoOpen(command)
		elif command[0] == '..':
			currentFolder = currentFolder.parent
		elif command[0] == 'list':
			DoList()
		else:
			print('Invalid command')



if __name__ == '__main__':
	print('Python Note Organizer:')
	main()
	print('exited succesfuly!')
