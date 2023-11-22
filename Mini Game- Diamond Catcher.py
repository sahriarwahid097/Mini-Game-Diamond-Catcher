from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

current_x, current_y = 0, 240
ctop_x1,ctop_y1,ctop_x2,ctop_y2=-185, -220, -80, -220
cbottom_x1,cbottom_y1,cbottom_x2,cbottom_y2=-100, -240, -165, -240
cleft_x1,cleft_y1,cleft_x2,cleft_y2= -165, -240, -185, -220
cright_x1,cright_y1,cright_x2,cright_y2=-100, -240, -80, -220
catcher_color=(1,1,1)
catcher_color_original=(1,1,1)
diamond_speed=3
current_color=(1,1,0)
catcher_speed=10
paused=False
score=0
missed=False
restart=False

def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3 
        elif dx < 0 and dy < 0:
            return 4  
        else:
            return 7  
    else:
        if dx >= 0 and dy >= 0:
            return 1 
        elif dx < 0 and dy >= 0:
            return 2  
        elif dx < 0 and dy < 0:
            return 5  
        else:
            return 6  

def convert_to_zone0(x, y, original_zone):
    if original_zone == 0:
        return x, y
    elif original_zone == 1:
        return y, x
    elif original_zone == 2:
        return -y, x
    elif original_zone == 3:
        return -x, y
    elif original_zone == 4:
        return -x, -y
    elif original_zone == 5:
        return -y, -x
    elif original_zone == 6:
        return y, -x
    elif original_zone == 7:
        return x, -y

def convert_to_original_zone(x, y, original_zone):
    if original_zone == 0:
        return x, y
    elif original_zone == 1:
        return y, x
    elif original_zone == 2:
        return -y, x
    elif original_zone == 3:
        return -x, y
    elif original_zone == 4:
        return -x, -y
    elif original_zone == 5:
        return -y, -x
    elif original_zone == 6:
        return y, -x
    elif original_zone == 7:
        return x, -y

def midpoint_line(x1, y1, x2, y2, original_zone):
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    x, y = x1, y1

    while x <= x2:
        x_orig, y_orig = convert_to_original_zone(x, y, original_zone)
        glVertex2f(x_orig, y_orig)

        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
        x += 1


def draw_line(x1, y1, x2, y2,color=(1,1,1)):
    zone = find_zone(x1, y1, x2, y2)
    x1, y1 = convert_to_zone0(x1, y1, zone)
    x2, y2 = convert_to_zone0(x2, y2, zone)
    glBegin(GL_POINTS) 
    glColor3f(*color)
    midpoint_line(x1, y1, x2, y2, zone)
    glEnd()



def draw_pause_play_button():
    if paused==False:
        draw_line(-5,200,-5,245,(1,0.7,0))
        draw_line(15,200,15,245,(1,0.7,0))
    else:
        draw_line(-10,200,-10,245,(1,0.7,0))
        draw_line(-10,245,20,220,(1,0.7,0))
        draw_line(-10,200,20,220,(1,0.7,0))
        


def draw_back_button():
    draw_line(-230,220,-200,200,(0.0, 0.8, 0.8))
    draw_line(-230,220,-200,245,(0.0, 0.8, 0.8))
    draw_line(-230,220,-175,220,(0.0, 0.8, 0.8))

def draw_cross_button():
    draw_line(175,245,230,200,(1.0, 0.0, 0.0))
    draw_line(175,200,230,245,(1.0, 0.0, 0.0))


def draw_box(x1,y1,x2,y2,x3,y3,x4,y4):
    draw_line(x1,y1,x2,y2,(0,0,0))
    draw_line(x2,y2,x3,y3,(0,0,0))
    draw_line(x3,y3,x4,y4,(0,0,0))
    draw_line(x1,y1,x4,y4,(0,0,0))

def draw_diamond(x, y,diamond_color):
    if x-10<-250 or x+10>250:
        pass
    else:
        draw_line(x, y -10, x - 10, y, diamond_color)
        draw_line(x - 10, y, x, y + 10, diamond_color)
        draw_line(x, y + 10, x + 10, y, diamond_color)
        draw_line(x + 10, y, x, y - 10, diamond_color)

def draw_catcher():
    global ctop_x1,ctop_y1,ctop_x2,ctop_y2
    global cbottom_x1,cbottom_y1,cbottom_x2,cbottom_y2
    global cleft_x1,cleft_y1,cleft_x2,cleft_y2
    global cright_x1,cright_y1,cright_x2,cright_x2
    global catcher_color
    draw_line(ctop_x1,ctop_y1,ctop_x2,ctop_y2,catcher_color) 
    draw_line(cbottom_x1,cbottom_y1,cbottom_x2,cbottom_y2,catcher_color)
    draw_line( cleft_x1,cleft_y1,cleft_x2,cleft_y2,catcher_color)
    draw_line(cright_x1,cright_y1,cright_x2,cright_y2,catcher_color)

    

def check_collision():
    global ctop_x1,ctop_y1,ctop_x2,ctop_y2
    global current_x,current_y
    if current_x+10>=ctop_x1 and current_x-10<=ctop_x2 and current_y-10==ctop_y1+10:
        return True
    

def check_miss():
    if -250<=current_y+10<=-240 and (current_x+10<ctop_x1 or current_x-10>ctop_x2):
        return True
    

def specialKeyListener(key, x, y):
    global ctop_x1,ctop_x2
    global cbottom_x1,cbottom_x2
    global cleft_x1,cleft_x2
    global cright_x1,cright_x2
    global catcher_speed
    dx=catcher_speed

    if key==GLUT_KEY_LEFT and (ctop_x1>-240 and cbottom_x1>-250 and cleft_x1>-250):
        ctop_x1,ctop_x2=ctop_x1-dx,ctop_x2-dx
        cbottom_x1,cbottom_x2=cbottom_x1-dx,cbottom_x2-dx
        cleft_x1,cleft_x2=cleft_x1-dx,cleft_x2-dx
        cright_x1,cright_x2=cright_x1-dx,cright_x2-dx

    elif key==GLUT_KEY_RIGHT and (ctop_x2<250 and cbottom_x2<250 and cright_x1<250):
        ctop_x1,ctop_x2=ctop_x1+dx,ctop_x2+dx
        cbottom_x1,cbottom_x2=cbottom_x1+dx,cbottom_x2+dx
        cleft_x1,cleft_x2=cleft_x1+dx,cleft_x2+dx
        cright_x1,cright_x2=cright_x1+dx,cright_x2+dx


        
def mouseListener(button, state, x, y):
    global diamond_speed, paused, current_x, current_y
    global catcher_speed
    global score
    global catcher_color
    global catcher_color_original
    global restart
    global missed
    x = x - 250
    y = 250 - y
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if -10 <= x <= 20 and 200 <= y <= 245:
            if not paused:
                diamond_speed = 0
                catcher_speed= 0 
                paused = True
            else:
                diamond_speed =3
                catcher_speed=10
                paused = False

        elif 175<=x<=230 and 200<=y<=245:
            glutLeaveMainLoop()
            print("Score:",score)
            print("GoodBye")

        elif -230<=x<=-200 and 200<=y<=245:
            score=0
            diamond_speed = 3
            catcher_color=catcher_color_original
            restart=True
            missed=False
            print('Starting Over')
        

def display():
    global current_x, current_y
    global current_color
    global diamond_speed
    global score
    global catcher_color
    global restart
    global missed
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPointSize(2.0)
    draw_catcher()
    draw_box(-230,200,-175,200,-175,245,-230,245)
    draw_box(-10,200,20,200,20,245,-10,245)
    draw_box(230,200,175,200,175,245,230,245)
    draw_pause_play_button()
    draw_back_button()
    draw_cross_button()
    draw_diamond(current_x, current_y,current_color)
    if check_collision() or restart:
        restart=False
        current_x, current_y = random.randint(-250, 250), 250
        current_color=(random.uniform(0.5,1),random.uniform(0.5,1),random.uniform(0.5,1))
    current_y -=1*diamond_speed

    if check_collision():
        score=score+1
        print('Score: ',score)

    if check_miss():
       catcher_color=(1.0, 0.0, 0.0)
       if not missed:
           missed=True 
           print("Game Over! Score:",score)
       else:
           pass
       
    glutSwapBuffers()
    glutPostRedisplay()



glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutCreateWindow(b"Mini Game- Diamond Catcher")
glutDisplayFunc(display)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glClearColor(0.0, 0.0, 0.0, 1.0)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(-250, 250, -250, 250, -1, 1)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glutMainLoop()