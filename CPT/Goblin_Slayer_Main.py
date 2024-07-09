'''
Name: and Aarav Rothe
Date: Wed Jun 5, 2023
Task: Goblin Slayer game with American ideologies of our glorious Uncle Sam (Definitely not named after the anime ^_^)
'''

#import pygame,random, tkinter, and messagebox, and os module
import pygame,os
import random
from tkinter import Tk, messagebox, simpledialog

#Create and then close the Tk window
Tk().withdraw()
#initialize pygame and initialize the music as well
pygame.init()
pygame.mixer.init()

#initalize holding down keys to yes and have a delay
pygame.key.set_repeat(60, 120)

#load the music background, play it, and set the volume
pygame.mixer.music.load('arcade-party-173553.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.1)

#here are the sound effects all in a list
sounds = {'shot': pygame.mixer.Sound('gun-shot-6178.wav'), 'die':pygame.mixer.Sound('pixel-death-66829.wav'), 'gobdie': pygame.mixer.Sound('goblin-death-6729.wav') }

#creating the background images and then smoothscale them, for the deck, the background, and set the surface
backgroundd = pygame.image.load('20483.jpg')
background = pygame.transform.scale(backgroundd, (backgroundd.get_width() * 0.15, backgroundd.get_height() * 0.15))
#create the display window
surface = pygame.display.set_mode((background.get_width(), background.get_height()))
#deck image smoothscale and loading
deck = pygame.image.load('wooden_deck.png')
deckscaled = pygame.transform.smoothscale (deck, (105,surface.get_height()))

#creating the first font using  sys font and render the title of GOBLIN SLAYA!!!!!
f = pygame.font.SysFont(name = "gabriola", size = 75, bold = True, italic = False)
output = f.render("Goblin Slayer" , True, (225, 125, 0))

#set caption and logo of the window to make program look kewler
pygame.display.set_caption('GOBLIN SLAYA!')
pygame.display.set_icon(pygame.image.load('E_E_Gun__Run_000_000.png'))

#withdraw the window when displaying a messagebox
Tk().withdraw()

#do a try except error to ask the user for how many seconds they want the goblins to spawn, and only enter floating point numbers
while True:
    #try the timer messagebox, and ask them
    try:
        timer = simpledialog.askfloat('Challenge Yourself!', 'How often do you want the goblins to spawn in seconds? \n (the normal number is every 3 seconds and the number has to be between 1 and 6)')
        #if they choose a number that is too high or too low, show them
        if timer < 1 or timer > 6:
            messagebox.showinfo("Error", "Please enter a number or decimal \n that is >=1 or <=6 seconds")
        else:
            #if they answer correctly, break and move on in life, program
            break
    except:
        #if there is an error, idk just move on
        pass

#if the timer is very high, only start out with 20 bullets so the diffculty is balanced
if timer <= 7 and timer >= 2:
    bulletnumber = 20
#if the timer is less than 2, then give them 35 bullets
elif timer < 2:
    bulletnumber = 35
#multiply the user entered number by 1000 and make it an integer
timer = int(timer * 1000)
#set the diffculty level to 1 and the total kills counter to 0
difficultylvl = 1
totalgoblinkills = 0

#set the new fonts and their sizes
font2 = pygame.font.Font('Stoneyard.ttf', 29)
font3 = pygame.font.Font('Stoneyard.ttf', 37)
#render the total bullets display counter
totalbullets = font2.render(f'Total Bullets: {bulletnumber}', True, 'green')
#render the difficulty level
Difficultylevel = font2.render(f'Difficulty level: {difficultylvl}', True, 'green')
#render the total kills counter displuy
TotalKills = font2.render(f'Kills: {totalgoblinkills}', True, 'green')
#render the display level for the screen
DisplayLevel1 = font3.render('The Difficulty level has Increased!', True, 'red')
DisplayLevel2 = font3.render('You obtain more bullets', True, 'red')
DisplayLevel3 = font3.render('More goblins and knives!!', True, 'red')

#declare variables to store the surface's height and width
height = surface.get_height()
width = surface.get_width()

#declare lists to store images of soldier animations, make for loops to append animations
soldierrun = []
soldieridle = []
soldierdie = []
#soldier shooting animation list
soldiershoot = []
#since all soldier animations are 10 images, loop all the list cyclers under one for loop and add their animations to the list
for counter1 in range (10):
    #soldier running animations
    soldierrun.append(pygame.transform.smoothscale((pygame.transform.flip((pygame.image.load(f'02-Run/E_E_Gun__Run_000_00{counter1}.png')), True, False)), (150,140)))
    #idle soldier animations
    soldieridle.append(pygame.transform.smoothscale((pygame.transform.flip((pygame.image.load(f'01-Idle/E_E_Gun__Idle_00{counter1}.png')), True, False)), (150,130)))
    #soldier shooting variable
    soldiershoot.append(pygame.transform.smoothscale((pygame.transform.flip((pygame.image.load(f'03-Shot/E_E_Gun__Attack_00{counter1}.png')), True, False)), (160,135)))
    #soldier dying animation
    soldierdie.append(pygame.transform.smoothscale((pygame.transform.flip((pygame.image.load(f'Soldier-Guy-PNG/06-Die/E_E__Die_00{counter1}.png')), True, False)), (170,160)))
    
#list codes and variables for bullet
bullets = []
#load bullet image and smoothscale it
basebullet = pygame.image.load('Bullet.png')
bullet = pygame.transform.smoothscale(basebullet, (25,25))
#declare movement x and y positions variables for the bullet positions
BULspeed = 15
yposBUL = 0
#declare soldier starting point on screen, that is later altered to move along the y-axis
yposSOL = surface.get_height() // 2 - soldierrun[0].get_height() + 25

#throwing knife image load and scaling, and declare the knife list
knifeunscaled = pygame.image.load('Sword01.png')
throwingknife = pygame.transform.smoothscale(knifeunscaled, (55,30))
knifelist = []

#load the health power up and more bullets power up in images and smoothscale them 
healthpowerupscaled = pygame.image.load('PowerUp_05.png')
healthpowerup = pygame.transform.scale(healthpowerupscaled, (75,75))
bulletspowerupscaled = pygame.image.load ('PowerUp_08.png')
bulletspowerup = pygame.transform.scale(bulletspowerupscaled, (75,75))

#declare variables, animation lists, storage lists, and tracking lists for the goblins
goblinrun = []
goblins2 = []
goblindie = []

#since all goblin animations are 10 images, loop all the list cyclers under one for loop and add their animations to the list
for counter4 in range (7):
    goblindie.append(pygame.transform.smoothscale((pygame.transform.flip((pygame.image.load(f'CHIBI GOBLIN-PNG/06-Die_/2D_GOBLIN__Die_00{counter4}.png')), True, False)), (150,160)))
    goblinrun.append(pygame.transform.smoothscale((pygame.transform.flip((pygame.image.load(f'CHIBI GOBLIN-PNG/02-Run_/2D_GOBLIN__Run_00{counter4}.png')), True, False)), (150,160)))
#declare goblin position variables
xgoblin = 0
ygoblin = 0
#delcare the giblin death index to cycle through the death images
indexdiegob = 0
#the bulletdone variable checks if the bullets are run out, and is currently set to false
bulletdone = False

#declare the power ups lists to store and track them
powerlist = []
powerhealthlist = []
#if the soldier dies by a knife, then end the game (currently set to false)
deathbyknife = False

#goblin_rect = pygame.Rect(0,20 ,goblinrun[0].get_width() - 42 ,goblinrun[0].get_height() - 50)
#if the goblin in shot, set this variable to True
goblinshot = False
goblinmetJesus = False
#if the bullet has collided with the goblin, this will be True
bulletcollide = False
#declare image cyclers and indexes to cycle through each of the soldier animations
indexsoldier = 0
indexidle = 0
indexshoottimes = -1
indexshoot = 0

#show the level and display it 
showlevel = False

#declare booleans to check for the soldier animations to see if they are idle, running or dying
soldierwalk = False
soldierhashot = False
soldierisidle = True
#bullet is shot variable
bullettravel = False

#choice list for yspeed of goblin between -3 and 3
yspeedchoice = [-3,3]
#set a uservent to make random knives spawn in every few seconds
timer2 = 3000

#declare all the userevents
pygame.time.set_timer(pygame.USEREVENT, timer) #goblin spawner userevent
pygame.time.set_timer(pygame.USEREVENT + 1, timer2) #knife coming our userevent
pygame.time.set_timer(pygame.USEREVENT + 2, 14500) #bullet powerup userevent
pygame.time.set_timer(pygame.USEREVENT + 3, 21500) #health powerup Userevent
pygame.time.set_timer(pygame.USEREVENT + 4, 35000) #difficulty change Userevent

#goblin death index cycler for death animation and soldier death animations
goblindeathindex = 0
indexdeath = 0

#the bullets that are to be added at each difficulty change
bulletsadded = 12

#these are the keys that allow multiple buttons to be pressed at once
keys = [False, False, False, False]
#set the soldier current knife bar and bullet hits to 0
hitsSOL = 0
#create the event handler and main while loop to show events and also set the quit variable (done)
done = False
while done == False:
            
    #blit the background images and deck as well as title and bullet left and make it a function so you can potentially use them later 
    def allbackground():
        surface.blit(background,(0,0))
        surface.blit(output, (background.get_width()//2 - output.get_width()//2, 0))
        surface.blit (deckscaled, (width - 150,0))
        surface.blit(totalbullets, (10, height - 30))
        surface.blit(Difficultylevel, (10, 10))
        surface.blit(TotalKills, (10,35))
    allbackground()
 
    #event handler for pygame.event.get()
    for event in pygame.event.get():
        #if player x out screen or quit, then quit and make done = True
        if event.type == pygame.QUIT:
            done = True
        #if player hold down w or s to move up or down
        if event.type == pygame.KEYDOWN:
            #if W or S are pressed, make the keys equal to true for their respective indexes
            if event.key == pygame.K_w:
                if deathbyknife == False:
                    keys[0] = True
            elif event.key == pygame.K_s:
                if deathbyknife == False:
                    keys [1] = True

        #if the player shoots their gun and hits the mouse button
        if event.type == pygame.MOUSEBUTTONDOWN:
            #if the user had not been hit by 2 knives yet,
            if deathbyknife == False and bulletdone == False:
                #make the shot variable True
                keys[2] = True
                #play the shot sound effect
                pygame.mixer.Sound.play(sounds['shot'])
                #make the other animations false and set the shot animations true
                bullettravel = False
                soldierhashot = True
                soldierisidle = False
                #set the constant bullet y position based on the soldier y position
                yposBUL = yposSOL
                #increase the index shoot times variable
                indexshoottimes += 1
                xbulspeed = 10  #set the bulletspeed
                xbullet = width - 180 #set the bullet starting point that will ve altered as it moves along
                ybullet = yposSOL
                #decrease the bullet number by 1 for every shot
                bulletnumber -= 1
                #if the bulletnumber is 0, make the bulletdone variable true and end the game
                if bulletnumber <= 0:
                    bulletdone = True  
                #add a bullet's info to the bullets list and display the bullet change on the screen           
                bullets.append([xbullet,ybullet,xbulspeed])
                totalbullets = font2.render(f'Total Bullets: {bulletnumber}', True, 'green') 
                   
        #if any key is released, activate the idle animations variable
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                if deathbyknife == False:
                    keys[0] = False
                    soldierwalk = False
                    soldierisidle = True
            if event.key == pygame.K_s:
                if deathbyknife == False:
                    soldierwalk = False
                    soldierisidle = True
                    keys[1] = False
        #if the mousebutton is released, set the movements to false
        if event.type == pygame.MOUSEBUTTONUP:
            keys[2] = False
            bullettravel = True
        #if W is pressed, then make the soldier go up by 20 studs and make the running animation variable true as well as increase the animation cycler and make the idle boolean false
        if keys[0] == True:
            yposSOL -= 20
            soldierwalk = True
            indexsoldier += 1
            soldierisidle = False
        #if S is pressed, then make the soldier go up by 20 studs and make the running animation variable true as well as increase the animation cycler and make the idle boolean false
        if keys[1] == True:
            yposSOL += 20
            soldierwalk = True
            indexsoldier += 1
            soldierisidle = False
           
        #at every userevent, add goblins onto the goblin list, append, and store the variable
        if event.type == pygame.USEREVENT:
            xgoblin = -75 #set the goblin to spawn behind the screen
            #set the y goblin speed and randomly make them go up or down, and set their random position along the y-axis, and set the x-speed as well
            ygoblin = random.randint(30, surface.get_height() - goblinrun[0].get_height() - 5)
            goblin_yspeed = random.choice([-3,3])
            goblin_xspeed = 3
            indexgobdie = 0 #goblin death cycler
            goblindeathindex = 0
            hits = 0  #checking for how many hits the goblin has for the healthbar
            indexgoblin = 0
            #set the goblins list and append a new goblin's info at every userevent
            goblins2.append([xgoblin,ygoblin,goblin_xspeed, goblin_yspeed,'running', hits , -1, goblindeathindex,indexgoblin])
        #if the knife is summoned, generate a knife's details
        if event.type == pygame.USEREVENT + 1:
            xknife = -75 #generate the knife behind the screen
            yknife = random.randint(20, surface.get_height() - 20) #choose a random y-axis spot for the item to generate behind the screen
            xspeedknife = 8 #set the speed of the knife
            knifelist.append([xknife, yknife,xspeedknife])  #append the variables to a list keeping track of each knife
        #if a bulletspowerup drops, append it to the respective list
        if event.type == pygame.USEREVENT + 2:
            xpower = -75 #generate the powerup behind the screen
            ypower = random.randint(bulletspowerup.get_height(), surface.get_height() - bulletspowerup.get_height())  #choose a random y-axis spot for the item to generate behind the screen
            xspeedpower = 12 #set the speed of the powerup
            powerlist.append([xpower,ypower,xspeedpower]) #append the variables to a list keeping track of each bullet power-up
        #at every heal powerup, append its info to a list
        if event.type == pygame.USEREVENT + 3:
            xpower2 = -75 #generate the powerup behind the screen
            ypower2 = random.randint(healthpowerup.get_height(), surface.get_height() - healthpowerup.get_height())  #choose a random y-axis spot for the item to generate behind the screen
            xspeedpower2 = 12 #set the speed of the heal powerup
            powerhealthlist.append([xpower2,ypower2,xspeedpower2])  #append the variables to a list keeping track of each healup
        #at every difficulty change, decrease the knife and goblin spawn rate and display the new difficulty change 
        if event.type == pygame.USEREVENT + 4:
            difficultylvl += 1 #increase the difficulty level display by 1 at every USEREVENT + 4
            Difficultylevel = font2.render(f'Difficulty level: {difficultylvl}', True, 'green')  #blit the new level on screen
            timer = int(timer * 0.80) #decrease the goblin spawn rate
            pygame.time.set_timer(pygame.USEREVENT, timer) #update the userevent timer with the lessened timer
            if bulletnumber < 16: #if the bulletnumber at this point is less than 16, give the user 16 bullets
                bulletnumber = 16
            print('Every', timer, 'milliseconds, a goblin spawns') #testing print
            #cap out the bulletsadded variable at 22 to prevent too many new bullets from being added
            if bulletsadded >= 22:
                bulletsadded = 22
            else:
                bulletsadded += 5
            #keep decreasing the knife spawn interval at this USEREVENT until it hits every 1.8 seconds, to avoid too much difficulty
            if timer2 >= 1700:
                timer2 = int (timer2 - 250)
            elif timer2 < 1700:
                timer2 = 1700
            #set the new knife timer and update timer2
            pygame.time.set_timer(pygame.USEREVENT + 1, timer2)
            print ('Every', timer2, 'milliseconds, a knife will spawn') #testing print for checking the timer2
            #show that the difficulty change has happened and pause the program for 3 seconds
            surface.blit(DisplayLevel1, (width//2 - DisplayLevel1.get_width() // 2, height // 2 - DisplayLevel1.get_height() // 2))
            surface.blit(DisplayLevel2, (width//2 - DisplayLevel2.get_width() // 2, height // 2 - DisplayLevel2.get_height() // 2 + 35))
            surface.blit(DisplayLevel3, (width//2 - DisplayLevel3.get_width() // 2, height // 2 - DisplayLevel3.get_height() // 2 + 70))
            pygame.display.update()  # Update the display for the message to stay
            pygame.time.wait(3000)  # Wait for 3 seconds to allow the user to read
            totalbullets = font2.render(f'Total Bullets: {bulletnumber}', True, 'green') 
            
        #Constantly check to see if the character is dead, and then start the death animation userevent if so and increase the death animation cycler
        if event.type ==  pygame.USEREVENT + 5:
            if deathbyknife == True: 
                indexdeath += 1 #increase the death index

    #if the soldier image index cyclers reach past their index limit, reset them back to 0
    if indexsoldier >= 10 or indexidle >= 10:
        indexsoldier = 0
    #try to blit the following rectangles on the character and if there is a surface not found error, avoid it and end the program
    try:
        #always have a background red health bar on the soldier moving with him at all times
        pygame.draw.rect(surface, 'red', (width - 145, yposSOL - 20,100, 10)) 
        #if the soldier is not hit at all, he has a full green healthbar
        if hitsSOL == 0:
            pygame.draw.rect(surface, 'green', (width - 145, yposSOL - 20,100, 10))  
        #if the soldier is hit once, he has half a health bar
        if hitsSOL == 1:
            pygame.draw.rect(surface, 'green', (width - 145, yposSOL - 20,50, 10))
        #if the soldier is dead, he has no green health bar
        if hitsSOL == 2:
            pygame.draw.rect(surface, 'green', (width - 145, yposSOL - 20,0, 10))
    except: #if an error is found, just quit the game
        done = True
        pygame.quit()
        
    #initialize the soldier hitbox by using his same y-position and set x-position    
    soldier_rect = pygame.Rect(width - 130, yposSOL + 10,soldierdie[0].get_width() - 135, soldierdie[0].get_height() - 20)
    #pygame.draw.rect (surface,'black',soldier_rect) 
    
    #make sure the soldier doesnt go off the screen for y pos by making the soldier stay in place in that case
    if yposSOL <= 0:
        yposSOL = 0
    #if the soldier goes to the bottom of the screen, return him back to normal
    elif yposSOL + soldierrun[0].get_height() >= height:
        yposSOL = height - soldierrun[0].get_height()
    
    #blit the soldier walking if the soldier is moving and only if the variable is true, or make the soldier idle if not moving
    if deathbyknife == False:
        #if the soldier has shot, start his shooting animation with the indexshoot animation cycler
        if soldierhashot == True:
            surface.blit (soldiershoot[indexshoot], (width - 195, yposSOL - 8))
            indexshoot += 1 #increase the shoot animation every time he shoots
            #reset the animation cycler back to 0 if it goes above 10 and make the idle animation true again
            if indexshoot >= 10:
                indexshoot = 0
                soldierhashot = False  
                soldierisidle = True    
        #if the soldier is walking, blit those animations along with his walking animation cycler 
        elif soldierwalk == True:
            surface.blit (soldierrun[indexsoldier], (width - 195, yposSOL))
        #if the soldier is idle, blit those animations along with his idle animation cycler 
        elif soldierisidle == True:
            surface.blit (soldieridle[indexidle], (width - 195, yposSOL))
            #reset the idle animations cycler if it goes beyond 10
            indexidle += 1
            if indexidle > 9:
                indexidle = 0
    
    #if the bullet or goblin dissapears due to being shot or the bullet going off the screen, append the removed bullets to these two lists (to avoid some stupid error I cannot fix)
    bulletgone = []
    goblingone = []
    
    #cycle through each bullet's information in the total bullets list, and keep track of each bullet's index as well
    for index,bulletd in enumerate(bullets):
        #subtract an x-speed to the bullet's x axis variable
        bulletd[0] -= bulletd[2]
        #if the bullet's x-position reaches below 10 on the end of the screen, append it to the bulletgone list to get rid of it later
        if bulletd[0] < 10:
            bulletgone.append(index)
            #if the bullets run out, make this variable true, show a game over screen, and exit the game
            if len(bullets) <= 1 and bulletnumber < 1:
                if bulletdone == True:
                    pygame.mixer.Sound.play(sounds['die']) #play a death sound
                    messagebox.showinfo('Game Over Scrub', f'Game Over! No More Bullets! You got {totalgoblinkills} kills')
                    done = True
        #try to have a bullet hitbox, and account for an index or name error that happens when the game ends
        try:
            bullet_rect = pygame.Rect(bulletd[0],bulletd[1] + 77,bullet.get_width() ,bullet.get_height())
            #pygame.draw.rect(surface,'black', bullet_rect)
            surface.blit(bullet, (bulletd[0], bulletd[1] + 75)) #show the bullet travelling on the screen using each individual bullet's positions
        except (IndexError, NameError): #for any errors, just pass
            pass
        #cycle through the goblin list inside the bullet list to make collision detection quicker and smoother and keep track of the each goblin's index in the total list
        for index2, goblin in enumerate(goblins2):
            #if the goblin is running on the screen,
            if goblin[4] == 'running':
                #make a goblin hit box using the goblin's x and y positions
                goblin_rect = pygame.Rect(goblin[0] + 30,goblin[1] + 25 ,goblinrun[0].get_width() - 62 ,goblinrun[0].get_height() - 60)
                #pygame.draw.rect(surface, 'black', goblin_rect)
                #if the bullet in this current list collides with the goblin being tracked, add to the goblin hits variable to see if it has reached two hits or not
                if bullet_rect.colliderect(goblin_rect):
                    goblin[5] += 1
                    bulletgone.append(index) #get rid of the bullet in case of collision
                    #if the goblin has been hit two times, then delete the goblin and play his death animations
                    if goblin[5] >= 2:
                        #play the goblin death sound after death
                        pygame.mixer.Sound.play(sounds['gobdie'])
                        #the goblin is now dying, and add to the total goblin kills counter, and show this change on the screen using the TotalKills display variable
                        goblin[4] = 'dying'
                        totalgoblinkills += 1
                        TotalKills = font2.render(f'Kills: {totalgoblinkills}', True, 'green')
                        #blit the goblin death animations using the goblin death animation cycler in the goblin's list index
                        surface.blit(goblindie[goblin[6]], (goblin[0],goblin[1]))
                        #add to the goblin death animation cycler
                        goblin[6] += 1
                        #if the goblin death animation cycler is done cycling, remove the goblin from the goblins2 total goblin list
                        if goblin[6] > 6:
                           goblingone.append(index2)
                        #if the last bullet has been shot, let it travel before the game over message, and check for the bulletdone variable being true
                        if len(bullets) <= 1 and bulletnumber <3:
                            if bulletdone == True:
                                #display the messagebox and then quit the game
                                pygame.mixer.Sound.play(sounds['die']) #play a death sound
                                messagebox.showinfo('Game Over Scrub', f'Game Over! No More Bullets! You got {totalgoblinkills} kills')
                                done = True
                        break #break out of the loop to move on to the next bullet
                    break #break out of the loop to avoid it checking an already collided bullet
                
    #now sort through all the removed bullets, sort the list to prevent removing the wrong bullets, and account for a possible TypeError        
    for bulletno in sorted (bulletgone):
        try:
            del bullets[bulletno]
        except: #if there is an INDEXERROR or TYPEERROR, just pass the error and move on
            pass
    #now sort through all the removed goblins, sort the list to prevent removing the wrong goblins, and account for a possible ValueError
    for goblinno in sorted(goblingone):
        try:
            del goblins2 [goblinno]
        except: #if there is an INDEXERROR or TYPEERROR, just pass the error and move on
            pass
    
    
    #cycle through the goblin list total to individually move each goblin (the first goblin for loop is simply to check for collision and this one is for moving the goblin)
    for goblin in (goblins2):
        #if the goblin is running, then add on to the goblin's y-position and x-position with a speed to move them constantly
        if goblin[4] == 'running':
            goblin[0] += goblin[2]
            goblin[1] += goblin[3]
            #add on to the goblin walk animation cycler by 1 for each individual goblin to have separate, clean animations
            goblin[8] += 1
            #if the goblin index cycler goes beyong 6, reset the animation back to 0
            if goblin[8] > 6:
                goblin[8] = 0
            #if the goblin goes to the top of the screen or the bottom of the screen, simply reverse the y-speed to make the goblin go the other way (keep the x-speed the same)
            if goblin[1] < 30 or goblin[1] > height - goblinrun[0].get_height():
                goblin[3] = -goblin[3]
        #blit the goblin run animation using the goblin's [8] index animation cycler and its x and y positions on the screen
            surface.blit(goblinrun[goblin[8]], (goblin[0], goblin[1]))
            #make sure each goblin has a healthbar, always make it have a red health bar with it at all times to show health lost
            pygame.draw.rect(surface, 'red', (goblin[0] + 30, goblin[1] + 5,100, 10))
            #if the goblin has been hit two times, make the health bar that is green non-existant
            if goblin[5] == 2:
                pygame.draw.rect(surface,'green', (goblin[0] + 30, goblin[1] + 5, 0, 10))
            #if the goblin has only been hit once, make the health bar half green
            elif goblin[5] == 1:
                (pygame.draw.rect(surface,'green', (goblin[0] + 30, goblin[1] + 5, 50, 10)))
            #if the goblin has not been hit yet, make its healthbar fully green
            elif goblin[5] <= 0:
                pygame.draw.rect(surface,'green', (goblin[0] + 30, goblin[1] + 5, 100, 10))
            
            #if the goblin has reached the boardwalk, show a game over message and end the game
            if goblin[0] >=width - 180:
                #pygame.draw.rect(surface,'black',(0,0,width,height))
                pygame.mixer.Sound.play(sounds['die']) #play a death sound
                #show a gave over message box
                messagebox.showinfo('Game Over Scrub', f'Game Over! The goblins got to the base!\n You got {totalgoblinkills} kills')
                done = True #exit the main loop to end the game
    
    
    #go through each knife's details in the total knife list to move it on the screen and to check for collision
    for knife in knifelist:
        #add the knife's x-speed to the x-position every time to move the knife on the screen
        knife [0] = knife[0] + knife [2]
        #make a hit box for the knife using its position
        knife_rect = pygame.Rect(knife[0],knife[1] , throwingknife.get_width(), throwingknife.get_height())
        #pygame.draw.rect(surface, 'black', knife_rect)
        #blit the knife's image along with its moving x and y positions
        surface.blit(throwingknife, (knife[0],knife[1])) 
        #if the knife reaches the end of the screen, remove the knife from the knife list
        if knife[0] >= width:
            knifelist.remove(knife)
        #if the knife collides with the soldier add to the soldier hits variable and check to see if the soldier has been hit two times yet or not
        if knife_rect.colliderect(soldier_rect):
            knifelist.remove(knife)
            hitsSOL += 1 #add to the total soldier knife hits counter
            #if the soldier has been hit two times, kill the player, show a game over message box, and quit the game
            if hitsSOL >= 2:
                #play the death sound effect
                pygame.mixer.Sound.play(sounds['die'])
                deathbyknife = True #make death by knife true to start the game over sequence and death animations
                pygame.time.set_timer(pygame.USEREVENT + 5, 250) #start the death animation cycler userevent
                pygame.mixer.music.stop() #stop playing the arcade game music for this somber time in a brave soldier's life
                #make the soldier walk and idle booleans false to avoid the player still being able to shoot or move
                soldierwalk = False
                soldierisidle = False
                #break out of the program to avoid unncessary collision detection again
                break
    
    #for the more bullets powerup, cycle through each poowerup tuple to check for collision
    for powerup in powerlist:
        #move the powerup by adding a speed to the x position
        powerup [0] = powerup[0] + powerup [2]
        #create a hitbox for the bullets powerup that moves along with the bullet
        power_rect = pygame.Rect(powerup[0],powerup[1] , bulletspowerup.get_width(), bulletspowerup.get_height())
        #blit the bullet image itself as it moves along with the hitbox
        surface.blit(bulletspowerup, (powerup[0],powerup[1]))
        #if the powerup goes off the screen, delete it from a list
        if powerup[0] >= width:
            powerlist.remove(powerup)
        #if collision with the player is detected, remove the powerup and give the player 12 more bullets and display the total bullets on screen
        if power_rect.colliderect(soldier_rect):
            bulletdone = False
            powerlist.remove(powerup)
            bulletnumber += bulletsadded   
            totalbullets = font2.render(f'Total Bullets: {bulletnumber}', True, 'green') 
            
            
    #for the healing powerup, cycle throuhg each tuple in the list appended to move them and check for collision        
    for powerup2 in powerhealthlist:
        #move the powerup x position by a speed
        powerup2 [0] = powerup2[0] + powerup2 [2]
        #create the heal hitbox
        power2_rect = pygame.Rect(powerup2[0],powerup2[1] , bulletspowerup.get_width(), bulletspowerup.get_height())
        #blit the powerup, and its moving x position and also its constant y position
        surface.blit(healthpowerup, (powerup2[0],powerup2[1]))
        #if the powerup reaches the end of the screen, remove the powerup from the healin powerup list
        if powerup2[0] >= width:
            powerhealthlist.remove(powerup2)
        #if the powerup collides with the soldier hitbox, make the hitsSOL = 0, so basically make the healthbar full again and remove the powerup from the screen
        if power2_rect.colliderect(soldier_rect):
            hitsSOL = 0 
            powerhealthlist.remove(powerup2)   
    
    #if a knife kills you, blit the images of the death images
    if deathbyknife == True:
        surface.blit(soldierdie[indexdeath], (width - 195, yposSOL))

    #update the screen constantly and set the refresh rate delay
    pygame.display.update()
    # Cap the frame rate and 30fps
    pygame.time.Clock().tick(30)
    
    #if the death animation exceeds 9, then exit out of the 6th timer, show a game over messagebox, and quit the game
    if indexdeath >= 9:
        pygame.time.set_timer(pygame.USEREVENT + 5, 0)
        messagebox.showinfo('Game Over Scrub', f'Game Over! The goblins got you! You got {totalgoblinkills} kills')
        done = True
        pygame.quit()
 
