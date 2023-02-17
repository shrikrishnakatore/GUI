import sys
import os
import csv
import PyQt6, pathlib
from PyQt6.QtCore import QTimer, QDateTime, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog, QPlainTextEdit, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6 import uic

import StmProgrammer


class MyApp(QWidget):
    inFname=''
    inSerialNumber=''
    fileFolder=''
    terminate=False
    def __init__(self):
        super().__init__()
        uic.loadUi('gui.ui', self)
        self.showTime.setPlainText(QDateTime.currentDateTime().toString('dddd dd-MM-yyyy hh:mm:ss'))
        self.timer = QTimer(self)
        self.showTime.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        self.timer.timeout.connect(lambda: self.showTime.setPlainText(QDateTime.currentDateTime().toString('dddd dd-MM-yyyy hh:mm:ss')))
        self.timer.start(1000)
        self.statusProgress.setValue(0)
        self.browse.setEnabled(False)
        self.actionCheck.setEnabled(False)
        self.actionProgram.setEnabled(False)
        self.actionCancel.setEnabled(False)
        self.setWindowTitle('ST MICRO PROGRAMMER')
        self.setWindowIcon(QIcon('Re_logo.svg'))
        self.resize(900,800)
        self.serialNumber.setReadOnly(True)
        self.filename.setReadOnly(True)
        self.versionSelect.setInsertPolicy(PyQt6.QtWidgets.QComboBox.InsertPolicy.InsertAlphabetically)
        self.versionSelect.setSizeAdjustPolicy(PyQt6.QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.deviceSelect.setInsertPolicy(PyQt6.QtWidgets.QComboBox.InsertPolicy.InsertAlphabetically)
        self.deviceSelect.setSizeAdjustPolicy(PyQt6.QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.versionSelect.clear()
        self.deviceSelect.insertItems(0,['None','DC1000','PYTHON','PYRAMID'])
        self.deviceSelect.currentIndexChanged.connect(self.deviceselection)
        self.serialNumber.editingFinished.connect(self.deviceSerialNumberChanged)
        self.actionCheck.clicked.connect(self.deviceSerialNumberChanged)
        self.browse.clicked.connect(self.browsefs)
        self.actionProgram.clicked.connect(self.startClicked)
        self.actionCancel.clicked.connect(self.cancelCliked)
        self.commentSection.clear()
        self.commentSection.setReadOnly(True)
        self.deviceLog.clear()
        self.deviceLog.setReadOnly(True)
        self.statusFlashUnlock.setChecked(False)
        self.statusFlashErase.setChecked(False)
        self.statusFlashWrite.setChecked(False)
        self.statusFlashLock.setChecked(False)
        self.statusFlashUnlock.setCheckable(False)
        self.statusFlashErase.setCheckable(False)
        self.statusFlashWrite.setCheckable(False)
        self.statusFlashLock.setCheckable(False)


    def versionselection(self):
        if(self.versionSelect.count() != 0):
            self.fileFolder = os.getcwd()+'\\' + self.deviceSelect.currentText()
            self.inFname = self.fileFolder+'\\'+[file for file in os.listdir(self.fileFolder)  if file.endswith(self.versionSelect.currentText().replace('.','_') +'.elf')][0]
            self.filename.setText(self.inFname)
        else:
            self.fileFolder = os.getcwd()
            self.filename.clear()

    def deviceselection(self):
        self.versionSelect.clear()
        self.commentSection.setReadOnly(False)
        if(self.deviceSelect.currentText()!= 'None'):
            self.browse.setEnabled(True)
            self.actionCheck.setEnabled(True)
            self.fileFolder = os.getcwd()+'\\' + self.deviceSelect.currentText()
            self.serialNumber.setReadOnly(False)
            files = [file for file in os.listdir(self.fileFolder)  if file.endswith('.elf')]
            if files:
                for ver in files:
                    self.versionSelect.addItem(ver[-10:][:6].replace('_','.'))
                self.versionSelect.setCurrentIndex(self.versionSelect.count()-1)
                self.versionSelect.currentIndexChanged.connect(self.versionselection)
                self.inFname = self.fileFolder+'\\' + max(files)
                self.filename.setText(self.inFname)
            else:
                self.inFname = ''
                self.filename.clear()
                try:
                    self.versionSelect.currentIndexChanged.disconnect()
                except TypeError:
                    pass
                QMessageBox.warning(self,"WARNING", "No Firmware file present for " + self.deviceSelect.currentText() + ' select the file using browse button or put the file in the folder named :' + self.deviceSelect.currentText() + ' and restart the application')
        else:
            self.filename.clear()
            self.browse.setEnabled(False)
            self.actionCheck.setEnabled(False)
            self.serialNumber.setReadOnly(True)
            QMessageBox.warning(self,"WARNING", "Select a device first")
            

    def browsefs(self):
        file = QFileDialog.getOpenFileName(self, 'Open file', self.fileFolder, 'ELF files (*.elf)')[0]
        if file.lower().endswith('.elf') :
            self.inFname = file
            self.filename.setText(self.inFname)
        else:
            if(self.inFname):
                self.filename.setText(self.inFname)
                QMessageBox.warning(self,"WARNING", "No new file selected!! , Using a file :-\n" + self.inFname)
            else:
                QMessageBox.critical(self,"ERROR", "Select valid file !!")

    def deviceSerialNumberChanged(self):
        self.deviceLog.clear()
        if(self.serialNumber.text() == ''):
            QMessageBox.warning(self,"WARNING", "Enter a valid PCB Serial Number")
            self.actionProgram.setEnabled(False)
        else:
            self.inSerialNumber=self.serialNumber.text()
            if pathlib.Path(self.fileFolder+'\\'+ 'device_log.csv').exists():
                with open(self.fileFolder+'\\'+ 'device_log.csv','r',encoding='UTF8') as log_file:
                    devices = csv.reader(log_file)
                    for device in devices:
                        try:
                            if device[0] == self.inSerialNumber:
                                self.deviceLog.setPlainText(device[2])
                        except:
                            continue
            self.actionProgram.setEnabled(True)

    def startClicked(self):
        self.inSerialNumber=self.serialNumber.text()
        self.statusProgress.setValue(0)
        self.statusFlashUnlock.setCheckable(True)
        self.statusFlashErase.setCheckable(True)
        self.statusFlashWrite.setCheckable(True)
        self.statusFlashLock.setCheckable(True)
        self.statusFlashUnlock.setChecked(False)
        self.statusFlashErase.setChecked(False)
        self.statusFlashWrite.setChecked(False)
        self.statusFlashLock.setChecked(False)
        self.statusFlashUnlock.setCheckable(False)
        self.statusFlashErase.setCheckable(False)
        self.statusFlashWrite.setCheckable(False)
        self.statusFlashLock.setCheckable(False)
        if(self.inSerialNumber == ''):
            QMessageBox.warning(self,"WARNING", "Enter a valid PCB Serial Number")
        else:
            if pathlib.Path(self.inFname).is_file():
                self.browse.setEnabled(False)
                self.commentSection.setReadOnly(True)
                self.actionProgram.setEnabled(False)
                self.actionCancel.setEnabled(True)
                self.actionCheck.setEnabled(False)
                self.serialNumber.setReadOnly(True)
                self.deviceSelect.setEnabled(False)
                self.versionSelect.setEnabled(False)
                if(self.programming() ==0):
                    self.log_info()
                else:
                    QMessageBox.critical(self,"ERROR", "ERROR in Programming , device not programmed !!")
                self.browse.setEnabled(True)
                self.commentSection.setReadOnly(False)
                self.actionProgram.setEnabled(True)
                self.actionCancel.setEnabled(False)
                self.actionCheck.setEnabled(True)
                self.serialNumber.setReadOnly(False)
                self.deviceSelect.setEnabled(True)
                self.versionSelect.setEnabled(True)
            else :
                self.browse.setEnabled(True)
                self.inSerialNumber.setReadOnly(False)
                self.actionCancel.setEnabled(False)
                self.actionCheck.setEnabled(True)
                self.commentSection.setReadOnly(False)
                QMessageBox.critical(self,"ERROR", "Selected file dose not exist !!")

    def cancelCliked(self):
        self.actionProgram.setEnabled(True)

    def programming(self):
        stmDevice = StmProgrammer.stmdevice()
        if(stmDevice.unlock()!=0):
            return -1
        self.statusFlashUnlock.setCheckable(True)
        self.statusFlashUnlock.setChecked(True)
        self.statusFlashUnlock.setCheckable(False)
        self.statusProgress.setValue(25)
        if(stmDevice.erase()!=0):
            return -1
        self.statusFlashErase.setCheckable(True)
        self.statusFlashErase.setChecked(True)
        self.statusFlashErase.setCheckable(False)
        self.statusProgress.setValue(50)
        if(stmDevice.flash(self.inFname)!=0):
            return -1
        if(stmDevice.reset()!=0):
            return -1
        self.statusFlashWrite.setCheckable(True)
        self.statusFlashWrite.setChecked(True)
        self.statusFlashWrite.setCheckable(False)
        self.statusProgress.setValue(75)
        if(stmDevice.lock()!=0):
            return -1
        self.statusFlashLock.setCheckable(True)
        self.statusFlashLock.setChecked(True)
        self.statusFlashLock.setCheckable(False)
        self.statusProgress.setValue(100)
        return 0

    def log_info(self):
        found=False
        rows=[]
        time = QDateTime.currentDateTime().toString('dd-MM-yyyy hh:mm:ss')
        if not pathlib.Path(self.fileFolder+'\\'+ 'device_log.csv').exists():
            with open(self.fileFolder+'\\'+ 'device_log.csv','w',encoding='UTF8') as empty_file:
                csv.writer(empty_file).writerow(['PCB Serial Number','Last Programmed', 'Comment','Files used'])
        with open(self.fileFolder+'\\'+ 'device_log.csv','r',encoding='UTF8') as log_file:
            devices = list(csv.reader(log_file))
            for row in devices:
                try:
                    if row[0] == self.inSerialNumber:
                        row[2] = time + ' : '+ self.commentSection.toPlainText() +'\n' + row[2]
                        row[1] = time
                        row[3] = time + ' : ' + self.inFname + '\n' + row[3]
                        found = True
                    rows.append(row)
                except:
                    continue
        if found == False:
            row=['','','','']
            row[0] = self.inSerialNumber
            row[2] = time +' : ' + self.commentSection.toPlainText()
            row[1] = time
            row[3] = time + ' : ' + self.inFname
            rows.append(row)
        with open(self.fileFolder+'\\'+ 'device_log.csv','w',encoding='UTF8') as log_file:
            device_writer = csv.writer(log_file)
            device_writer.writerows(rows)


if __name__ == '__main__':
    os.environ["PATH"] ="C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\\bin;"+ os.environ["PATH"]
    app = QApplication(sys.argv)
    mainwindow = MyApp()
    mainwindow.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')



