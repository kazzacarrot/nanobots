#saving.py
import pygame
import inventory
import os

#decide which file , aka score board
def decideOnFile(keyPressed):
    fileList = getFiles()  #get the list of files
    #sort file list
    displayScores(screen.gameScreen, fileList)  #pass a screen in to the scores subroutine
    fileNotChosen = True
    n = 0   #the part of the list that is highlighted
    while fileNotChosen: #so it only advances when somthing has happened
        if keyPressed == "up":
            #highlight the file above.
            n -=1
            if n<0:
                n=len(fileList)-1
        if keyPressed == "down":
            n+=1
            if n> len(fileList)-1:
                n=0
        if keyPressed == "enter":
            loadAFile(n)
    return fileList[chosenFile]

def sortFiles(items):
    sortedlist = []
    fullList = len(items)
    while fullList != len(sortedlist):
        print("the play time for this loop")
        maxPos =0
        playTimeList = []
        for i in range(len(items)):
            File = open(items[i], "r")
            playTimeList.append(File.readline(4).rstrip())
            File.close()
        for i in range(len(items)):
            File = open(items[i], "r")
            healthy = File.readline(2).rstrip()
            ill = File.readline(3).rstrip()
            playTime = File.readline(4).rstrip()
            print(str(File.name) + "playtime = " + str(playTime) +"ill= " + str(ill) + "healthy= " + str(healthy))
            if playTime> playTimeList[maxPos]:
                maxPos = i
            File.close()
        print(maxPos)
        sortedlist.append(items.pop(maxPos))
    return sortedlist

 #what is the value of the key that has been pressed. get value. check its its acceptable.
 #if unacceptable then here is true.

def saveFile(fileToWrite):#save a file
    File = open(fileToWrite, "w") #as w used this will empty the file first.
    #take the number of heathly nanobots and ill and fighters
    healthy = inventory.Inventory.livingPopulation
    ill = inventory.Inventory.Lenemies
    playTime = inventory.Inventory.playTime
    defeated = inventory.Inventory.defeated
    print(defeated)
    #write the number of healthy on the first protocol
    File.write(str(healthy) + os.linesep) # type error = int does not support the buffer interface
    #write the number of ill on the second protocol
    File.write(str(ill)+ os.linesep)
    File.write(str(playTime)+ os.linesep)
    File.write(str(defeated)+ os.linesep)
    #close the file.
    File.close()

#loading
def loadAFile(fileToLoad):#open a file.
    File = open(fileToLoad,"r")
    healthy = File.readline(1).rstrip() #healthy is protocol one
    ill = File.readline(2).rstrip() #ill is protocol two
    playTime = File.readline(3).rstrip()
    defeated = File.readline(4)
    if healthy == "":
        healthy = 0
    else:
        healthy = int(healthy)

    if ill == "":
        ill =0
    else:
        int(ill)

    if playTime == "":
        playTime = 0
    else:
        playTime = int(playTime)

    if defeated == "":
        defeated = 0
    else:
        defeated = int(defeated)

    File.close()
    return healthy, ill, playTime, defeated

def getFiles(root = os.getcwd()): #i've made the rood a parameter so i have the option of re-using it.
    userFiles  = [] #create a list of possible user files
    CurrentDirectory = root # this is the path to the current folder
    listFilter = "txt" #the file extention i need
    for path,directory,file in os.walk(CurrentDirectory): #os.walk() returns a tuple hence path, directory,file
        for f in file: # for each file
            if f[-3:] == listFilter: #check the file extention to see if it is txt file
                userFiles.append(f) #if it is, add it into the list!
    if len(userFiles) != 0:
        userFiles = sortFiles(userFiles)
    return userFiles