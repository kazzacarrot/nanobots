import pygame

class Food():
#food images
    try:
        foodImage = pygame.image.load("FOOD.jpg")

        foodImage = pygame.transform.smoothscale(foodImage,(20,20))
    except:
        print("image failed to load")
#food lists
    foodList =[]
    def __init__(self):
        self.x,self.y = pygame.mouse.get_pos()
        self.expirly = 50
        self.stuck= False
        self.image= Food.foodImage
        Food.foodList.append(self)
        self.counter= 0 # allows it to expire

    def create(self,mousePressed):
        #the food will follow the mouse until the user clicks
        if self.stuck == False:
            self.x,self.y = pygame.mouse.get_pos()
            self.stuck = mousePressed

        if self.x>400 or self.y>400 or self.x<0 or self.y<0:
            self.x = 200
            self.y = 200

    def expire(self):
        if self.counter== self.expirly:
            Food.foodList.remove(self)
            del(self)

    def beingEatten(self):
        Food.foodList.remove(self)
        del(self)

    def update(self,mousePressed):
        self.counter +=1 #increment the counter
        #call create
        self.create(mousePressed)
        #check to see if expired
        self.expire()

    def draw(self,surface):
        surface.blit(self.image,(self.x,self.y))
        return surface
