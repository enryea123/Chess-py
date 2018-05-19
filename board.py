import sys

class board():
	def __init__(self):
		self._n=8
		self.matrixboard=[[0 for i in range(self._n)] for j in range(self._n)]


	def cellname(self,x,y):
		if(x>7 or x<0 or y>7 or y<0):
			print "Error 0"
		else:
			if x==0:
				print "A%s" % str(y+1),
			elif x==1:
				print "B%s" % str(y+1),
			elif x==2:
				print "C%s" % str(y+1),
			elif x==3:
				print "D%s" % str(y+1),
			elif x==4:
				print "E%s" % str(y+1),
			elif x==5:
				print "F%s" % str(y+1),
			elif x==6:
				print "G%s" % str(y+1),
			elif x==7:
				print "H%s" % str(y+1),
			else:
				print "Cell Error"


	def printboard(self):
		count=0

		print " _ _______________________________________________ "
		print "| |     |     |     |     |     |     |     |     |"
		print "|8|",
		for i in range(self._n-1,-1,-1):
			for j in range(self._n):

				if(count>=self._n):
					print ""
					print "|_|_____|_____|_____|_____|_____|_____|_____|_____|"
					print "| |     |     |     |     |     |     |     |     |"
					print "|%s|" % str(i+1),
					count=0

				count+=1

				if(self.matrixboard[j][i]<0):
					sys.stdout.write(" -")
				else:
					sys.stdout.write("  ")

				if abs(self.matrixboard[j][i])==0:
					print "   |",
				elif abs(self.matrixboard[j][i])==1:
					print "p  |",
				elif abs(self.matrixboard[j][i])==2:
					print "k  |",
				elif abs(self.matrixboard[j][i])==3:
					print "B  |",
				elif abs(self.matrixboard[j][i])==4:
					print "R  |",
				elif abs(self.matrixboard[j][i])==5:
					print "Q  |",
				elif abs(self.matrixboard[j][i])==6:
					print "Ki |",
				else:
					print "Board Error"
					break

		print ""
		print "|_|_____|_____|_____|_____|_____|_____|_____|_____|"
		print "  |__A__|__B__|__C__|__D__|__E__|__F__|__G__|__H__|"
		print ""


	def printboard_small(self):
		count=0

		print " _ _________________________________ "
		print "| |                                 |"
		print "|8|",
		for i in range(self._n-1,-1,-1):
			for j in range(self._n):

				if(count>=self._n):
					print "|"
					print "| |                                 |"
					print "|%s|" % str(i+1),
					count=0

				count+=1

				if(self.matrixboard[j][i]<0):
					sys.stdout.write(" -")
				else:
					sys.stdout.write("  ")

				if abs(self.matrixboard[j][i])==0:
					print ". ",
				elif abs(self.matrixboard[j][i])==1:
					print "p ",
				elif abs(self.matrixboard[j][i])==2:
					print "k ",
				elif abs(self.matrixboard[j][i])==3:
					print "B ",
				elif abs(self.matrixboard[j][i])==4:
					print "R ",
				elif abs(self.matrixboard[j][i])==5:
					print "Q ",
				elif abs(self.matrixboard[j][i])==6:
					print "Ki",
				else:
					print "Board Error"
					break

		print "|"
		print "|_|_________________________________|"
		print "  |__A___B___C___D___E___F___G___H__|"
		print ""


	def printnumbers(self):
		count=0

		print " _ _________________________________ "
		print "| |                                 |"
		print "|8|",
		for i in range(self._n-1,-1,-1):
			for j in range(self._n):

				if(count>=self._n):
					print "|"
					print "| |                                 |"
					print "|%s|" % str(i+1),
					count=0

				count+=1

				if(self.matrixboard[j][i]>=0):
					print "",
				if(self.matrixboard[j][i]==0):
					print" .",
				else:
					print " %s" % str(self.matrixboard[j][i]),

		print "|"
		print "|_|_________________________________|"
		print "  |__A___B___C___D___E___F___G___H__|"
		print ""


	def fillcell(self,x,y,Z):
		if(x<self._n and x>=0 and y<self._n and y>=0):
			self.matrixboard[x][y]=Z


	def verifycell(self,x,y):
		if(x<self._n and x>=0 and y<self._n and y>=0):
			if(self.matrixboard[x][y]>0):
				return 1
			elif(self.matrixboard[x][y]<0):
				return -1
			else:
				return 0


	def verifypiece(self,x,y):
		if(x<self._n and x>=0 and y<self._n and y>=0):
			return abs(self.matrixboard[x][y])


	def getboard(self,x,y):
		if(x<self._n and x>=0 and y<self._n and y>=0):
			return self.matrixboard[x][y]


	def compare(self,B):
		equality=True
		for i in range(self._n):
			for j in range(self._n):
				if(self.matrixboard[i][j]!=B.getboard(i,j)):
					equality=False
		return equality

