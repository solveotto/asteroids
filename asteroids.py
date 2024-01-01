
import sys
import math
import random
import pygame

# Local modules
from library import debris, player, highscore, bullets, rocks, ufo
from library.utils import *

# Global variables
highScore = highscore.HighScore()
   
    
def mainMenu():
    mainMenuRunnig = True
    asteroides = []
    menuChoice = "none"

    while mainMenuRunnig:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                
                mainMenuRunnig = False

            if event.type == pygame.KEYDOWN:
                mainMenuRunnig = False
                asteroides = []
                menuChoice = "play"

        highScore.loadHighScore()

        SCREEN.fill(BLACK)
        drawText("Asteroides", DISPLAY_WIDTH/2, 100, 100, WHITE)
        drawText(f"Highscores", DISPLAY_WIDTH/2, 200, 34, WHITE)
        drawText(f"1 COIN 1 PLAY", DISPLAY_WIDTH/2, 550, 26, WHITE)  
        
        highScoreNumber = 1
        highScorePos = 10

        if highScore.highScoreLoaded:
            for item in highScore.highScore:
                for name, score in item.items():
                    drawText(f"{highScoreNumber}.", DISPLAY_WIDTH/2 - 120, 220+(highScorePos * highScoreNumber*2+10), 22, WHITE, orient="right")
                    drawText(f"{score}  {name}", DISPLAY_WIDTH/2 + 120, 220+(highScorePos * highScoreNumber*2+10), 22, WHITE, orient="right")
                    highScoreNumber += 1
        else:
            drawText(f"ERROR - NO DATA", DISPLAY_WIDTH/2, 320, 30, WHITE, orient="centered")
        
        # Astroide i bakgrunnen
        if len(asteroides) == 0:     
            for x in range(4):
                xSpwn = random.randint(0, int(DISPLAY_WIDTH/2))
                ySpwn = random.randint(0, int(DISPLAY_HEIGHT/2))
                asteroides.append(rocks.Rocks(xSpwn, ySpwn, "large"))
        for a in asteroides:
            a.update_asteroide()
        
        pygame.display.update()
        CLOCK.tick(30)
        
    if menuChoice == "play":
        gameloop("playing")


def gameloop(startingState):
    # Initial variables
    gameState = startingState
    player_ = player.Player(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2)
    ufo_ = ufo.Ufo()
    debris_ = debris.ManageDebris()
    rocks_ = rocks.ManageRocks()
    stage = 1
    nextLvlDelay  = 30
    gameOverDelay = 120

    # Main loop
    while gameState != "exit":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player_.thrust = True
                    
                if event.key == pygame.K_LEFT:
                    player_.rtspeed = -PLAYER_MAX_RTSPEED
                if event.key == pygame.K_RIGHT:
                    player_.rtspeed = PLAYER_MAX_RTSPEED
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player_.thrust = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player_.rtspeed = 0
                if event.key == pygame.K_SPACE and player_.state == "alive":
                    player_.bullets.append(bullets.Bullet(player_.x, player_.y, player_.dir))
                    SND_CHANNEL_FIRE.play(SND_FIRE)
                if event.key == pygame.K_LSHIFT and player_.state == "alive":
                    player_.hyperspace = 30

        SCREEN.fill((0, 0, 0))

        player_.updatePlayer()
        

        ## UFO LOGIKK ##
        if ufo_.state == "dead":
            if ufo_.spawn_time == 0:
                if random.randrange(0,30) == 0:
                    '''Ufo spawn rate'''
                    ufo_.create_ufo(player_.score)
            else:
                ufo_.spawn_time -= 1
        else:
            # Ufo nøyaktighet og kuleretning
            acc = ufo_.small_ufo_acc * 4 / stage
            ufo_.bdir = math.degrees(math.atan2(-ufo_.y + player_.y, -ufo_.x + player_.x) + 
                                    math.radians(random.uniform(acc, -acc)))
            
            if ufo_.type == "small":
                # Only play the sound if the channel is not busy
                if not SND_CHANNEL_UFO.get_busy():
                    SND_CHANNEL_UFO.play(SND_UFO_SMALL)
            else:
                # Only play the sound if the channel is not busy
                if not SND_CHANNEL_UFO.get_busy():
                    SND_CHANNEL_UFO.play(SND_UFO_LARGE)

            # Sjekk UFOs kollisjon med spiller
            if player_.state != "dead":
                if collision(player_.x, player_.y, ufo_.x, ufo_.y, ufo_.size):
                    ufo_.state = "dead"
                    player_.score += ufo_.get_ufo_score()
                    killPlayer(player_, debris_)

            # Sjekker om UFO kolliderer med astroider
            for a in rocks_.asteroids:
                if collision(a.x, a.y, ufo_.x, ufo_.y, a.size):
                    ufo_.state = "dead"
                    rocks_.split_asteroid(a)
                    rocks_.asteroids.remove(a)

            # UFO bullets
            for b in ufo_.bullets:
                b.update_bullet()

                # UFO bullets collision with player
                if collision(player_.x, player_.y, b.x, b.y, player_.size):
                    ufo_.bullets.remove(b)
                    ufo_.state = "dead"
                    killPlayer(player_, debris_)
                    break

                # UFO bullets collision with asteroids
                for a in rocks_.asteroids:
                    if collision(b.x, b.y, a.x, a.y, a.size):
                        rocks_.asteroids.remove(a)
                        ufo_.bullets.remove(b)
                        rocks_.split_asteroid(a)  
                        break                   
                        
                # Remove bullets afer a interval
                if b.life <= 0 and b in ufo_.bullets:
                    ufo_.bullets.remove(b)
                        
            # Player bullets collision with UFO
            for b in player_.bullets:
                if collision(b.x, b.y, ufo_.x, ufo_.y, ufo_.size):
                    debris_.create_debris(ufo_.x, ufo_.y, 10)
                    ufo_.state = "dead"
                    player_.score += ufo_.get_ufo_score()
            
            ufo_.update_ufo()
            ufo_.draw_ufo()    


        ## ASTROIDE LOGIC ##
        # Spawns Asteroids away from center of screen if none are present
        if len(rocks_.asteroids) == 0 and player_.state == "alive":
            if nextLvlDelay >= 0:
                nextLvlDelay -= 1
            else:
                rocks_.spawn_asteroids(stage, player_)

        for a in rocks_.asteroids:
            a.update_asteroide()
            if player_.state != "dead":
                if collision(player_.x, player_.y, a.x, a.y, a.size):
                    killPlayer(player_, debris_)
 
                # Player bullets collision with asteroids
                for b in player_.bullets:
                    if collision(b.x, b.y, a.x, a.y, a.size):
                        player_.bullets.remove(b)
                        debris_.create_debris(a.x, a.y, 10)
                        rocks_.split_asteroid(a)
                        if a.type == "large":
                            player_.score += 20
                        elif a.type == "medium":
                            player_.score += 50
                        else:
                            player_.score += 100
                        rocks_.asteroids.remove(a)

        # Displays current score
        drawText(x=15,y=10,size=26, msg="Poeng: "+str(player_.score), color=WHITE, orient="none")
        
        # Current lives
        for x in range(player_.lives):
            player.Player((40+(x*20)),65).drawPlayer()

        # Fragments
        for fragmet in player_.player_pieces:
            fragmet.update_dead_player()
            if fragmet.pieces_dur > 0:
                fragmet.pieces_dur -= 1
            else:
                player_.player_pieces.remove(fragmet)
                      
        # Bullets
        if len(player_.bullets) > 0:
            for bullet in player_.bullets:
                bullet.update_bullet()
                if bullet.life == 0:
                    player_.bullets.remove(bullet)

        # Check ivinsible and hyperspace state
        if player_.invisible_dur != 0:
            player_.invisible_dur -= 1
        elif player_.hyperspace == 0:
            player_.state = "alive"    
            
        # Hyperspace
        if player_.hyperspace != 0:
            player_.state = "dead"
            player_.hyperspace -= 1
            if player_.hyperspace == 1:
                player_.x = random.randrange(0, DISPLAY_WIDTH)
                player_.x = random.randrange(0, DISPLAY_HEIGHT)
    
        # Gives extra lives every 10 000 points
        if player_.score > player_.extra_lives_multiplier * 10000:
            player_.lives += 1
            player_.extra_lives_multiplier += 1
            SND_CHANNEL_OTHER.play(SND_EXTRA_SHIP)
    
        # Draws player
        if gameState != "gameOver":
            if player_.state == "dead":   
                if player_.hyperspace == 0:
                    if player_.spawn_dur == 0:
                        if player_.blink < 5:
                            if player_.blink == 0:
                                player_.blink = 10
                            else:
                                player_.drawPlayer()
                        player_.blink -= 1
                    else:
                        player_.spawn_dur -= 1
            else:
                
                player_.drawPlayer()
            
        # Updates debris if there are any
        debris_.update(SCREEN)

        # Is game over
        if player_.lives <= 0:
            gameState = "gameOver"
            if gameOverDelay > 0:
                drawText(x=DISPLAY_WIDTH/3, y=200,size=50, msg="Game Over", color=WHITE, orient="none")
                gameOverDelay -= 1
                
            else:
                highScore.evaluateScore(player_.score)
                gameState = "exit"

        pygame.display.flip()
        CLOCK.tick(30)

    mainMenu()


if __name__ == "__main__":    
    mainMenu()
    pygame.quit()
    sys.exit()