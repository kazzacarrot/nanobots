import pygame
pygame.init()
class Inventory():
    livingPopulation =0
    deadPopulation =0
    defeated = 0
    Lenemies = 0
    playTime=0

    def __init__(self,playTime = 0,Lpopulation=0, Lenemies = 0,Denemies =0,Dpopulation=0):
        self.font=pygame.font.Font('freesansbold.ttf', 15)
        Inventory.livingPopulation = int(Lpopulation)
        Inventory.deadPopulation = int(Dpopulation)
        Inventory.playTime = int(playTime)
        Inventory.Lenemies = int(Lenemies)
        Inventory.defeated = int(Denemies)
        self.firstHeadingX, self.firstHeadingY = 430, 100
        self.labelHeadings = ["living population", "dead population","enemies present", "you've defeated", "play time" ]
        self.firstValueX, self.firstValueY= self.firstHeadingX +180, self.firstHeadingY +50

    def increasePlayTime():
        Inventory.playTime +=1

    def increasePopulation():
        Inventory.livingPopulation +=1

    def increaseEnemies():
        Inventory.Lenemies +=1

    def decreasePopulation():
        Inventory.deadPopulation +=1
        Inventory.livingPopulation -=1

    def increaseDefeated():
        Inventory.defeated +=1
        Inventory.Lenemies -=1

    def draw(self,screen):
        sentences = [[None,0,0,None,0,0] for row in range(5) ]
        self.labelValues= [str(Inventory.livingPopulation), str(Inventory.deadPopulation),str(Inventory.Lenemies), str(Inventory.defeated), (str(Inventory.playTime/5) +"secs") ]
        screen.blit(self.font.render("inventory", True, (0,0,0)), (430,50))
        if len(self.labelValues) == len(self.labelHeadings):
            for row in range(len(self.labelHeadings)):
                   sentences[row][0]=self.font.render(self.labelHeadings[row], True, (0,0,0))
                   sentences[row][1] =self.firstHeadingX
                   sentences[row][2] = self.firstHeadingY + row*50
                   sentences[row][3] = self.font.render(self.labelValues[row], True,(0,0,0))
                   sentences[row][4] = self.firstHeadingX + 180
                   sentences[row][5] = sentences[row][2]
            for sentence in sentences:
                screen.blit(sentence[0],(sentence[1], sentence[2]) )
                screen.blit(sentence[3],(sentence[4], sentence[5]))
