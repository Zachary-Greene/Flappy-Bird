# todo Improve the score system
# todo Make start screen
# todo Make death screen
# todo Eliminate clipping

import pygame  # import Pygame and Random
import random

pygame.init()  # initiate the pygame

w, h = 288, 512  # set the width and height of the pygame window

win = pygame.display.set_mode((w, h))  # define win as the size of the window
pygame.display.set_caption('Flappy Bird')  # set the window title to Flappy Bird

# define variables as image frames/sprites
normalBird = [pygame.image.load('r1.png'), pygame.image.load('r2.png'), pygame.image.load('r3.png')]
BirdJump1 = [pygame.image.load('f1.png'), pygame.image.load('f2.png'), pygame.image.load('f3.png')]
BirdJump2 = [pygame.image.load('f4.png'), pygame.image.load('f5.png'), pygame.image.load('f6.png')]
BirdJump3 = [pygame.image.load('f7.png'), pygame.image.load('f8.png'), pygame.image.load('f9.png')]
scores = [pygame.image.load('0.png'), pygame.image.load('1.png'), pygame.image.load('2.png'),
          pygame.image.load('3.png'), pygame.image.load('4.png'), pygame.image.load('5.png'),
          pygame.image.load('6.png'), pygame.image.load('7.png'), pygame.image.load('8.png'),
          pygame.image.load('9.png')]

# define variables for backgrounds and menus
bg = pygame.image.load('bg.png')
normalFg = pygame.image.load('fg.png')
# cityFg = pygame.image.load('CityFg.png')  # in progress
start = pygame.image.load('st.png')
gameover = pygame.image.load('gameover.png')

normalPipe = pygame.image.load('pipe.png')  # normal up pipe
normalPipe2 = pygame.image.load('pipe2.png')  # normal down pipe
# CityPipe1 = pygame.image.load('CityPipe1.png')  # city up pipe -- in progress
# CityPipe2 = pygame.image.load('CityPipe2.png')  # city down pipe -- in progress

# define clock as the tick
clock = pygame.time.Clock()

count = 0  # second digit in tens -- only digit in ones
lock = 0  # lock the score from increasing by more then 1
scoreMulti = 0  # first digit in tens -- nonexistent in ones

# define the position of the ground
groundLevel = 375


# create the Menu object
class Menu(object):
    def __init__(self, x, y, width, height):  # creating variables to set object position and width + height
        self.x = x  # defining x
        self.y = y  # defining y
        self.width = width  # defining width
        self.height = height  # defining height

    def draw(self, win):  # defining the function to draw the start menu
        win.blit(start, (self.x, self.y))


# creating the death screen object
class Death(object):
    def __init__(self, x, y, width, height):  # creating variables to set object position and width + height
        self.x = x  # defining x
        self.y = y  # defining y
        self.width = width  # defining width
        self.height = height  # defining height

    def draw(self, win):  # defining the function to draw the death screen
        win.blit(gameover, (self.x, self.y))


# create the player object
class Player(object):
    def __init__(self, x, y, width, height):  # creating variables to set object position and width + height
        self.x = x  # defining x
        self.y = y  # defining y
        self.width = width  # defining width
        self.height = height  # defining height
        self.vel = 5  # how fast the player rises/falls
        self.isJump = False  # defining whether the player can jump or not
        self.walkCount = 0  # defining the beginning frame of the player animation
        # self.hitbox = (self.x, self.y, self.width + 30, self.height + 20)  # create the hitbox

    def draw(self, win):  # defining the function to to draw and animate the player
        if self.walkCount + 1 >= 3:  # testing if the animation frame is beyond the frame count
            self.walkCount = 0  # setting back to the first frame

        if self.isJump == True:  # testing if the player can jump
            win.blit(normalBird[self.walkCount // 1], (self.x, self.y))  # drawing the frame
            self.walkCount += 1  # increasing the frame number
            self.y -= self.vel  # making the player jump
        elif self.isJump == False:  # testing if the player can't jump
            win.blit(normalBird[0], (self.x, self.y))  # setting the frame to the first one
            self.y += self.vel  # making the player fall

        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # draw the hitbox
        # self.hitbox = (self.x, self.y, self.width + 30, self.height + 20)  # create the hitbox


# define the first pipe object
class CityEnemy1(object):
    img = normalPipe

    def __init__(self, x, y, width, height):  # creating variables to set object position and width + height
        self.x = x  # defining x
        self.y = y  # defining y
        self.width = width  # defining width
        self.height = height  # defining height

    def draw(self, win):  # defining the function to draw the object
        win.blit(self.img, (self.x, self.y))  # drawing the object with the given x and y coords


# define the second pipe object
class CityEnemy2(object):
    img = normalPipe2

    def __init__(self, x, y, width, height):  # creating variables to set object position and width + height
        self.x = x  # defining x
        self.y = y  # defining y
        self.width = width  # defining width
        self.height = height  # defining height

    def draw(self, win):  # defining the function to draw the object
        win.blit(self.img, (self.x, self.y))  # drawing the object with the given x and y coords


# define the score object
class Score(object):
    def __init__(self, x, y, width, height):  # creating variables to set object position and width + height
        self.x = x  # defining x
        self.y = y  # defining y
        self.width = width  # defining width
        self.height = height  # defining height

    def draw(self, win):  # defining the function to draw the object to the screen
        global count, lock, scoreMulti  # making outer variables known inside the function

        if scoreMulti == scoreMulti + 10:  # if count is equal to the scoreMulti plus 9 then add 10 to scoreMulti
            scoreMulti += 10  # increase scoreMulti by 10 to increase score to next 10
            print(scoreMulti)  # for debugging -- doesn't work??
            print(count)  # for debugging -- doesn't work??

        if count <= 9:  # if count is less then or equal to 9 then move on
            win.blit(scores[count], (self.x, self.y))  # draw the score as long as it is below 9
        elif count > 9:
            win.blit(scores[int(count / 10)], (
            self.x, self.y))  # draw the first digit *bug* index out of range when score reaches 19 see line 118
            win.blit(scores[count % 10],
                     (self.x + 20, self.y))  # draw the second digit -- error: 'IndexError: list index out of range'

        for obstacle1 in pipe1:  # if there is an obstacle1 in pipe1
            if obstacle1.x < Bird.x < obstacle1.x + 52 and lock == 0:  # if obstacle x is less then bird x and bird x is less then onbstacle x + 52 and lock is equal to 0
                count += 1  # add one to count
                lock = 1  # redefine lock as equaling 1
            elif obstacle1.x < Bird.x > obstacle1.x + 52:  # if obstacle x is less then bird x and bird x is greater then obstacle x + 52
                lock = 0  # redefine lock as 0


# define the method of refreshing the screen
def redrawWindow():
    # drawing all the objects
    win.blit(bg, (0, 0))
    Bird.draw(win)
    for obstacle1 in pipe1:
        obstacle1.draw(win)
    for obstacle2 in pipe2:
        obstacle2.draw(win)
    Scores.draw(win)
    win.blit(normalFg, (0, 400))
    # StartMenu.draw(win)
    # DeathScreen.draw(win)
    pygame.display.update()  # updating the display


# defining the coordinates of the objects and width and height
Bird = Player(125, 200, 34, 24)  # setting the x pos, y pos, width and height of the bird
Scores = Score(125, 20, 24, 36)
StartMenu = Menu(0, 0, 184, 267)
DeathScreen = Death(50, 150, 184, 267)
run = True  # define run as True to initiate the loop

pipe1 = []  # create arrays for the obstacles to go in
pipe2 = []

pygame.time.set_timer(pygame.USEREVENT + 2, random.randrange(2000, 3500))  # create event to continously make pipes

# creating the main game loop
while run:
    clock.tick(15)  # setting the tick speed

    for event in pygame.event.get():  # testing for if the players exits the window
        if event.type == pygame.QUIT:
            run = False  # stopping the loop
            pygame.quit()  # quiting the window
            quit()

        if event.type == pygame.USEREVENT + 2:  # testing if the userevent is + 2
            r1 = random.randrange(-300, -100)  # define a y pos for the pipes
            r2 = random.randrange(170, 350)
            pipe1.append(CityEnemy2(300, r1, 64, 64))  # adding the pipe objects to the arrays with the random y pos
            pipe2.append(CityEnemy1(300, r1 + 400, 64, 64))

    for obstacle1 in pipe1:  # while there is a pipe obstacle in that array move down
        obstacle1.x -= 5  # move the obstacle -5 each time the while loop loops
        if obstacle1.x < obstacle1.width * -1:  # If the obstacle is off the screen remove it
            pipe1.pop(pipe1.index(obstacle1))  # destroying the offscreen pipes

    for obstacle2 in pipe2:  # while there is a pipe obstacle in that array move down
        obstacle2.x -= 5  # move the obstacle -5 each time it loops
        if obstacle2.x < obstacle2.width * -1:  # If the obstacle is off the screen move it
            pipe2.pop(pipe2.index(obstacle2))  # destroying the offscreen pipes

    keys = pygame.key.get_pressed()  # assigning keys to the pygame event

    if keys[pygame.K_SPACE] and Bird.y > Bird.vel:  # checking if the player presses the jump button
        Bird.isJump = True  # making the bird jump
    else:
        Bird.isJump = False  # making the bird fall

    if Bird.y >= groundLevel:  # checking if the bird hits the ground
        run = False  # stops the while loop

    for obstacle2 in pipe2:  # while there is a pipe obstacle in that array move to next line
        if obstacle2.x < Bird.x < obstacle2.x + 52 and Bird.y > obstacle2.y:  # if the bird is at the same x and y pos as the pipe
            # print('DEAD')  #prints to the shell that you died (for troubleshooting purposes)
            run = False  # stops the while loop, effectively ending the program

    for obstacle1 in pipe1:  # while there is a pipe obstacle in that array move to next line
        if obstacle1.x < Bird.x < obstacle1.x + 52 and Bird.y < obstacle1.y + 300:  # if the bird is at the same x and y pos as the pipe
            # print('DEAD')  # prints that you died (for troubleshooting purposes)
            # print(count)  # prints the score (for troubleshooting purposes)
            run = False  # stops the while loop, effectively ending the program

    # refreshing the screen
    redrawWindow()
