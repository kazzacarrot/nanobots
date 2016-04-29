import pygame
import random
from inventory import *

class NanoBot():
    nanobotList = []
    healthyNanoBotList = []
    illNanobotList=[]
    goodSide =[]
    illPresent = False
    images = []

    def loadInImages(images):
        images.append(pygame.image.load("bot(cheapone).jpg"))
        images.append(pygame.image.load("dyingNano.jpg"))
        images.append(pygame.image.load("evilNanobot.jpg"))
        images.append(pygame.image.load("fighting evilNano.jpg"))
        images.append(pygame.image.load("gravestone.jpg"))
        images.append(pygame.image.load("hungry.jpg"))
        images.append(pygame.image.load("error.jpg"))

        for image in images:
            image = pygame.transform.smoothscale(image,(40,40))
        return images

    images = loadInImages(images)

    def changeImage(self, description):
        images = NanoBot.images
        print("Change Image")
        if description == "healthy":
            return images[0]
        elif description == "dying":
            return images[1]
        elif description ==  "ill":
            return images[2]
        elif description == "fighter":
            return images[3]
        elif description == "fighting fighter":
            return images[4]
        elif description == "fighting ill":
            return images[5]
        elif description == "gravestone":
            return images[5]
        else:
            return images[6] #error

    def __init__(self, xpos, ypos, age):
        self.bot = pygame.sprite.Sprite()
        self.bot.image = self.changeImage("healthy")
        self.x = xpos
        self.y = ypos
        self.lifeSpan = 200
        self.bodyClock = age
        self.status = "healthy"
        NanoBot.nanobotList.append(self)
        self.health = 130
        self.targetX = 0
        self.targetY = 0
        self.counter = 0

    def drawNano(self, surface):
        surface.blit(self.bot.image,[self.x,self.y]) #add the image to the screen
        return surface

    def update(self, foodlist):
        #see if its hungry and possibly feed it
        self.dealWithHunger(foodlist)
        #but if there are enemies move away instead
        self.dealWithEnemies()
        #die.
        self.timeToDie()
        #get older
        self.bodyClock += 1
        if NanoBot.illPresent == True: #coughs and sneezes spread diseases!!
            #get iller
            self.reduceHealth(2)

    def targetedMovement(self, to = "from"):
        a = 10
        p = self.targetX - self.x
        if p == 0:
            p=1
        m = (self.targetY -self.y)/ p
        
        if to =="from":
            propY = m*self.x +a
            propX = (propY-a)/m
        else:
            propY = m*self.x -a
            propX = (propY+a)/m  
        if validateMovement(propX,propY):
            self.x, self.y= propX, propY
        else:
            self.moveIntoGameSpace()
     
    def moveIntoGameSpace(self):
        if self.y>=400:
            self.y = 390
        elif self.y<= 0:
            self.y = 1
        if self.x>= 400:
            self.x = 390
        elif self.x<= 0 :
            self.x= 1  

    def moveRandomly(self):
        b = 10
        x = random.uniform(-b,b) #create a random x
        y = random.uniform(-b,b) #create a random y
        if validateMovement((self.x +x), (self.y +y)):
            self.x +=x #make the self's coordinates change to the new ones.
            self.y +=y
        else:
            self.moveIntoGameSpace()

    def dealWithEnemies(self):
        if NanoBot.illPresent ==True: # there is an enemy
            #detect where the nearest one is
            closest_enemy = self.Detection(NanoBot.illNanobotList)
            #use targeted movement to move away from it.
            self.targetedMovement()

    def timeToDie(self):
        self.reduceHealth(1)
        if self.health<50 or self.bodyClock > self.lifeSpan: #is its health poor or is it old
            self.counter +=1 #increment the counter
            self.bot.image = self.changeImage("dying") #make it die.
            self.status= "dying"
            if self.counter > 6:# After one minute
                self.bot.image = self.changeImage("gravestone") #refresh the sprite again so it is a grave stone
            if self.counter > 10: #if counter is at one minute and twenty seconds
                NanoBot.nanobotList.remove(self)
                print(self)
                NanoBot.goodSide.remove(self)
                Inventory.decreasePopulation()
                del(self) #d.     Delete the nanobot in the list

    def dealWithHunger(self,foodList):
        ff = False  #local boolean variable, ff means found food
        if self.health < 100: # am i hungry?
            self.status = "hungry"
            self.changeImage(self.status)
            if len(foodList) !=0: #is there food?
                print("we have food")
                food_item = self.Detection(foodList)#this is what im gonna eat
                if Distance(self.x,self.y,self.targetX,self.targetY) < 10:#
                    print("ive eatten the food")
                    self.health += 50
                    self.status = "eatting"
                    food_item.beingEatten()
                self.targetedMovement("towards") # this is how im gonna get there
                ff = True
        if ff == False:
            self.moveRandomly()

    def Detection(self,targets):
        indexD = [] #the distances list is defined
        i = 0 #an index is created
        minDistance = 400
        thing = None
        for target in targets: #use a for loop to go through every item in a given list
            indexD.append(Distance(self.x,self.y,target.x,target.y))  #4        If distance < minDistance  then
            if indexD[i] < minDistance:
                minDistance = indexD[i]#       Distance[i] = minDistance
                thing = target    #6        detected thing is the target[i]
                print(thing)
                print(minDistance)
        if thing != None:
            #8.     tell the nanobot where it wants to go.
            self.targetY = targets[i].y
            self.targetX = targets[i].x
        return thing

    def reduceHealth(obgect,amount = 1):
        obgect.health = obgect.health-amount


def Distance(firstX,firstY,secondX,secondY):
    return ((firstX - secondX)**2 + (firstY - secondY)**2)**0.5

def validateMovement(x,y):
    leftBound = 0
    rightBound =  400
    bottomBound = 0
    topBound =  400
        #make sure its in the screen
    if y<bottomBound or y>topBound:
       return False
    if x<leftBound or x>rightBound:
       return False
        #for loop to go through each nanobot
    for index in NanoBot.nanobotList:
            #if it overlapps at all
        if (y >= index.y and y<=(index.y+10)) and (x>= index.x and x<= (index.x+10)):
                    #the self will overlap another nanobot
            return False
    return True  #if it hasnt yet returned false then return true

class HealthyNanobot(NanoBot):
    def __init__(self, xpos, ypos,age):
        super().__init__(xpos, ypos, age)
        Inventory.increasePopulation()
        super().healthyNanoBotList.append(self)
        super().goodSide.append(self)

    def update(self,foodlist):
        self.Reproduce()
        super().update(foodlist)

    def Reproduce(self):
        #if this guy is healthy then
        if self.health>95 and self.isHappy()==True and self.counter>20:
            #its baby time!
            coords = [self.x -5, self.y-5]
            HealthyNanobot(coords[0],coords[1],0)
            self.counter = 0
        self.counter +=1

    def isHappy(self):
        if NanoBot.illPresent == False and self.health >60:
            return True
        return False

class IllNanobot(NanoBot):
    def __init__(self,x,y,age= 0):
        self.reward = "food"
        Inventory.increaseEnemies()
        NanoBot.illPresent = True
        super().__init__(x,y,age)
        self.lifeSpan =9999
        self.bot.image = self.changeImage("ill")
        self.bot.image = pygame.transform.smoothscale(self.bot.image,(20,20))
        self.health = 200
        self.status= "ill"
        super().illNanobotList.append(self)
        self.timeWaited = 0
        self.opponent = None

    def getKilled(self,):
        #the user clicks on them several times to kill them
        mouseX, mouseY = pygame.mouse.get_pos()
        if mouseX >self.x and mouseX< (self.x+35):
            if mouseY > self.y and mouseY< (self.y+35):
                self.die()

    def dealWithEnemies(self):
        if len(NanoBot.goodSide) >0: # there are actually emimies present.
            if self.opponent != None:
                self.targetX = self.opponent.x
                self.targetY = self.opponent.y
                self.targetedMovement("towards")
                if Distance(self.opponent.x,self.opponent.y,self.x,self.y)<10:
                    self.timeWaited +=1
                    self.bot.image = self.changeImage("fighting ill")
                    if self.timeWaited == 10:
                        self.bot.image = self.changeImage("ill")
                        self.opponent.reduceHealth(20)
                        self.timeWaited = 0
            else:
                self.opponent = self.Detection(super().goodSide)

    def timeToDie(self):
        pass #so they dont die unless they are pressed

    def die(self):
        NanoBot.illNanobotList.remove(self)
        NanoBot.nanobotList.remove(self)
        if len(NanoBot.illNanobotList) == 0:
            NanoBot.illPresent = False
        Inventory.increaseDefeated()
        del(self)
