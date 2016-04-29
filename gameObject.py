#game object class
import pygame
import sys
import saving
from nanobot import *
from food import *
from inventory import *



class colours():
    BLACK = (0,0,0)
    RED = (255,0,0)
    GREEN = (84,104,86)
    BLUE = (0,0,255)
    YELLOW = (255,255,0)


class Game():
    def __init__(self): #create a game object
        self._display_surface= None
        self.size= self.width,self.height = 640,400
        self.gameState= 0
        self.headingPos= (50,50)
        self.firstSubHeading = self.x, self.y = 50, 100
        self.mousePressed = False

    def startup(self): #do these things before all the other methods below, so the game won't run with errors
        pygame.init()
        self._display_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._Game_surface= pygame.Surface((400,400))
        self._running = True
        self._display_surface.convert()
        self._display_surface.fill(colours.YELLOW)
        self.font=pygame.font.Font('freesansbold.ttf', 32)
        self.subFont= pygame.font.Font('freesansbold.ttf', 20)
        self.fileList = []
        self.counter = 0
        self.currentTextList = []
        self.n =0

    def showWelcome(self): #when gamestate is 0, show the word Welcome and 'press any key' in the centre of the screen
        Header = self.font.render("welcome!", True, colours.BLUE)  # create the words
        suber = self.subFont.render("press any key", True, colours.RED)
        self._display_surface.blit(Header, (self.width/3, self.height/3))
        self._display_surface.blit(suber, (self.width/3, self.height/2))

    def showMenu(self): #list their options and blit them to the screen
        Header = self.font.render("menu", True, (0,255,0))  # create the words
        suber = []
        suber.append(self.subFont.render("1. press O to open a file", True, colours.BLACK))
        suber.append(self.subFont.render("2. press C to create a file", True, colours.BLACK))
        suber.append(self.subFont.render("3.press I to see instructions", True, colours.BLACK))
        self._display_surface.blit(Header, self.headingPos)
        for i in range(len(suber)):
            increment = i *100
            self._display_surface.blit(suber[i], (self.x, self.y+ increment))

    def showMainGame(self): #the game section is green, use the draw methods of nanobots and food to put them on the screen
        self._Game_surface.fill(colours.GREEN)
        for bot in NanoBot.nanobotList:
                bot.drawNano(self._Game_surface)
        for food in Food.foodList:
                food.draw(self._Game_surface)
        if NanoBot.illPresent ==True:
            Header = self.font.render("save us!",True, colours.RED)
            self._Game_surface.blit(Header, self.headingPos)
        self._display_surface.blit(self._Game_surface,(0,0))


    def showInstructions(self): #list the users options
        Header = self.font.render("Instructions", True, colours.BLUE)
        subs = []
        subs.append(self.subFont.render("care for your nanobots,", True, colours.RED))
        subs.append(self.subFont.render("click on the 'f' button to create food.", True, colours.RED))
        subs.append(self.subFont.render("then mouse click where you want it to be", True, colours.RED))
        subs.append(self.subFont.render("protect them from infected nano bots", True, colours.RED))
        subs.append(self.subFont.render("click on the enemies to kill them and save your bots", True, colours.RED))
        subs.append(self.subFont.render("make more nanobots by keeping them happy", True, colours.RED))
        subs.append(self.subFont.render(" ", True, colours.RED))
        subs.append(self.subFont.render("click to start playing", True, colours.RED))
        self._display_surface.blit(Header, self.headingPos)
        for line in range( len(subs)):
            sentence = subs[line]
            self._display_surface.blit(sentence, [self.x, self.y + line *20]) #self.x and self.y are the coordinates of the first sub heading

    def showFiles(self): #show a sorted list of the possible files
        self.fileList = saving.getFiles()
        Header = self.font.render("Choose a file", True, colours.BLUE)
        self._display_surface.blit(Header, self.headingPos)
        subs = []
        subs.append(self.subFont.render("use the up and down buttons to select your file", True, colours.RED))
        subs.append(self.subFont.render("the black file is selected", True, colours.RED))
        subs.append(self.subFont.render(" ", True, colours.RED))
        if len(self.fileList) ==0:
            subs.append(self.subFont.render("there are no files", True, colours.RED))
            subs.append(self.subFont.render("click to create a new file for yourself",True, colours.RED))
        else:
            for File in range(len(self.fileList)):
                if File == self.n:
                    subs.append(self.subFont.render(str(self.fileList[File]), True, colours.BLACK))
                else:
                    subs.append(self.subFont.render(str(self.fileList[File]), True, colours.BLUE))
        for line in range( len(subs)):
            sentence = subs[line]   #put 20 pixels between each of the sub headings
            self._display_surface.blit(sentence, [self.x, self.y + line *20])

    def showCreateNewFile(self):
        #show a window with a heading and a box with user entered text in it.
        header = self.font.render("please enter your name", True, colours.BLUE)
        subHeader = self.subFont.render("press the dot to clear it", True, colours.BLACK)
        subHeader2 = self.subFont.render("dont press the back space!", True, colours.BLACK)
        subHeader3  = self.subFont.render("press enter to go to the menu, then click o to open your new file", True, colours.BLACK)
        self._display_surface.blit(header,self.headingPos)
        self._display_surface.blit(subHeader,self.firstSubHeading)
        self._display_surface.blit(subHeader2,(self.x, self.y +50))
        self._display_surface.blit(subHeader3,(self.x, self.y +300))
        if len(self.currentTextList) != 0:
            userText = ''.join(self.currentTextList)
            self._display_surface.blit( self.font.render(userText,1, colours.BLACK),(50,200))

    def createGame(self,healthy=5,enemy =0,playTime = 0,defeated = 0):
        self.gameState = 2  #create a game with a defaut of 5 healthy nanobots
        for i in range(healthy):
            HealthyNanobot(i*20,i*10,i)
        for i in range(int(enemy)):
            IllNanobot(0,0,0)
        self.invent= Inventory(playTime,healthy, enemy,defeated)

    def enterEnemyCounter(self):
           # self.counter +=1
           # i = self.counter/40
           # m = self.counter//40
           # n = i -m
           # if n == 0:
           ##     IllNanobot(0,0,0)
           print ("enemy not created")

    def eventHandling(self, event):
        if event.type ==pygame.QUIT: #they've pressed the little X
            self._running = False # this will stop the game at the approprait spot.
        if self.gameState ==0:
            if event.type == pygame.KEYUP: # any key has been pressed
               self.gameState +=1 #go to the next page

        elif self.gameState == 1:  #1 is the menu screen
            self.handleMenu(event)

        elif self.gameState ==2:    #2 is the main game
            self.handleMainGame(event)

        elif self.gameState == 3: #deciding on a file
            self.handleFiles(event)

        elif self.gameState == 4: #instructions
            self.handleInstructions(event)
        elif self.gameState == 5:
            self.handleText(event)
        elif self.gameState == 6:
            self.handleFiles(event)

    def handleInstructions(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN: #has the mouse been pressed
            if event.button == 1: #is it the left button
                self.mousePressed = True
                self.gameState = 2
                self.createGame()
        else:
            self.mousePressed = False

    def handleFiles(self,event):
        if len(self.fileList) !=0:
            if event.type == pygame.KEYUP: # if a key has been pressed.
                if event.key == pygame.K_UP:
                    if self.n ==0:
                        self.n = len(self.fileList)
                    else:
                        self.n -=1
                elif event.key == pygame.K_DOWN:
                    if self.n == len(self.fileList):#highlight the sentence below
                        self.n == 0
                    else:
                        self.n+=1
                elif event.key == pygame.K_RETURN: # is it the enter key
                    if self.gameState == 3: #do we want to save or open a game
                        h,i,pt,d = saving.loadAFile(self.fileList[self.n])
                        self.gameState =2
                        self.createGame(h, i,pt,d)
                    elif self.gameState == 6:
                        saving.saveFile(self.fileList[self.n])
                        self.gameState = 0
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.gameState = 5

    def handleMenu(self, event):
        if event.type == pygame.KEYUP: # if a key has been pressed.
            if event.key == pygame.K_i:
                self.gameState = 4
            elif event.key == pygame.K_o:
                #open a file
                self.gameState =3
            elif event.key == pygame.K_c:
                #create a file
                self.gameState = 5
            elif event.key == pygame.K_s: # is it a letter S
                # save the game
                self.gameState == 6

    def handleMainGame(self,event):
        if event.type == pygame.MOUSEBUTTONUP: #has the mouse been pressed
            self.mousePressed = True
            if NanoBot.illPresent == True:
                for enemy in NanoBot.illNanobotList:
                    enemy.getKilled()
        else:
            self.mousePressed = False #is it the right button?

        if event.type == pygame.KEYUP: # if a key has been pressed.
            if event.key == pygame.K_y: #if the key is a letter y
                IllNanobot(100,0,0)     #create an ill nanobot
            elif event.key == pygame.K_u: # is it a letter U
                HealthyNanobot(200,random.randint(0, 480),0) #create a healthy nanobot
            elif event.key == pygame.K_f: # is it a letter F
                Food() #create a food item
            elif event.key == pygame.K_s: # is it a letter S
                self.gameState = 6


    def handleText(self,event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN: #user has completed their name
                fileToOpen = ''.join(self.currentTextList) + ".txt"
                file = open(fileToOpen, "w+") #this creates the file
                file.close()    #this clears the game memory of the file
                self.gameState =2
                self.createGame()
            elif event.key == pygame.K_PERIOD:
                self.currentTextList =[]
            elif event.key <= 127:
                self.currentTextList.append(chr(event.key))

    def update(self):
        if self.gameState==2: #their playing the actual game.
            if len(Food.foodList) !=0:
                for food in Food.foodList:
                    food.update(self.mousePressed)
            if len(NanoBot.nanobotList) == 0:
                HealthyNanobot(0,0,0)   #Create a healthy nanobot
            for bot in NanoBot.nanobotList:
                bot.update(Food.foodList)
            self.enterEnemyCounter()

    def draw(self):
        #blit everything to the main window
        if self.gameState ==0: #at welcome
            self.showWelcome()
        elif self.gameState ==1:
            self.showMenu()     #at menu screen

        elif self.gameState == 2: #at game
            self.showMainGame()
            self.invent.draw(self._display_surface)

        elif self.gameState == 3 or self.gameState == 6 :
            self.showFiles()    #for loading in and saving

        elif self.gameState == 4:
            self.showInstructions()

        elif self.gameState == 5:
            self.showCreateNewFile()

        pygame.display.flip()
        self._display_surface.fill(colours.YELLOW)

    def cleanup(self):
        pygame.display.quit()
        del(self)
        sys.exit()

    def loop(self):
        FPS = 5
        fpsClock = pygame.time.Clock()
        if self.startup() == False:
            self._running = False
        while(self._running):
            for event in pygame.event.get():
                self.eventHandling(event)
            self.update()
            self.draw()
            fpsClock.tick(FPS)
            Inventory.increasePlayTime()
        self.cleanup()


gameObject = Game()
gameObject.loop()
