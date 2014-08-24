#Includes the raw internal methods of GUI classes:
import sys, pygame

class Window_:

    def _background(self):
        self.options["background"] = self.current
        self.options["screen"].fill(self.current)

    def _transparent(self):
        self.options["transparant"] = self.current
        self.options["screen"].set_colorkey(self.current)

    def _fullscreen(self):
        width = self.options["width"]
        height = self.options["height"]
        if self.options["fullscreen"]:
            screen = pygame.display.set_mode((width, height),
                                             pygame.FULLSCREEN , 32)

    def _save(self):
        pygame.image.save(self.options["screen"], self.current)

class Object_:

    def _coords(self):
        self.data["rect"].x, self.data["rect"].y = self.current

    def _image(self):
        self.data["image"] = pygame.image.load(self.current)

    def _chop(self):
        self.data["image"] = self.data["image"].subsurface(self.current)
        self.data["height"] = self.data["image"].get_height
        self.data["width"] = self.data["image"].get_width


    def _rotate(self):
        oldCenter = self.data["rect"].center
        self.data["image"] = pygame.transform.rotate(self.data["image"], self.current)
        self.data["rect"] = self.data["image"].get_rect()
        self.data["rect"] = self.data["image"].get_rect()
        self.data["rect"].center = oldCenter


class Object(Object_):
        
    def __init__(self, filename):

        self.functions = {"coords" : self._coords, "image" : self._image,
                          "chop" : self._chop, "rotate" : self._rotate}
        

        image = pygame.image.load(filename)
        rect = image.get_rect()
        height, width = image.get_height(), image.get_width()
        self.data = {"image" : image, "coords" : (0, 0), "rect" : rect,
                     "chop" : None, "rotate" : 0, "height" : height,
                     "width" : width}
        

        self.current = None

    def Transparent(self, color):
        self.data["image"].set_colorkey(color)

    def PixelColor(self, coords):
        return self.data["image"].get_at(coords)

    def Modify(self, option, value):
        self.current = value
        self.data[option] = value
        if option in self.functions:
            self.functions[option]()
        else:
            raise Exception("given option not available.")

    def Get(self, option):
        return self.data[option]

    def Remove(self):
        self = None

    def AlphaBlit(self, screen):
        self.data["image"] =pygame.Surface.convert_alpha(self.data["image"])
        screen.blit(self.data["image"], self.data["rect"])


    def Blit(self, screen):
        self.data["image"] = pygame.Surface.convert(self.data["image"])
        screen.blit(self.data["image"], self.data["rect"])


class Poly:
    
    options_order = \
        {
        "line" : ["color", "start", "end", "width"]
        }
    

    def __init__(self, n_type):
        self.all_options = \
            {
                "line" : {"start" : [0, 0], "end" : [0, 0], "color" : (0,0,0), \
                          "width" : 0}
            }
        self.draw = {"line" : pygame.draw.line}
        if n_type not in self.draw:
            raise Exception("No such polygon available.")
        self.options = self.all_options[n_type]
        self.type = n_type

    def Modify(self, option, value):
        self.options[option] = value

    def Blit(self, screen):
        newargs = [self.all_options[self.type][i] for i in self.options_order[self.type]]
        self.draw[self.type](screen, *newargs)
        
class Text:

    def __init__(self, string, color, pos, size):
        self.Font = pygame.font.SysFont("Arial", size)
        self.obj = self.Font.render(string, False, color)
        self.rect = self.obj.get_rect()
        self.color = color
        self.string = string
        self.size = size
        self.rect.x, self.rect.y = pos

    def Pos(self, pos):
        self.rect.x, self.rect.y = pos

    def Color(self, color):
        self.color = color

    def Size(self, size):
        self.size = size

    def String(self, string):
        self.string = string

    def Blit(self, screen):
        screen.blit(self.obj, self.rect) 

##class BuiltIn_:
##
##    def _coords(self):
##        self.data["rect"].x, self.data["rect"].y = self.current
##
##    def _chop(self):
##        self.data["image"] = self.data["image"].subsurface(self.current)
##        self.data["height"] = self.data["image"].get_height
##        self.data["width"] = self.data["image"].get_width
##
##
##    def _rotate(self):
##        oldCenter = self.data["rect"].center
##        self.data["image"] = pygame.transform.rotate(self.data["image"], self.current)
##        self.data["rect"] = self.data["image"].get_rect()
##        self.data["rect"] = self.data["image"].get_rect()
##        self.data["rect"].center = oldCenter
##        
##class BuiltIn(BuiltIn_):
##
##    def __init__(self, shape, coords):
        
