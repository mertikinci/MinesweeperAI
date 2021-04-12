from MineSweeperBoard import MineSweeperBoard
from MineSweeperAI import MineSweeperAI

CONST_GAMEBOARD_ROWS_BEGINNER = 9
CONST_GAMEBOARD_COLS_BEGINNER = 9
CONST_GAMEBOARD_MINES_BEGINNER = 10

CONST_GAMEBOARD_ROWS_INTERMEDIATE = 16
CONST_GAMEBOARD_COLS_INTERMEDIATE = 16
CONST_GAMEBOARD_MINES_INTERMEDIATE = 40

CONST_GAMEBOARD_ROWS_EXPERT = 16
CONST_GAMEBOARD_COLS_EXPERT = 30
CONST_GAMEBOARD_MINES_EXPERT = 99

# Main application logic
if __name__ == "__main__":

    flag = True
    while flag:
        difficulty = int(input("Enter \n 1 for BEGINNER level, \n 2 for INTERMEDIATE level \n 3 for EXPERT level."))
        if difficulty == 2:
            CONST_GAMEBOARD_ROWS = CONST_GAMEBOARD_ROWS_INTERMEDIATE
            CONST_GAMEBOARD_COLS = CONST_GAMEBOARD_COLS_INTERMEDIATE
            CONST_GAMEBOARD_MINES = CONST_GAMEBOARD_MINES_INTERMEDIATE
            flag = False
        elif difficulty == 1:
            CONST_GAMEBOARD_ROWS = CONST_GAMEBOARD_ROWS_BEGINNER
            CONST_GAMEBOARD_COLS = CONST_GAMEBOARD_COLS_BEGINNER
            CONST_GAMEBOARD_MINES = CONST_GAMEBOARD_MINES_BEGINNER
            flag = False
        elif difficulty == 3:
            CONST_GAMEBOARD_ROWS = CONST_GAMEBOARD_ROWS_EXPERT
            CONST_GAMEBOARD_COLS = CONST_GAMEBOARD_COLS_EXPERT
            CONST_GAMEBOARD_MINES = CONST_GAMEBOARD_MINES_EXPERT
            flag = False
        else:
            print("not a valid difficulty please give 1,2 or 3")


    # Create a new instance of the Minesweeper game board
    NewAI = MineSweeperAI(CONST_GAMEBOARD_ROWS, CONST_GAMEBOARD_COLS, CONST_GAMEBOARD_MINES)
    NewGameboard = MineSweeperBoard(CONST_GAMEBOARD_ROWS, CONST_GAMEBOARD_COLS, CONST_GAMEBOARD_MINES)
    NewGameboard.print()
    # NewGameboard.printDebug()
    # While the game is not over, the AI should keep
    # being prompted for their next move
    while not NewGameboard.isGameOver():
      NewAI.updateAIViewBoard(NewGameboard.getAIBoard())
      xCoordinate, yCoordinate = NewAI.makeMove()
      print('AI\'s move: {},{}'.format(xCoordinate, yCoordinate))
      #xCoordinate = int(input('Please enter the x component of the tile: '))
      #yCoordinate = int(input('Please enter the y component of the tile: '))
      try:
        NewGameboard.makeMove(xCoordinate, yCoordinate)
        NewGameboard.print()
        # NewGameboard.printDebug()
      except ValueError as error:
        print(error)
        print('invalid move selected, please select another tile')
        continue
    # When the game has ended, then print a game over message
    # and exit the application
    print('Game Over !!')
    exit(0)
