import FileHandler as fh
from datetime import datetime
import os
import prompt_toolkit as pt
from fuzzyfinder import fuzzyfinder

author = 'HakierGrzonzo'
currentFolder = None
NoteDir = os.path.expanduser('~/PNO/Notebooks/')
TemplateDir = os.path.expanduser('~/PNO/templates')

PNOkeywords = ['open', 'list', 'make', 'markdown', 'section', 'page', 'subsection', 'new', 'exit']

class PNOCompleter(pt.completion.Completer):

    def get_completions(self, document, complete_event):
        global currentFolder
        if not currentFolder == None:
            additionalKeys = [f.properties['Title'] for f in currentFolder.folders]
        else:
            additionalKeys = list()
        word_before_cursor = document.get_word_before_cursor( WORD = True)
        matches = fuzzyfinder(word_before_cursor, [*PNOkeywords, *additionalKeys])
        
        for m in matches:
            yield pt.completion.Completion(m, start_position = -len(word_before_cursor))

def shortText(text, limit):
	if len(text) > limit + 4 and limit > 4:
		text = text[:limit] + '...'
	return text

def initialize():
	try:
		os.mkdir(os.path.expanduser('~/PNO/'))
	except Exception as e:
		pass
	try:
		os.mkdir(NoteDir)
	except:
		pass
	try:
		os.mkdir(TemplateDir)
	except:
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

	try:
		number = int(command[1])
		if not number > len(currentFolder.folders):
			currentFolder = currentFolder.folders[number - 1]
			if currentFolder.properties['Type'] != 'page':
					DoList()

	except Exception as e:
		previousFolder = currentFolder
		try:

			if currentFolder == None:
				currentFolder = fh.Folder(NoteDir + command[1])
				if currentFolder.properties['Type'] != 'page':
					DoList()

			else:

				done = False
				for folder in currentFolder.folders:
					if folder.properties['Title'] == command[1]:
						currentFolder = folder
						done = True
						break

				if not done:
					currentFolder = fh.Folder(NoteDir + currentFolder.dir + command[1], parent = previousFolder)

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
			string += '/' + shortText(folder, 25)
		return string + ': '
	else:
		return ': '

def DoList():
	global currentFolder
	didSth = False

	if len(currentFolder.folders) > 0:
		didSth = True
		print('Folders: ')
		x = 1

		for folder in currentFolder.folders:
			print('  '+ str(x) + '. ' + shortText(folder.properties['Title'], 80))
			x = x+1

	if len(currentFolder.files) > 0:
		didSth = True
		print('Files: ')
		for file in currentFolder.files:
			print('  ' + file)

	if not didSth:
		print('wow such empty')

def DoMake(command):
	global currentFolder
	try:
		command = command[1].split(' ')
		if (len(command) > 1):
			fh.MakeTemplate(command[0], currentFolder, extension = command[1])
		else:
			fh.MakeTemplate(command[0], currentFolder)
	except Exception as e:
		print(e)

def main():
	global currentFolder
        
	session = pt.PromptSession()
	while True:
		command = session.prompt( ShellString(), completer = PNOCompleter() )
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
