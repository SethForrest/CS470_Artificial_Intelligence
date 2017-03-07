# Seth Forrest
# connect 4 - A
# CS470 - AI

# Adapted from https://github.com/erikackermann/Connect-Four


import random
import os
import time

class Game(object):
  
  board = None
  match = None
  finished = None
  winner = None
  turn = None
  players = [None, None]
  gameName = "Seth's Connect 4"
  tiles = ["x", "o"]
  
  def __init__(self):
    self.match = 1
    self.finished = False
    self.winner = None
    
    # clear screen
    os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
    print("Welcome to {0}!".format(self.gameName))    
    print("Player 1 goes first.")
    while self.players[0] == None:
      name = str(input("What is your name? "))
      self.players[0] = Player(name, self.tiles[0])
    print("{0} will play as {1}\n".format(self.players[0].name, self.tiles[0]))
    
    print("How about player 2?")
    while self.players[1] == None:
      name = str(input("What is Player 2's name? "))
      self.players[1] = Player(name, self.tiles[1])
    print("{0} will play as {1}\n".format(self.players[1].name, self.tiles[1]))

    self.turn = self.players[0] # Start with player 1
    
    self.board = []
    for i in range(6):
      self.board.append([])
      for j in range(7):
        self.board[i].append(' ')

  def resetBoard(self):
    """ Resets the game
    """
    self.match = 1
    self.finished = False
    self.winner = None    
    self.turn = self.players[0] # Start with player 1
    
    self.board = []
    for i in range(6):
      self.board.append([])
      for j in range(7):
        self.board[i].append(' ')

  def switchTurn(self):
    if self.turn == self.players[0]:
      self.turn = self.players[1]
    else:
      self.turn = self.players[0]

    self.match += 1 # Match counter

  def nextMove(self):
    player = self.turn

    # Check for cats-game
    if self.match > 42:
      self.finished = True
      return
      
    move = player.move(self.board)

    for i in range(6):
      if self.board[i][move] == ' ':
        self.board[i][move] = player.tile
        self.switchTurn()
        self.checkForFours()
        self.printState()
        return

    # if we get here, then the column is full
    print("Invalid move (column is full)")
    return

  def checkForFours(self):
    # for each piece in the board...
    for i in range(6):
      for j in range(7):
        if self.board[i][j] != ' ':
          # check if a vertical four-in-a-row starts at (i, j)
          if self.verticalCheck(i, j):
            self.finished = True
            return
        
          # check if a horizontal four-in-a-row starts at (i, j)
          if self.horizontalCheck(i, j):
            self.finished = True
            return
        
          # check if a diagonal (either way) four-in-a-row starts at (i, j)
          # also, get the slope of the four if there is one
          diag_fours, slope = self.diagonalCheck(i, j)
          if diag_fours:
            print(slope)
            self.finished = True
            return

  def verticalCheck(self, row, col):
    fourInARow = False
    consecutiveCount = 0

    for i in range(row, 6):
      if self.board[i][col].lower() == self.board[row][col].lower():
        consecutiveCount += 1
      else:
        break

    if consecutiveCount >= 4:
      fourInARow = True
      if self.players[0].tile.lower() == self.board[row][col].lower():
        self.winner = self.players[0]
      else:
        self.winner = self.players[1]

    return fourInARow

  def horizontalCheck(self, row, col):
    fourInARow = False
    consecutiveCount = 0
    
    for j in range(col, 7):
      if self.board[row][j].lower() == self.board[row][col].lower():
        consecutiveCount += 1
      else:
        break

    if consecutiveCount >= 4:
      fourInARow = True
      if self.players[0].tile.lower() == self.board[row][col].lower():
        self.winner = self.players[0]
      else:
        self.winner = self.players[1]

    return fourInARow

  def diagonalCheck(self, row, col):
    fourInARow = False
    count = 0
    slope = None

    # check for diagonals with positive slope
    consecutiveCount = 0
    j = col
    for i in range(row, 6):
      if j > 6:
        break
      elif self.board[i][j].lower() == self.board[row][col].lower():
        consecutiveCount += 1
      else:
        break
      j += 1 # increment column when row is incremented
      
    if consecutiveCount >= 4:
      count += 1
      slope = 'positive'
      if self.players[0].tile.lower() == self.board[row][col].lower():
        self.winner = self.players[0]
      else:
        self.winner = self.players[1]

    # check for diagonals with negative slope
    consecutiveCount = 0
    j = col
    for i in range(row, -1, -1):
      if j > 6:
        break
      elif self.board[i][j].lower() == self.board[row][col].lower():
        consecutiveCount += 1
      else:
        break
      j += 1 # increment column when row is decremented

    if consecutiveCount >= 4:
      count += 1
      slope = 'negative'
      if self.players[0].tile.lower() == self.board[row][col].lower():
        self.winner = self.players[0]
      else:
        self.winner = self.players[1]

    if count > 0:
      fourInARow = True
    if count == 2:
      slope = 'both'
    return fourInARow, slope

  def findFours(self):
    """ Finds start i,j of four-in-a-row
      Calls highlightFours
    """

    for i in range(6):
      for j in range(7):
        if self.board[i][j] != ' ':
          # check if a vertical four-in-a-row starts at (i, j)
          if self.verticalCheck(i, j):
            self.highlightFour(i, j, 'vertical')
          
          # check if a horizontal four-in-a-row starts at (i, j)
          if self.horizontalCheck(i, j):
            self.highlightFour(i, j, 'horizontal')
          
          # check if a diagonal (either way) four-in-a-row starts at (i, j)
          # also, get the slope of the four if there is one
          diag_fours, slope = self.diagonalCheck(i, j)
          if diag_fours:
            self.highlightFour(i, j, 'diagonal', slope)

  def highlightFour(self, row, col, direction, slope=None):
    """ This function enunciates four-in-a-rows by capitalizing
      the character for those pieces on the board
    """
    
    if direction == 'vertical':
      for i in range(4):
          self.board[row+i][col] = self.board[row+i][col].upper()
  
    elif direction == 'horizontal':
      for i in range(4):
        self.board[row][col+i] = self.board[row][col+i].upper()
  
    elif direction == 'diagonal':
      if slope == 'positive' or slope == 'both':
        for i in range(4):
          self.board[row+i][col+i] = self.board[row+i][col+i].upper()

      elif slope == 'negative' or slope == 'both':
        for i in range(4):
          self.board[row-i][col+i] = self.board[row-i][col+i].upper()

    else:
      print("Error - Cannot enunciate four-of-a-kind")

  def printState(self):
    # cross-platform clear screen
    os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
    print(u"{0}!".format(self.gameName))
    print("Match: " + str(self.match))

    for i in range(5, -1, -1):
      print("\t", end="")
      for j in range(7):
        print("| " + str(self.board[i][j]), end=" ")
      print("|")
    print("\t  _   _   _   _   _   _   _ ")
    print("\t  0   1   2   3   4   5   6 ")

    if self.finished:
      print("Game Over!")
      if self.winner != None:
        print(str(self.winner.name) + " is the winner")
      else:
        print("Game was a draw")
        
class Player(object):
  """ Player object.  This class is for human players.
  """
  
  type = None # eventually will be "Human" and "AI"
  name = None
  tile = None
  def __init__(self, name, tile):
    self.type = "Human"
    self.name = name
    self.tile = tile

  def move(self, state):
    print("{0}'s turn.  {0} is {1}".format(self.name, self.tile))
    column = None
    while column == None:
      try:
        choice = int(input("Enter a move (by column number): "))
      except ValueError:
        choice = None
      if 0 <= choice <= 6:
        column = choice
      else:
        print("Invalid choice, try again")
    return column

