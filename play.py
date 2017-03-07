# Seth Forrest
# connect 4 - A
# CS470 - AI

# Adapted from https://github.com/erikackermann/Connect-Four


from connect4 import *

def main():
  """ Play a game!
  """
  
  g = Game()
  g.printState()
  player1 = g.players[0]
  player2 = g.players[1]
  
  winTracker = [0, 0, 0] # Tracks match winners
  
  exit = False
  while not exit:
    while not g.finished:
      g.nextMove()
  
    g.findFours()
    g.printState()
    
    if g.winner == None:
      winTracker[2] += 1
  
    elif g.winner == player1:
      winTracker[0] += 1
      
    elif g.winner == player2:
      winTracker[1] += 1
  
    printStats(player1, player2, winTracker)
    
    while True:
      play_again = str(input("Do you want to play again? (y/n)\n"))
      
      if play_again.lower() == 'y' or play_again.lower() == 'yes': 
        g.resetBoard()
        g.printState()
        break
      elif play_again.lower() == 'n' or play_again.lower() == 'no':
        print("Thanks for playing!\n")
        exit = True
        break
      else:
        print("INVALID INPUT "),
  
def printStats(player1, player2, winTracker):
  print("{0}'s wins: {1}, {2}'s wins: {3}, {4} ties\n".format(player1.name,
    winTracker[0], player2.name, winTracker[1], winTracker[2]))
    
if __name__ == "__main__": # Default "main method" idiom.
  main()
