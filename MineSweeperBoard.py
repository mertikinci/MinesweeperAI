import random

class MineSweeperBoard:

  def __init__(self, xDimension, yDimension, numberMines):


    self.xDimension = xDimension
    self.yDimension = yDimension
    self.numberMines = numberMines

    # Store the coordinates of mines when they are created so
    self.mineCoordinates = []
    self.gameOver = False
    self.movesRemaining = (self.xDimension * self.yDimension) - self.numberMines
    if self.movesRemaining == 0:
      self.gameOver = True

    # Sanity check to make sure that there are not more mines
    # than actual tiles on the game board
    if ((self.numberMines > (self.xDimension * self.yDimension)) or self.numberMines < 0):
      raise ValueError('invalid number of mines entered')

    # Game state board consists of the following numbers:
    # -  -1 = Empty tile (only used when the board is first initialized)
    # -  -9 = Mine location
    # - 0-9 = Number of adjacent mines to a tile 
    self.gameStateBoard = [[-1 for x in range(self.yDimension)] for y in range(self.xDimension)]
    
    # AI gameboard view consists of the following symbols
    # -   X = Unknown (not yet selected) tile
    # -   x = Mine location
    # -   - = 0 value (no adjacent mines)
    # - 1-9 = Number of adjacent mines
    self.AIViewBoard = [['X' for x in range(self.yDimension)] for y in range(self.xDimension)]

    # Seed the board with mines and then determine the correct values
    # to assign for the remaining nodes based on adjacency to mines
    self.__seedMines()
    self.__seedValues()

  def isGameOver(self):
    #Returns whether the game has been marked as over
    return self.gameOver

  def __seedMines(self):
    #Seeds mines into an empty gameStateBoard
    minesRemaining = self.numberMines
    while minesRemaining > 0:
      x = random.randint(0, self.xDimension - 1)
      y = random.randint(0, self.yDimension - 1)
      if self.gameStateBoard[x][y] == -9:
        continue
      self.gameStateBoard[x][y] = -9
      self.mineCoordinates.append((x, y))
      minesRemaining -= 1

  def __seedValues(self):
    #Seeds values into tiles not containing mines in the gameStateBoard
    for x, row in enumerate(self.gameStateBoard):
      for y, value in enumerate(row):
        # If the tile contains a mine, we are not interested in it
        # so go onto the next tile
        if value == -9:
          continue
        # Otherwise, calculate the number of adjacent mines, so that
        # value can then be assigned to the tile
        tileValue = self.__getNumAdjMines(x, y)
        self.gameStateBoard[x][y] = tileValue

  def print(self, gameboard=None):
    #Print the AI gameboard
    board = self.AIViewBoard if (gameboard == None) else gameboard
    print('\n')
    print('\n'.join([' '.join([str(cell) for cell in row]) for row in board]))
    print('\n')

  def printDebug(self):
    #Prints the game state board
    self.print(self.gameStateBoard)

  def __hasMine(self, x, y):
    #Determines if a mine is present at the given location
    return True if self.gameStateBoard[x][y] == -9 else False

  def __revealMines(self):
    #Reveals all the mines on the AI visible gameboard
    for coordinatePair in self.mineCoordinates:
      xCoordinate = coordinatePair[0]
      yCoordinate = coordinatePair[1]
      self.__revealTile(xCoordinate, yCoordinate)

  def __coordinateCheck(self, x, y):
    #This is a helper function that checks to ensure that the input coordinates are within the dimensions of the board.
    if x < 0 or x >= self.xDimension:
      return False
    if y < 0 or y >= self.yDimension:
      return False
    return True
  
  def __getNumAdjMines(self, x, y):
    #This is a helper function used by the __seedValues() function to determine the number of mines adjacent to any given tile on the game state board.
    totalNumMines = 0
    ## Check the tile to the west
    if (self.__coordinateCheck(x, y-1)):
      if self.__hasMine(x, y-1):
        totalNumMines += 1
    ## Check the tile to the north-west
    if (self.__coordinateCheck(x-1, y-1)):
      if self.__hasMine(x-1, y-1):
        totalNumMines += 1
    ## Check the tile to the north
    if (self.__coordinateCheck(x-1, y)):
      if self.__hasMine(x-1, y):
        totalNumMines += 1
    ## Check the tile to the north-east
    if (self.__coordinateCheck(x-1, y+1)):
      if self.__hasMine(x-1, y+1):
        totalNumMines += 1
    ## Check the tile to the east
    if (self.__coordinateCheck(x, y+1)):
      if self.__hasMine(x, y+1):
        totalNumMines += 1
    ## Check the tile to the south-east
    if (self.__coordinateCheck(x+1, y+1)):
      if self.__hasMine(x+1, y+1):
        totalNumMines += 1
    ## Check the tile to the south
    if (self.__coordinateCheck(x+1, y)):
      if self.__hasMine(x+1, y):
        totalNumMines += 1
    ## Check the tile to the south-west
    if (self.__coordinateCheck(x+1, y-1)):
      if self.__hasMine(x+1, y-1):
        totalNumMines += 1
    ## Return the total number of adjacent mines found
    return totalNumMines

  def __revealTile(self, x, y):
    #This is a helper function that reveals the tile found at coordinates (x, y) in the AIViewBoard.
    # If the gameStateBoard contains a mine at the input coordinates,
    # show a mine on the AIViewBoard
    if self.gameStateBoard[x][y] == -9:
      self.AIViewBoard[x][y] = 'x'
    elif self.gameStateBoard[x][y] == 0:
      self.AIViewBoard[x][y] = '-'
      self.movesRemaining -= 1
    else:
      self.AIViewBoard[x][y] = self.gameStateBoard[x][y]
      self.movesRemaining -= 1

  def __hasBeenPlayed(self, x, y):
    #Check the AIViewBoard to see if a tile has already been played
    return False if self.AIViewBoard[x][y] == 'X' else True

  def __uncoverAdjTiles(self, x, y):
    #This function is used when the AI selects a '0' tile on the game state board.
    # Ensure that the input coordinates belong to a tile containing a
    # zero value (i.e. no adjacent mines)
    if self.gameStateBoard[x][y] == 0:
      ## Check the tile to the west
      if (self.__coordinateCheck(x, y-1)):
        if not self.__hasBeenPlayed(x, y-1):
          self.__revealTile(x, y-1)
          self.__uncoverAdjTiles(x, y-1)
      ## Check the tile to the north-west
      if (self.__coordinateCheck(x-1, y-1)):
        if not self.__hasBeenPlayed(x-1, y-1):
          self.__revealTile(x-1, y-1)
          self.__uncoverAdjTiles(x-1, y-1)
      ## Check the tile to the north
      if (self.__coordinateCheck(x-1, y)):
        if not self.__hasBeenPlayed(x-1, y):
          self.__revealTile(x-1, y)
          self.__uncoverAdjTiles(x-1, y)
      ## Check the tile to the north-east
      if (self.__coordinateCheck(x-1, y+1)):
        if not self.__hasBeenPlayed(x-1, y+1):
          self.__revealTile(x-1, y+1)
          self.__uncoverAdjTiles(x-1, y+1)
      ## Check the tile to the east
      if (self.__coordinateCheck(x, y+1)):
        if not self.__hasBeenPlayed(x, y+1):
          self.__revealTile(x, y+1)
          self.__uncoverAdjTiles(x, y+1)
      ## Check the tile to the south-east
      if (self.__coordinateCheck(x+1, y+1)):
        if not self.__hasBeenPlayed(x+1, y+1):
          self.__revealTile(x+1, y+1)
          self.__uncoverAdjTiles(x+1, y+1)
      ## Check the tile to the south
      if (self.__coordinateCheck(x+1, y)):
        if not self.__hasBeenPlayed(x+1, y):
          self.__revealTile(x+1, y)
          self.__uncoverAdjTiles(x+1, y)
      ## Check the tile to the south-west
      if (self.__coordinateCheck(x+1, y-1)):
        if not self.__hasBeenPlayed(x+1, y-1):
          self.__revealTile(x+1, y-1)
          self.__uncoverAdjTiles(x+1, y-1)

  def makeMove(self, x, y):
   #This is a public function that the AI calls when they have selected a tile to uncover for their move.
    # Sanitize the user input coordinates
    if not self.__coordinateCheck(x, y):
      raise ValueError('invalid coordinate pair chosen')
    # Check if the move has already been made
    if self.__hasBeenPlayed(x, y):
      raise ValueError('move has already been played')
    # Check if the AI has hit a mine
    if self.__hasMine(x, y):
      self.__revealMines()
      self.gameOver = True
      print('AI hits a mine... BOOM!!')
    # If a AI selects a tile with a zero value
    # (i.e. no adjacent tiles contain a mine), uncover
    # all adjacent tiles
    elif self.gameStateBoard[x][y] == 0:
      self.__revealTile(x,y)
      self.__uncoverAdjTiles(x,y)
      # If there are no move valid moves the AI can make
      # then the game is over; the AI wins!
      if self.movesRemaining == 0:
        self.gameOver = True
        print('AI Victory!')
    # If the AI selects a tile that contains a
    # non-negative, non-zero value - then just reveal
    # that single tile
    elif self.gameStateBoard[x][y] > 0:
      self.__revealTile(x,y)
      if self.movesRemaining == 0:
        self.gameOver = True
        print('AI Victory')

  def getAIBoard(self):
    # This function returns the 2D AIViewBoard
    return self.AIViewBoard
