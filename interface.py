import tkinter
import os

import random

class App:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title("Cards")

        #LoadFile
        self.buttonLoadCards = tkinter.Button(self.window, text="Load", command=self.load)
        self.buttonLoadCards.grid(column=1, row=0)

        #Cards
        self.cards = []

        self.cards_textblock = tkinter.Listbox(self.window, width=50, height=20)
        self.cards_textblock.grid(column=1, row=1)


        #Start Tests
        self.testButtonEng = tkinter.Button(self.window, text="Start test with english words",
                                            command=lambda: self.startTest("Eng"))
        self.testButtonEng.grid(column=1, row=2)

        self.testButtonRus = tkinter.Button(self.window, text="Start test with russian words",
                                            command=lambda: self.startTest("Rus"))
        self.testButtonRus.grid(column=1, row=3)

        # info
        self.mode = None
        self.iteration = None
        self.currentCards = None
        self.wordsInThisIteration = None
        self.currentWordNumber = None
        self.currentWord = None
        self.remainToTranslate = None

        self.testwindow = None
        self.iterationLabel = None
        self.remainToTranslateLabel = None

        self.wordLabel = None
        self.translationLabel = None

        self.inThisIterationLabel = None

        self.next = None
        self.gotIt = None
        self.noooo = None


        self.window.mainloop()

    def load(self):
        print("Load")
        loadwindow = tkinter.Tk()
        loadwindow.title("Load")

        files = tkinter.Listbox(loadwindow, selectmode=tkinter.SINGLE)
        files.grid(column=1, row=0)
        # r=root, d=directories, f = files
        for r, d, f in os.walk('./'):
            for file in f:
                if '.txt' in file:
                    files.insert(tkinter.END, os.path.join(r, file))

        but = tkinter.Button(loadwindow, text="Load",
                             command=lambda: self.getCards(files.get(tkinter.ACTIVE), loadwindow))
        but.grid(column=1, row=1)

        loadwindow.mainloop()

    def getCards(self, filename: str, window: tkinter.Tk):
        self.cards = []
        print(filename)
        f = open(filename)
        s = f.readline()
        while s:
            s = s.replace("\n", "")
            s = s.split(":")
            if len(s) == 2:
                self.cards.append(s)
            else:
                print(s)
            s = f.readline()

        self.cards_textblock.delete(0, tkinter.END)

        for s in self.cards:
            t = s[0] + ": " + s[1]
            self.cards_textblock.insert(tkinter.END, t)

        self.cards_textblock.update()

        window.destroy()

    def destroyTest(self):
        self.testButtonEng.config(state=tkinter.NORMAL)
        self.testButtonRus.config(state=tkinter.NORMAL)
        self.buttonLoadCards.config(state=tkinter.NORMAL)
        self.testwindow.destroy()

    def startTest(self, mode: str):
        self.cards_textblock.delete(0, tkinter.END)
        self.testButtonEng.config(state=tkinter.DISABLED)
        self.testButtonRus.config(state=tkinter.DISABLED)
        self.buttonLoadCards.config(state=tkinter.DISABLED)

        self.testwindow = tkinter.Tk()
        self.testwindow.title("Test")
        self.testwindow.protocol('WM_DELETE_WINDOW', lambda: self.destroyTest() )

        # Labels

        self.iterationLabel = tkinter.Label(self.testwindow, width=5, text="1", font=('times', 20, 'normal'))
        self.iterationLabel.grid(column=1, row=0)

        self.wordLabel = tkinter.Label(self.testwindow, width=30, heigh=3, text="", font=('times', 20, 'bold'))
        self.translationLabel = tkinter.Label(self.testwindow, width=30, heigh=3, text="",
                                              font=('times', 20, 'bold'))

        self.wordLabel.grid(column=0, row=3)
        self.translationLabel.grid(column=2, row=3)

        t1 = tkinter.Label(self.testwindow, text="In this iteration:", font=('times', 14, 'normal'))
        t2 = tkinter.Label(self.testwindow, text="Remain to translate:", font=('times', 14, 'normal'))

        t1.grid(column=0, row=1)
        t2.grid(column=0, row=2)

        self.inThisIterationLabel = tkinter.Label(self.testwindow, text=str(len(self.cards)), font=('times', 14, 'bold'))
        self.remainToTranslateLabel = tkinter.Label(self.testwindow, text=str(len(self.cards)), font=('times', 14, 'bold'))

        self.inThisIterationLabel.grid(column=1, row=1)
        self.remainToTranslateLabel.grid(column=1, row=2)

        # Buttons

        self.next = tkinter.Button(self.testwindow, width=10, text="Take",
                                   command=lambda: self.doSomething(self.next['text']))
        self.gotIt = tkinter.Button(self.testwindow, text="Got It", state=tkinter.DISABLED,
                                    command=lambda: self.doSomething("Got It"))
        self.noooo = tkinter.Button(self.testwindow, text="No :-( ", state=tkinter.DISABLED,
                                    command=lambda: self.doSomething("No"))

        self.next.grid(column=1, row=4)
        self.gotIt.grid(column=1, row=5)
        self.noooo.grid(column=1, row=6)

        # info
        self.mode = mode
        self.iteration = 1
        self.currentCards = self.cards.copy()
        random.shuffle(self.currentCards)
        self.wordsInThisIteration = len(self.currentCards)
        self.currentWordNumber = 0
        self.currentWord = []
        self.remainToTranslate = len(self.currentCards)

        # programm
        self.testwindow.mainloop()

    def doSomething(self, stage):
        if stage == "Take":
            if self.remainToTranslate == 0:
                self.testButtonEng.config(state=tkinter.NORMAL)
                self.testButtonRus.config(state=tkinter.NORMAL)
                self.buttonLoadCards.config(state=tkinter.NORMAL)
                self.testwindow.destroy()
                return

            self.next.config(text="Translate")
            self.currentWord = self.currentCards[self.currentWordNumber]
            if self.mode == "Eng":
                self.wordLabel.config(text=self.currentWord[0])
                self.translationLabel.config(text="")
            else:
                self.wordLabel.config(text=self.currentWord[1])
                self.translationLabel.config(text="")

        elif stage == "Translate":
            self.next.config(text="Take", state=tkinter.DISABLED)
            self.gotIt.config(state=tkinter.NORMAL)
            self.noooo.config(state=tkinter.NORMAL)
            if self.mode == "Eng":
                self.translationLabel.config(text=self.currentWord[1])
            else:
                self.translationLabel.config(text=self.currentWord[0])

        elif stage == "Got It":
            self.next.config(state=tkinter.NORMAL)
            self.gotIt.config(state=tkinter.DISABLED)
            self.noooo.config(state=tkinter.DISABLED)

            self.currentCards.pop(self.currentWordNumber)
            self.remainToTranslate -= 1

        elif stage == "No":
            self.next.config(state=tkinter.NORMAL)
            self.gotIt.config(state=tkinter.DISABLED)
            self.noooo.config(state=tkinter.DISABLED)

            self.currentWordNumber += 1

        if stage == "Got It" or stage == "No":
            if self.currentWordNumber == len(self.currentCards):
                self.iteration += 1
                self.iterationLabel.config(text=str(self.iteration))
                random.shuffle(self.currentCards)
                self.currentWordNumber = 0

            self.remainToTranslateLabel.config(text=str(self.remainToTranslate))
            self.inThisIterationLabel.config(text=str(len(self.currentCards) - self.currentWordNumber))
            self.wordLabel.config(text="")
            self.translationLabel.config(text="")




if __name__ == '__main__':
    I = App()
