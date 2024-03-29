#pygame is a library inside a python ,there are 4 important things in pygame they are GAME LOOP,EVENTS,SPRITES AND SOUND
#the other games that can be done with pygame is angrybird,spiderman,fruit ninja 
#gameloop is a kind of while loop(infinite loop), where sprites are blit(displayed) again and again,because we are going to display the game screen again and again as well as sound and events are accepted from user
#we are bliting(continuously) displaying the changes on screen ,so that user will think it as game thats been changing on time 
#this file is converted to .exe(execution) file means this file can be shared to others
#the first procedure is to extract images(.png),sound,background
import random # For generating random numbers which are used in generating pipes
import sys # We will use sys.exit later to exit the program
import pygame
from pygame.locals import * # Basic pygame imports

# Global Variables for the game which are used throughout the game
FPS = 32 #it tells how many frames are displayed per second,less fps leads to game lagging
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))#.set mode initialise a window or screen for display with given height and width
GROUNDY = SCREENHEIGHT * 0.8#base.png is our ground y,80% of the screenheight away from y=0
GAME_SPRITES = {}#to store game images
GAME_SOUNDS = {}#to store game sound
#just importing the respective images and storing in player,bg,pipe
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'

def welcomeScreen():
    """
    Shows welcome images on the screen
    """

    playerx = int(SCREENWIDTH/5)#we want to start the screen at 1/5th part of x coord
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)#to show it in centre
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)#message allignment in y coord
    basex = 0
    while True:
        for event in pygame.event.get():
            # Pygame will register all events(mouse click,spacebar) from the user into an event queue which can be received with the code pygame. event. get() .
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()#escape key -- k_escape ,keydown -- some key is pressed
                sys.exit()#close the game window

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            #now leave the welcome screen and enter maingame() where game is once again started,== is used because it is an assignment operator
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0)) #screen.blit is a function which takes two arguements like image and its coord
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))    
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))    
                pygame.display.update()#the screen is changed with objects inside it
                FPSCLOCK.tick(FPS)#game fps is controlled,means it is fixed to the value and doesnot change wrt time

def mainGame():
    score = 0#score starts from 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4 #pipes velocity by which it will move

    playerVelY = -9 #bird(player) velocity,means player will fall by velocity of -9
    playerMaxVelY = 10 #bird max velocity
    playerMinVelY = -8 #bird min velocity
    playerAccY = 1 #bird acceleration

    playerFlapAccv = -8 # velocity while flapping(jumping)
    playerFlapped = False # It is true only when the bird is flapping

    #gameloop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:#means playery is inside the screen
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()#bird fly with sound


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed by any one of them
        if crashTest:
            return     

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2#this means that score is displayed at the centre
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2#this gives pipe centre
            if pipeMidPos<= playerMidPos < pipeMidPos +4:#means if the bird cross pipes then score get increased by 1
                score +=1
                print(f"Your score is {score}") #In Python source code, an f-string is a literal string, prefixed with f , which contains expressions inside braces. The expressions are replaced with their values.” 
                GAME_SOUNDS['point'].play() #sound generated when earned a point


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False      #this is to check whether user is continuously using keys,here if user flaps one time then we make it false
        playerHeight = GAME_SPRITES['player'].get_height() #player height is stored
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)#this is to ensure whether user not reached ground if reached then fall with constant velocity

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):#zipping two values[(U,L)]
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]#to show score
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()#blit score at exact centre
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:#when u hit upper pipe
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:#when you hit lower pipe
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()#pick the pipe from gamesprites and get its height
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))#randrage is a function which generates random number
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe#just the dimensions of generating pipes both upper and lower






if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock() #Creates a new Clock object that can be used to track an amount of time. The clock also provides several functions to help control a game's framerate.
    pygame.display.set_caption('Flappy Bird by CodeWithHarry') #just a caption displayed initially in game
    GAME_SPRITES['numbers'] = ( 
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )#numbers are the keys,the keyvalue pair is added to the empty dictionary,convert alpha is a function helps in faster blitting,means images are optimised for game

    GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    )#two pipes are shown by 180 d and they are opposite as well.pipe is a global variable which is already defined

    # Game sounds with path
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame() # This is the main game function  
