#! /usr/bin/env python
__author__ = 'Cindalis Cepero'
import random

# randomNumberGen = random.randint(0, 9) - 1

class Square(object): #the squares
    def __init__(self):
        self.mark = -1 #this set the squares so that you can use 1-9 instead of 0-9

    def isEmpty(self): #check to see if the square is empty
        if self.mark < 0: #if it is
            return True #return true
        else: #otherwise,
            return False #return false

    def getMark(self): #setter for mark
        return self.mark #return whatever mark the user chooses

    def setMark(self, playNumber): #getter for mark
        self.mark = playNumber #this sets the variables X and O  to numbers 1 and 2 so its easier to reffer to.

class Board(object): #the board
    def __init__(self, size = 3): #size is a 3 x 3 board
        self.size = size
        self.won = False #functions that checks whether someone has won.
        self.winCounter = -1 #the wins counter
        self.currentPlayer = 1 #the player who's turn it is.
        self.userPlayingAsMark = 1  #sets the user with their  specific mark
        self.gameBoard = [] #sets the game board to an empty list
        for squareNumber in range(0, 9):
            self.gameBoard.append(Square())
        self.nextBlockList = [] #this creates a list for the number of moves to block the opponent from winning.
        # self.randomNumber = randomNumberGen #this allows the computer to pick a random number if the board is empty/it does not need to block
        self.spacesAvailable = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.winningCombinations = [(0, 1, 2), #list of combinations that meet the winning requirements
                                    (3, 4, 5),
                                    (6, 7, 8),
                                    (0, 3, 6),
                                    (1, 4, 7),
                                    (2, 5, 8),
                                    (0, 4, 8),
                                    (2, 4, 6)]
    def hasWon(self):
        for winningResult in self.winningCombinations:
            if self.gameBoard[winningResult[0]].getMark == self.gameBoard[winningResult[1]].getMark and self.gameBoard[winningResult[1]].getMark == self.gameBoard[winningResult[2]].getMark:
                self.won = True
                return self.won
        self.won = False
        return self.won

    def boardIsEmpty(self):
        for square in self.gameBoard:
            if not square.isEmpty():
                return False
        return True

    def getMarkForBoard(self):
        for square in self.gameBoard:
            if not square.getMark():
                return False
        return True

    def getAvailableRandomSquare(self):
        chosenSquare = random.choice(self.spacesAvailable)
        del self.spacesAvailable[self.spacesAvailable.index(chosenSquare)]
        return chosenSquare

    # def isEmpty(self, squareNumber):
    #     return self.gameBoard[squareNumber].isEmpty()

    # def getMark(self, squareNumber):
    #     return self.gameBoard[squareNumber].getMark()



