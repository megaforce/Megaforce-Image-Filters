import PIL.Image
import sys
from PyQt5.QtWidgets import QMainWindow, QAction
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import  QLabel
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (QProgressBar)
from PyQt5.QtWidgets import (QPushButton, QApplication)
import webbrowser

class reportAnError(QMainWindow):
    def __init__(self, parent=None):
        super(reportAnError, self).__init__(parent)

        webbrowser.open('https://github.com/megaforce/Megaforce-Image-Filters/issues')

class about(QMainWindow):
    def __init__(self, parent=None):
        super(about, self).__init__(parent)

        webbrowser.open('https://github.com/megaforce/Megaforce-Image-Filters/blob/master/README.md')

class gamma(QMainWindow):
    global gammaValue
    def __init__(self, parent=None):
        super(gamma, self).__init__(parent)

        self.getInteger()

    def getInteger(self):
        global gammaValue
        gammaValue, okPressed = QInputDialog.getDouble(self, "Get integer", "Gamma:", 0, 0, 3,2)


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
    global Percentage
    global imageType

    thresholdInputValue = 0
    fileName = ""
    saveFileName = ""
    image_file = ""
    image_save = ""
    filterType = ""
    gammaValue = 0
    thresholdInputValue = 125
    imageType = ".jpg"
    laplaceSobel = "Sobel"
    filterType = "Grayscale"

    def __init__(self):
        super().__init__()
        self.title = 'Megaforce image filters'
        self.left = 50
        self.top = 50
        self.width = 670
        self.height = 300
        self.setFixedSize(self.width, self.height)
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
        fileMenu = mainMenu.addMenu('Aplication')
        helpMenu = mainMenu.addMenu('Help')

        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)

        issuesButton = QAction(QIcon('exit24.png'), 'Report an error', self)
        issuesButton.triggered.connect(self.getlIssuesBox)

        aboutButton = QAction(QIcon('exit24.png'), 'About', self)
        aboutButton.triggered.connect(self.getaboutBox)

        helpMenu.addAction(aboutButton)
        helpMenu.addAction(issuesButton)
        fileMenu.addAction(exitButton)


        loadFileButton = QPushButton('Load Image', self)
        loadFileButton.setToolTip('This button loads an image')
        loadFileButton.move(20, 65)
        loadFileButton.clicked.connect(self.openFileNameDialog)

        saveFileButton = QPushButton('Save Image', self)
        saveFileButton.setToolTip('This button saves an image')
        saveFileButton.move(20, 100)
        saveFileButton.clicked.connect(self.saveFileDialog)

        applyButton = QPushButton('Apply filter', self)
        applyButton.setToolTip('This button applys filter')
        applyButton.move(20, 135)
        applyButton.clicked.connect(self.applyFilter)

        showOldButton = QPushButton('See old image', self)
        showOldButton.setToolTip('This button shows you the old image')
        showOldButton.move(300, 240)
        showOldButton.clicked.connect(self.showOldImage)

        showNewButton = QPushButton('See new image', self)
        showNewButton.setToolTip('This button shows you the new image')
        showNewButton.move(525, 240)
        showNewButton.clicked.connect(self.showImage)

        self.lbl = QLabel("", self)
        combo = QComboBox(self)

        combo.addItem("Grayscale")
        combo.addItem("Negativ")
        combo.addItem("Box filter")
        combo.addItem("Sharpening")
        combo.addItem("Threshold")
        combo.addItem("Gamma correction")
        combo.addItem("Edge detection")

        combo.move(20, 30)
        self.lbl.move(100, 20)

        combo.activated[str].connect(self.onActivated)

        thresholdButton = QPushButton('Threshold value', self)
        thresholdButton.setToolTip('This button sets threshold')
        thresholdButton.move(20, 170)
        thresholdButton.clicked.connect(self.thresholdInput)

        thresholdButton = QPushButton('Gamma value', self)
        thresholdButton.setToolTip('This button sets gamma')
        thresholdButton.move(20, 205)
        thresholdButton.clicked.connect(self.gammaInput)

        filterKind = QPushButton('Laplace/Sobel', self)
        filterKind.setToolTip('This button Laplace/Sobel')
        filterKind.move(20, 240)
        filterKind.clicked.connect(self.setLaplaceSobel)

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(20, 280, 640, 10)

        self.show()

    def paintEvent(self, event):
        global fileName
        global saveFileName
        painter = QPainter(self)
        painter.begin(self)
        pixmap = QPixmap(fileName)
        painter.drawPixmap(QRect(200, 30, 200, 200), pixmap)
        painter2 = QPainter(self)
        painter2.begin(self)
        pixmap2 = QPixmap(saveFileName)
        painter2.drawPixmap(QRect(420, 30, 200, 200), pixmap2)
        painter.end()

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
        dialog.show()

    @pyqtSlot()
    def gammaInput(self):
        global gammaValue
        dialog = gamma()
        dialog.show()

    @pyqtSlot()
    def showImage(self):
        global image_save
        if (image_save != ""):
            image_save = saveFileName
            im = PIL.Image.open(image_save)
            im.show()

    @pyqtSlot()
    def showOldImage(self):
        global image_file
        if (image_file != ""):
            image_file = fileName
            im = PIL.Image.open(image_file)
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


    @pyqtSlot()
    def getlIssuesBox(self):
        dialog = reportAnError()
        dialog.show()

    @pyqtSlot()
    def getaboutBox(self):
        dialog = about()
        dialog.show()
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
        if (fileName != "" and filterType != "" and saveFileName != ""):
            image_file = fileName
            image_save = saveFileName
            im = PIL.Image.open(image_file)
            imtmp = PIL.Image.open(image_file)
            px = im.load()
            pxtmp = imtmp.load()
            width, height = im.size

            if(filterType == "Grayscale"):
                Percentage = 0
                for x in range(0, im.size[0]):
                    Percentage = Percentage + 1
                    self.pbar.setValue(Percentage)
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
                Percentage = 0
                for x in range(0, im.size[0]):
                    Percentage = Percentage + 1
                    self.pbar.setValue(Percentage)
                    for y in range(0, im.size[1]):
                        for z in range(0, 3):
                            if (px[x, y][z] > int(n)):
                                px[x, y] = (int(255), int(255), int(255))
                            else:
                                px[x, y] = (int(0), int(0), int(0))
                im.save(image_save)

            elif(filterType == "Negativ"):
                Percentage = 0
                for x in range(0, im.size[0]):
                    Percentage = Percentage + 1
                    self.pbar.setValue(Percentage)
                    for y in range(0, im.size[1]):
                        r = 255 - px[x, y][0]
                        g = 255 - px[x, y][1]
                        b = 255 - px[x, y][2]
                        px[x, y] = (int(r), int(g), int(b))
                im.save(image_save)

            elif(filterType == "Gamma correction"):
                global gammaValue
                gamma = gammaValue
                Percentage = 0
                for x in range(0, im.size[0]):
                    Percentage = Percentage + 1
                    self.pbar.setValue(Percentage)
                    for y in range(0, im.size[1]):
                        r = px[x, y][0] * 0.299
                        g = px[x, y][1] * 0.514
                        b = px[x, y][2] * 0.144
                        gammachange = (r + g + b) ** float(gamma)
                        px[x, y] = (int(gammachange), int(gammachange), int(gammachange))
                im.save(image_save)

            elif (filterType == "Box filter"):
                Percentage = 0

                for x in range(1, im.size[0] - 1):
                    Percentage = Percentage + 1
                    self.pbar.setValue(Percentage)
                    for y in range(1, im.size[1] - 1):
                        R = 0
                        B = 0
                        G = 0
                        for i in range(-1, 2):
                            for j in range(-1, 2):
                                R += px[x + j, y + i][0]
                                G += px[x + j, y + i][1]
                                B += px[x + j, y + i][2]
                        R /= 9
                        G /= 9
                        B /= 9
                        px[x, y] = (int(R), int(G), int(B))
                im.save(image_save)

            elif (filterType == "Edge detection"):

                global laplaceSobel
                type = laplaceSobel
                Percentage = 0
                if (type == "Laplace"):
                    for x in range(1, imtmp.size[0] - 1):
                        Percentage = Percentage + 1
                        self.pbar.setValue(Percentage)
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
                        Percentage = Percentage + 1
                        self.pbar.setValue(Percentage)
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
                Percentage = 0
                if (type == "Laplace"):
                    for x in range(1, imtmp.size[0] - 1):
                        Percentage = Percentage + 1
                        self.pbar.setValue(Percentage)
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
                        Percentage = Percentage + 1
                        self.pbar.setValue(Percentage)
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