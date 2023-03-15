#Drawing a blockgrid using pygame to visualise different algorithms that randomly generates unique worlds
#Project is created for the creation of images that are going to be used in my Bachelors thesis in Computer Engineering

import pygame, sys, random, numpy, perlin_noise, noise


#Color variables to simplify code
GRAY = (75, 75, 75)
DARK_GRAY = (25, 25, 25)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 200, 255)
RED = (200, 0, 0)
YELLOW = (200, 200, 0)
OCEAN = (61, 78, 186)
BEACH = (222, 217, 126)
GRASS = (20, 110, 10)
MOUNTAIN = (100, 100, 100)
SNOW = (255, 255, 255)

#Define window and block size for the program
GRIDSIZE = 500
SQUARE_SIZE = 2
WINDOW_HEIGHT = SQUARE_SIZE*GRIDSIZE
WINDOW_WIDTH = SQUARE_SIZE*GRIDSIZE

#Player variables(not fully used anymore)
MOVESPEED = SQUARE_SIZE
PLAYER_SIZE = SQUARE_SIZE

#Number of random steps in randomWalk() function
STEPS = 100000

#Integer value for creation of BSP rooms(not working currently)
ROOMVALUE = 1

#Position variables for the player object
RED_POS_X = (GRIDSIZE//2)*SQUARE_SIZE
RED_POS_Y = (GRIDSIZE//2)*SQUARE_SIZE

#Movement variables
moveUp = False
moveDown = False
moveRight = False
moveLeft = False

#Create the blockgrid array
grid = []
for row in range(GRIDSIZE):
    grid.append([])
    for column in range(GRIDSIZE):
        grid[row].append(0)

def main():

    pygame.init()
    global SCREEN, CLOCK, SECOND_SURFACE, PLAYER, RED_POS_X, RED_POS_Y, moveUp, moveDown, moveRight, moveLeft, player_rect, path_rect_list, exit_rect_list, grid
    SCREEN = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
    SECOND_SURFACE = pygame.Surface([SQUARE_SIZE,SQUARE_SIZE])
    PLAYER = pygame.Surface([PLAYER_SIZE,PLAYER_SIZE])
    CLOCK = pygame.time.Clock()

    while True:

        path_rect_list = []
        exit_rect_list = []
        #drawCave()
            
        player_rect = pygame.Rect(RED_POS_X, RED_POS_Y, PLAYER_SIZE, PLAYER_SIZE)
        pygame.draw.circle(SCREEN, RED, (RED_POS_X+SQUARE_SIZE//2, RED_POS_Y+SQUARE_SIZE//2), PLAYER_SIZE/2)

        pygame.display.flip()
        CLOCK.tick(20)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                resetGrid()
                randomWalk()
                RED_POS_X = (GRIDSIZE//2)*SQUARE_SIZE
                RED_POS_Y = (GRIDSIZE//2)*SQUARE_SIZE

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                resetGrid()
                PerlinMap()
                RED_POS_X = (GRIDSIZE//2)*SQUARE_SIZE
                RED_POS_Y = (GRIDSIZE//2)*SQUARE_SIZE

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    moveUp = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    moveDown = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    moveRight = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    moveLeft = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    moveUp = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    moveDown = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    moveRight = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    moveLeft = False
        
        if moveUp and player_rect.top > 0 and checkPos(RED_POS_X//SQUARE_SIZE, RED_POS_Y//SQUARE_SIZE-1) == 1 or checkPos(RED_POS_X//SQUARE_SIZE, RED_POS_Y//SQUARE_SIZE-1) == 2:
            RED_POS_Y -= MOVESPEED
        if moveDown and player_rect.bottom < WINDOW_HEIGHT and checkPos(RED_POS_X//SQUARE_SIZE, RED_POS_Y//SQUARE_SIZE+1) == 1 or checkPos(RED_POS_X//SQUARE_SIZE, RED_POS_Y//SQUARE_SIZE+1) == 2:
            RED_POS_Y += MOVESPEED
        if moveRight and player_rect.right < WINDOW_WIDTH and checkPos(RED_POS_X//SQUARE_SIZE+1, RED_POS_Y//SQUARE_SIZE) == 1 or checkPos(RED_POS_X//SQUARE_SIZE+1, RED_POS_Y//SQUARE_SIZE) == 2:
            RED_POS_X += MOVESPEED
        if moveLeft and player_rect.left > 0 and checkPos(RED_POS_X//SQUARE_SIZE-1, RED_POS_Y//SQUARE_SIZE) == 1 or checkPos(RED_POS_X//SQUARE_SIZE-1, RED_POS_Y//SQUARE_SIZE) == 2:
            RED_POS_X -= MOVESPEED

        if player_rect.collidelistall(exit_rect_list):
            resetGrid()
            randomWalk()
            RED_POS_X = (GRIDSIZE//2)*SQUARE_SIZE
            RED_POS_Y = (GRIDSIZE//2)*SQUARE_SIZE

def checkPos(x,y):
    if grid[x][y] == 1:
        return 1
    if grid[x][y] == 2:
        return 2
    else:
        return 0
    
def drawCave():
    SCREEN.fill(GRAY)
    for row in range (GRIDSIZE):
        for col in range (GRIDSIZE):
            if grid[row][col] == 0:
                path_rect = pygame.Rect(row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(SCREEN, DARK_GRAY, path_rect)
                path_rect_list.append(path_rect)
            if grid[row][col] == 2:
                exit_rect = pygame.Rect(row*SQUARE_SIZE, col*SQUARE_SIZE, PLAYER_SIZE, PLAYER_SIZE)
                pygame.draw.circle(SCREEN, YELLOW, (row*SQUARE_SIZE+SQUARE_SIZE//2, col*SQUARE_SIZE+SQUARE_SIZE//2), SQUARE_SIZE/2)
                exit_rect_list.append(exit_rect)

def randomWalk():
    x = GRIDSIZE//2
    y = GRIDSIZE//2
    grid[x][y] = 1
    for i in range (STEPS):
        rand = random.randint(0,3) #0 = up 1 = down 2 = right 3 = left
        if rand == 0:
            if y > 0:
                y = y - 1
                grid[x][y] = 1
        if rand == 1:
            if y < GRIDSIZE-1:
                y = y + 1
                grid[x][y] = 1
        if rand == 2:
            if x < GRIDSIZE-1:
                x = x + 1
                grid[x][y] = 1
        if rand == 3:
            if x > 0:
                x = x - 1
                grid[x][y] = 1
    drawCave()
    createExit()

def randomPartition():
    firstWall = random.randint(0,GRIDSIZE-1)
    print(firstWall)
    yWall = (GRIDSIZE-1)
    print(yWall)
    for value in range (ROOMVALUE):
        createVerticalWall(firstWall, yWall)

    """for wall in range (1):
        yWall = random.randint(0,GRIDSIZE-1)
        xWall = random.randint(0,GRIDSIZE-1)
        for y in range (0, GRIDSIZE):
            if grid[yWall][y] == 1:
                yWall = random.randint(0,GRIDSIZE-1)
            else:
                grid[yWall][y] = 1
        for x in range (0, GRIDSIZE):
            if grid[x][xWall] == 1:
                xWall = random.randint(0,GRIDSIZE-1)
            else:
                grid[x][xWall] = 1"""

def createVerticalWall(x,y):
    grid[25][1] = 1
    for i in range (0,y):
        grid[x][i] = 1

def createXWall(x,y):
    not_good = 1

def PerlinMap():
    seed = random.randint(0,10000)
    for row in range(GRIDSIZE):
        for column in range(GRIDSIZE):
            grid[row][column] = noise.pnoise3(row/GRIDSIZE, column/GRIDSIZE, seed, octaves=9, persistence=0.6,lacunarity=2)
    drawPerlin()

def drawPerlin():
    SCREEN.fill(RED)
    for row in range (GRIDSIZE):
        for col in range (GRIDSIZE):
            if grid[row][col] < -0.01:
                map_rect = pygame.Rect(row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(SCREEN, OCEAN, map_rect)
            elif grid[row][col] < 0.01:
                map_rect = pygame.Rect(row*SQUARE_SIZE, col*SQUARE_SIZE, PLAYER_SIZE, PLAYER_SIZE)
                pygame.draw.rect(SCREEN, BEACH, map_rect)
            elif grid[row][col] < 0.12:
                map_rect = pygame.Rect(row*SQUARE_SIZE, col*SQUARE_SIZE, PLAYER_SIZE, PLAYER_SIZE)
                pygame.draw.rect(SCREEN, GRASS, map_rect)
            elif grid[row][col] < 0.2:
                map_rect = pygame.Rect(row*SQUARE_SIZE, col*SQUARE_SIZE, PLAYER_SIZE, PLAYER_SIZE)
                pygame.draw.rect(SCREEN, MOUNTAIN, map_rect)
            elif grid[row][col] < 1:
                map_rect = pygame.Rect(row*SQUARE_SIZE, col*SQUARE_SIZE, PLAYER_SIZE, PLAYER_SIZE)
                pygame.draw.rect(SCREEN, SNOW, map_rect)

def createExit():
    rand1 = random.randint(0, GRIDSIZE-1)
    rand2 = random.randint(0, GRIDSIZE-1)
    if grid[rand1][rand2] == 1:
        grid[rand1][rand2] = 2
    else:
        createExit()

def resetGrid():
    for row in range (GRIDSIZE):
        for col in range (GRIDSIZE):
            grid[row][col] = 0

if __name__ == "__main__":
    main()