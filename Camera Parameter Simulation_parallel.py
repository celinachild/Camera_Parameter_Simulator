import numpy as np
import read_paramters as rp

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

# filename_prefix = 'param/20150819/Ground truth/cam'
filename_prefix = 'param/20150819/cam_param/cam'

vertices = (
    (1,-1,-1),
    (1,1,-1),
    (-1,1,-1),
    (-1,-1,-1),
    (1,-1,1),
    (1,1,1),
    (-1,-1,1),
    (-1,1,1)
)


edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7),
)

surfaces = (
    (0,1,2,3),  # front
#    (3,2,7,6), # left
#    (6,7,5,4), # back
#    (4,5,1,0), # right
#    (1,5,7,2), # bottom
    (4,0,3,6)   # up
)

def Cube(pos, rot, size):
    v = np.array(vertices)*size

#    rot = [[1, 0, 0],
#           [0, np.cos(45), -np.sin(45)],
#           [0, np.sin(45), np.cos(45)]]

    glBegin(GL_LINES)
    glColor3fv((1,0,0))
    for edge in edges:
        for vertex in edge:
            temp = np.array(v[vertex])
            temp = np.dot(rot, temp)
            temp = temp + pos
            glVertex3fv(temp)
    glEnd()    
    
    glBegin(GL_QUADS)
    glColor3fv((0,1,0))
    for surface in surfaces:
        for vertex in surface:
            temp = np.array(v[vertex])
            temp = np.dot(rot, temp)
            temp = temp + pos
            glVertex3fv(temp)
    glEnd()    
    
def init_paramters(filename_prefix, n_cam):
    filename = '%s%d_param.txt' % (filename_prefix, 1)
    A,R,t = rp.read_paramters_from_file(filename)
    rot = R    
    pos = t    
    
    for i in range(2,n_cam+1):
        filename = '%s%d_param.txt' % (filename_prefix, i)
        A,R,t = rp.read_paramters_from_file(filename)    
        rot = np.append(rot,R, axis=0)
        pos = np.append(pos,t, axis=0)
    
    rot = np.vsplit(rot,n_cam)
    pos = np.hsplit(pos,n_cam)
    
    return rot, pos
    
def main():
    
    # Init    
    # Parallel    
    n_cam = 5 
    cam_z = -500.0
    cube_size = 10
    
    # Arc
#    n_cam = 8
#    cam_z = -150.0
#    cube_size = 1
#    filename_prefix = 'param/20150522/camParam_'
    
    rot, pos = init_paramters(filename_prefix,n_cam); 
#    krot,kpos = init_paramters('param/20150522/camParam_kinect',2); 
    
    pygame.init()
    display = (1000,1000)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    cent = np.average(pos, axis=0)
    pos = pos - cent
        
    gluPerspective(45, (display[0]/display[1]), 1.0, 10000.0)
    
#    glTranslatef(-cent[0], -cent[1], -5000.0)
    glTranslatef(0, 0, cam_z)
    
    glRotatef(0, 0, 0, 0)

    mouse_hold = False
    px, py = 0, 0
    cx, cy = 0, 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    quit()
                if event.key == K_r:
                    print 'r'
                if event.key == pygame.K_LEFT:
                    glTranslatef(-100,0,0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(100,0,0)
                if event.key == pygame.K_UP:
                    glTranslatef(0,100,0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0,-100,0)
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_hold = True
                    px, py = pygame.mouse.get_pos()
                if event.button == 4:
                    glTranslatef(0,0,100)
                if event.button == 5:
                    glTranslatef(0,0,-100)
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_hold = False
            
            if mouse_hold == True:
                cx, cy = pygame.mouse.get_pos()
                dx = px-cx
                dy = py-cy
                dist = np.sqrt(dx**2 + dy**2)
                glRotatef(dist/10, dy, dx, 0)
                px, py = cx, cy
                
#        glRotatef(1, 3, 1, 1)        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)        
        
        for i in range(0,n_cam):
            Cube(pos[i],rot[i], cube_size)

        pygame.display.flip()
        pygame.time.wait(10)

main()
