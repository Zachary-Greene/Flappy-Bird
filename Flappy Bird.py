import pygame  # import Pygame, Random
import random

pygame.init()  # initiate pygame

w, h = 288, 512  # set the width and height of the pygame window

win = pygame.display.set_mode((w, h))  # define win as the size of the window
pygame.display.set_caption('Flappy Bird')  # set the window title to Flappy Bird

# define variables as image frames/sprites
normalBird = [pygame.image.load('C:\\Users\\zacha\\OneDrive\\Desktop\\PythonScripts\\FlappyBird\\r1.png'),
              pygame.image.load('C:\\Users\\zacha\\OneDrive\\Desktop\\PythonScripts\\FlappyBird\\r2.png'),
              pygame.image.load('C:\\Users\\zacha\\OneDrive\\Desktop\\PythonScripts\\FlappyBird\\r3.png')]
scores = [pygame.image.load('C:\\Users\\zacha\\OneDrive\\Desktop\\PythonScripts\\FlappyBird\\0.png'),
          pygame.image.load('C:\\Users\\zacha\\OneDrive\\Desktop\\PythonScripts\\FlappyBird\\1.png'),
          pygame.image.load('C:\\Users\\zacha\\OneDrive\\Desktop\\PythonScripts\\FlappyBird\\2.png'),
          pygame.image.load('C:\\Users\\zacha\\OneDrive\\Desktop\\PythonScripts\\FlappyBird\\3.png'),
          pygame.image.load('C:\\Users\\zacha\\OneDrive\\Desktop\\PythonScripts\\FlappyBird\\4.png'),
          pygame.image.load('C:\\Users\\zacha\\OneDrive\\Desktop\\PythonScripts\\FlappyBird\\5.png'),
          pygame.image.load('C:\\Users\\zacha\\OneDrive\\Desktop\\PythonScripts\\FlappyBird\\6.png'),
          pygame.image.load('C:\\Users\\zacha\\OneDrive\\Desktop\\PythonScripts\\FlappyBird\\7.png'),
          pygame.image.load('C:\\Users\\zacha\\OneDrive\\Desktop\\PythonScripts\\FlappyBird\\8.png'),
          pygame.image.load('C:\\Users\\zacha\\OneDrive\\Desktop\\PythonScripts\\FlappyBird\\9.png')]

# define variables for backgrounds and menus
bg = pygame.image.load('C:\\Users\\zacha\\OneDrive\\Desktop\\PythonScripts\\FlappyBird\\bg.png')
normalFg = pygame.image.load('C:\\Users\\zacha\\OneDrive\\Desktop\\PythonScripts\\FlappyBird\\fg.png')

startscreen = pygame.image.load('C:\\Users\\zacha\\OneDrive\\Desktop\\PythonScripts\\FlappyBird\\st.png')
deathscreen = pygame.image.load('C:\\Users\\zacha\\OneDrive\\Desktop\\PythonScripts\\FlappyBird\\gameover.png')

normalPipe = pygame.image.load('C:\\Users\\zacha\\OneDrive\\Desktop\\PythonScripts\\FlappyBird\\pipe.png')  # normal up pipe
normalPipe2 = pygame.image.load('C:\\Users\\zacha\\OneDrive\\Desktop\\PythonScripts\\FlappyBird\\pipe2.png')  # normal down pipe

# define clock as the tick
clock = pygame.time.Clock()

count = 0  # second digit in tens -- only digit in ones
lock = 0  # lock the score from increasing by more then 1
scoreMulti = 0  # first digit in tens -- nonexistent in ones

dead = False
dead_count = 0

# define the position of the ground
groundLevel = 375


# create the player object
class Player(object):
    def __init__(self, x, y, width, height, birdtype):  # creating variables to set object position and width + height
        self.x = x  # defining x
        self.y = y  # defining y
        self.width = width  # defining width
        self.height = height  # defining height
        self.birdType = birdtype
        self.vel = 5  # how fast the player rises/falls
        self.isJump = False  # defining whether the player can jump or not
        self.walkCount = 0  # defining the beginning frame of the player animation
        self.hitbox = (self.x, self.y, self.width, self.height)  # create the hitbox
        self.rect = 0

    def draw(self, win):  # defining the function to to draw and animate the player
        if self.walkCount + 1 >= 3:  # testing if the animation frame is beyond the frame count
            self.walkCount = 0  # setting back to the first frame

        if self.isJump == True:  # testing if the player can jump
            win.blit(self.birdType[self.walkCount // 1], (self.x, self.y))  # drawing the frame
            self.walkCount += 1  # increasing the frame number
            self.y -= self.vel  # making the player jump
        elif self.isJump == False:  # testing if the player can't jump
            win.blit(self.birdType[0], (self.x, self.y))  # setting the frame to the first one
            self.y += self.vel  # making the player fall

        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # draw the hitbox
        self.hitbox = (self.x, self.y, self.width, self.height)  # create the hitbox


# define the first pipe object
class CityEnemy1(object):
    img = normalPipe

    def __init__(self, x, y, width, height):  # creating variables to set object position and width + height
        self.x = x  # defining x
        self.y = y  # defining y
        self.width = width  # defining width
        self.height = height  # defining height
        self.hitbox = (self.x - 5, self.y, self.width, self.height)

    def draw(self, win):  # defining the function to draw the object
        win.blit(self.img, (self.x, self.y))  # drawing the object with the given x and y coords

        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # draw the hitbox
        self.hitbox = (self.x - 5, self.y, self.width, self.height)  # create the hitbox


# define the second pipe object
class CityEnemy2(object):
    img = normalPipe2

    def __init__(self, x, y, width, height):  # creating variables to set object position and width + height
        self.x = x  # defining x
        self.y = y  # defining y
        self.width = width  # defining width
        self.height = height  # defining height
        self.hitbox = (self.x - 5, self.y, self.width, self.height)

    def draw(self, win):  # defining the function to draw the object
        win.blit(self.img, (self.x, self.y))  # drawing the object with the given x and y coords

        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # draw the hitbox
        self.hitbox = (self.x - 5, self.y, self.width, self.height)  # create the hitbox


# define the score object
class Score(object):
    def __init__(self, x, y, width, height):  # creating variables to set object position and width + height
        self.x = x  # defining x
        self.y = y  # defining y
        self.width = width  # defining width
        self.height = height  # defining height

    def draw(self, win):  # defining the function to draw the object to the screen
        global count, count2, lock, scoreMulti  # making outer variables known inside the function

        if scoreMulti == scoreMulti + 10:  # if count is equal to the scoreMulti plus 9 then add 10 to scoreMulti
            scoreMulti += 10  # increase scoreMulti by 10 to increase score to next 10

        if count <= 9:  # if count is less then or equal to 9 then move on
            win.blit(scores[count], (self.x, self.y))  # draw the score as long as it is below 9
        elif count > 9:
            win.blit(scores[int(count / 10)], (
                self.x, self.y))  # draw the first digit
            win.blit(scores[count % 10],
                     (self.x + 20, self.y))  # draw the second digit

        for obstacle1 in pipe1:  # if there is an obstacle1 in pipe1
            if obstacle1.x < Bird.x < obstacle1.x + 52 and lock == 0:  # if obstacle x is less then bird x and bird x is less then obstacle x + 52 and lock is equal to 0
                lock = 1  # redefine lock as equaling 1
                count += 1  # add one to count
                # print(count)  # debugging
            elif obstacle1.x < Bird.x > obstacle1.x + 52:  # if obstacle x is less then bird x and bird x is greater then obstacle x + 52
                lock = 0  # redefine lock as 0


class Main(object):
    def __init__(self, clockSpeed, runStatus):  # create variable to store the clockSpeed and runStatus
        self.clockSpeed = clockSpeed  # defining clockSpeed
        self.runStatus = runStatus  # defining runStatus

    def mainLoop(self):
        global count, dead, dead_count, run

        while self.runStatus:
            clock.tick(self.clockSpeed)  # setting the tick speed

            redrawWindow()  # draw everything to the screen

            for event in pygame.event.get():  # testing for if the players exits the window
                if event.type == pygame.QUIT:
                    self.runStatus = False  # stopping the loop
                    pygame.quit()  # quiting the window
                    quit()

                if event.type == pygame.USEREVENT + 2:  # testing if the userevent is + 2
                    r1 = random.randrange(-300, -100)  # define a y pos for the pipes
                    pipe1.append(CityEnemy2(300, r1, 52, 320))  # adding the pipe objects to the arrays with the random y pos
                    pipe2.append(CityEnemy1(300, r1 + 400, 52, 320))

            if dead:  # check if dead is True
                if dead_count >= 1:  # check if the players dead_count is more or equal to 1
                    startScreen()  # show the start screen

            for obstacle1 in pipe1:  # for every pipe obstacle in that array
                obstacle1.x -= 5  # move the obstacle -5 each time the while loop loops
                if obstacle1.x < obstacle1.width * -1:  # If the obstacle is off the screen
                    pipe1.pop(pipe1.index(obstacle1))  # destroying the off screen pipes

            for obstacle2 in pipe2:  # for every pipe obstacle in that array
                obstacle2.x -= 5  # move the obstacle -5 each time it loops
                if obstacle2.x < obstacle2.width * -1:  # If the obstacle is off the screen
                    pipe2.pop(pipe2.index(obstacle2))  # destroying the off screen pipes

            keys = pygame.key.get_pressed()  # assigning keys to the pygame event

            if keys[pygame.K_SPACE] and Bird.y > Bird.vel:  # checking if the player presses the jump button
                Bird.isJump = True  # making the bird jump
            else:
                Bird.isJump = False  # making the bird fall

            if Bird.y >= groundLevel:  # checking if the bird hits the ground
                Bird.x = 125  # resetting the birds x and y vals
                Bird.y = 200
                try:
                    pipe1.clear()  # removing the pipe obstacles from the screen
                    pipe2.clear()
                    count -= count  # resetting the score
                    dead = True  # make the player dead
                    dead_count += 1  # incremente the dead_count by 1
                except:
                    count -= count  # resetting the score
                    dead = True  # make the player dead
                    dead_count += 1  # incremente the dead_count by 1

            for obstacle2 in pipe2:  # for every pipe obstacle in that array
                if obstacle2.hitbox[0] <= Bird.hitbox[0] + 34 <= obstacle2.hitbox[0] + 80 and Bird.hitbox[1] + 24 >= obstacle2.hitbox[1]:
                    Bird.x = 125  # resetting the birds x and y vals
                    Bird.y = 200
                    pipe1.clear()  # removing the pipe obstacles from the screen
                    pipe2.clear()
                    count -= count  # resetting the score
                    dead = True  # make the player dead
                    dead_count += 1  # incremente the dead_count by 1

            for obstacle1 in pipe1:  # while there is a pipe obstacle in that array move to next line
                if obstacle1.hitbox[0] <= Bird.hitbox[0] + 34 <= obstacle1.hitbox[0] + 80 and obstacle1.hitbox[1] <= \
                        Bird.hitbox[1] <= obstacle1.hitbox[1] + 320:
                    Bird.x = 125  # resetting the birds x and y vals
                    Bird.y = 200
                    pipe1.clear()  # removing the pipe obstacles from the screen
                    pipe2.clear()
                    count -= count  # resetting the score
                    dead = True  # make the player dead
                    dead_count += 1  # increment the dead_count by 1


def startScreen():
    global dead_count
    run = True  # setting run as True
    while run:
        win.blit(bg, (0, 0))  # draw everything necessary to the screen
        win.blit(normalFg, (0, 400))
        win.blit(startscreen, (0, 0))
        pygame.display.update()  # update the display
        keys = pygame.key.get_pressed()  # define keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if there is the user presses the quit button
                run = False  # change run to false
                pygame.quit()  # quit the module
                break  # quit the program
            if keys[pygame.K_SPACE]:  # check if the player presses space
                dead_count = 0  # set dead_count to 0
                Bird.x = 125  # set the bird position to the center of the screen
                Bird.y = 200
                GameLoop.mainLoop()  # enter the main game loop


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
    pygame.display.update()  # updating the display


# defining the coordinates of the objects and width + height
Bird = Player(125, 200, 34, 24, normalBird)  # setting the x pos, y pos, width, height and type of bird
Scores = Score(125, 20, 24, 36)
GameLoop = Main(20, True)

pipe1 = []  # create arrays for the obstacles to go in
pipe2 = []

pygame.time.set_timer(pygame.USEREVENT + 2, random.randrange(2000, 3500))  # create event to continuously make pipes

startScreen()  # activate the main loop
