import tkinter as tk
from tkinter import PhotoImage, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import pathlib, shutil
import functools

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)

        self.master.title("Hokuren Kouzatsu")
        self.master.state("zoomed")

        self.master.update_idletasks()
        self.winWidth = self.master.winfo_width()
        self.winHeight = self.master.winfo_height()
        self.dirPathList = []
        self.processCount = 0
        self.initImagePlace()
        self.autoSetInput = 6

        self.fourSortedDir = ""
        self.sixSortedDir = ""

        self.initFrameAndButtonSet()

    def makeDir(self, dirPath):
        self.fourSortedDir = dirPath.parent / "MIJ-15(4枚整頓版)"
        self.sixSortedDir = dirPath.parent / "MIJ-15(6枚整頓版)"

        if not self.fourSortedDir.exists():
            self.fourSortedDir.mkdir()

        if not self.sixSortedDir.exists():
            self.sixSortedDir.mkdir()

    def initFrameAndButtonSet(self):
        self.imageFrame = tk.Frame(
            self.master,
            height = self.winHeight,
            width = self.winWidth * 4 / 5,
            bg = "#c0c0c0"
        )

        operateFrame = tk.Frame(
            self.master,
            height = self.winHeight,
            width = self.winWidth / 5,
            bg = "#c0c0c0"
        )

        inputFrame = tk.Frame(
            operateFrame,
            height = 10,
            width = 50,
            bg = "#c0c0c0"
        )

        self.csvButton = tk.Button(
            operateFrame,
            text = "Click to read CSV",
            height = 10,
            width = 50,
            command = self.getImagePathsFromCsv
        )

        self.clearButton = tk.Button(
            operateFrame,
            text = "Clear",
            height = 10,
            width = 50,
            command = self.clearButtonClicked,
            state = tk.DISABLED
        )

        self.processLabel = tk.Label(
            operateFrame,
            height = 10,
            width = 50,
        )

        self.stringVar = tk.StringVar()
        self.stringVar.set(self.autoSetInput)

        self.inputDialog = tk.Entry(
            inputFrame,
            width = 5,
            font = ("arial.ttf", 20),
            background = "#f0f0f0",
            justify = tk.CENTER,
            textvariable = self.stringVar
        )

        self.inputDialogButton = tk.Button(
            inputFrame,
            width = 5,
            height = 1,
            text = "Set",
            command = self.reloadButtonClicked
        )

        self.doneButton = tk.Button(
            operateFrame,
            text = "Done",
            height = 10,
            width = 50, 
            command = self.doneButtonClicked,
            state = tk.DISABLED
        )

        self.imageFrame.pack(side = tk.LEFT, fill = tk.BOTH)
        operateFrame.pack(side = tk.RIGHT, fill = tk.BOTH)
        self.csvButton.pack(side = tk.TOP, pady = 10,)
        self.processLabel.pack(side = tk.TOP, pady = 10,)
        inputFrame.pack(side = tk.TOP, fill = tk.X, pady = 15)
        self.inputDialog.pack(side = tk.LEFT, padx = 40)
        self.inputDialogButton.pack(side = tk.RIGHT, padx = 40)
        self.doneButton.pack(side = tk.BOTTOM, pady = 10,)
        self.clearButton.pack(side = tk.BOTTOM, pady = 10,)


    def reloadButtonClicked(self):
        self.autoSetInput = int(self.stringVar.get())
        self.initImagePlace()
        self.imageSet(self.dirPathList[self.processCount], True)

    def getImagePathsFromCsv(self):
        iDir = os.path.expanduser('~/Document/MIJDB')
        dPath = filedialog.askdirectory(initialdir = iDir)

        dPath = pathlib.Path(dPath)
        dPathList = list(dPath.iterdir())

        self.makeDir(dPath)
        self.sortByIndivNumber(dPathList)
    

    def sortByIndivNumber(self, dPathList):           
        # WindowsPath('C:/Users/user/Downloads/AmazonPhotos (1)/
        # 20220217102111_
        # 2511447117498112202153101002440700201351761220019_
        # 5176.jpg')

        tempList = []
        for path in dPathList:
            date = path.name.split("_")[0]
            indivNum = path.name.split("_")[1]

            tempList.append([path, date, indivNum])

        flagIndexList = []
        for i, temp in enumerate(tempList):
            if i in flagIndexList:
                continue
            
            sameIndivList = []
            sameIndivList.append(temp)

            for j, t in enumerate(tempList):
                if temp[2] == t[2] and i != j:
                    sameIndivList.append(t)
                    flagIndexList.append(j)

            self.dirPathList.append(sameIndivList)
        
        self.imageSet(self.dirPathList[0], True)
        self.switchToEditMode()
        

    def switchToEditMode(self):
        self.csvButton.configure(state = tk.DISABLED)
        self.csvButton.configure(text = "CSV Loaded")
        self.clearButton.configure(state = tk.NORMAL)
        self.processLabel.configure(text = str(self.processCount + 1) + " / " + str(len(self.dirPathList)))

    def initImageSet(self, horiSet, verSet, xPadding, yPadding, imageWidth, imageHeight, length):
        for i in range(verSet):
            for j in range(horiSet):
                if horiSet*i+j >= length:
                    break
                self.imageButton = tk.Button(
                    self.imageFrame,
                    image = PhotoImage(width = 1, height = 1),
                    width = imageWidth,
                    height = imageHeight
                )
                self.imageButton.place(
                    x = xPadding / 2 + (self.winWidth * 4 / (5 * horiSet)) * j,
                    y = (self.winHeight / verSet - imageHeight) / 2 + (self.winHeight / verSet) * i
                )
                self.imageButtonList.append(self.imageButton)

    
    def imageSet(self, dirPath, autoSetFlag):
        xPadding = 20
        yPadding = 20
        horiSet = 4
        verSet = 2

        imageWidth = int(self.winWidth * 4 / (5 * horiSet) - xPadding)
        imageHeight = int(19 * imageWidth / 22)

        self.initImageSet(horiSet, verSet, xPadding, yPadding, imageWidth, imageHeight, len(dirPath))

        for i in range(verSet):
            for j in range(horiSet):
                if horiSet*i+j >= len(dirPath):
                    break
                img = Image.open(str(dirPath[horiSet*i+j][0]))
                img = img.resize((imageWidth, imageHeight))
                self.PILimageList.append(img)

                img = ImageTk.PhotoImage(img)
                self.imageButtonList[horiSet*i+j].configure(
                    image = img,
                    command = functools.partial(self.imageClicked, [dirPath[horiSet*i+j], horiSet*i+j, len(dirPath)])
                )
                self._temp_list.append(img)

        if len(dirPath) == self.autoSetInput and autoSetFlag:
            for i in range(len(dirPath)):
                self.imageClicked([dirPath[i], i, len(dirPath)])



    def imageClicked(self, dirPathAndIndex):
        dirPath = dirPathAndIndex[0]
        clickedIndex = dirPathAndIndex[1]
        displayedImageNum = dirPathAndIndex[2]

        if self.nameIndexCount > self.autoSetInput:
            return

        # if clickedIndex not in [i[1] for i in self.clickOrderPathList]:
        self.clickOrderPathList.append([dirPath, clickedIndex, self.nameIndexCount])
        self.nameOnImage(clickedIndex, self.nameIndexCount)
        
        if self.nameIndexCount == displayedImageNum or self.nameIndexCount == self.autoSetInput:
            self.doneButton.configure(state = tk.NORMAL)

        self.nameIndexCount += 1
        
    
    def nameOnImage(self, clickedIndex, nameIndexCount):
        img = self.PILimageList[clickedIndex].convert("RGBA")
        img.putalpha(128)

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 100)
        draw.text((img.width/2-50,img.height/2-50), str(nameIndexCount) ,(20,20,20),font=font)

        img = ImageTk.PhotoImage(img)
        self.imageButtonList[clickedIndex].configure(image = img)
        self._temp_list[clickedIndex] = img

    def clearButtonClicked(self):
        self.initImagePlace()
        self.imageSet(self.dirPathList[self.processCount], False)
        self.doneButton.configure(state = tk.DISABLED)

    def initImagePlace(self):
        self._temp_list = []
        if self.processCount != 0:
            for i in self.imageButtonList:
                i.place_forget()
        self.imageButtonList = []
        self.clickOrderPathList = []
        self.PILimageList = []
        self.nameIndexCount = 1

    def doneButtonClicked(self):
        self.renamePaths()
        self.processCount += 1
        self.processLabel.configure(text = str(self.processCount + 1) + " / " + str(len(self.dirPathList)))
        
        self.initImagePlace()
        self.doneButton.configure(state = tk.DISABLED)

        if self.processCount + 1 > len(self.dirPathList):
            self.processLabel.configure(text = "")
            return
        
        self.imageSet(self.dirPathList[self.processCount], True)

    def renamePaths(self):
        for path in self.clickOrderPathList:
            oriPath = path[0][0]
            order = path[2]
            sixPath = str(self.sixSortedDir) + "/" + oriPath.stem + "_" + str(order) + oriPath.suffix
            if order in [1, 2, 3, 4]:
                fourPath = str(self.fourSortedDir) + "/" + oriPath.stem + "_" + str(order) + oriPath.suffix
                shutil.copy(oriPath, fourPath)
            shutil.copy(oriPath, sixPath)
        

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    app.mainloop()



