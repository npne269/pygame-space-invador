import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))

# title
pygame.display.set_caption("Space Invador")
icon = pygame.image.load('images/ufo.png')
# background = pygame.image.load('images/background.jpg')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('images/ufo.png')
# playerImg = pygame.transform.scale(playerImg, (64, 64))
playerX = 370
playerY = 480
playerXchange = 0

# list of enemies

enemyImg = []
enemyX = []
enemyY = []
enemyXchange = []
enemyYchange = []
no_of_enemies = 6

# enemy
for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('images/enemy.png'))
    enemyX.append(random.randint(0, 760))
    enemyY.append(random.randint(50, 150))
    enemyXchange.append(1)
    enemyYchange.append(20)

# enemy
bulletImg = pygame.image.load('images/goli.png')
# playerImg = pygame.transform.scale(enemyImg, (64, 64))
bulletX = 370
bulletY = 480
bulletXchange = 0
bulletYchange = 2
bullet_state = "ready"

mybutton = pygame.Rect(340, 360, 150, 50)

# score
score = 0
font = pygame.font.Font('fonts/Nunito-Bold.ttf', 32)
game_over_font = pygame.font.Font('fonts/Nunito-Bold.ttf', 64)
textX = 10
textY = 10

GTextX = 250
GTextY = 250

pygame.mixer.load('music/back.mp3')
pygame.mixer.play(-1)


def game_over(x, y):
    gameovertext = game_over_font.render("Game Over", True, (255, 255, 255))
    show_score(x + 100, y + 65)
    screen.blit(gameovertext, (x, y))


def show_score(x, y):
    score_text = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (x, y))


# playerShow
def player(x, y):
    screen.blit(playerImg, (x, y))


def fireBullet(x, y):
    screen.blit(bulletImg, (x + 20, y + 10))


# playerShow
def enemy(x, y, k):
    screen.blit(enemyImg[k], (x, y))


def didCollide(bx, by, ex, ey):
    if (ex - 20) < bx < (ex + 20) and (ey - 20) < by < (ey + 20):
        return True
    else:
        return False


def restartGame():
    for j in range(no_of_enemies):
        enemyY[j] = random.randint(50, 150)
        global score
        score = 0


# Game Loop
running = True
while running:
    screen.fill((0, 255, 0))
    # screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXchange = -4
            if event.key == pygame.K_RIGHT:
                playerXchange = 4
            if event.key == pygame.K_UP:
                if bullet_state == "ready":
                    pygame.mixer.Sound('music/bullet.wav').play()
                    bulletX = playerX
                    bullet_state = "fire"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if mybutton.collidepoint(event.pos):
                    restartGame()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXchange = 0
            # if event.key == pygame.K_UP:
            #     bulletYchange = -40

    playerX += playerXchange

    if playerX < -20:
        playerX = -20
    elif playerX > 720:
        playerX = 720

    # enemy boundary
    for i in range(no_of_enemies):
        enemyX[i] += enemyXchange[i]
        if enemyX[i] > 760:
            enemyXchange[i] = -1
            enemyY[i] += enemyYchange[i]
        elif enemyX[i] < -20:
            enemyXchange[i] = 1
            enemyY[i] += enemyYchange[i]

        if enemyY[i] > 400:
            for j in range(no_of_enemies):
                enemyY[j] = 1000
            game_over(GTextX, GTextY)
            pygame.draw.rect(screen, (255, 255, 0), mybutton)
            screen.blit(font.render('Restart', True, (0, 255, 0)), (350, 365))
            break
        else:
            show_score(textX, textY)

        collide = didCollide(bulletX, bulletY, enemyX[i], enemyY[i])
        if collide:
            pygame.mixer.Sound('music/explode.wav').play()
            bulletY = 480
            bullet_state = "ready"
            enemyX[i] = random.randint(0, 760)
            enemyY[i] = random.randint(50, 150)
            score += 1

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletYchange

    player(playerX, playerY)
    pygame.draw.rect(screen, (255, 0, 0), (0, 440, 800, 1))
    pygame.display.update()
