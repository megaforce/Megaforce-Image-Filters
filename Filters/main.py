import PIL.Image
import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QAction
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import  QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QWidget, QLabel,
    QComboBox, QApplication)
from PyQt5.QtWidgets import  QLabel
from PyQt5.QtGui import QIcon, QPixmap

class App(QMainWindow):

    global fileName
    global saveFileName

    fileName = ""
    saveFileName = ""
    if (fileName != "" and saveFileName != ""):
        global image_file
        image_file = fileName
        global image_save
        image_save = saveFileName
        global im
        im = PIL.Image.open(image_file)
        global imtmp
        imtmp = PIL.Image.open(image_file)
        global px
        px = im.load()
        global pxtmp
        pxtmp= imtmp.load()
        width, height = im.size

    def __init__(self):
        super().__init__()
        self.title = 'Image filters created by Megaforce https://github.com/megaforce/Image-Filters'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 400
        self.initUI()

    def onActivated(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        helpMenu = mainMenu.addMenu('Help')


        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        loadFileButton = QPushButton('Load Image', self)
        loadFileButton.setToolTip('This button loads an image')
        loadFileButton.move(100, 70)
        loadFileButton.clicked.connect(self.openFileNameDialog)

        saveFileButton = QPushButton('Save Image', self)
        saveFileButton.setToolTip('This button saves an image')
        saveFileButton.move(100, 100)
        saveFileButton.clicked.connect(self.saveFileDialog)

        self.lbl = QLabel("", self)
        combo = QComboBox(self)
        combo.addItem("Grayscale")
        combo.addItem("Negativ")
        combo.addItem("Box filter")
        combo.addItem("Sharpening")
        combo.addItem("Threshold")

        combo.move(100, 40)
        self.lbl.move(100, 20)

        combo.activated[str].connect(self.onActivated)



        self.show()




    @pyqtSlot()
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)

    @pyqtSlot()
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        saveFileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if saveFileName:
            print(saveFileName)

    def grayscale(self):
        for x in range(0, im.size[0]):
            for y in range(0, im.size[1]):
                r = px[x, y][0] * 0.299
                g = px[x, y][1] * 0.514
                b = px[x, y][2] * 0.144
                gray = r + g + b
                px[x, y] = (int(gray), int(gray), int(gray))
        im.save(image_save)

    def gammaCorrection(self):
        gamma = input("Gamma factor ")
        for x in range(0, im.size[0]):
            for y in range(0, im.size[1]):
                r = px[x, y][0] * 0.299
                g = px[x, y][1] * 0.514
                b = px[x, y][2] * 0.144
                gammachange = (r + g + b) ** float(gamma)
                px[x, y] = (int(gammachange), int(gammachange), int(gammachange))

    def negativ(self):
        for x in range(0, im.size[0]):
            for y in range(0, im.size[1]):
                r = 255 - px[x, y][0]
                g = 255 - px[x, y][1]
                b = 255 - px[x, y][2]
                gray = g + r + b
                px[x, y] = (int(gray), int(gray), int(gray))

    def treshold(self):
        n = input("Treshold ")
        for x in range(0, im.size[0]):
            for y in range(0, im.size[1]):
                for z in range(0, 3):
                    if (px[x, y][z] > int(n)):
                        px[x, y] = (int(255), int(255), int(255))
                    else:
                        px[x, y] = (int(0), int(0), int(0))

    def boxfilter(self):
        matrika = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        for x in range(0 + 1, im.size[0] - 1):
            for y in range(0 + 1, im.size[1] - 1):
                if ((y == 0 and x == 0) or (y == im.size[0] and x == 0)):
                    tmp = ((px[x, y][0] + px[x, y][1] + px[x, y][2]) + (
                                px[x + 1, y][0] + px[x + 1, y][1] + px[x + 1, y][2]) + (
                                       px[x, y + 1][0] + px[x, y + 1][1] + px[x, y + 1][2]) + (
                                       px[x + 1, y + 1][0] + px[x + 1, y + 1][1] + px[x + 1, y + 1][2]))
                    px[x, y] = (int(tmp / 4), int(tmp / 4), int(tmp / 4))
                elif ((y == 0 and x == im.size[1]) or (y == im.size[0] and x == im.size[1])):
                    tmp = ((px[x, y][0] + px[x, y][1] + px[x, y][2]) + (
                                px[x - 1, y][0] + px[x - 1, y][1] + px[x - 1, y][2]) + (
                                       px[x, y - 1][0] + px[x, y - 1][1] + px[x, y - 1][2]) + (
                                       px[x + 1, y - 1][0] + px[x + 1, y - 1][1] + px[x + 1, y - 1][2]))
                    px[x, y] = (int(tmp / 4), int(tmp / 4), int(tmp / 4))
                else:
                    tmp = ((px[x - 1, y - 1] * matrika[0] + px[x, y - 1] * matrika[1] + px[x + 1, y - 1] * matrika[2] +
                            px[x - 1, y] * matrika[3] + px[x, y] * matrika[4] + px[x + 1, y] * matrika[5] + px[
                                x - 1, y + 1] * matrika[6] + px[x, y + 1] * matrika[7] + px[x + 1, y + 1] * matrika[
                                8]) / 9)
                    px[x, y] = (int(tmp), int(tmp), int(tmp))

    def EdgeDetection(self):
        type = input("Edge detection type (Sobel / Lapace) : ")
        if (type == "Lapace"):
            for x in range(1, imtmp.size[0] - 1):
                for y in range(1, imtmp.size[1] - 1):
                    tmp = (px[x - 1, y - 1][0] * 0 + px[x, y - 1][0] * 1 + px[x + 1, y - 1][0] * 0 + px[x - 1, y][
                        0] * 1 +
                           px[x, y][0] * (-4) + px[x + 1, y][0] * 1 + px[x - 1, y + 1][0] * 0 + px[x, y + 1][0] * 1 +
                           px[x + 1, y + 1][0] * 0)
                    pxtmp[x, y] = (int(tmp), int(tmp), int(tmp))
            imtmp.save(image_save)
        elif (type == "Sobel"):
            for x in range(1, im.size[0] - 1):
                for y in range(1, im.size[1] - 1):
                    tmp = (px[x - 1, y - 1][0] * 1 + px[x, y - 1][0] * 2 + px[x + 1, y - 1][0] * 1 + px[x - 1, y][
                        0] * 0 +
                           px[x, y][0] * (0) + px[x + 1, y][0] * 0 + px[x - 1, y + 1][0] * (-1) + px[x, y + 1][0] * (
                               -2) +
                           px[x + 1, y + 1][0] * (-1))
                    pxtmp[x, y] = (int(tmp), int(tmp), int(tmp))

            imtmp.save(image_save)

    def Sharpening(self):
        im2 = PIL.Image.open(image_file)
        px2 = im2.load()
        for x in range(0, im2.size[0]):
            for y in range(0, im2.size[1]):
                r = px2[x, y][0] * 0.299
                g = px2[x, y][1] * 0.514
                b = px2[x, y][2] * 0.144
                gray = r + g + b
                px2[x, y] = (int(gray), int(gray), int(gray))
        im2.save(image_save)


        im = PIL.Image.open(image_save)
        imtmp = PIL.Image.open(image_save)
        px = im.load()
        pxtmp = imtmp.load()
        type = input("Kernel type (Sobel / Lapace) : ")
        if (type == "Lapace"):
            for x in range(1, imtmp.size[0] - 1):
                for y in range(1, imtmp.size[1] - 1):
                    tmp = (px[x - 1, y - 1][0] * 0 + px[x, y - 1][0] * 1 + px[x + 1, y - 1][0] * 0 + px[x - 1, y][
                        0] * 1 +
                           px[x, y][0] * (-4) + px[x + 1, y][0] * 1 + px[x - 1, y + 1][0] * 0 + px[x, y + 1][0] * 1 +
                           px[x + 1, y + 1][0] * 0)
                    pxtmp[x, y] = (px[x, y][0] - int(tmp), px[x, y][1] - int(tmp), px[x, y][2] - int(tmp))
            imtmp.save(image_save)
        elif (type == "Sobel"):
            for x in range(1, im.size[0] - 1):
                for y in range(1, im.size[1] - 1):
                    tmp = (px[x - 1, y - 1][0] * 1 + px[x, y - 1][0] * 2 + px[x + 1, y - 1][0] * 1 + px[x - 1, y][
                        0] * 0 +
                           px[x, y][0] * (0) + px[x + 1, y][0] * 0 + px[x - 1, y + 1][0] * (-1) + px[x, y + 1][0] * (
                               -2) +
                           px[x + 1, y + 1][0] * (-1))
                    pxtmp[x, y] = (px[x, y][0] - int(tmp), px[x, y][1] - int(tmp), px[x, y][2] - int(tmp))

            imtmp.save(image_save)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

