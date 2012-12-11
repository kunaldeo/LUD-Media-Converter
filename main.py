#!/usr/bin/env python3

# This application is written by Kunal Deo (kunaldeo2006@gmail.com) and can be redistributed under BSD License
# (c) 2012 Kunal Deo <kunaldeo2006@gmail.com>

from PyQt4 import QtCore, QtGui
from os.path import expanduser
import sys
import fcntl
import os
import subprocess
import shlex
import time

#import Converted Python UI File
from mainwindow import Ui_MainWindow
import resources_rc

__author__ = 'Kunal Deo'

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect the Buttons
        QtCore.QObject.connect(self.ui.selectFileButton,QtCore.SIGNAL("clicked()"),self.selectFile)
        QtCore.QObject.connect(self.ui.convertButton,QtCore.SIGNAL("clicked()"),self.convert)

        # Connect the Radio Buttons
        QtCore.QObject.connect(self.ui.androidHDRadioButton,QtCore.SIGNAL("toggled(bool)"),self.androidHDSelected)
        QtCore.QObject.connect(self.ui.androidQHDRadioButton,QtCore.SIGNAL("toggled(bool)"),self.androidqHDSelected)
        QtCore.QObject.connect(self.ui.appleHDRadioButton,QtCore.SIGNAL("toggled(bool)"),self.appleHDSelected)
        QtCore.QObject.connect(self.ui.appleFullHDRadioButton,QtCore.SIGNAL("toggled(bool)"),self.appleFullHDSelected)
        
        # Draw Images
        self.drawImages()
        
        #Setup Process
        self.process = QtCore.QProcess(self)
        QtCore.QObject.connect(self.process,QtCore.SIGNAL("finished(int)"),self.processCompleted)
        QtCore.QObject.connect(self.process,QtCore.SIGNAL("readyReadStandardError()"),self.readStdError)
                
    # Set the output format

    def drawImages(self):
        pixmap = QtGui.QPixmap("images/webmlogo.png")
        self.ui.imageLabel1.setPixmap(pixmap)
        
        pixmap = QtGui.QPixmap("images/h264logo.jpg")
        self.ui.imageLabel2.setPixmap(pixmap)
    
    def androidHDSelected(self):
        self.ui.outputFormat.setText("Android HD")
        
    def androidqHDSelected(self):
        self.ui.outputFormat.setText("Android qHD")
        
    def appleHDSelected(self):
        self.ui.outputFormat.setText("Apple HD")
        
    def appleFullHDSelected(self):
        self.ui.outputFormat.setText("Apple Full HD")

    def selectFile(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,'Open Media File',expanduser("~"),'Media Files (*.mov *.avi *.mkv *.mpg)')
        self.ui.fileName.setText(fileName)

    def convertFile(self):
        
        inputFile = str(self.ui.fileName.text())
        outputFormat = str(self.ui.outputFormat.text())
        
        if outputFormat == ('Android HD'):
            cmd = '-i "%s" -codec:v libvpx -quality good -cpu-used 0 -b:v 2000k -qmin 10 -qmax 42 -maxrate 2000k -y -bufsize 2000k -vf scale=-1:720 -threads 2 ' + \
                      '-codec:a libvorbis -b:a 128k "%s.webm"'
        elif outputFormat == ('Android qHD'):
            cmd = '-i "%s" -codec:v libvpx -quality good -cpu-used 0 -b:v 1500k -qmin 10 -qmax 42 -maxrate 1500k -y -bufsize 500k -vf scale=-1:540 -threads 2 ' + \
                      '-codec:a libvorbis -b:a 128k "%s.webm"'
        elif outputFormat == ('Apple HD'):
            cmd = '-i "%s" -codec:v libx264 -quality good -cpu-used 0 -b:v 2000k -profile:v baseline -level 30 -y -maxrate 2000k -bufsize 2000k -vf scale=-1:720 -threads 2 ' + \
                      '-codec:a libvo_aacenc -b:a 128k "%s.mp4"'
        elif outputFormat == ('Apple Full HD'):
            cmd = '-i "%s" -codec:v libx264 -quality good -cpu-used 0 -b:v 4000k -profile:v baseline -level 30 -y -maxrate 4000k -bufsize 2000k -vf scale=-1:1080 -threads 2 ' + \
                        '-codec:a libvo_aacenc -b:a 128k "%s.mp4"'
        elif outputFormat == ('Output Format'):
            QtGui.QMessageBox.warning(self,"Input Format Not Selected","Please select an appropriate Output Format")
            return ('Selection Not Proper')
        
        if inputFile == ('File Name'):
            QtGui.QMessageBox.warning(self,"Media Not Selected","Please select a file to convert")
            return ('Selection Not Proper')
        
        argument = shlex.split(cmd % (inputFile,inputFile[:-4]))
        command = os.path.join(os.getcwd(),"ffmpeg")
        
        self.ui.statusText.setText("Please Wait....")
        self.ui.convertButton.setDisabled(True)
        self.process.start(command,argument)
                
    def convert(self):
        self.convertFile()
        
    def processCompleted(self):
        self.ui.statusText.setText("Conversion Complete")
        self.ui.convertButton.setEnabled(True)
        self.ui.textBrowser.append('Conversion Complete')
        
    def readStdError(self):
        self.ui.textBrowser.append(str(self.process.readAllStandardError()))
        
    def openConvertedFile(self):
        fileName = (self.ui.fileName.text())
        

def main():
    app = QtGui.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()




