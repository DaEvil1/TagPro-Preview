from _GUIWrapper import *
import pygame, sys, os
from pygame.locals import *

class Window(Window_):

    def __init__(self, name, width, height, position = (5, 20)):
        os.environ['SDL_VIDEO_WINDOW_POS'] \
                = str(position[0]) + "," + str(position[1])
        pygame.init()
        pygame.event.clear()
        screen = pygame.display.set_mode((width, height), 0, 32)
        screen.fill((255, 255, 255))
        pygame.display.set_caption(name)

        self.options = {"background" : (255, 255, 255), \
                        "screen" : screen, "transparent" : 0,
                        "event" : None, "fullscreen" : False,
                        "eventlist" : (0, 0), "width" : width, "height" : height,
                        "save" : None}
        
        self.functions = {"background" : self._background,
                          "transparent" : self._transparent,
                          "fullscreen" : self._fullscreen,
                          "save" : self._save}

        self.current = None

        #Needed to write text to canvas. Yay pygame...
        pygame.font.init()
        

    def Modify(self, option, value):
        self.current = value
        self.options[option] = value
        if option in self.functions:
            self.functions[option]()

    def Get(self, option):
        return self.options[option]

    def Event(self):
        self.options["event"] = None
        self.options["eventlist"] = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.options["event"] = "quit"
            elif event.type == pygame.KEYDOWN:
                self.options["event"] = pygame.key.name(event.key)
            elif event.type == pygame.KEYUP:
                self.options["event"] = pygame.key.name(event.key)

    def Blit(self):
        self.options["screen"].fill(self.options["background"])

    def NewRes(self, height, width):
        self.options["width"] = width
        self.options["height"] = height
        if self.options["fullscreen"]:
            screen = pygame.display.set_mode((width + 20, height + 20),
                                             pygame.FULLSCREEN , 32)
        else:
            screen = pygame.display.set_mode((width + 20, height + 20),
                                             0 , 32)            
    def Update(self):
        pygame.event.pump()
        pygame.display.flip()
    
    def Quit(self):
        pygame.quit()
        sys.exit()

class Objects:

    def __init__(self):
        self.ID = {}

    def Add(self, ID, filename, coords, chopArea=None):
        newItem = Object(filename, coords, chopeArea)
        self.ID[ID] = newItem

    def Modify(self, ID, option, value):
        self.ID[ID].Modify(option, value)

    def Get(self, option):
        self.ID[ID].Get(option, value)

    def Remove(self, ID):
        self.ID[ID].Remove()
        del self.ID[ID]

    def Blit(self, screen):
        for element in self.ID:
            element.Blit(screen)


#Does exactly the same as Objects. The only thing that needs to be fixed
# is the pointer to Object in Add to Poly.
class Polys(Objects):

    def Add(self, ID, filename, coords, chopArea=None):
        newItem = Poly(filename, coords, chopeArea)
        self.ID[ID] = newItem
        

