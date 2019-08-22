import curses, json, operator
import FileStrucHandler as Files



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

def getInput(con, posX, posY):
	string = str()
	while True:
		chra = con.getkey()
		if chra =='\n':
			break
		else:
			string = string + str(chra)
			con.addstr(posY, posX, string)
			con.refresh()
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

def openNotebook(con, book):
	y = 0
	maxY = con.getmaxyx()
	con.clear()
	con.addstr(0,0,book.properties['Title'])

	SectionPerferences = list()
	SectionList = list()
	for section in book.sections:
		SectionPerferences.append(section.perferences)
		SectionList.append(section)

	SectionPerferences.sort(key=lambda x:x['date'])



def main(con):
	con.clear()
	key = MainMenu(con)
	if key == 'n' or key == 'N':
		pass
	elif key == 'o' or key == 'O':
		pass
	elif key == 'r' or key == 'R':
		pass
	else:
		settingsUI(con, perferences)


if __name__ == '__main__':
	try:
		perferencesFile = '/home/admin/Desktop/programy/PyMen/perferences.json'
		perferences = json.load(open(perferencesFile,'r'))
		FirstTime = False
	except Exception as e:
		print(e)
		FirstTime = True
	
	con = init()
	main(con)
	con.getkey()
	deinit(con)
	print('exited correctly')
