import PIL.Image
import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QAction
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import  QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QWidget, QLabel,
    QComboBox, QApplication)
from PyQt5.QtWidgets import  QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class gamma(QMainWindow):
    global gammaValue
    def __init__(self, parent=None):
        super(gamma, self).__init__(parent)

        self.getInteger()

    def getInteger(self):
        global gammaValue
        thresholdInputValue, okPressed = QInputDialog.getInt(self, "Get integer", "Gamma:", 0, 0, 3, 1)
        if okPressed:
            gammaValue = 251

class threshold(QMainWindow):
    global thresholdInputValue
    def __init__(self, parent=None):
        super(threshold, self).__init__(parent)

        self.getInteger()

    def getInteger(self):
        global thresholdInputValue
        thresholdInputValue, okPressed = QInputDialog.getInt(self, "Get integer", "Threshold:", 0, 0, 250, 1)

class sobelLaplace(QMainWindow):
    global laplaceSobel
    def __init__(self, parent=None):
        super(sobelLaplace, self).__init__(parent)

        self.getChoice()

    def getChoice(self):
        global laplaceSobel
        items = ("Sobel", "Laplace")
        laplaceSobel, okPressed = QInputDialog.getItem(self, "Get item", "Filter:", items, 0, False)

class App(QMainWindow):

    global fileName
    global saveFileName
    global filterType
    global pxtmp
    global px
    global imtmp
    global im
    global image_save
    global image_file
    global thresholdInputValue
    global laplaceSobel
    global gammaValue

    thresholdInputValue = 0
    fileName = ""
    saveFileName = ""

    def __init__(self):
        super().__init__()
        self.title = 'Image filters created by Megaforce'
        self.left = 50
        self.top = 50
        self.width = 640
        self.height = 400
        self.initUI()

    def onActivated(self, text):
        global filterType
        self.lbl.setText(text)
        filterType = self.lbl.text()
        self.lbl.setText("")


    def initUI(self):

        global filterType
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

        applyButton = QPushButton('Apply filter', self)
        applyButton.setToolTip('This button applys filter')
        applyButton.move(100, 150)
        applyButton.clicked.connect(self.applyFilter)

        applyButton = QPushButton('See new image', self)
        applyButton.setToolTip('This button shows you the new image')
        applyButton.move(100, 200)
        applyButton.clicked.connect(self.showImage)

        self.lbl = QLabel("", self)
        combo = QComboBox(self)

        combo.addItem("Grayscale")
        combo.addItem("Negativ")
        combo.addItem("Box filter")
        combo.addItem("Sharpening")
        combo.addItem("Threshold")
        combo.addItem("Gamma correction")
        combo.addItem("Edge detection")

        combo.move(100, 40)
        self.lbl.move(100, 20)

        combo.activated[str].connect(self.onActivated)

        self.statusBar().showMessage('https://github.com/megaforce/Image-Filters')

        thresholdButton = QPushButton('Threshold value', self)
        thresholdButton.setToolTip('This button sets threshold')
        thresholdButton.move(200, 200)
        thresholdButton.clicked.connect(self.thresholdInput)

        thresholdButton = QPushButton('Gamma value', self)
        thresholdButton.setToolTip('This button sets gamma')
        thresholdButton.move(200, 230)
        thresholdButton.clicked.connect(self.gammaInput)

        filterKind = QPushButton('Laplace/Sobel', self)
        filterKind.setToolTip('This button Laplace/Sobel')
        filterKind.move(200, 250)
        filterKind.clicked.connect(self.setLaplaceSobel)

        self.show()

    @pyqtSlot()
    def setLaplaceSobel(self):
        global laplaceSobel
        dialog = sobelLaplace()
        while (laplaceSobel == 0):
            dialog.show()
    @pyqtSlot()
    def thresholdInput(self):
        global thresholdInputValue
        dialog = threshold()
        while(thresholdInputValue == 0):
            dialog.show()

    @pyqtSlot()
    def gammaInput(self):
        global gammaValue
        dialog = gamma()
        while (gammaValue == 0):
            if (gammaValue == 251):
                gammaValue = 0
            dialog.show()

    @pyqtSlot()
    def showImage(self):
        global image_save
        image_save = saveFileName
        im = PIL.Image.open(image_save)
        im.show()



    def openFileNameDialog(self):
        global fileName
        obj = App()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)


    @pyqtSlot()
    def saveFileDialog(self):
        global saveFileName
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
                px[x, y] = (int(r), int(g), int(b))

    def treshold(self):
        global thresholdInputValue
        n = thresholdInputValue
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

    def edgeDetection(self):
        type = input("Edge detection type (Sobel / Lapace) : ")
        if (type == "Laplace"):
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

    def sharpening(self):
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
        type = input("Kernel type (Sobel / Laplace) : ")
        if (type == "Laplace"):
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

    @pyqtSlot()
    def applyFilter(self):
        global fileName
        global saveFileName
        global filterType
        global pxtmp
        global px
        global imtmp
        global im
        global image_save
        global image_file
        global thresholdInputValue
        global laplaceSobel
        global gammaValue

        image_file = fileName
        image_save = saveFileName
        im = PIL.Image.open(image_file)
        imtmp = PIL.Image.open(image_file)
        px = im.load()
        pxtmp = imtmp.load()
        width, height = im.size

        if(filterType == "Grayscale"):
            for x in range(0, im.size[0]):
                for y in range(0, im.size[1]):
                    r = px[x, y][0] * 0.299
                    g = px[x, y][1] * 0.514
                    b = px[x, y][2] * 0.144
                    gray = r + g + b
                    px[x, y] = (int(gray), int(gray), int(gray))
            im.save(image_save)

        elif(filterType == "Threshold"):
            global thresholdInputValue
            n = thresholdInputValue
            for x in range(0, im.size[0]):
                for y in range(0, im.size[1]):
                    for z in range(0, 3):
                        if (px[x, y][z] > int(n)):
                            px[x, y] = (int(255), int(255), int(255))
                        else:
                            px[x, y] = (int(0), int(0), int(0))
            im.save(image_save)

        elif(filterType == "Negativ"):
            for x in range(0, im.size[0]):
                for y in range(0, im.size[1]):
                    r = 255 - px[x, y][0]
                    g = 255 - px[x, y][1]
                    b = 255 - px[x, y][2]
                    gray = g + r + b
                    px[x, y] = (int(gray), int(gray), int(gray))
            im.save(image_save)

        elif(filterType == "Gamma correction"):
            global gammaValue
            gamma = gammaValue
            for x in range(0, im.size[0]):
                for y in range(0, im.size[1]):
                    r = px[x, y][0] * 0.299
                    g = px[x, y][1] * 0.514
                    b = px[x, y][2] * 0.144
                    gammachange = (r + g + b) ** float(gamma)
                    px[x, y] = (int(gammachange), int(gammachange), int(gammachange))
            im.save(image_save)

        elif (filterType == "Box filter"):
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
                        tmp = ((px[x - 1, y - 1] * matrika[0] + px[x, y - 1] * matrika[1] + px[x + 1, y - 1] * matrika[
                            2] +
                                px[x - 1, y] * matrika[3] + px[x, y] * matrika[4] + px[x + 1, y] * matrika[5] + px[
                                    x - 1, y + 1] * matrika[6] + px[x, y + 1] * matrika[7] + px[x + 1, y + 1] * matrika[
                                    8]) / 9)
                        px[x, y] = (int(tmp), int(tmp), int(tmp))
                im.save(image_save)

        elif (filterType == "Edge detection"):

            if (type == "Laplace"):
                for x in range(1, imtmp.size[0] - 1):
                    for y in range(1, imtmp.size[1] - 1):
                        tmp = (px[x - 1, y - 1][0] * 0 + px[x, y - 1][0] * 1 + px[x + 1, y - 1][0] * 0 + px[x - 1, y][
                            0] * 1 +
                               px[x, y][0] * (-4) + px[x + 1, y][0] * 1 + px[x - 1, y + 1][0] * 0 + px[x, y + 1][
                                   0] * 1 +
                               px[x + 1, y + 1][0] * 0)
                        pxtmp[x, y] = (int(tmp), int(tmp), int(tmp))
                imtmp.save(image_save)
            elif (type == "Sobel"):
                for x in range(1, im.size[0] - 1):
                    for y in range(1, im.size[1] - 1):
                        tmp = (px[x - 1, y - 1][0] * 1 + px[x, y - 1][0] * 2 + px[x + 1, y - 1][0] * 1 + px[x - 1, y][
                            0] * 0 +
                               px[x, y][0] * (0) + px[x + 1, y][0] * 0 + px[x - 1, y + 1][0] * (-1) + px[x, y + 1][
                                   0] * (
                                   -2) +
                               px[x + 1, y + 1][0] * (-1))
                        pxtmp[x, y] = (int(tmp), int(tmp), int(tmp))

                imtmp.save(image_save)

        elif (filterType == "Sharpening"):
            global laplaceSobel
            type = laplaceSobel
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

            if (type == "Laplace"):
                for x in range(1, imtmp.size[0] - 1):
                    for y in range(1, imtmp.size[1] - 1):
                        tmp = (px[x - 1, y - 1][0] * 0 + px[x, y - 1][0] * 1 + px[x + 1, y - 1][0] * 0 + px[x - 1, y][
                            0] * 1 +
                               px[x, y][0] * (-4) + px[x + 1, y][0] * 1 + px[x - 1, y + 1][0] * 0 + px[x, y + 1][
                                   0] * 1 +
                               px[x + 1, y + 1][0] * 0)
                        pxtmp[x, y] = (px[x, y][0] - int(tmp), px[x, y][1] - int(tmp), px[x, y][2] - int(tmp))
                imtmp.save(image_save)
            elif (type == "Sobel"):
                for x in range(1, im.size[0] - 1):
                    for y in range(1, im.size[1] - 1):
                        tmp = (px[x - 1, y - 1][0] * 1 + px[x, y - 1][0] * 2 + px[x + 1, y - 1][0] * 1 + px[x - 1, y][
                            0] * 0 +
                               px[x, y][0] * (0) + px[x + 1, y][0] * 0 + px[x - 1, y + 1][0] * (-1) + px[x, y + 1][
                                   0] * (
                                   -2) +
                               px[x + 1, y + 1][0] * (-1))
                        pxtmp[x, y] = (px[x, y][0] - int(tmp), px[x, y][1] - int(tmp), px[x, y][2] - int(tmp))

                imtmp.save(image_save)


def main():
   app = QApplication(sys.argv)
   ex = App()
   ex.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

