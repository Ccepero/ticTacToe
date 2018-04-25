#! /usr/bin/env python
__author__ = 'Cindalis Cepero'

#!/usr/bin/env python
from sys import path
import sys
from os import path
import random
# from ticTacToeGame import *
import ticTacToeResource_rc
from time import sleep
from logging import basicConfig, getLogger, DEBUG, INFO, CRITICAL
from pickle import dump, load
from PyQt5.QtCore import pyqtSlot, QSettings, QCoreApplication, Qt, QTimer
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import  QMainWindow, QApplication, QDialog, QMessageBox

logFileNameDefault = 'dice.log'
pickleFileNameDefault = ".crapsSavedObjects.pl"

class TicTacToe(QMainWindow) :

    def __init__( self, parent=None ):

        super().__init__(parent)

        self.logger = getLogger("TicTacToe")
        self.appSettings = QSettings("Cepero Software", "TicTacToe")
        self.quitCounter = 0

        self.game = TicTacToe()

        uic.loadUi('ticTacToeUI.ui', self)

        self.userPlayingWithMark = self.appSettings.value("startingMarkChoice")
        self.userWins = 0
        self.computerWins = 0
        self.gameInProgress = True
        self.messageString = "Welcome! Click Start to Begin."
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

        self.markLabelButton.clicked.connect(self.markLabelButtonClickedHandler)
        self.restartButton.triggered.connect(self.restartButtonTriggeredHandler)
        self.quitButton.triggered.connect(self.quitButtonTriggeredHandler)
        self.preferencesButton.triggered.connect(self.preferencesSelectButtonTriggeredHandler)

        self.pickleFileName = pickleFileNameDefault

        self.restoreSettings()

        if path.exists(self.pickleFileName):
            self.userPlayingWithMark, self.userWins, self.computerWins, self.gameInProgress, self.messageString, self.game = self.restoreGame()

        else:
            self.restartGame()

    def button1Handler(self):
        #unfilled
        pass

    def __str__(self):
        return "Game: {0}".format(self.game.displayGame())

    def saveGame(self):
        saveItems = (self.winsCount, self.lossesCOunt)
        if self.appSettings.contains('pickleFileName'):
            with open(path.join(path.dirname(path.realpath(__file__)), self.appSettings.value('pickleFileName', type= str)), 'wb') as pickleFile:
                dump(saveItems, pickleFile)
        else:
            self.logger.critical("No pickle Filename")
    def saveSettings(self):
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
            self.appSettings.value('pickleFileName', type = str)
            with open(path.join(path.dirname(path.realpath(__file__)), self.appSettings.value('pickleFileName', type= str)), 'rb') as pickleFile:
                return load(pickleFile)
        else:
            self.logger.critical("No pickle Filename")
    def restoreSettings(self):
        if self.appSettings.contains('radioButtonX'): #implement X radio button, if clicked then start as X and stay as X untill someone wins/ all boxes are filled. If the user picks X, then the Comp must be O.
            self.radioButtonX = self.appSettings.value('radioButtonX', type=bool)
        else:
            self.radioButtonX = radioButtonXDefault
            self.appSettings.setValue('radioButtonX', self.radioButtonX)
        if self.appSettings.contains('radioButtonO'): #implement O, if clicked then start as X and stay as X untill someone wins/all boxes are filled. If the user picks O, then the Comp must be X
            self.radioButtonO = self.appSettings.value('radioButtonO', type=bool)
        else:
            self.radioButtonO = radioButtonODefault
            self.appSettings.setValue('radioButtonO', self.radioButtonO)
        if self.appSettings.contains('createLogFile'):
            self.createLogFile=appSettings.value('createLogFile',type=bool)
        else:
            self.createLogFile= logFileNameDefault
            self.appSettings.setValue('createLogFile', self.createLogFile)

    def updateUI(self):
        for squareNumber in range(1,10):
            if self.gameBoard.squareIsEmpty(squareNumber):
                self.buttonList[squareNumber - 1].setText("")
            elif self.gameBoard.getSquareValue(squareNumber) == 1:
                self.buttonList[squareNumber - 1].setText("X")
            else:
                self.buttonList[squareNumber - 1].setText("O")
        self.userWinsLabel.setText("%i" % self.userWins)
        self.computerWinsLabel.setText("%i" % self.computerWins)
        self.resultsLabel.setText(self.messageString)
        if self.userPlayingWithMark == 1:
            self.markLabelButton.setText("X")
        elif self.userPlayingWithMark == 2:
            self.markLabelButton.setText("O")
        else:
            self.markLabelButton.setText("-")

    def setUserPlayerWithMark(self, playerNumber):
        if playerNumber == 1 or playerNumber == 2:
            self.userPlayingWithMark = playerNumber
        else:
            self.logger.error("invalid playerNumber in setUserPlayerNumber: {0}".format(playerNumber))

    def clearUserPlayerWithMark(self):
        self.userPlayingWithMark = self.startingMarkChoice

    def getUserPlayerWithMark(self):
        return self.userPlayingWithMark

    def playSquare(self, currentPlayerNumber, squareToPlay = -1):

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
            self.playSquare(self.getUserPlayerWithMark(), buttonNumber)
        else:
            self.setMessage("Square %i has been used already" % buttonNumber)
            self.updateUI()

    @pyqtSlot()
    def markLabelButtonClickedHandler(self): #The buttons (1-9)


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

    @pyqtSlot()
    def quitButtonTriggeredHandler(self):

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
    #put in saveSettings
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
