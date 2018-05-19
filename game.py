import sys
import piece
import board

def bigger(a,b):
	if(abs(a)>=abs(b)):
		return abs(a)
	else:
		return abs(b)

################################################################################
class game():
	def __init__(self):
		self._n=8
		self.checkmate=False
		self.stalmate=False
		self.draw=False

		self.passant_=False
		self.passant=[-1,-1]
		self.N_50draw=0
		self.castle_spoiler=[False for i in range(4)]
		self.BD=board.board()
		self.BD_old1=board.board()
		self.BD_old2=board.board()
		self.N_3rep=0

		self.chessboard=[[piece.empty(i,j,self.BD) for i in range(self._n)] for j in range(self._n)]

		# white pieces
		self.chessboard[0][0]=piece.rook(0,0,1,self.BD)
		self.chessboard[1][0]=piece.knight(1,0,1,self.BD)
		self.chessboard[2][0]=piece.bishop(2,0,1,self.BD)
		self.chessboard[3][0]=piece.queen(3,0,1,self.BD)
		self.chessboard[4][0]=piece.king(4,0,1,self.BD)
		self.chessboard[5][0]=piece.bishop(5,0,1,self.BD)
		self.chessboard[6][0]=piece.knight(6,0,1,self.BD)
		self.chessboard[7][0]=piece.rook(7,0,1,self.BD)

		self.chessboard[0][1]=piece.pawn(0,1,1,self.BD)
		self.chessboard[1][1]=piece.pawn(1,1,1,self.BD)
		self.chessboard[2][1]=piece.pawn(2,1,1,self.BD)
		self.chessboard[3][1]=piece.pawn(3,1,1,self.BD)
		self.chessboard[4][1]=piece.pawn(4,1,1,self.BD)
		self.chessboard[5][1]=piece.pawn(5,1,1,self.BD)
		self.chessboard[6][1]=piece.pawn(6,1,1,self.BD)
		self.chessboard[7][1]=piece.pawn(7,1,1,self.BD)

		# black pieces
		self.chessboard[0][7]=piece.rook(0,7,-1,self.BD)
		self.chessboard[1][7]=piece.knight(1,7,-1,self.BD)
		self.chessboard[2][7]=piece.bishop(2,7,-1,self.BD)
		self.chessboard[3][7]=piece.queen(3,7,-1,self.BD)
		self.chessboard[4][7]=piece.king(4,7,-1,self.BD)
		self.chessboard[5][7]=piece.bishop(5,7,-1,self.BD)
		self.chessboard[6][7]=piece.knight(6,7,-1,self.BD)
		self.chessboard[7][7]=piece.rook(7,7,-1,self.BD)

		self.chessboard[0][6]=piece.pawn(0,6,-1,self.BD)
		self.chessboard[1][6]=piece.pawn(1,6,-1,self.BD)
		self.chessboard[2][6]=piece.pawn(2,6,-1,self.BD)
		self.chessboard[3][6]=piece.pawn(3,6,-1,self.BD)
		self.chessboard[4][6]=piece.pawn(4,6,-1,self.BD)
		self.chessboard[5][6]=piece.pawn(5,6,-1,self.BD)
		self.chessboard[6][6]=piece.pawn(6,6,-1,self.BD)
		self.chessboard[7][6]=piece.pawn(7,6,-1,self.BD)

		self.BD.printboard()

	def start(self):
		while(True):
			self.turn(1)
			self.turn(-1)

			self.threefold()
			if(self.checkmate==True):
				print "Checkmate!"
			if(self.stalmate==True):
				print "Stalmate!"
			if(self.draw==True):
				print "Draw!"
			if(self.checkmate==True or self.stalmate==True or self.draw==True):
				break


	def turn(self,color):

		N_checks=0
		N_defs=0

		pieces=[]
		enemies=[]
		checkenemies=[]

		xking=-1
		yking=-1

		#----------------------------------------------------------------------------------#
		#------------------- Find the pieces, the king and the enemies --------------------#
		#----------------------------------------------------------------------------------#
		for i in range(self._n):
			for j in range(self._n):
				if(self.chessboard[i][j].getcolor()==color):
					pieces.append(self.chessboard[i][j])
					if(self.chessboard[i][j].getid()==6):
						xking=i
						yking=j
				elif(self.chessboard[i][j].getcolor()==-color):
					enemies.append(self.chessboard[i][j])

		self.parity_verify(pieces,enemies)	# check if it is a draw

		#----------------------------------------------------------------------------------#
		#-------------- Save the dangerous cells and control if it is check ---------------#
		#----------------------------------------------------------------------------------#

		dangermatrix=board.board()	# checks matrix
		self.chessboard[xking][yking]=piece.empty(xking,yking,self.BD)	# temporarely empty the king cell (king can't hide behind itself)

		for i in range(self._n):
			for j in range(self._n):
				if(self.chessboard[i][j].getcolor()==-color):
					if(self.chessboard[i][j].getid()!=1):	# exclude piece.pawns for now
						for l in range(2):
							for k in range(len(self.chessboard[i][j].move()[l])):
								dangermatrix.fillcell(self.chessboard[i][j].move()[l][k][0],self.chessboard[i][j].move()[l][k][1],dangermatrix.verifycell(self.chessboard[i][j].move()[l][k][0],self.chessboard[i][j].move()[l][k][1])+1)

								if(self.chessboard[i][j].move()[l][k][0]==xking and self.chessboard[i][j].move()[l][k][1]==yking):
									checkenemies.append(self.chessboard[i][j])
									N_checks+=1

					else:	# check and dangermatrix by piece.pawns
						if(j-color>=0 and j-color<self._n and i+1>=0 and i+1<self._n):
							dangermatrix.fillcell(i+1,j-color,dangermatrix.verifycell(i+1,j-color)+1)
						if(j-color>=0 and j-color<self._n and i-1>=0 and i-1<self._n):
							dangermatrix.fillcell(i-1,j-color,dangermatrix.verifycell(i-1,j-color)+1)

						for s in range(-1,2,2):
							if(i+s==xking and j-color==yking):	# piece.pawns giving check are here
								checkenemies.append(self.chessboard[i][j])
								N_checks+=1

		self.chessboard[xking][yking]=piece.king(xking,yking,color,self.BD)	# fill again the king cell

		if(N_checks>0):
			print "Check by",
			for i in range(N_checks):
				print checkenemies[i].getname(),
				self.BD.cellname(checkenemies[i].getx(),checkenemies[i].gety())
				if(N_checks>1 and i==0):
					print " and",

			print ""


		#----------------------------------------------------------------------------------#
		#---------------------------- Look for locked pieces ------------------------------#
		#----------------------------------------------------------------------------------#

		locked=[]	# locked pieces that cover the king from a check
		lockcells=[]	# moves of the locked pieces along the covering direction are allowed
		lockmove=[]

		for s in range(-1,2):
			for t in range(-1,2):
				if not(s==0 and t==0):
					direction=False
					for d in range(self._n,0,-1):
						for i in range(len(enemies)):
							if(enemies[i].getx()==xking+s*d and enemies[i].gety()==yking+t*d):
								if(enemies[i].getid()!=2 and enemies[i].getid()!=6 and enemies[i].getid()!=1):
									direction=True

							if(direction==True):

								if(len(lockcells)==0):
									lockcells.append([xking+s*d,yking+t*d])
								if(len(lockcells)>0 and lockcells[-1]!=[xking+s*d,yking+t*d]):
									lockcells.append([xking+s*d,yking+t*d])

								for j in range(len(pieces)):
									if(pieces[j].getx()==xking+s*d and pieces[j].gety()==yking+t*d):
										for k in range(len(enemies[i].move()[0])):
											if(enemies[i].move()[0][k][0]==xking+s*d and enemies[i].move()[0][k][1]==yking+t*d):
												behind=True	# check that the cells behind the piece are empty
												while(d>1):	# d>1 because we are checking around the king
													d-=1
													if(len(lockcells)==0):
														lockcells.append([xking+s*d,yking+t*d])
													if(len(lockcells)>0 and lockcells[-1]!=[xking+s*d,yking+t*d]):
														lockcells.append([xking+s*d,yking+t*d])
													if(self.chessboard[xking+s*d][yking+t*d].getid()!=0):
														behind=False
												print lockcells
												if(behind==True):
													locked.append(pieces[j])
													for k1 in range(len(lockcells)):
														for k2 in range(len(locked[-1].move()[0])):
															if(locked[-1].move()[0][k2][0]==lockcells[k1][0] and locked[-1].move()[0][k2][1]==lockcells[k1][1]):
																lockmove.append([len(locked)-1,k2])

		#----------------------------------------------------------------------------------#
		#-------------------- If it is check look for defending pieces --------------------#
		#----------------------------------------------------------------------------------#

		defender=[]	# pieces who can cover the check or take the piece giving check
		defendmove=[]	# moves of the defender pieces

		n=0

		if(N_checks>0):
			for k in range(len(self.chessboard[xking][yking].move()[0])):	# King can run away (it is a defending piece)
				if(dangermatrix.verifycell(self.chessboard[xking][yking].move()[0][k][0],self.chessboard[xking][yking].move()[0][k][1])==0):
					defendmove.append([N_defs,k])
					if(len(defender)==0):
						defender.append(self.chessboard[xking][yking])
					n+=1
			if(n>0):
				N_defs+=1	# adds the king at the list of defenders
			n=0

			if(N_checks==1):	# other pieces can defend only if the check is given by a single enemy piece
				for j in range(len(pieces)):
					for k in range(len(pieces[j].move()[0])):
						if(pieces[j].getid()!=6 and checkenemies[0].getid()!=2):	# if the piece is not a knight
							L=bigger(checkenemies[0].getx()-xking,checkenemies[0].gety()-yking)

							for s in range(-1,2):
								for t in range(-1,2):
									if not(s==0 and t==0):
										direction=False
										for d in range(L,0,-1):	# start from further away and go closer
											if(checkenemies[0].getx()==xking+s*d and checkenemies[0].gety()==yking+t*d):
												direction=True	# the direction is given by (s,t)

											if(direction==True):
												if(pieces[j].move()[0][k][0]==xking+s*d and pieces[j].move()[0][k][1]==yking+t*d):
													if(len(defender)>0 and pieces[j]==defender[-1]):
														N_defs-=1
													else:
														defender.append(pieces[j])
													defendmove.append([N_defs,k])
													N_defs+=1

						elif(pieces[j].getid()!=6 and checkenemies[0].getid()==2):	# if the piece giving check is a knight it can be covered, only taken
							if(pieces[j].move()[0][k][0]==checkenemies[0].getx() and pieces[j].move()[0][k][1]==checkenemies[0].gety()):
								if(len(defender)>0 and pieces[j]==defender[-1]):
									N_defs-=1
								else:
									defender.append(pieces[j])
								defendmove.append([N_defs,k])
								N_defs+=1

			if(N_defs>0):
				pieces=defender
			else:
				self.checkmate=True


		#----------------------------------------------------------------------------------#
		#--------------------------- Search the movable pieces ----------------------------#
		#----------------------------------------------------------------------------------#

		temp=[]	# temporary array to store the pieces that can move
		for j in range(len(pieces)):
			N_moves=0

			if(N_checks==0):
				N_moves=len(pieces[j].move()[0])
			else:
				for w in range(len(defendmove)):
					if(defendmove[w][0]==j):
						N_moves+=1

			if(len(locked)>0):
				for i in range(len(locked)):
					if(pieces[j]==locked[i]):
						N_moves=0
						for w in range(len(lockmove)):
							if(lockmove[w][0]==i):
								N_moves+=1

			if(pieces[j].getid()==6):	# check if the king can move
				N_moves=0
				for k in range(len(pieces[j].move()[0])):
					if(dangermatrix.verifycell(pieces[j].move()[0][k][0],pieces[j].move()[0][k][1])==0):
						if(self.chessboard[pieces[j].move()[0][k][0]][pieces[j].move()[0][k][1]].getid()==0 or self.chessboard[pieces[j].move()[0][k][0]][pieces[j].move()[0][k][1]].getcolor()==-color):
							N_moves+=1

			if(N_moves!=0):
				temp.append(pieces[j])

		if(len(temp)==0 and N_checks==0):	# control if it is stalmate
			self.stalmate=True
		else:
			del pieces
			pieces=temp


		#----------------------------------------------------------------------------------#
		#---------------------------------- Make the move ---------------------------------#
		#----------------------------------------------------------------------------------#

		while(self.checkmate==False and self.stalmate==False and self.draw==False):	# continue until a move is made
			N_moves=0

			#----------------------------------------------------------------------------------#
			#------------------------------- Select the piece ---------------------------------#
			#----------------------------------------------------------------------------------#

			print "Select a piece:",
			for i in range(len(pieces)):
				print pieces[i].getname(),
				self.BD.cellname(pieces[i].getx(),pieces[i].gety())
				sys.stdout.write(" (%s)" % str(i+1))
				if(i<len(pieces)-1):
					print ",",
				else:
					print ":",

			a=-1
			while 1>a or a>len(pieces):
				try:
					a=int(raw_input(""))
					if (1>a or a>len(pieces)):
						print "Select a valid piece:",
				except ValueError:
					print "Select a valid piece:",

			P=pieces[a-1]	# selected piece
			print P.getname(),
			self.BD.cellname(P.getx(),P.gety())
			print "(0) selected:",

			self.enpassant(P,-1,-1,color)	# enpassant prepare

			#----------------------------------------------------------------------------------#
			#--------------------------- Search the allowed moves -----------------------------#
			#----------------------------------------------------------------------------------#

			castle1now=False
			castle2now=False

			if(P.getid()==6):	# If the piece selected is the king N_moves is different
				for k in range(len(P.move()[0])):
					if(self.chessboard[P.move()[0][k][0]][P.move()[0][k][1]].getid()==0 or self.chessboard[P.move()[0][k][0]][P.move()[0][k][1]].getcolor()==-color):
						if(dangermatrix.verifycell(P.move()[0][k][0],P.move()[0][k][1])==0):
							N_moves+=1

				if(N_checks==0):
					if(self.castle_spoiler[0]==False and color==1 or self.castle_spoiler[2]==False and color==-1):
						if(dangermatrix.verifycell(xking+1,yking)==0 and dangermatrix.verifycell(xking+2,yking)==0):	# count short castle move
							if(self.chessboard[xking+1][yking].getid()==0 and self.chessboard[xking+2][yking].getid()==0):
								if(self.chessboard[7][yking].getid()==4 and self.chessboard[7][yking].getcolor()==color):
									N_moves+=1
									castle1now=True

					if(self.castle_spoiler[1]==False and color==1 or self.castle_spoiler[3]==False and color==-1):
						if(dangermatrix.verifycell(xking-1,yking)==0 and dangermatrix.verifycell(xking-2,yking)==0):	# count long castle move
							if(self.chessboard[xking-1][yking].getid()==0 and self.chessboard[xking-2][yking].getid()==0 and self.chessboard[xking-3][yking].getid()==0):
								if(self.chessboard[0][yking].getid()==4 and self.chessboard[0][yking].getcolor()==color):
									N_moves+=1
									castle2now=True


			else:	# calculate the number of moves if the piece is not the king
				if(N_checks==0):
					N_moves=len(P.move()[0])
				else:
					for w in range(len(defendmove)):
						if(defendmove[w][0]==a-1):
							N_moves+=1


			allowed=[]

			if(P.getid()==6):	# if the piece is the king it cannot go in a dangerous cell
				for k in range(len(P.move()[0])):
					if(self.chessboard[P.move()[0][k][0]][P.move()[0][k][1]].getid()==0 or self.chessboard[P.move()[0][k][0]][P.move()[0][k][1]].getcolor()==-color):
						if(dangermatrix.verifycell(P.move()[0][k][0],P.move()[0][k][1])==0):
							allowed.append(P.move()[0][k])

				if(castle1now==True):	# short castle
					allowed.append([6,yking])

				if(castle2now==True):	# long castle
					allowed.append([2,yking])

			else:
				if(N_checks>0):

					for i in range(len(locked)):
						if(P==locked[i]):
							break	# check if it works properly

					for w in range(len(defendmove)):
						if(defendmove[w][0]==a-1):
							allowed.append(P.move()[0][defendmove[w][1]])

				else:

					if(len(locked)>0):
						for i in range(len(locked)):
							if(P==locked[i]):
								N_moves=0
								for w in range(len(lockmove)):
									if(lockmove[w][0]==i):
										allowed.append(P.move()[0][lockmove[w][1]])
										N_moves+=1

							else:
								for i in range(N_moves):
									allowed.append(P.move()[0][i])
					else:
						for i in range(N_moves):
							allowed.append(P.move()[0][i])


			#----------------------------------------------------------------------------------#
			#----------------------------------------------------------------------------------#
			#----------------------------------------------------------------------------------#

			for i in range(N_moves):
				self.BD.cellname(allowed[i][0],allowed[i][1])
				if(self.chessboard[allowed[i][0]][allowed[i][1]].getcolor()==-color):
					sys.stdout.write("->")
				sys.stdout.write(" (%s)" % str(i+1))
				if(i<N_moves-1):
					print ",",
				else:
					print ":",

			b=-1
			while 0>b or b>N_moves:
				try:
					b=int(raw_input(""))
					if (0>b or b>N_moves):
						print "Select a valid move:",
				except ValueError:
					print "Select a valid move:",


			X=allowed[b-1][0]
			Y=allowed[b-1][1]

			if(b==0):
				print P.getname(),
				print "not moved"
				del allowed
			else:

				self.enpassant(P,X,Y,color)	# enpassant reset

				self.chessboard[P.getx()][P.gety()]=piece.empty(P.getx(),P.gety(),self.BD)
				self.chessboard[X][Y]=P
				self.chessboard[X][Y].setposition(X,Y)

				if(castle1now==True and X==6):	# create new rook in case it is castle
					self.chessboard[7][yking]=piece.empty(7,yking,self.BD)
					self.chessboard[5][yking]=piece.rook(5,yking,color,self.BD)
					print "Castled Kingside",
				elif(castle2now==True and X==2):
					self.chessboard[0][yking]=piece.empty(0,yking,self.BD)
					self.chessboard[3][yking]=piece.rook(3,yking,color,self.BD)
					print "Castled Queenside",
				else:
					print P.getname(),
					print "moved to",
					self.BD.cellname(X,Y)

				if(self.chessboard[X][Y].getid()==1 and (Y==0 or Y==7)):
					self.pawnpromotion(X,Y,color)	# piece.pawn promotion

				print ""

				self.castlespoiled(P,color) # spoils the castles if the rooks or king are moved
				break # if the move is done the turn finishes

		self.BD.printboard()


	#----------------------------------------------------------------------------------#
	def pawnpromotion(self,x,y,color):
		print ""
		print "Promote the piece.pawn to Queen (1), Rook (2), Bishop (3), Knight (4):",

		c=-1
		while c>a or c>4:
			c=int(raw_input("Select a valid choice: "))

		if c==1:
			self.chessboard[x][y]=piece.queen(x,y,color,self.BD)
		elif c==2:
			self.chessboard[x][y]=piece.rook(x,y,color,self.BD)
		elif c==3:
			self.chessboard[x][y]=piece.bishop(x,y,color,self.BD)
		elif c==4:
			self.chessboard[x][y]=piece.knight(x,y,color,self.BD)

		print "piece.pawn promoted to",
		print self.chessboard[x][y].getname()

	#----------------------------------------------------------------------------------#

	def enpassant(self,P,X,Y,color):
		if(X==-1 and Y==-1):	# enpassant prepare
			if(P.getid()==1 and self.passant_==True):
				if(P.getx()-1>=0 and self.chessboard[P.getx()-1][P.gety()].getid()==1):
					if(self.passant[0]==self.chessboard[P.getx()-1][P.gety()].getx() and self.passant[1]==self.chessboard[P.getx()-1][P.gety()].gety()):
						self.chessboard[P.getx()-1][P.gety()+color]=piece.pawn(P.getx()-1,P.gety()+color,-color,self.BD)
				if(P.getx()+1<self._n and self.chessboard[P.getx()+1][P.gety()].getid()==1):
					if(self.passant[0]==self.chessboard[P.getx()+1][P.gety()].getx() and self.passant[1]==self.chessboard[P.getx()+1][P.gety()].gety()):
						self.chessboard[P.getx()+1][P.gety()+color]=piece.pawn(P.getx()+1,P.gety()+color,-color,self.BD)

		else:	# enpassant reset
			if(P.getid()==1 and self.passant_==True and P.gety()==self.passant[1]):
				s=1
				if(P.getx()==self.passant[0]+1):
					s=-1

				if(self.chessboard[P.getx()+s][P.gety()].getid()==1):
					if(X==self.passant[0]):
						self.chessboard[P.getx()+s][P.gety()]=piece.empty(P.getx()+s,P.gety(),self.BD)
					else:
						self.chessboard[P.getx()+s][P.gety()+color]=piece.empty(P.getx()+s,P.gety()+color,self.BD)

			self.passant_=False
			self.passant[0]=-1
			self.passant[1]=-1

			if(P.getid()==1 and Y==P.gety()+2*color):
				self.passant_=True
				self.passant[0]=X
				self.passant[1]=Y


	#----------------------------------------------------------------------------------#
	def castlespoiled(self,P,color):
		if(P.getid()==6 or P.getid()==4 and P.getx()==7 or self.chessboard[7][0].getid()!=4 and self.chessboard[7][0].getcolor()!=color):
			if(color==1):
				self.castle_spoiler[0]=True
			else:
				self.castle_spoiler[2]=True
		if(P.getid()==6 or P.getid()==4 and P.getx()==0 or self.chessboard[0][0].getid()!=4 and self.chessboard[0][0].getcolor()!=color):
			if(color==1):
				self.castle_spoiler[1]=True
			else:
				self.castle_spoiler[3]=True


	#----------------------------------------------------------------------------------#
	def parity_verify(self,pieces,enemies):
		value1=0.
		value2=0.
		for i in range(len(pieces)):
			value1+=pieces[i].getvalue()
		for i in range(len(enemies)):
			value2+=enemies[i].getvalue()

		value1-=10000.	# remove the king value of 10000
		value2-=10000.

		if(value1<0.1 and value2<0.1):
			self.draw=True	# king vs king

		if((value1<3.025 and value1>3.005 and value2<0.1) or (value2<3.025 and value2>3.005 and value1<0.1)):
			self.draw=True	# knight or bishop vs king

		if(value1<3.025 and value1>3.005 and value2<3.025 and value2>3.005):
			self.draw=True	# knight or bishop vs knight or bishop (sometimes it can be mate but can't be forced)

		if((value1>6.015 and value1<6.025 and value2<0.1) or (value2>6.015 and value2<6.025 and value1<0.1)):
			self.draw=True	# two knights vs king (mate can't be forced)

		if(value2==0):	# 50 moves repetition
			self.N_50draw+=1
		if(self.N_50draw==50):
			self.draw=True


	#----------------------------------------------------------------------------------#
	def threefold(self):	# the threefold repetition rule is, in general, slightly more complicated than this

		if(self.BD_old2.compare(self.BD)==False):
			N_3rep=0
		else:
			N_3rep+=1

		for i in range(self._n):
			for j in range(self._n):
				self.BD_old2.fillcell(i,j,self.BD_old1.getboard(i,j))

		for i in range(self._n):
			for j in range(self._n):
				self.BD_old1.fillcell(i,j,self.BD.getboard(i,j))

		if(N_3rep==3):
			self.draw=True

################################################################################
