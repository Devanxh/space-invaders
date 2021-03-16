import pygame
import math
import random

#initialise the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800,600))

#background
bgImg = pygame.image.load('bg.jpg')

#title and icon
pygame.display.set_caption("Space Invasion")
icon = pygame.image.load('ship.bmp')
pygame.display.set_icon(icon)


#player
playerImg = pygame.image.load('ufo.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
	enemyImg.append(pygame.image.load('alien.png'))
	enemyX.append(random.randint(0,735))
	enemyY.append(random.randint(50,150))
	enemyX_change.append(0.3)
	enemyY_change.append(50)

#BULLET
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.5
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX =10
textY =10

#game over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def bg(x,y):
	screen.blit(bgImg, (x,y))

def game_over_text(x, y):
	over_text = over_font.render("GAME OVER" ,True, (255,255,255))
	screen.blit(over_text, (200, 300))
	
	
def show_score(x, y):
	score = font.render("Score :" + str(score_value),True, (255,255,255))
	screen.blit(score, (x,y))

def player(x, y):
	#blit draws the image
	screen.blit(playerImg,(x, y))

def enemy(x, y, i):
	screen.blit(enemyImg[i], (x, y))
	
def fire_bullet(x,y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bulletImg, (x+4, y+10))
	
def isCollision(enemyX,enemyY,bulletX,bulletY):
	distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
	if distance <27:
		return True
	else:
		return False
		
#game loop
running = True
while running:	
	
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change = -0.3
			if event.key == pygame.K_RIGHT:
				playerX_change = 0.3
			if event.key == pygame.K_UP:
				playerY_change = -0.2
			if event.key == pygame.K_DOWN:
				playerY_change = 0.2
			
			if event.key == pygame.K_RSHIFT:
				if bullet_state == "ready":
					bulletX = playerX
					bulletY = playerY
					fire_bullet(playerX, bulletY)
			
				
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change = 0
			if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				playerY_change = 0	

	screen.fill((0,0,0))
	bg(0,0)
	
	playerX += playerX_change
	playerY += playerY_change
	#boundaries
	if playerX <= 0:
		playerX = 0
	if playerX >= 768:
		playerX = 768
	
	#enemy movement
	for i in range(num_of_enemies):
		
		#game over
		if enemyY[i] > 400:
			for j in range(num_of_enemies):
				enemyY[j] = 2000
			game_over_text(200, 300)
			break

		
		enemyX[i] += enemyX_change[i]
		
		if enemyX[i] <= 0:
			enemyX_change[i] = 0.3
			enemyY[i] += enemyY_change[i]
		if enemyX[i] >= 736:
			enemyX_change[i] = -0.3
			enemyY[i] += enemyY_change[i]
			
		#collision
		collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
		if collision:
			bulletY = 480
			bullet_state = "ready"
			score_value += 1
			enemyX[i] = random.randint(0,735)
			enemyY[i] = random.randint(50,150)	
	
		enemy(enemyX[i], enemyY[i], i)

		collision2 = isCollision(enemyX[i], enemyY[i],playerX,playerY)
		if collision2:
			for i in range(num_of_enemies):
				enemyY[i] = 2000
			game_over_text(200, 300)
			break
			
	#bullet movt
	if bulletY <= 0:
		bulletY = playerY
		bullet_state = "ready"
	if bullet_state == "fire":
		fire_bullet(bulletX,bulletY)
		bulletY -= bulletY_change
		
	
	
	player(playerX, playerY)
	show_score(textX,textY)
	pygame.display.update()
