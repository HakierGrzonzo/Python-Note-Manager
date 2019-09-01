from FileStrucHandler import *
import datetime
import traceback



def DoNew(command):

	date = datetime.datetime.now()
	datestr = str(date.year) + '-' + str(date.month) + '-' + str(date.day)
	try:
		if command[1] == 'notebook':
			prop = properties(command[2], 'Notebook', datestr, 'Prof. Proof')
			book = Notebook('./' + command[2], MakeNew = True, properties = prop)
		elif command[1] == 'section':
			prop = properties(command[2], 'Section', datestr, 'Prof. Proof')
			section = Section(book.dir + command[2], MakeNew = True, properties = prop)
			book = Notebook(book.dir)
		elif command[1] == 'subsection':
			prop = properties(command[2], 'SubSection', datestr, 'Prof. Proof')
			subsection = SubSection(section.dir + command[2], MakeNew = True, properties = prop)
			section = Section(section.dir)
			book = Notebook(book.dir)
		elif command[1] == 'page':
			prop = properties(command[2], 'Page', datestr, 'Prof. Proof')
			page = Page(subsection.dir + command[2], MakeNew = True, properties = prop)
			subsection = SubSection(subsection.dir)
			section = Section(section.dir)
			book = Notebook(book.dir)
		print('success!')
	except Exception as e:
		traceback.print_exc()
		print('An error accured: ' + str(e))

	

book = None
section = None
subsection = None
page = None

def main():
	print('Proof of concept: PNO')
	while True:
		command = input('> ')
		command.lower()

		if command =='exit':
			break

		command = command.split(' ')
		if command[0] == 'new':
			DoNew(command)
		elif command[0] == 'list':
			DoList(command)
		elif command[0] == 'open':
			DoOpen(command)
		elif command[0] == 'help':
			print('no help for you')
			break

if __name__ == '__main__':
 	main()

