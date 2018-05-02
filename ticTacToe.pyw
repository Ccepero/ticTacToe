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
playerLetterDefault = 'X'
createLogFileDefault = True

class TicTacToe(QMainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.logger = getLogger("ticTacToe")
        self.appSettings = QSettings()
        self.quitCounter = 0  # used in a workaround for a QT5 Bug.

        uic.loadUi('ticTacToeUI.ui', self)
        self.human = 'X'
        self.computer = 'O'
        self.winsCount = 0
        self.lossesCount = 0
        self.drawsCount = 0
        self.used = []
        self.cornerValues = [self.button1, self.button3, self.button7, self.button9]
        self.players = (self.human, self.computer)

        self.buttonList = [self.button1,
                           self.button2,
                           self.button3,
                           self.button4,
                           self.button5,
                           self.button6,
                           self.button7,
                           self.button8,
                           self.button9]
        self.messageString = "Welcome! Choose your mark in the preferences to Begin."

        if path.exists(path.join(path.dirname(path.realpath(__file__)), self.pickleFileName)):
            self.human,self.computer, self.winsCount, self.lossesCount, self.drawsCount,self.used,self.cornerValues, self.players, self.messageString = self.restoreGame()
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


    def restartGame(self):
        self.winsCount = 0
        self.lossesCOunt = 0
        self.messageString = "Welcome! Choose your mark in the preferences to Begin."
        self.userPlayingWithMark = playerLetterDefault
        self.lossesLabel.setText("")
        for button in self.buttons:
            button.setEnabled(True)
            button.setText("")
        self.used = []
        self.updateUI()

    def saveGame(self):
        saveItems = (self.human,self.computer, self.winsCount, self.lossesCount, self.drawsCount,self.used,self.cornerValues, self.players, self.messageString)
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

    def checkWinner(self):
        if self.button1.text() == self.button2.text() == self.button3.text() and self.button1.text() in self.players:
            return self.button1, self.button2, self.button3

        elif self.button4.text() == self.button5.text() == self.button6.text() and self.button4.text() in self.players:
            return self.button4, self.button5, self.button6

        elif self.button7.text() == self.button8.text() == self.button9.text() and self.button7.text() in self.players:
            return self.button7, self.button8, self.button9

        elif self.button1.text() == self.button4.text() == self.button7.text() and self.button1.text() in self.players:
            return self.button1, self.button4, self.button7

        elif self.button2.text() == self.button5.text() == self.button8.text() and self.button2.text() in self.players:
            return self.button2, self.button5, self.button8

        elif self.button3.text() == self.button6.text() == self.button9.text() and self.button3.text() in self.players:
            return self.button3, self.button6, self.button9

        elif self.button1.text() == self.button5.text() == self.button9.text() and self.button1.text() in self.players:
            return self.button1, self.button5, self.button9

        elif self.button7.text() == self.button5.text() == self.button3.text() and self.button7.text() in self.players:
            return self.button7, self.button5, self.button3
        return False

    def updateUI(self):
        self.lossesLabel.setText(str(self.lossesCount))
        self.winsLabel.setText(str(self.winsCount))
        self.resultsLabel.setText(self.result)

    def clickedHandler(self, number):
        buttonHolder = self.buttons[number - 1]
        buttonHolder.setText(str(self.human))
        buttonHolder.setEnabled(False)

        status = self.checkWinner()
        if status:
            self.winsCount += 1
            self.endGame()
            self.result = "You win!"
            self.updateUI()
            return

        self.getComputerMove()
        status = self.checkWinner()

        if status:
            self.lossesCount += 1
            self.endGame()
            self.result = "You lose!"
            self.updateUI()
            return

        if self.checkBoard():
            self.result = "You draw!"
            self.drawsCount += 1
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
        if self.human == 'X':
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
                self.makeMove(button, self.human)
                if self.checkWinner():
                    self.makeMove(button, self.computer)
                    return
                self.deleteMove(button)

        # Go to center if player uses corner in first try
        if len(self.used) == 1 and self.used[0] in self.cornerValues:
            self.makeMove(self.button5, self.computer)
            return

        # Take the corner if available
        random.shuffle(self.cornerValues)
        for corner in self.cornerValues:
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