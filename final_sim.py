from cmath import isnan, nan
from types import NoneType
import pygame
import pymunk
import random
import math

pygame.init()
display = pygame.display.set_mode((1000,1000))
pygame.display.set_caption("PHYSICS")
display.fill((120,20,0))
type_ = "d"
pygame.display.flip()
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0,200
FPS = 50
randcolor = lambda : (random.randint(0,255),random.randint(0,255),random.randint(0,255))
def convert_coords(point):

    return int(point[0]),int(point[1])
class Box():
    def __init__(self,point1,point2,type_str):
        elas = 1
        self.point1 = point1
        self.point2 = point2
        self.isreal = True
        self.startpos = ((point1[0]+point2[0])/2),((point1[1]+point2[1])/2)
        self.width = (point1[0] - point2[0])
        self.height = (point1[1] - point2[1])
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        if type_str == "s":
            pass
            #print("Static ----------")
        elif type_str == "d" :
            self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
            self.body.mass = round(abs(point1[0]-point2[0])/50)*5 +  round(abs(point1[1]-point2[1])/50)*5 + 10
            widhi = (self.width,self.height)
            if widhi[0]<100 or widhi[1]<100:
                widsizeformoment = (100,100)
            else :
                widsizeformoment = widhi
            self.body.moment = pymunk.moment_for_box(self.body.mass, widsizeformoment)
            
            #print("Dynamic ----------")
        else :
            print(type_str)
        self.body.position = (((point1[0]+point2[0])/2),((point1[1]+point2[1])/2))

        self.shape = pymunk.Poly.create_box(self.body,[self.width,self.height])
        self.rgb = randcolor()
        
        
        self.shape.elasticity = elas

        space.add(self.body,self.shape)

    def draw(self):
        #pointlist = [(self.body._get_position()[0] + x[0], self.body._get_position()[1] + x[1]) for x in self.shape.get_vertices()]
        #pointlist = [(self.startpos[0] + x[0], self.startpos[1] + x[1]) for x in self.shape.get_vertices()] #### only works in static 
        #print(pointlist)
        pointlist = [convert_coords(self.body.local_to_world((x[0],x[1]))) for x in self.shape.get_vertices()] 
        pygame.draw.polygon(display, self.rgb, pointlist)
    def remove(self):
        self.isreal = False
        space.remove(self.body,self.shape)
class Ball():
    def __init__(self,x,y,type_str,velo = (0,0)):
        self.rad = 10
        elas = 1
        dens = 10
        
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        if type_str == "s":
            pass
            #print("Static ----------")
        elif type_str == "d" :
            self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
            #print("Dynamic ----------")
        else :
            print(type_str)
        self.body.position = x,y
        self.body.velocity = velo
        self.isreal = True
        self.shape = pymunk.Circle(self.body,self.rad)
        self.shape.elasticity = elas
        self.shape.density = dens
        space.add(self.body,self.shape)
        self.rgb = randcolor()
    def draw(self):
        if self.isreal:
            pygame.draw.circle(display, self.rgb,convert_coords(self.body.position),self.rad)
    def remove(self):
        self.isreal = False
        space.remove(self.body,self.shape)

class Segment():
    def __init__(self,point1,point2,type_str):
        #print(type_str + "_____<<<,<")
        elas = 1
        dens = 1
        self.midpoint = ((point1[0]+point2[0])/2,(point1[1]+point2[1])/2)
        #print("^^^")
        self.type_str = type_str
        self.body =  pymunk.Body(body_type=pymunk.Body.STATIC)
        if type_str == "s":
            pass
            #print("Static ----------")
        elif type_str == "d" :
            self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
            #print("Dynamic ----------")
        else :
            print(type_str)


        
        self.point1 = point1
        self.point2 = point2
        self.isreal = True
        self.shape = pymunk.Segment(self.body,point1, point2, 5)
        self.initpos = self.body.position
        self.len = ((point1[0]-point2[0]),(point1[1]-point2[1]))
        self.midpoint = ((point1[0]-point2[0])/2,(point1[1]-point2[1])/2)

        self.shape.elasticity = elas
        self.shape.density = dens
        space.add(self.body,self.shape)
        self.rgb = randcolor()
    def draw(self):
        if self.isreal:
            if self.type_str == "d" :
                diff1 = float(self.initpos[0] - self.body.position[0])
                diff2 = float(self.initpos[1] - self.body.position[1])
                pygame.draw.line(display,self.rgb,convert_coords(self.body.local_to_world(self.shape.a)),convert_coords((self.body.local_to_world(self.shape.b))),5)
                #works -- pygame.draw.line(display,self.rgb,convert_coords((self.point1[0]-diff1,self.point1[1]-diff2)),convert_coords((self.point2[0]-diff1,self.point2[1]-diff2)),5)
                
                #CLOSE : pygame.draw.line(display,self.rgb,convert_coords((self.point1[0]-diff1,self.point1[1]-diff2)),convert_coords((self.point2[0]-diff1,self.point1[1]-diff2)),5)


                #pygame.draw.line(display,self.rgb,convert_coords((self.body.position[0]+self.midpoint[0],self.body.position[1]+self.midpoint[1])),convert_coords(((self.body.position[0]-self.midpoint[0],self.body.position[1]-self.midpoint[1]))),3)
                ###pygame.draw.circle(display,(0,0,0), self.midpoint,10)
            # self.initpos = (self.body.position[0],self.body.position[1])
            elif self.type_str == "s" :
                ### Works - pygame.draw.line(display,self.rgb,convert_coords(self.point1),convert_coords(self.point2),5)
                pygame.draw.line(display,self.rgb,convert_coords(self.body.local_to_world(self.shape.a)),convert_coords((self.body.local_to_world(self.shape.b))),5)


    def remove(self):
        self.isreal = False
        space.remove(self.body,self.shape)
class Button():
    """Create a button, then blit the surface in the while loop"""
 
    def __init__(self, text,  pos, feedbackfunct, font, bg="black", feedback="", imglist= []):
        self.x, self.y = pos
        self.imglist = imglist
        
        self.actingimg = imglist[0]
        
        self.font = pygame.font.SysFont("Arial", font)
        if feedback == "":
            self.feedback = "text"
        elif feedback == None :
            self.feedback == text
        else:
            self.feedback = feedback

        self.change(text, (0,200,0))
        self.feedbackfunct = feedbackfunct
    def change(self, text, bg="black", switchimg = False):
        """Change the text whe you click"""
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()[0],self.text.get_size()[1]+30
        

        self.surface = pygame.Surface(self.size)
        self.surface.fill((0,200,0))
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

        
        if self.imglist.index(self.actingimg) <= len(self.imglist)-2: 
            self.actingimg = self.imglist[self.imglist.index(self.actingimg) + 1]
        else :
            self.actingimg = self.imglist[0]
        img = pygame.image.load(self.actingimg)
        print(self.actingimg)
        
        img = pygame.transform.scale(img,(30,30))
        
        self.surface.blit(img,(0,30))
        print("AHHHHH")
        
    def show(self):
        display.blit(self.surface, (self.x, self.y))
 
    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.change(self.feedback, bg="blue", switchimg = True)
                    self.feedbackfunct(self.actingimg)
                    return True
def game():
    button1 = Button(
    "Choose a shape",
    (10, 10),
    lambda a : print("clicked"),
    font=30,
    bg="blue",
    feedback="Choose a shape!",
    imglist=["circle.png", "minus.png","square.png"])

    button2 = Button(
    "Dynamic/Static",
    (10, 100),
    switchbodytype,
    font=30,
    bg="blue",
    feedback="Dynamic/Static",
    imglist=["s.png","d.png"])

    button3 = Button(
    "Pause",
    (10, 210),
    pause,
    font=30,
    bg="blue",
    feedback="Pause",
    imglist=["play.png","pause.png"])
    
    #ball1 = Ball(140,120)
    #ball2 = Ball(180,120,(-20,0))
    lineseg = Segment((0,900),(900,900),"s")
    clickvar = False
    while True:
        [boxes.draw() for boxes in rects]
        [ball.draw() for ball in balls]
        [segment_.draw() for segment_ in segments]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down_x, mouse_down_y = event.pos
                if button1.click(event) or button2.click(event) or button3.click(event):
                    print("BUTTON")
                    clickvar = True
                    
                else :
                    print( str(mouse_down_x) + "," + str(mouse_down_y) + "     < Coords of Click")
                    clickvar = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_up_x, mouse_up_y = event.pos
                print(str(clickvar) + "<This is clickvar")
                if not clickvar:
                    if button1.actingimg == "minus.png" :
                        segments.append(Segment((mouse_down_x, mouse_down_y), (mouse_up_x, mouse_up_y),type_str=type_))
                    elif button1.actingimg == "circle.png" :
                        balls.append(Ball(mouse_up_x, mouse_up_y,type_str=type_))
                    elif button1.actingimg == "square.png":
                        rects.append(Box((mouse_down_x, mouse_down_y), (mouse_up_x, mouse_up_y),type_str=type_))
                    clickvar = False


        #ball1.draw()
        #ball2.draw()
        lineseg.draw()
        button1.show()
        button2.show()
        button3.show()
        pygame.display.update()
        display.fill((255,255,255))
      
        if not paused :
            clock.tick(FPS)
            space.step(1/FPS)
        else:
            pass
def switchbodytype(param):
    global type_

    type_ = param.replace(".png","")
    print(type_)
    
def pause(param):
    
    global paused
    if paused :
     paused = False
    elif not paused :
        paused = True

    print("______________")
    print(paused)
  
paused = False
balls = []
segments = []
rects = []
game()
pygame.quit()





def makeballs() :
    [ball.remove() for ball in balls]
    [segment_.remove() for segment_ in segments]
    balls.clear()
    segments.clear()
    for i in range(20):
            a = random.randint(0,900)
            b = random.randint(0,900)
            c = (random.randint(0,900),random.randint(0,900))
            
            balls.append(Ball(a,b,(random.randint(0,200),random.randint(0,200))))
            if c[0] % 2 == 0 :
                d = c[0] + 80, c[1]+60
            else :
                d = c[0]+90, c[1]-60
            segments.append(Segment(c,d))
      