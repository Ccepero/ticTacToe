#! /usr/bin/env python
__author__ = 'Cindalis Cepero'

from sys import path
import sys, random
import ticTacToeResource_rc
from time import sleep
from logging import basicConfig, getLogger, DEBUG, INFO, CRITICAL
from pickle import dump, load
from os import path
from PyQt5.QtCore import pyqtSlot, QCoreApplication, QSettings, QTimer
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox

logFilenameDefault = 'ticTactoe.log'
pickleFilenameDefault = ".ticTactoeSavedObjects.pl"
playerLetterDefault = 'x'

class Board(QMainWindow):
    def __init__(self, parent=None):
        """Build a game with _____"""

        super().__init__(parent)

        self.logger = getLogger("Cepero.ticTacToe")
        self.appSettings = QSettings()
        self.quitCounter = 0  # used in a workaround for a QT5 bug.

        uic.loadUi("ticTacToeUI.ui", self)
        self.result = "Welcome to Tic Tac Tce!!"
        self.pickleFilename = pickleFilenameDefault
        self.player = 'X'
        self.computer = 'O'
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.used = []
        self.corners = [self.button1, self.button3, self.button7, self.button9]
        self.values = (self.player, self.computer)
        self.buttons = [self.button1, self.button2, self.button3, self.button4, self.button5, self.button6, self.button7,
                           self.button8, self.button9]
        self.results = 'Welcome to Tic Tac Toe'
        self.button1.clicked.connect(lambda: self.clickedHandler(1))
        self.button2.clicked.connect(lambda: self.clickedHandler(2))
        self.button3.clicked.connect(lambda: self.clickedHandler(3))
        self.button4.clicked.connect(lambda: self.clickedHandler(4))
        self.button5.clicked.connect(lambda: self.clickedHandler(5))
        self.button6.clicked.connect(lambda: self.clickedHandler(6))
        self.button7.clicked.connect(lambda: self.clickedHandler(7))
        self.button8.clicked.connect(lambda: self.clickedHandler(8))
        self.button9.clicked.connect(lambda: self.clickedHandler(9))
        self.restartButton.clicked.connect(self.restartGame)
        self.restartButton.clicked.connect(self.restartGame)

        # self.restoreSettings()

    def restartGame(self):
        for button in self.buttons:
            button.setEnabled(True)
            button.setText("")
        self.used = []
        self.result = "Another round of Tic Tac Toe!"
        self.updateUI()

    def checkWinner(self):
        if self.button1.text() == self.button2.text() == self.button3.text() and self.button1.text() in self.values:
            return self.button1, self.button2, self.button3

        elif self.button4.text() == self.button5.text() == self.button6.text() and self.button4.text() in self.values:
            return self.button4, self.button5, self.button6

        elif self.button7.text() == self.button8.text() == self.button9.text() and self.button7.text() in self.values:
            return self.button7, self.button8, self.button9

        elif self.button1.text() == self.button4.text() == self.button7.text() and self.button1.text() in self.values:
            return self.button1, self.button4, self.button7

        elif self.button2.text() == self.button5.text() == self.button8.text() and self.button2.text() in self.values:
            return self.button2, self.button5, self.button8

        elif self.button3.text() == self.button6.text() == self.button9.text() and self.button3.text() in self.values:
            return self.button3, self.button6, self.button9

        elif self.button1.text() == self.button5.text() == self.button9.text() and self.button1.text() in self.values:
            return self.button1, self.button5, self.button9

        elif self.button7.text() == self.button5.text() == self.button3.text() and self.button7.text() in self.values:
            return self.button7, self.button5, self.button3
        return False

    def updateUI(self):
        self.lossesLabel.setText(str(self.losses))
        self.winsLabel.setText(str(self.wins))
        self.resultsLabel.setText(self.result)

    def clickedHandler(self, number):
        buttonHolder = self.buttons[number - 1]
        buttonHolder.setText(str(self.player))
        buttonHolder.setEnabled(False)

        status = self.checkWinner()
        if status:
            self.wins += 1
            self.endGame()
            self.result = "You win!"
            self.updateUI()
            return

        self.getComputerMove()
        status = self.checkWinner()

        if status:
            self.losses += 1
            self.endGame()
            self.result = "You lose!"
            self.updateUI()
            return

        if self.checkBoard():
            self.result = "You draw!"
            self.draws += 1
            self.updateUI()
            self.endGame()
            return

    def endGame(self):
        for button in self.buttons:
            button.setEnabled(False)

    def makeMove(self, arg, value, boolean=True, append=True):
        arg.setText(value)
        if boolean:
            arg.setEnabled(False)
        if append:
            self.used.append(arg)

    def deleteMove(self, arg):
        arg.setText("")
        arg.setEnabled(True)
        if arg in self.used:
            self.used.remove(arg)

    def getComputerMove(self):
        if self.player == 'X':
            self.computer = 'O'
        else:
            self.computer = 'X'

        # First check if computer can be a winner
        for button in self.buttons:
            if button.isEnabled():
                self.makeMove(button, self.computer)
                if self.checkWinner():
                    return
                else:
                    self.deleteMove(button)

        # Second check if player can be a winner
        for button in self.buttons:
            if button.isEnabled():
                self.makeMove(button, self.player)
                if self.checkWinner():
                    self.makeMove(button, self.computer)
                    return
                self.deleteMove(button)

        # Go to center if player uses corner in first try
        if len(self.used) == 1 and self.used[0] in self.corners:
            self.makeMove(self.button5, self.computer)
            return

        # Take the corner if available
        random.shuffle(self.corners)
        for corner in self.corners:
            if corner.isEnabled():
                self.makeMove(corner, self.computer)
                return

        # Take the middle position if available
        if self.button5.isEnabled():
            self.makeMove(self.button5, self.computer)
            return

        # Random
        random.shuffle(self.buttons)
        for button in self.buttons:
            if button.isEnabled():
                self.makeMove(button, self.computer)
                return

    def checkBoard(self):
        for button in self.buttons:
            if button.isEnabled():
                return False
        return True

    def isSpaceFree(board, move):
        return board[move] == ' '

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
    def __init__(self):
        super(PreferencesDialog, self).__init__()
        self.logger = getLogger("ticTactoe")

        uic.loadUi('PreferencesButton.ui', self)
        self.appSettings = QSettings()
        if self.appSettings.contains('createLogFile'):
            self.createLogFile=appSettings.value('createLogFile',type=bool)
        else:
            self.createLogFile= 'ticTactoe.log'
            self.appSettings.setValue('createLogFile', self.createLogFile)

        self.buttonBox.accepted.connect(self.okayClickedHandeler)
        self.buttonBox.rejected.connect(self.cancleClickedHandler)
        self.createLogFileCheckBox.stateChanged.connect(self.createLogFileChanged)

        self.updateUI()

    def createLogFileChanged(self):
        self.createLogFile=self.createLogFileCheckBox

    def updateUI(self):
        if self.createLogFile:
            self.createLogFileCheckBox.setCheckState(QtGui.Checked)
        else:
            self.createLogFileCheckBox.setCheckState(QtGui.Unchecked)


    @pyqtSlot()
    def okayClickedHandeler(self):
        print("Clicked okay button")
        basePath = path.dirname(path.realpath(__file__))
        self.logFileName = self.ticTagtoe.log()
        self.logFileName = "ticTactoe.log"
        self.preferencesGroup = (('logFile', self.logFileName), )
        #write settings values.
        for setting, variableName in self.preferencesGroup:
           # if self.appSettings.contains(setting):
            self.appSettings.setValue(setting, variableName)
        self.close()


    def cancleClickedHandler(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    testApp = Board()
    testApp.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
        QCoreApplication.setOrganizationName("Jazmine's Organization");
        QCoreApplication.setOrganizationDomain("jazminezation.com");
        QCoreApplication.setApplicationName("TicTacToe");
        appSettings = QSettings()
        startingFolderName = path.dirname(path.realpath(__file__))
        if appSettings.contains('logFile'):
            logFileName = appSettings.value('logFile', type=str)
        else:
            logFileName = 'ticTactoe.log'
            appSettings.setValue('logFile', logFileName)
        basicConfig(filename=path.join(startingFolderName, logFileName), level=INFO,
                    format='%(asctime)s %(name)-8s %(levelName)-8s %(message)s')