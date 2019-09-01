import curses, json, operator, os
import FileStrucHandler as Files
import datetime



def init():
	con = curses.initscr()
	curses.curs_set(0)
	maxY, maxX = con.getmaxyx()
	name = 'Python Note Organizer'
	center = int(maxX / 2)
	i = 0
	curses.noecho()
	curses.cbreak()
	con.keypad(False)
	con.clear()

	for x in range(maxX):
		if (x < center - int(len(name) / 2)):
			con.addstr(0, x, ' ', curses.A_REVERSE)
		elif (x > center + int(len(name) / 2)):
			con.addstr(0, x, ' ', curses.A_REVERSE)
		else:
			con.addstr(0, x, name[i], curses.A_REVERSE)
			i = i+1

	con.refresh()

	return curses.newwin(maxY - 1, maxX, 1, 0)

def deinit(con):
	curses.nocbreak()
	con.keypad(False)
	curses.echo()
	curses.endwin()

def getInput(con, posX, posY, normal = None):
	curses.curs_set(1)
	con.keypad(True)

	if not normal == None:
		string = normal
		con.addstr(posY, posX, string)
		con.refresh()
	else:
		string = str()

	
	"""
	while True:
		chra = con.getch()
		if chr(chra) =='\n':
			break
		else:
			string = string + chr(chra)
			con.addstr(posY, posX, string)
			con.refresh()
	"""
	con.keypad(False)
	curses.curs_set(0)
	return string

def GetChar(con, keys):
	while True:
		key = con.getkey()
		if key in keys:
			break
	return key

def GetNum(con, i):
	while True:
		try:
			z = int(con.getkey())
			if (z <= i) and not(z == 0):
				break
		except Exception as e:
			pass

def NumberMenu(con, x, y, options):
	i = 1
	for option in options:
		con.addstr(y + i - 1, x, str(i) + '. ' + option)
		i = i + 1
	con.refresh()
	return GetNum(con, i-1)

def option(con, text, x,y, pos = 0):
	if pos == 0:
		con.addstr(y, x, text[0], curses.A_REVERSE)
		con.addstr(y,x+1,text[1:])
	else:
		con.addstr(y, x, text[:pos-1])
		con.addstr(y, x + pos, text[pos], curses.A_REVERSE)
		con.addstr(y, x + pos + 1, text[pos+1:])

def MainMenu(con):
	def Logo(con, x, y):
		i = 0
		logo = [
			' _____  _   _  ____  ',
			'|  __ \\| \\ | |/ __ \\ ',
			'| |__) |  \\| | |  | |',
			'|  ___/| . ` | |  | |',
			'| |    | |\\  | |__| |',
			'|_|    |_| \\_|\\____/ '
		]
		for line in logo:
			con.addstr(y + i, x, line)
			i = i+1

	con.border()
	if FirstTime:
		con.addstr(1,1, 'Hello new user! Please visit settings')
	else:
		con.addstr(1,1, 'Welcome back ' + perferences["username"] + '!')
	Logo(con, 3,3)
	option(con, 'New Notebook',4,10)
	option(con, 'Open Notebook',4,12)

	if not FirstTime:
		option(con,'Open Recent ' + perferences["LastName"],4,13, pos = 5)
		con.addstr(14,4,'in '+perferences["LastDIR"])
		option(con,'Settings',4,16)
	else:
		option(con,'Settings',4,15)
	con.refresh()
	if  not FirstTime:
		return GetChar(con, ['n','o','r','s','N','O','R','S'])
	else:
		return GetChar(con, ['n','o','s','N','O','S'])

def settingsUI(con, perferences):
	maxY, maxX = con.getmaxyx()
	Limiter = 5
	con.clear()
	con.border()
	selected = 0
	while True:
		key = con.getkey()
		con.addstr(1,1,str(key))
		con.refresh()
		if key == curses.KEY_BACKSPACE:
			break
		con.getkey()
		break		

def selector(con, arr):
	con.keypad(True)
	select = 0
	while True:
		con.clear()
		y = 0
		for item in arr:
			if y == select:
				con.addstr(y, 0, item, curses.A_REVERSE)
			else:
				con.addstr(y,0,item)
			y = y + 1

		con.refresh()
		chra = con.getch()

		if chr(chra) == '\n':
			break
		elif chra == curses.KEY_UP:
			if not select == 0:
				select = select - 1
		elif chra == curses.KEY_DOWN:
			if not select == len(arr) - 1:
				select = select + 1
	con.keypad(False)
	return select

def openNotebook(con, book):
	con.clear()
	maxY, maxX = con.getmaxyx()
	selectcon = curses.newwin(maxY - 2, maxX, 2, 1)
	con.addstr(0,0,'Browsing '+book.properties['Title'])

	arr = list()
	for section in book.sections:
		arr.append(section.properties['Title'])

	select = selector(selectcon, arr)



def MakeBook(con, perferences):
	def MakebookDialog(con):
		con.clear()
		con.addstr(1,1,'Enter Title:')
		con.refresh()
		Title = getInput(con, 1,2)
		con.addstr(3,1,'Enter dir to save Notebook in:')
		con.refresh()
		Dir = getInput(con, 1, 4, normal = os.path.expanduser('~/PNO/' + Title))
		return Title, Dir

	date = datetime.datetime.now()
	datestr = str(date.year) + '-' + str(date.month) + '-' + str(date.day)
	Title, Dir = MakebookDialog(con)
	return Files.Notebook(Dir, MakeNew = True, properties = Files.properties(Title, 'Notebook', datestr, perferences['username']))




def main(con):
	con.clear()
	key = MainMenu(con)
	if key == 'n' or key == 'N':
		OpenBook(con, MakeBook(con, perferences))
	elif key == 'o' or key == 'O':
		pass
	elif key == 'r' or key == 'R':
		pass
	else:
		settingsUI(con, perferences)


if __name__ == '__main__':

	try:
		perferencesFile = 'perferences.json'
		perferences = json.load(open(perferencesFile,'r'))
		FirstTime = False
	except Exception as e:
		print(e)
		FirstTime = True

	con = init()

	MakeBook(con,perferences)
	#main(con)
	con.getkey()
	deinit(con)
	print(selector)
