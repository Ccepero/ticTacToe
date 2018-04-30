#! /usr/bin/env python
__author__ = 'Cindalis Cepero'

#!/usr/bin/env python
from sys import path
import sys
from os import path
from ticTacToeObjects import *
import random
import ticTacToeResource_rc
from time import sleep
from logging import basicConfig, getLogger, DEBUG, INFO, CRITICAL
from pickle import dump, load
from PyQt5.QtCore import pyqtSlot, QSettings, QCoreApplication, Qt, QTimer
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox

logFileNameDefault = 'dice.log'
pickleFileNameDefault = ".crapsSavedObjects.pl"

class TicTacToe(QMainWindow) :

    game = None

    def __init__( self, parent=None ):

        super().__init__(parent)

        self.logger = getLogger("TicTacToe")
        self.appSettings = QSettings("Cepero Software", "TicTacToe")

        #self.game = TicTacToe()

        uic.loadUi('ticTacToeUI.ui', self)

        self.userPlayingWithMark = self.appSettings.value("startingMarkChoice")
        self.userWins = 0
        self.userLosses = 0
        self.gameInProgress = True
        self.messageString = "Welcome! Click Start to Begin."
        self.square = Square
        self.board = Board
        self.markLabelButton = None

        self.buttonList = [self.button1,
                           self.button2,
                           self.button3,
                           self.button4,
                           self.button5,
                           self.button6,
                           self.button7,
                           self.button8,
                           self.button9]

        self.button1.clicked.connect(lambda:self.dynamicbuttonsClickedHandler(1))
        self.button2.clicked.connect(lambda:self.dynamicbuttonsClickedHandler(2))
        self.button3.clicked.connect(lambda:self.dynamicbuttonsClickedHandler(3))
        self.button4.clicked.connect(lambda:self.dynamicbuttonsClickedHandler(4))
        self.button5.clicked.connect(lambda:self.dynamicbuttonsClickedHandler(5))
        self.button6.clicked.connect(lambda:self.dynamicbuttonsClickedHandler(6))
        self.button7.clicked.connect(lambda:self.dynamicbuttonsClickedHandler(7))
        self.button8.clicked.connect(lambda:self.dynamicbuttonsClickedHandler(8))
        self.button9.clicked.connect(lambda:self.dynamicbuttonsClickedHandler(9))

        self.restartButton.clicked.connect(self.restartButtonTriggeredHandler)
        self.preferencesButton.clicked.connect(self.preferencesSelectButtonTriggeredHandler)

        self.pickleFileName = pickleFileNameDefault

        self.restoreSettings()

        if path.exists(self.pickleFileName):
            self.userPlayingWithMark, self.userWins, self.userLosses, self.gameInProgress, self.messageString, self.markLabelButton, self.square, self.board, self.game = self.restoreGame()

        else:
            self.restartGame()

    def saveGame(self):
        saveItems = (self.winsCount, self.lossesCOunt)
        if self.appSettings.contains('pickleFileName'):
            with open(path.join(path.dirname(path.realpath(__file__)), self.appSettings.value('pickleFileName', type= str)), 'wb') as pickleFile:
                dump(saveItems, pickleFile)
        else:
            self.logger.critical("No pickle Filename")
    def saveSettings(self):
        radioButtonXDefault = False
        radioButtonODefault = False
        if self.appSettings.contains('radioButtonX'): #implement X
            self.radioButtonX = self.appSettings.value('radioButtonX', type=bool)
        else:
            self.radioButtonX = radioButtonXDefault
            self.appSettings.setValue('radioButtonX', self.radioButtonX)
        if self.appSettings.contains('radioButtonO'): #implement O
            self.radioButtonO = self.appSettings.value('radioButtonO', type=bool)
        else:
            self.radioButtonO = radioButtonODefault
            self.appSettings.setValue('radioButtonO', self.radioButtonO)
        if self.appSettings.contains('createLogFile'):
            self.createLogFile=appSettings.value('createLogFile',type=bool)
        else:
            self.createLogFile= logFileNameDefault
            self.appSettings.setValue('createLogFile', self.createLogFile)
    def restoreGame(self):
        if self.appSettings.contains('pickleFileName'):
            pickleFileName = path.join(path.dirname(path.realpath(__file__)), self.appSettings.value('pickleFileName', type=str)) #is this right?
            try:
                with open(pickleFileName, 'rb') as pickleFile:
                    return load(pickleFile)
            except FileNotFoundError as errorVal:
                print('errorVal')
        else:
            self.logger.critical("No pickle Filename")
    def restoreSettings(self):
        self.startingMarkChoice = self.appSettings.value('startingMarkChoice')
        self.createLogFile = self.appSettings.value('createLogFile')
        self.logFileName = self.appSettings.value('pickleFileName')
        return True


    def updateUI(self):
        for squareNumber in range(1,10):
            if self.square.isEmpty(squareNumber): #check if the squareNumber is empty
                self.buttonList[squareNumber - 1].setText("") #if it is make sure it has no mark
            elif self.square.getMark(squareNumber) == 1: #if the player is X and they mark the square then set the text to X
                self.buttonList[squareNumber - 1].setText("X")
            else:
                self.buttonList[squareNumber - 1].setText("O") #if the player is O and they mark the square then set the text to O
        self.winsLabel.setText("%i" % self.userWins) #set the users winsLabel to whatever their winCount is
        self.lossesLabel.setText("%i" % self.userLosses) #set the users lossesLabel to whatever their lossesCount is
        self.resultsLabel.setText(self.messageString) #set the resultsLabel to whatever the messageString is set to
        if self.userPlayingWithMark == 1: #if the user selects X, set the value to 1
            self.markLabelButton.setText("X")
        elif self.userPlayingWithMark == 2: #if the user select O, set the value to 2
            self.markLabelButton.setText("O")
        else:
            self.markLabelButton.setText("-") #otherwise leave the value at None

    def setUserPlayerWithMark(self, playerNumber):
        if playerNumber == 1 or playerNumber == 2:
            self.userPlayingWithMark = playerNumber
        else:
            self.logger.error("invalid playerNumber in setUserPlayerNumber: {0}".format(playerNumber))

    def clearUserPlayerWithMark(self):
        self.userPlayingWithMark = self.startingMarkChoice

    def getUserPlayingWithMark(self):
        return self.userPlayingWithMark

    def playSquare(self, currentPlayerNumber, squareToPlay = -1): #the game
        self.logger.info("entering playSquare with playNumber {0} and squareNumber {1}".format(currentPlayerNumber, squareToPlay))
        if currentPlayerNumber != self.userPlayingWithMark(): #If the human is not equal to the userPlayingWithMark
            if self.game.checkForBlock(currentPlayerNumber): #if the player finds any move where they can be blocked/loose
                self.logger.info(self.game.getBlockList())
                chosenSquare = self.game.block() #block that spot
            elif self.game.checkForBlock(self.game.getOpposingPlayer()): #if not, check the game to see if the opponent can be blocked
                self.logger.info(self.game.getBlockList())
                chosenSquare = self.game.block() #block the opponent
            else:
                chosenSquare = self.game.selectSquare() #otherwise pick any square.
        else:
            chosenSquare = squareToPlay
            self.game.randomNumber.setToggel(squareToPlay) #otherwise pick any square according to numGenerator

        row = (((chosenSquare - 1) // self.game.getSize()) + 1) #set the row
        column = ((chosenSquare + 2) % self.game.getSize()) + 1 #set the column
        self.game.mark(row, column) #fill in the gameBoard

        if self.game.getWon(): #if anyone wins
            if self.game.getWinner() == 1: #find which player is the winner: if its X
                self.setMessage("X won!")  #set the resultsLabel to X won
                if self.userPlayingWithMark() == 1: #if the userPlayingWithMark is the human and they won
                    self.userWins += 1 #bring up the userWinsCounter by 1
                else:
                    self.userLosses += 1 #otherwise, computer wins
                    self.logger.info("X won!") #print computer won
                self.updateUI()

            else:
                self.setMessage("O won!") #otherwise all the same applies but with O instead of X
                if self.userPlayingWithMark() == 2:
                    self.userWins += 1
                else:
                    self.userLosses += 1
                    self.logger.info("O won!")
                self.updateUI()
                self.logger.info("Game Over")
            self.gameInProgress = False #sets the game to stop
            self.restartTimer = QTimer #restarts the game
            self.restartTime.singleShot(2500, self.restartGame)  #this calls the restarts the function specifically after restartGame is triggered.
        elif self.game.squareAvailable(): #See if the the game has available squares
            self.game.toggleCurrentPlayer() #this ensures that turns are taken one after the other
        else: #if not and nobody has won:
            self.setMessage("Game was a tie!") #its a tie
            self.logger.debug(self.game.displayGame)
            self.logger.info("Game was a tie!")
            self.gameInProgress = False #close the game
            self.updateUI()
            self.restartTimer = QTimer() #restart the game
            self.restartTimer.singleShot(2500, self.restartGame)

        if self.gameInProgress and currentPlayerNumber == self.userPlayingWithMark() and not self.game.getWon(): #if the game is in progress and it is the humans turn and they have not won:
            self.playSquare(self.game.getCurrentPlayer()) #get whatever square they fill in and updateUI

        self.updateUI()

    def restartGame(self):
    #create python class for computer plays
        self.winsCount = 0
        self.lossesCOunt = 0
        self.lossesLabel.setText("")

    @pyqtSlot()
    def dynamicButtonsClickedHandler (self, buttonNumber):
        self.logger.debug("Button %i was clicked" % buttonNumber)

        if self.game.squareIsEmpty(buttonNumber):
            self.setMessage("Square %i was clicked" % buttonNumber)
            self.updateUI()
            self.playSquare(self.userPlayingWithMark(), buttonNumber)
        else:
            self.setMessage("Square %i has been used already" % buttonNumber)
            self.updateUI()

    @pyqtSlot() #user is requesting preferences editing dialog box.
    def preferencesSelectButtonTriggeredHandler(self):
        print("Setting preferences")
        preferencesDialog = PreferencesDialog()
        preferencesDialog.show()
        preferencesDialog.exec_()
        self.restoreSettings()
        self.updateUI()

    @pyqtSlot()
    def restartButtonTriggeredHandler(self):
        self.restartGame()
        self.saveGame()
        self.updateUI()

    @pyqtSlot() #Player asked to quit game
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
    def __init__(self, parent = TicTacToe):
        super(PreferencesDialog, self).__init__()
        self.logger = getLogger("TicTacToe")

        uic.loadUi('PreferencesDialog.ui', self)
        self.appSettings = QSettings()
        if self.appSettings.contains('createLogFile'):
            self.createLogFile=appSettings.value('createLogFile',type=bool)
        else:
            self.createLogFile= logFileNameDefault
            self.appSettings.setValue('createLogFile', self.createLogFile)

        self.buttonBox.accepted.connect(self.okayClickedHandeler)
        self.buttonBox.rejected.connect(self.cancleClickedHandler)
        self.createLogFileCheckBox.stateChanged.connect(self.createLogFileChanged)
        self.radioButtonX.pressed.connect(self.radioButtonXStateChanged)
        self.radioButtonO.pressed.connect(self.radioButtonOStateChanged)

        self.updateUI()

    def createLogFileChanged(self):
        self.createLogFile=self.createLogFileCheckBox

    def updateUI(self):
        if self.createLogFile:
            self.createLogFileCheckBox.setCheckState(Qt.Checked)
        else:
            self.createLogFileCheckBox.setCheckState(Qt.Unchecked)


    def okayClickedHandeler(self):
        #print("Clicked okay handler")
        basePath = path.dirname(path.realpath(__file__))
        #self.logFileName = self.logFileNameEdit.text()
        self.logFileName = "ticTacToe.log"
        #write out all settings
        self.preferencesGroup = (('logFile', self.logFileName), )
        #write settings values.
        for setting, variableName in self.preferencesGroup:
            #if self.appSettings.contains(setting):
            self.appSettings.setValue(setting, variableName)
        self.close()


    def cancleClickedHandler(self):
        self.close()

    def radioButtonXStateChanged(self):
        self.startingMarkChoice = 1

    def radioButtonOStateChanged(self):
        self.startingMarkChoice = 2


if __name__ == "__main__":
    QCoreApplication.setOrganizationName("Cindalis Software");
    QCoreApplication.setOrganizationDomain("cindalissoftware.com");
    QCoreApplication.setApplicationName("TicTacToe");
    appSettings = QSettings()
    startingFolderName = path.dirname(path.realpath(__file__))
    if appSettings.contains('logFile'):
        logFileName = appSettings.value('logFile', type= str)
    else:
        logFileName = logFileNameDefault
        appSettings.setValue('logFile', logFileName)
    basicConfig(filename= path.join(startingFolderName, logFileName), level=INFO, format='%(asctime)s %(name)-8s %(levelName)-8s %(message)s')

    app = QApplication(sys.argv)
    tictactoeApp = TicTacToe()
    tictactoeApp.updateUI()
    tictactoeApp.show()
    sys.exit(app.exec_())
