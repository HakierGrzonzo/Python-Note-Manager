 import curses

 class CursesWidget(object):
 	"""docstring for CursesWidget"""
 	def __init__(self, con, posX, posY):
 		super(CursesWidget, self).__init__()
 		self.posX = posX
 		self.posY = posY
 		self.con = con

 	def Draw():
 		pass

class Header(CursesWidget):
	"""docstring for Header"""
	def __init__(self, con, posX, posY, title, maxX = None):
		super(Header, self).__init__(con, posX, posY)
		self.title = title
		if maxX == None:
			maxY, maxX = self.con.getmaxyx()
		self.maxX = maxX
		self.Draw()

	def Draw():
		name = self.title
		i = 0
		for x in range(self.posX, self.maxX):
			if (x < center - int(len(name) / 2)):
				self.con.addstr(0, x, ' ', curses.A_REVERSE)
			elif (x > center + int(len(name) / 2)):
				self.con.addstr(0, x, ' ', curses.A_REVERSE)
			else:
				self.con.addstr(0, x, name[i], curses.A_REVERSE)
				i = i+1
		
 		
