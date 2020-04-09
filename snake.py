import os
import numpy as np
import pygame
import random

pygame.init()

w_width,w_height = 300,300
win = pygame.display.set_mode((w_width,w_height))
background = pygame.Surface((w_width,w_height))

pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

block_size = 10
grid = np.zeros((w_width//block_size,w_height//block_size)).astype(int)

colors = [(0,0,0),(154,205,50),(125,125,125)]

def draw_gridlines():
    for row in range(len(grid)):
        pygame.draw.line(win,(100,100,100),(0,row*block_size),(w_width,row*block_size))
    for col in range(len(grid[0])):
        pygame.draw.line(win,(100,100,100),(col*block_size,0),(col*block_size,w_height))
        
def update_grid(grid,snake):
    for coord in snake[:-snake_length]:
        grid[coord[1]][coord[0]] = 0
    for coord in snake[-snake_length:]:
        grid[coord[1]][coord[0]] = 1

def update_snake(snake,next_coord,snake_length):
    snake.append(next_coord)
    
    return snake

def snake_direction(snake):
    i = -1
    while snake[i] == snake[i-1]: #snake is not moving in relation to game loop because of slowdown loop
        i -= 1
    if snake[i][0] < snake[i-1][0]: #snake is moving left
        return 'left'
    elif snake[i][0] > snake[i-1][0]: #snake is moving right
        return 'right'
    elif snake[i][1] < snake[i-1][1]: #snake is moving up
        return 'up'
    elif snake[i][1] > snake[i-1][1]: #snake is moving down
        return 'down'

def check_game_over():
    if head_x >= w_width//block_size or head_x < 0 or head_y >= w_height//block_size or head_y < 0: #if out of bounds
        return True
    if grid[head_y][head_x] == 1:
        return True
    else:
        return False    

def game_over():
    font = pygame.font.SysFont('comicsans',50,True)
    text = font.render('GAME OVER',1,(255,0,0))
    win.blit(text,(w_width//10,20))    
    pygame.display.update()    
    
def lay_food():
    while True:
        x,y = random.randint(0,w_width//block_size-1),random.randint(0,w_height//block_size-1)
        if grid[y][x] == 0:
            grid[y][x] = 2
            return (x,y)
        else:
            continue
        
def redrawGameWindow(grid,score):
    win.blit(background,(0,0))
    
    for row in range(len(grid)):
        for col in range(len(grid[row])):
                pygame.draw.rect(win, colors[grid[row][col]], (col*block_size, row*block_size, block_size, block_size))
    
    draw_gridlines()
    
    score_font = pygame.font.SysFont('comicsans',30,True)
    score_text = score_font.render('Score: '+str(score),1,(0,255,0))
    win.blit(score_text,(20,w_height-40))        
    
    pygame.display.update()

x,y = 0,150//block_size
snake = [(x,y),(x+1,y),(x+2,y),(x+3,y)]

score = 0
food_coord = lay_food()
slowdown = 0
snake_length = len(snake)
play = True
run = True
while run:
    clock.tick(27)
    
    #Allows X to exit the game
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  
    
    if slowdown > 0:
        slowdown += 1
    if slowdown > 3:
        slowdown = 0     
    
    keys = pygame.key.get_pressed()
    
    head_x = snake[-1][0]
    head_y = snake[-1][1]
    
    direction = snake_direction(snake)
    if slowdown == 0:
        if direction == 'left':
            head_x -= 1
        elif direction == 'right':
            head_x += 1
        elif direction == 'up':
            head_y -= 1
        elif direction == 'down':
            head_y += 1
        
        slowdown = 1
            
    if keys[pygame.K_LEFT] and direction != 'right' and head_x-1 >= 0:
        head_x -= 1
    elif keys[pygame.K_RIGHT] and direction != 'left' and head_x+1 < w_width//block_size:
        head_x += 1
    elif keys[pygame.K_UP] and direction != 'down' and head_y-1 >= 0:
        head_y -= 1
    elif keys[pygame.K_DOWN] and direction != 'up' and head_x+1 < w_height//block_size:
        head_y += 1
               
    coord = (head_x,head_y)
       
    if coord != snake[-1]: #snake has moved
        
        
        if coord == food_coord:
            food_coord = lay_food()
            score += 1
            snake_length += 1
        
        if check_game_over():
            game_over()
            play = False      
                          
        if play:
                        
            snake = update_snake(snake,coord,snake_length)
            
            update_grid(grid,snake)
                
            redrawGameWindow(grid,score)
            
pygame.quit()

#glitches
#changing direction not always working
    
    