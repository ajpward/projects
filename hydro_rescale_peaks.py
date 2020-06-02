# -*- coding: utf-8 -*-
"""
Created on Thu May  7 16:16:14 2020

@author: Dell
"""

import pygame
import random
import numpy as np
import matplotlib.pyplot as plt
import pickle
import time

"""
Check if peak_routes.data has been created. If not, create new file and write an empty list
"""
try:
    with open('peaks_routes.data', 'rb') as f:
        all_routes = pickle.load(f)
except FileNotFoundError:
    with open('peaks_routes.data', 'wb') as f:
        all_routes = []
        pickle.dump(all_routes, f)  

def DEM_resizer(num_squares):
    """
    Parameters
    ----------
    desired_grid_res : TYPE INT
        desired size of each grid square in meters

    Returns
    -------
    resized_dem : TYPE numpy array
        Numpy array with elevation averaged over the grid squares within a desired grid res 

    """
    
    resized_dem = np.zeros((int(dem_array.shape[0]/num_squares),int(dem_array.shape[1]/num_squares)))
    startx,starty = 0,0
    stopx,stopy = num_squares,num_squares
    for y in range(resized_dem.shape[0]):
        for x in range(resized_dem.shape[1]):
            resized_dem[y,x] = np.average(dem_array[starty:stopy,startx:stopx])
            startx += num_squares
            stopx += num_squares
        startx = 0
        stopx = num_squares
        starty += num_squares
        stopy += num_squares
        
    return resized_dem

class rainDrop(object):
    list_raindrops = []
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.route = []
        self.list_raindrops.append(self)
        self.N_elevation = {}
        self.neighbours = []
        # self.current_N_elevation = {}
   
    
    def draw(self):
        pygame.draw.rect(win,(0,0,255),(self.y/6,self.x/6,1,1))  
                
    def move(self):
        
        #prev_routes(drop)
                     
        if (self.x,self.y) not in self.route:
            self.route.append((self.x,self.y))
            
        self.find_neighbours()
        # neighbours = [neighbour for neighbour in self.neighbours if neighbour not in self.route] #removes previous drop locations (route) from list of neighbours
        # print (neighbours,self.neighbours)
        # new_neighbours = []
        # for neighbour in self.neighbours:
        #     if neighbour not in self.route[-5000:]:
        #         new_neighbours.append(neighbour)
        #     else:# len(self.route)-self.route.index(neighbour) > 500:
        #         print (loop_count,neighbour,len(self.route)-self.route.index(neighbour))
        # neighbours = new_neighbours
        
  

        # neighbour_elevation = {neighbour:dem_array[neighbour[0],neighbour[1]] for neighbour in self.neighbours if neighbour not in self.route[-1000:]}     
        neighbour_elevation = {neighbour:dem_array[neighbour[0],neighbour[1]] for neighbour in self.neighbours if neighbour not in self.route[:]}
        self.N_elevation.update(neighbour_elevation)
        
        
        # for coord in self.route:
        #     if coord in self.N_elevation.keys():
        #         loop_list.append(loop_count)
        #         if coord != (self.x,self.y):
        #             print (coord,(self.x,self.y))
        #         del self.N_elevation[coord]

         
        if (self.x,self.y) in self.N_elevation.keys():
            del self.N_elevation[(self.x,self.y)]

        if len(neighbour_elevation.keys()) > 0: #drop location has neighbours that are not already in route
            
            lowest_neighbour = min(neighbour_elevation, key=neighbour_elevation.get) # key with the lowest value (lowest elevation)

            if dem_array[lowest_neighbour] <= dem_array[self.x,self.y]+1:
                self.x,self.y = lowest_neighbour[0],lowest_neighbour[1] 
            else:
                self.reservoir()
        else: #drop location has no neighbours that are not already in route
            self.reservoir() #call resevoir to find next lowest square
        
    def find_neighbours(self):  
        x,y = self.x,self.y
        
        N_neighbour = (x,y-1)
        NE_neighbour = (x+1,y-1)
        E_neighbour = (x+1,y)
        SE_neighbour = (x+1,y+1)
        S_neighbour = (x,y+1)
        SW_neighbour = (x-1,y+1)
        W_neighbour = (x-1,y)
        NW_neighbour = (x-1,y-1)
        
        self.neighbours = [N_neighbour,NE_neighbour,E_neighbour,SE_neighbour,S_neighbour,SW_neighbour,W_neighbour,NW_neighbour]

        
    def reservoir(self):
        search_area = 3
        while True:
            #N_elevation = {key:value for (key,value) in self.N_elevation.items() if self.N_elevation[key] < dem_array[self.x,self.y]+search_area}
            N_elevation = self.N_elevation
            if N_elevation != {}:
                lowest_neighbour = min(N_elevation, key=N_elevation.get)
                self.x,self.y = lowest_neighbour[0],lowest_neighbour[1]
                break
            else:
                search_area += 5
        
# def reservoir(drop):
#     backtrack = -100
#     while True:
#         route_N_list = []
#         for coord in drop.route[backtrack:]:
#             route_N_list += find_neighbours(coord)
#         route_N_list = set(route_N_list)
#         route_N_list = [neighbour for neighbour in route_N_list if neighbour not in drop.route] #removes previous drop locations (route) from list of neighbours
#         N_elevation = {neighbour:dem_array[neighbour[0],neighbour[1]] for neighbour in route_N_list} 
#         if N_elevation == {}:
#             backtrack -= 1
#             print (backtrack)
#             continue
#         break
#     lowest_neighbour = min(N_elevation, key=N_elevation.get)
#     drop.x,drop.y = lowest_neighbour[0],lowest_neighbour[1]
#     return N_elevation

# def reservoir(drop):
#     route_N_list = []
#     for coord in drop.route:
#         route_N_list += find_neighbours(coord)
#     route_N_list = set(route_N_list)
#     route_N_list = [neighbour for neighbour in route_N_list if neighbour not in drop.route] #removes previous drop locations (route) from list of neighbours
#     N_elevation = {neighbour:dem_array[neighbour[0],neighbour[1]] for neighbour in route_N_list} 
#     lowest_neighbour = min(N_elevation, key=N_elevation.get)
#     drop.x,drop.y = lowest_neighbour[0],lowest_neighbour[1]
#     return N_elevation
           
    

def save_all_routes():      
    for drop in rainDrop.list_raindrops:
        if len(drop.route) > 1000:
            all_routes.append(drop.route)
    
    with open('peaks_routes.data', 'wb') as f:
        pickle.dump(all_routes, f) 
        
def prev_routes(drop):
    for route in all_routes:
        if (drop.x,drop.y) in route[:-1]:
            drop.route += route[route.index((drop.x,drop.y)):] 
            for drop in route[route.index((drop.x,drop.y)):]:
                pygame.draw.rect(win,(0,255,0),(drop[1]/6,drop[0]/6,1,1))
                pygame.display.update() 
            drop.x,drop.y = route[-1][0],route[-1][1]
        
def plot_routes():
    for route in all_routes:
        if len(route) > 1000:
            for drop in route:
                pygame.draw.rect(win,(0,0,255),(drop[1]/6,drop[0]/6,1,1)) 
    pygame.display.update() 

def draw_annotations():
    font = pygame.font.SysFont('calibri',15,True)
    
    annotation_dict = {'Cities':{'Sheffield':(0.3811,abs(-0.4701)),'Leeds':(0.8008,abs(-0.5491))},'POI':{'Kinder Scout':(0.3849,abs(-0.8734))}}
    for city in annotation_dict['Cities'].items():
        city_x,city_y = (1-city[1][0])*s_height,s_width-(city[1][1])*s_width
        pygame.draw.rect(win,(255,100,0),(city_y,city_x,10,10))
        text = font.render(str(city[0]),1,(255,100,0))
        win.blit(text,(city_y+10,city_x+10))

    for POI in annotation_dict['POI'].items():
        POI_x,POI_y = (1-POI[1][0])*s_height,s_width-(POI[1][1])*s_width
        pygame.draw.rect(win,(0,150,0),(POI_y,POI_x,10,10))
        text = font.render(str(POI[0]),1,(0,150,0))
        win.blit(text,(POI_y+10,POI_x-15))

    
def redrawWindow():
    # win.blit(dem_background,(0,0))

    if annotations:
        draw_annotations()
              
    for drop in rainDrop.list_raindrops:
        # for coord in drop.current_N_elevation.keys():
        #     pygame.draw.rect(win,(255,0,0),(coord[1]/6,coord[0]/6,1,1))
        drop.draw()
    
    pygame.display.update() 

from PIL import Image
dem = Image.open('peak_district.tif')
dem_array = np.array(dem)

metres_pgc = dem_array.max()/255 #metres per change in grey scale value, elevation difference/numbers in rgb

pygame.init()
s_width,s_height = 300,600
win = pygame.display.set_mode((s_width,s_height))
pygame.display.set_caption("Hydrological discharge") 
NW,SE = (54.0,-2.0),(53.0,-1.0)
#plt.imsave('peaks_DEM_6square.png',DEM_resizer(6),cmap='gray')
dem_background = pygame.image.load('Peaks_DEM_resized.png')
map_background = pygame.image.load('peaks_map_300_600.png')
map_fit_background = pygame.image.load('peaks_map_250_500.png')

win.blit(dem_background,(0,0))

# win.blit(map_fit_background,(25,20))

annotations = False
run = True
timeline = []
while run == True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT: #allow exit using 'X' 
                run = False
                    
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1: #left mouse button pressed (1=left):
                pos1 = pygame.mouse.get_pos() 
                """make one raindrop"""
                grid_square = (pos1[1]*(int(dem_array.shape[0]/s_height)),pos1[0]*(int(dem_array.shape[1]/s_width))) #position on window multiplied by
                print (grid_square)
                print (dem_array[grid_square])
                rainDrop(grid_square[0],grid_square[1])
                
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3 and pos1: #right mouse button pressed (3=right)
                pos2 = pygame.mouse.get_pos() 
                
                """make many raindrops"""
                # rain_square = dem_array[pos1[0]:pos2[0],pos1[1]:pos2[1]] #creates an array of all gridsquares in box
                # for row in range(len(rain_square)):
                #     for col in range(len(rain_square[0])):
                #         rainDrop(pos1[0]+row,pos1[1]+col) #creates a raindrop instance for each gridsquare which falls within box

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_r]:
        print ('Loading routes')
        plot_routes()
    if pressed[pygame.K_a]:
        annotations = True
    
    redrawWindow()
    
    # t1 = time.time()
    for drop in rainDrop.list_raindrops:
        drop.move()  
    # t2 = time.time()
    # timeline.append(t2-t1)     
        
        

plt.plot(timeline)
plt.ylim(0,0.05)
save_all_routes()
    
pygame.quit()


                
