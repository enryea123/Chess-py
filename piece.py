import board

class piece():
	def getx(self):
		return self.x
	def gety(self):
		return self.y
	def getcolor(self):
		return self.color
	def getid(self):
		return self.iD
	def getname(self):
		return self.name
	def getvalue(self):
		return self.value
	def setposition(self,x,y):
		self.BD.fillcell(self.x,self.y,0)
		self.x=x
		self.y=y
		self.BD.fillcell(x,y,self.color*self.iD)

################################################################################
class empty(piece):
	def __init__(self,x,y,BD):
		self.x=x
		self.y=y
		self.color=0
		self.value=0
		self.iD=0
		self.name="Empty cell"
		BD.fillcell(x,y,0)


################################################################################
class pawn(piece):
	def __init__(self,x,y,color,BD):
		self._n=8
		self.x=x
		self.y=y
		self.color=color
		self.value=1.
		self.iD=1
		self.name="Pawn"
		self.BD=BD
		self.BD.fillcell(x,y,color*self.iD)

	def move(self):
		allowed=[]
		protect=[]

		if(self.y+self.color<self._n and self.y+self.color>=0):
			if(self.BD.verifycell(self.x,self.y+self.color)==0):
				allowed.append([self.x,self.y+self.color])

			if(self.x+1<self._n):
				if(self.BD.verifycell(self.x+1,self.y+self.color)==-self.color):
					allowed.append([self.x+1,self.y+self.color])
				else:
					protect.append([self.x+1,self.y+self.color])

			if(self.x-1>=0):
				if(self.BD.verifycell(self.x-1,self.y+self.color)==-self.color):
					allowed.append([self.x-1,self.y+self.color])
				else:
					protect.append([self.x-1,self.y+self.color])

		if((self.y==1 and self.color==1) or (self.y==6 and self.color==-1)):
			if(self.BD.verifycell(self.x,self.y+self.color)==0 and self.BD.verifycell(self.x,self.y+2*self.color)==0):
				allowed.append([self.x,self.y+2*self.color])

		return allowed, protect


################################################################################
class knight(piece):
	def __init__(self,x,y,color,BD):
		self._n=8
		self.x=x
		self.y=y
		self.color=color
		self.value=3.01
		self.iD=2
		self.name="Knight"
		self.BD=BD
		self.BD.fillcell(x,y,color*self.iD)

	def move(self):
		allowed=[]
		protect=[]

		for i in range(-2,3):
			for j in range(-2,3):
				if(i!=0 and j!=0 and i!=j and i!=-j):
					x0=self.x+i
					y0=self.y+j
					if(x0<self._n and x0>=0 and y0<self._n and y0>=0):
						if(self.BD.verifycell(x0,y0)!=self.color):
							allowed.append([x0,y0])
						else:
							protect.append([x0,y0])

		return allowed, protect


################################################################################
class bishop(piece):
	def __init__(self,x,y,color,BD):
		self._n=8
		self.x=x
		self.y=y
		self.color=color
		self.value=3.02
		self.iD=3
		self.name="Bishop"
		self.BD=BD
		self.BD.fillcell(x,y,color*self.iD)

	def move(self):
		d=0
		allowed=[]
		protect=[]

		direction=[False for i in range(self._n)]

		for s in range(-1,2):
			for t in range(-1,2):
				if(s!=0 and t!=0):
					for i in range(1,self._n):

						x0=self.x+i*s
						y0=self.y+i*t
						if(x0<self._n and x0>=0 and y0<self._n and y0>=0 and direction[d]==False):
							if(self.BD.verifycell(x0,y0)!=self.color):
								allowed.append([x0,y0])
								if(self.BD.verifycell(x0,y0)==-self.color):
									direction[d]=True
							else:
								protect.append([x0,y0])
								direction[d]=True
					d+=1

		return allowed, protect


################################################################################
class rook(piece):
	def __init__(self,x,y,color,BD):
		self._n=8
		self.x=x
		self.y=y
		self.color=color
		self.value=5.
		self.iD=4
		self.name="Rook"
		self.BD=BD
		self.BD.fillcell(x,y,color*self.iD)

	def move(self):
		d=0
		allowed=[]
		protect=[]

		direction=[False for i in range(self._n)]

		for s in range(-1,2):
			for t in range(-1,2):
				if((s==0 and t!=0) or (s!=0 and t==0)):
					for i in range(1,self._n):

						x0=self.x+i*s
						y0=self.y+i*t
						if(x0<self._n and x0>=0 and y0<self._n and y0>=0 and direction[d]==False):
							if(self.BD.verifycell(x0,y0)!=self.color):
								allowed.append([x0,y0])
								if(self.BD.verifycell(x0,y0)==-self.color):
									direction[d]=True
							else:
								protect.append([x0,y0])
								direction[d]=True
					d+=1

		return allowed, protect


################################################################################
class queen(piece):
	def __init__(self,x,y,color,BD):
		self._n=8
		self.x=x
		self.y=y
		self.color=color
		self.value=9.
		self.iD=5
		self.name="Queen"
		self.BD=BD
		self.BD.fillcell(x,y,color*self.iD)

	def move(self):
		d=0
		allowed=[]
		protect=[]

		direction=[False for i in range(self._n)]
		for s in range(-1,2):
			for t in range(-1,2):
				if not(s==0 and t==0):
					for i in range(1,self._n):

						x0=self.x+i*s
						y0=self.y+i*t
						if(x0<self._n and x0>=0 and y0<self._n and y0>=0 and direction[d]==False):

							if(self.BD.verifycell(x0,y0)!=self.color):
								allowed.append([x0,y0])
								if(self.BD.verifycell(x0,y0)==-self.color):
									direction[d]=True
							else:
								protect.append([x0,y0])
								direction[d]=True
					d+=1

		return allowed, protect


################################################################################
class king(piece):
	def __init__(self,x,y,color,BD):
		self._n=8
		self.x=x
		self.y=y
		self.color=color
		self.value=10000.
		self.iD=6
		self.name="King"
		self.BD=BD
		self.BD.fillcell(x,y,color*self.iD)

	def move(self):
		d=0
		allowed=[]
		protect=[]

		direction=[False for i in range(self._n)]

		for s in range(-1,2):
			for t in range(-1,2):
				if not(s==0 and t==0):
					for i in range(1,2):

						x0=self.x+i*s
						y0=self.y+i*t
						if(x0<self._n and x0>=0 and y0<self._n and y0>=0 and direction[d]==False):
							if(self.BD.verifycell(x0,y0)!=self.color):
								allowed.append([x0,y0])
								if(self.BD.verifycell(x0,y0)==-self.color):
									direction[d]=True
							else:
								protect.append([x0,y0])
								direction[d]=True
					d+=1

		return allowed, protect

################################################################################

