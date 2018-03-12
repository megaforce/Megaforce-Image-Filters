import PIL.Image
from tkinter import *

root = Tk()
root.title("Filters by Megaforce")
root.resizable(False, False)

tmp = ""
image_file = tmp
tmp = ""
image_save = tmp
im = PIL.Image.open(image_file)
imtmp = PIL.Image.open(image_file)
px = im.load()
pxtmp = imtmp.load()
width, height = im.size



def grayscale ():
    for x in range(0, im.size[0]):
        for y in range(0, im.size[1]):
            r = px[x, y][0] * 0.299
            g = px[x, y][1] * 0.514
            b = px[x, y][2] * 0.144
            gray = r + g + b
            px[x, y] = (int(gray), int(gray), int(gray))
    im.save(image_save)


def gammaCorrection ():
    gamma = input("Gamma factor ")
    for x in range(0, im.size[0]):
        for y in range(0, im.size[1]):
            r = px[x, y][0] * 0.299
            g = px[x, y][1] * 0.514
            b = px[x, y][2] * 0.144
            gammachange = (r + g + b) ** float (gamma)
            px[x,y] = (int (gammachange),int (gammachange),int (gammachange))

def  negativ ():
    for x in range(0, im.size[0]):
        for y in range(0, im.size[1]):
            r = 255 - px[x, y][0]
            g = 255 - px[x, y][1]
            b = 255 - px[x, y][2]
            gray = g+r+b
            px[x,y] = (int (gray),int (gray),int (gray))

def treshold ():
    n = input("Treshold ")
    for x in range(0, im.size[0]):
        for y in range(0, im.size[1]):
            for z in range(0, 3):
                if (px[x, y][z] > int (n)):
                    px[x, y] = (int(255), int(255), int(255))
                else:
                    px[x, y] = (int(0), int(0), int(0))

def boxfilter ():
    matrika = [1,1,1,1,1,1,1,1,1]
    for x in range(0 + 1, im.size[0]-1):
        for y in range(0 + 1, im.size[1]-1):
            if ((y == 0 and x == 0) or (y == height and x == 0)):
                tmp = (( px[x,y][0] + px[x,y][1] + px[x,y][2] ) + (px[x+1,y][0] + px[x+1,y][1] + px[x+1,y][2])+( px[x,y+1][0] + px[x,y+1][1] + px[x,y+1][2] ) + (px[x+1,y+1][0] + px[x+1,y+1][1] + px[x+1,y+1][2]))
                px[x, y] = (int (tmp/4),int (tmp/4),int (tmp/4))
            elif((y == 0 and x == width) or (y == height and x == width)):
                tmp = ((px[x, y][0] + px[x, y][1] + px[x, y][2]) + (px[x - 1, y][0] + px[x - 1, y][1] + px[x - 1, y][2])+( px[x,y-1][0] + px[x,y-1][1] + px[x,y-1][2] ) + (px[x+1,y-1][0] + px[x+1,y-1][1] + px[x+1,y-1][2]))
                px[x, y] = (int (tmp/4),int (tmp/4),int (tmp/4))
            else:
                tmp =(( px[x-1,y-1] * matrika[0] + px [x,y-1] * matrika[1] + px [x+1,y-1] * matrika[2] + px[x-1,y]*matrika[3] + px [x,y] * matrika[4] + px [x + 1,y] * matrika[5] + px[x-1,y+1]*matrika[6] + px [x,y+1] * matrika[7] + px [x +1 ,y+1] * matrika[8] ) / 9)
                px [x,y] = (int (tmp),int (tmp),int (tmp))

def EdgeDetection ():
    type = input("Edge detection type (Sobel / Lapace) : ")
    if (type == "Lapace"):
        for x in range(1, imtmp.size[0] - 1):
            for y in range(1, imtmp.size[1] - 1):
                tmp = (px[x - 1, y - 1][0] * 0 + px[x, y - 1][0] * 1 + px[x + 1, y - 1][0] * 0 + px[x - 1, y][0] * 1 +
                       px[x, y][0] * (-4) + px[x + 1, y][0] * 1 + px[x - 1, y + 1][0] * 0 + px[x, y + 1][0] * 1 +
                       px[x + 1, y + 1][0] * 0)
                pxtmp[x, y] = (int(tmp), int(tmp), int(tmp))
        imtmp.save(image_save)
    elif(type =="Sobel"):
        for x in range(1, im.size[0] - 1):
            for y in range(1, im.size[1] - 1):
                tmp = (px[x - 1, y - 1][0] * 1 + px[x, y - 1][0] * 2 + px[x + 1, y - 1][0] * 1 + px[x - 1, y][0] * 0 +
                       px[x, y][0] * (0) + px[x + 1, y][0] * 0 + px[x - 1, y + 1][0] * (-1) + px[x, y + 1][0] * (-2) +
                       px[x + 1, y + 1][0] * (-1))
                pxtmp[x, y] = (int(tmp), int(tmp), int(tmp))

        imtmp.save(image_save )

def Sharpening ():
    grayscale()
    im = PIL.Image.open(image_save)
    imtmp = PIL.Image.open(image_save)
    px = im.load()
    pxtmp = imtmp.load()
    type = input("Kernel type (Sobel / Lapace) : ")
    if (type == "Lapace"):
        for x in range(1, imtmp.size[0] - 1):
            for y in range(1, imtmp.size[1] - 1):
                tmp = (px[x - 1, y - 1][0] * 0 + px[x, y - 1][0] * 1 + px[x + 1, y - 1][0] * 0 + px[x - 1, y][0] * 1 +
                       px[x, y][0] * (-4) + px[x + 1, y][0] * 1 + px[x - 1, y + 1][0] * 0 + px[x, y + 1][0] * 1 +
                       px[x + 1, y + 1][0] * 0)
                pxtmp[x, y] = (px[x, y][0] - int(tmp), px[x, y][1] - int(tmp), px[x, y][2] - int(tmp))
        imtmp.save(image_save)
    elif(type =="Sobel"):
        for x in range(1, im.size[0] - 1):
            for y in range(1, im.size[1] - 1):
                tmp = (px[x - 1, y - 1][0] * 1 + px[x, y - 1][0] * 2 + px[x + 1, y - 1][0] * 1 + px[x - 1, y][0] * 0 +
                       px[x, y][0] * (0) + px[x + 1, y][0] * 0 + px[x - 1, y + 1][0] * (-1) + px[x, y + 1][0] * (-2) +
                       px[x + 1, y + 1][0] * (-1))
                pxtmp[x, y] = (px[x,y][0] - int(tmp),px[x,y][1] - int(tmp),px[x,y][2] - int(tmp))

        imtmp.save(image_save )

def process():

    global selectFunction

    if (selectFunction == "Grayscale"):
        grayscale()
    elif (selectFunction == "Gamma Correction"):
        gammaCorrection()
    elif (selectFunction == "Box Filter"):
        boxfilter()
    elif (selectFunction == "Negativ"):
        negativ()
    elif (selectFunction == "Treshold"):
        treshold()
    elif (selectFunction == "Box Filter"):
        boxfilter ()
    elif (selectFunction == "Edge Detection"):
        EdgeDetection ()
    elif (selectFunction == "Sharpening"):
        Sharpening()
    if(selectFunction != "Edge Detection " or selectFunction != "Sharpening"  ):
        im.save(image_save )

def setGrayScale():

    global selectFunction

    selected = Label(root, text="GrayScale")
    selected.grid(row=1, column=2)
    selectFunction = "Grayscale"
    return selectFunction

def setGammaCorrection():
    selected = Label(root, text="Gamma Correction")
    selected.grid(row=1, column=2)

top = Frame(root)
top.grid(row = 0)
author = Label (root , text = "Image filters created by Megaforce https://github.com/megaforce/Image-Filters",bg = "green",fg ="white")
author.grid(row = 4)
author.grid(columnspan = 3)


menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="GammaCorrection", command=setGammaCorrection)
filemenu.add_separator()
filemenu.add_command(label="Negativ", command="")
filemenu.add_separator()
filemenu.add_command(label="Grayscale", command=setGrayScale)
filemenu.add_separator()
filemenu.add_command(label="BoxFilter", command="")
filemenu.add_separator()
filemenu.add_command(label="Threshold", command="")
filemenu.add_separator()
filemenu.add_command(label="Edge Detection (Sobel)", command="")
filemenu.add_separator()
filemenu.add_command(label="Edge Detection (Lapace)", command="")
filemenu.add_separator()
filemenu.add_command(label="Sharpening (Sobel)", command="")
filemenu.add_separator()
filemenu.add_command(label="Sharpening (Lapace)", command="")

menubar.add_cascade(label="Filter", menu=filemenu)
root.config(menu=menubar)


fileTxt = Label (root,text = "File name")
saveTxt = Label (root,text = "Save file")
fileName =  Entry(root)
saveName = Entry (root)
fileTxt.grid(row = 1)
saveTxt.grid(row = 2)
fileName.grid(row = 1, column = 1)
saveName.grid(row = 2, column = 1)
confirm = Button(root, text="Confirm", fg="Black", command = process)
confirm.grid(row=2, column = 2)



root.mainloop()

