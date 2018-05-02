#! /usr/bin/env python
__author__ = 'Cindalis Cepero'

from sys import path
from ticTacToeObjects import *
import sys
from os import path
import random
import ticTacToeResource_rc
from time import sleep
from logging import basicConfig, getLogger, DEBUG, INFO, CRITICAL
from pickle import dump, load
from PyQt5.QtCore import pyqtSlot, QSettings, QCoreApplication, Qt, QTimer
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox

logFileNameDefault = 'ticTacToe.log'
pickleFileNameDefault = ".ticTacToeSavedObjects.pl"
userPlayingStartingMark = 'X'
createLogFileDefault = True

class TicTacToe(QMainWindow):

    game = None

    def __init__(self, parent=None):

        super().__init__(parent)

        self.logger = getLogger("ticTacToe")
        self.appSettings = QSettings()
        self.quitCounter = 0  # used in a workaround for a QT5 Bug.

        uic.loadUi('ticTacToeUI.ui', self)

        self.pickleFileName = pickleFileNameDefault
        self.winsCount = 0
        self.lossesCount = 0
        self.gameInProgress = True
        self.messageString = "Welcome! Choose your mark in the preferences to Begin."
        self.board = Board()

        self.buttonList = [self.button1,
                           self.button2,
                           self.button3,
                           self.button4,
                           self.button5,
                           self.button6,
                           self.button7,
                           self.button8,
                           self.button9]

        self.restoreSettings()

        if path.exists(path.join(path.dirname(path.realpath(__file__)), self.pickleFileName)):
            self.userPlayingWithMark, self.winsCount, self.lossesCount, self.gameInProgress, self.messageString, self.board, self.game = self.restoreGame()
        else:
            self.restartGame()

        self.button1.clicked.connect(lambda: self.dynamicButtonsClickedHandler(1))
        self.button2.clicked.connect(lambda: self.dynamicButtonsClickedHandler(2))
        self.button3.clicked.connect(lambda: self.dynamicButtonsClickedHandler(3))
        self.button4.clicked.connect(lambda: self.dynamicButtonsClickedHandler(4))
        self.button5.clicked.connect(lambda: self.dynamicButtonsClickedHandler(5))
        self.button6.clicked.connect(lambda: self.dynamicButtonsClickedHandler(6))
        self.button7.clicked.connect(lambda: self.dynamicButtonsClickedHandler(7))
        self.button8.clicked.connect(lambda: self.dynamicButtonsClickedHandler(8))
        self.button9.clicked.connect(lambda: self.dynamicButtonsClickedHandler(9))
        self.preferencesButton.clicked.connect(self.preferencesSelectButtonClickedHandler)
        self.restartButton.clicked.connect(self.restartButtonClickedHandler)

    def updateUI(self):

        for squareMark in range(0,9):
            if self.board.isEmpty(squareMark): #check if the squareMark is empty
                self.buttonList[squareMark - 1].setText("") #if it is make sure it has no mark
            elif self.board.getMark(squareMark) == 1: #if the player is X and they mark the square then set the text to X
                self.buttonList[squareMark - 1].setText("X")
                self.messageString = "You're playing as X"
            else:
                self.buttonList[squareMark - 1].setText("O") #if the player is O and they mark the square then set the text to O
                self.messageString = "You're playing as O"
        self.winsLabel.setText(str(self.winsCount))  # set the users winsLabel to whatever their winCount is
        self.lossesLabel.setText(str(self.lossesCount))  # set the users lossesLabel to whatever their lossesCount is
        self.resultsLabel.setText(self.messageString) #set the resultsLabel to whatever the messageString is set to

    def restartGame(self):
        self.winsCount = 0
        self.lossesCOunt = 0
        self.messageString = "Welcome! Choose your mark in the preferences to Begin."
        self.userPlayingWithMark = userPlayingStartingMark
        self.lossesLabel.setText("")

    def saveGame(self):
        saveItems = (self.userPlayingWithMark, self.winsCount, self.lossesCount, self.gameInProgress, self.messageString, self.board, self.game)
        if self.appSettings.contains('pickleFileName'):
            with open(path.join(path.dirname(path.realpath(__file__)), self.appSettings.value('pickleFileName', type=str)), 'wb') as pickleFile:
                dump(saveItems, pickleFile)
        else:
            self.logger.critical("No pickle Filename")

    def restoreGame(self):
        if self.appSettings.contains('pickleFileName'):
            self.appSettings.value('pickleFileName', type=str)
            with open(path.join(path.dirname(path.realpath(__file__)), self.appSettings.value('pickleFileName', type=str)), 'rb') as pickleFile:
                return load(pickleFile)
        else:
            self.logger.critical("No pickle Filename")

    def restoreSettings(self):
        if self.appSettings.contains('startingMarkChoice'):
            self.userPlayingWithMark = self.appSettings.value('startingMarkChoice', type=int)
        else:
            self.appSettings.setValue('startingMarkChoice', self.userPlayingWithMark)
        if self.appSettings.contains('createLogFile'):
            self.createLogFile = appSettings.value('createLogFile', type=bool)
        else:
            self.createLogFile = createLogFileDefault
            self.appSettings.setValue('createLogFile', self.createLogFile)
        if self.appSettings.contains('pickleFilename'):
            self.pickleFileName = appSettings.value('pickleFilename', type=str)
        else:
            self.pickleFileName = pickleFileNameDefault
            self.appSettings.setValue('pickleFilename', self.pickleFileName) #My code is exactly the same as craps and it works there, why not here?

    def saveSettings(self):
        self.logger.info("starting saveSettings")
        if self.appSettings.contains('startingMarkChoice'):
            self.userPlayingWithMark = self.appSettings.value('startingMarkChoice', type=bool)
        else:
            self.appSettings.setValue('startingMarkChoice', self.userPlayingWithMark)
        if self.appSettings.contains('createLogFile'):
            self.createLogFile = appSettings.value('createLogFile', type=bool)
        else:
            self.createLogFile = logFileNameDefault
            self.appSettings.setValue('createLogFile', self.createLogFile)
        if self.appSettings.contains('createPickleFile'):
            self.pickleFileName = appSettings.value('createPickleFiley', type=str)
        else:
            self.pickleFileName = pickleFileNameDefault
            self.appSettings.setValue('createPickleFile', self.createPickleFile)

    def setUserPlayerWithMark(self, playerMark):
        if playerMark == 'X' or playerMark == 'O':
            self.userPlayingStartingMark = playerMark
        else:
            self.logger.error("invalid playerMark in setUserPlayerMark {0}".format(playerMark))

    def clearUserPlayerWithMark(self):
        self.userPlayingStartingMark = self.startingMarkChoice

    def getUserPlayingWithMark(self):
        return self.userPlayingWithMark

    # I want to switch the playerMark to X and O instead of 1 and 2 so how might I do that and how will my code need to change? How come my squares aren't changing to X/O when I click on them? instead they just blow up. (look at line 186, 215, and the objects file.)

    def playUsersTurn(self, squareToPlay):
        squareToPlay = userPlayingStartingMark
        self.board.setMark(squareToPlay)
        for squareToPlay in self.board.spacesAvailable:
            self.board.spacesAvailable = self.board.spacesAvailable - squareToPlay
        return squareToPlay


    def getWon(self):
        executeWinnerIsUser = False
        if self.board.winningCombinations(userPlayingStartingMark):
            executeWinnerIsUser = True
            self.winsCount += 1
        else:
            executeWinnerIsUser = False
            self.lossesCount += 1
        return executeWinnerIsUser


    def playSquare(self, currentPlayerMark, squareToPlay = -1): #the game
        self.logger.info("entering playSquare with playNumber {0} and squareMark {1}".format(currentPlayerMark, squareToPlay))
        if currentPlayerMark != self.getUserPlayingWithMark(): #If its the computers turn
            if self.board.block(currentPlayerMark): #check to see if it can block human
                #self.logger.info(self.game.getBlockList())
                chosenSquare = self.board.block() #block that spot
                return chosenSquare
            else:
                chosenSquare = self.board.selectSquare() #otherwise pick a square that can get you a winning combination??? How might I code this??
        else:
            chosenSquare = self.board.getAvailableRandomSquare() #Idk what to put here ?????
        self.game.setMark(chosenSquare) #fill in the gameBoard with the choseSquares
        self.getWon()

        if self.getWon(): #if there is a win
            if self.getWon() == userPlayingStartingMark: #If the HumansMark won
                self.messageString = ("You won!")  #set the resultsLabel to you won
                if self.userPlayingWithMark() == 'X': #if the humansMark is X
                    self.winsCount += 1 #bring up the userWinsCounter by 1
                else:
                    self.lossesCount+= 1 #otherwise, computer wins
                    self.logger.info("The Computer won!")
                self.updateUI()

            else:
                self.messageString = ("You won!")
                if self.getUserPlayingWithMark() == 'O':
                    self.winsCount += 1
                else:
                    self.lossesCount += 1
                    self.logger.info("The Computer won!")
                self.updateUI()
                self.logger.info("Game Over")
            self.gameInProgress = False #sets the game to stop
            self.restartTimer = QTimer #restarts the game
            self.restartTime.singleShot(2500, self.restartGame)  #this calls the restarts the function specifically after restartGame is triggered.
        elif self.board.spacesAvailable: #See if the the game has anymore available squares
            pass #idk what to put here?????????
        else: #if not and nobody has won:
            self.messageString = ("Game was a tie!")
            self.logger.debug(self.game.displayGame)
            self.logger.info("Game was a tie!")
            self.gameInProgress = False #close the game
            self.updateUI()
            self.restartTimer = QTimer() #restart the game
            self.restartTimer.singleShot(2500, self.restartGame)

        if self.gameInProgress and currentPlayerMark == self.userPlayingWithMark() and not self.game.getWon(): #if the game is in progress and it is the humans turn and they have not won:
            self.playSquare(self.game.getCurrentPlayer()) #get whatever square they fill in and updateUI

        self.updateUI()

    def dynamicButtonsClickedHandler (self, buttonNumber):
        self.logger.debug("Button %i was clicked" % buttonNumber)
        print("Button %i was clicked" % buttonNumber)

        if self.board.isEmpty(buttonNumber):
            self.messageString = "Square %i was clicked" % buttonNumber
            self.playSquare(self.getUserPlayingWithMark(), buttonNumber)
        else:
            self.messageString("Square %i has been used already" % buttonNumber)
        self.updateUI()

    @pyqtSlot()  # user is requesting preferences editing dialog box.
    def preferencesSelectButtonClickedHandler(self):
        print("Setting preferences")
        preferencesDialog = PreferencesDialog()
        preferencesDialog.show()
        preferencesDialog.exec_()
        self.restoreSettings()
        self.updateUI()

    @pyqtSlot()
    def restartButtonClickedHandler(self):
        self.restartGame()
        self.saveGame()
        self.updateUI()

    @pyqtSlot()  # Player asked to quite game
    def closeEvent(self, event):
        if self.quitCounter == 0:
            self.quitCounter += 1
            quitMessage = "Are you sure you want to quit?"
            reply = QMessageBox.question(self, 'Message', quitMessage, QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.saveGame()
                event.accept()
            else:
                event.ignore()
            return super().closeEvent(event)


class PreferencesDialog(QDialog):

    def __init__(self, parent= TicTacToe):
        super(PreferencesDialog, self).__init__()
        self.logger = getLogger("TicTacToe")

        uic.loadUi('PreferencesDialog.ui', self)
        self.appSettings = QSettings()
        if self.appSettings.contains('createLogFile'):
            self.createLogFile = appSettings.value('createLogFile', type=bool)
        else:
            self.createLogFile = logFileNameDefault
            self.appSettings.setValue('createLogFile', self.createLogFile)

        self.buttonBox.accepted.connect(self.okayClickedHandeler)
        self.buttonBox.rejected.connect(self.cancleClickedHandler)
        self.radioButtonX.pressed.connect(self.radioButtonXStateChanged)
        self.radioButtonO.pressed.connect(self.radioButtonOStateChanged)

        self.updateUI()

    def radioButtonXStateChanged(self):
        self.startingMarkChoice = 'X'

    def radioButtonOStateChanged(self):
        self.startingMarkChoice = 'O'

    def createLogFileChanged(self):
        self.createLogFile = self.createLogFileCheckBox

    def updateUI(self):
        self.radioButtonX.pressed.connect(self.radioButtonXStateChanged)
        self.radioButtonO.pressed.connect(self.radioButtonOStateChanged)
        if self.createLogFile:
            self.createLogFileCheckBox.setCheckState(Qt.Checked)
        else:
            self.createLogFileCheckBox.setCheckState(Qt.Unchecked)

    def okayClickedHandeler(self):
        # print("Clicked okay handler")
        basePath = path.dirname(path.realpath(__file__))
        # self.logFileName = self.logFileNameEdit.text()
        self.logFileName = "ticTacToe.log"
        # write out all settings
        self.preferencesGroup = (('logFile', self.logFileName),)
        # write settings values.
        for setting, variableName in self.preferencesGroup:
            # if self.appSettings.contains(setting):
            self.appSettings.setValue(setting, variableName)
        self.close()

    def cancleClickedHandler(self):
        self.close()


if __name__ == "__main__":
    QCoreApplication.setOrganizationName("Cindalis Software")
    QCoreApplication.setOrganizationDomain("cindalissoftware.com")
    QCoreApplication.setApplicationName("TicTacToe")
    appSettings = QSettings()
    startingFolderName = path.dirname(path.realpath(__file__))
    if appSettings.contains('logFile'):
        logFileName = appSettings.value('logFile', type=str)
    else:
        logFileName = logFileNameDefault
        appSettings.setValue('logFile', logFileName)
    basicConfig(filename=path.join(startingFolderName, logFileName), level=INFO, format='%(asctime)s %(name)-8s %(levelName)-8s %(message)s')

    app = QApplication(sys.argv)
    ticTacToeApp = TicTacToe()
    ticTacToeApp.updateUI()
    ticTacToeApp.show()
    sys.exit(app.exec_())
