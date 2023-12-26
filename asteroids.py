
import sys
import math
import random
import pygame

# Local modules
from library import player, debries, highscore, bullets, rocks, ufo
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
    debris = debries.ManageDebris()
    asteroides = []
    stage = 1
    nextLvlDelay  = 30
    gameOverDelay = 120


    # Main loop
    while gameState != "exit":

        for event in pygame.event.get():
            print(player_.player_pieces)
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
                    SND_FIRE.play()
                if event.key == pygame.K_LSHIFT and player_.state == "alive":
                    player_.hyperspace = 30
                if event.key == pygame.K_y:
                    debris.create_debris(400, 300, 10)
        

        SCREEN.fill((0, 0, 0))
        player_.updatePlayer()

        # GFX           
        # Current score
        drawText(x=15,y=10,size=26, msg="Poeng: "+str(player_.score), color=WHITE, orient="none")
        
        # Current lives
        for x in range(player_.lives):
            player.Player((40+(x*20)),65).drawPlayer()


        # PLAYER LOGIC
        for fragmet in player_.player_pieces:
            fragmet.update_dead_player()
    

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


        ## UFO LOGIKK ##
        if ufo_.state == "dead":
            if ufo_.spawn_time == 0:
                if random.randrange(0,400) == 0:
                    ufo_.create_ufo(player_.score)
            else:
                ufo_.spawn_time -= 1
        else:
            # Ufo nøyaktighet og kuleretning
            acc = ufo_.small_ufo_acc * 4 / stage
            ufo_.bdir = math.degrees(math.atan2(-ufo_.y + player_.y, -ufo_.x + player_.x) + 
                                    math.radians(random.uniform(acc, -acc)))

            ufo_.update_ufo()
            ufo_.draw_ufo()
            
            # Sjekk UFOs kollisjon med spiller
            if player_.state != "dead":
                if collision(player_.x, player_.y, ufo_.x, ufo_.y, ufo_.size):
                    ufo_.state = "dead"

                    player_.score += ufo_.get_ufo_score()
                    
                    player_.player_pieces.append(player.DeadPlayer(player_.x, player_.y, 5 * player_.size / (2 * math.cos(math.atan(1 / 3)))))
                    player_.player_pieces.append(player.DeadPlayer(player_.x, player_.y, player_.size))
                    player_.player_pieces.append(player.DeadPlayer(player_.x, player_.y, player_.size / 2))
                    player_.state = "dead"
                    player_.invisible_dur  = 120
                    player_.spawn_dur = 30
                    player_.lives -= 1
                    player_.resetPlayer()
            

            # Sjekker om UFO kolliderer med astroider
            for a in asteroides:
                if collision(a.x, a.y, ufo_.x, ufo_.y, a.size):
                    ufo_.state = "dead"
                    if a.type == "large":
                        asteroides.append(rocks.Rocks(a.x,a.y, "medium"))
                        asteroides.append(rocks.Rocks(a.x,a.y, "medium"))
                    elif a.type == "medium":
                        asteroides.append(rocks.Rocks(a.x,a.y, "small"))
                        asteroides.append(rocks.Rocks(a.x,a.y, "small"))

                    asteroides.remove(a)

            
            # UFO kuler
            for b in ufo_.bullets:
                b.update_bullet()

                # Sjekker om kule treffer spiller
                if collision(player_.x, player_.y, b.x, b.y, player_.size):
                    ufo_.bullets.remove(b)
                    ufo_.state = "dead"

                    player_.player_pieces.append(player.DeadPlayer(player_.x, player_.y, 5 * player_.size / (2 * math.cos(math.atan(1 / 3)))))
                    player_.player_pieces.append(player.DeadPlayer(player_.x, player_.y, player_.size))
                    player_.player_pieces.append(player.DeadPlayer(player_.x, player_.y, player_.size / 2))
                    player_.state = "dead"
                    player_.invisible_dur  = 120
                    player_.spawn_dur = 30
                    player_.lives -= 1
                    player_.resetPlayer()
                    break

                # Sjekker om kuler treffer astroide
                for a in asteroides:
                    if collision(b.x, b.y, a.x, a.y, a.size):
                        asteroides.remove(a)
                        ufo_.bullets.remove(b)
                        if a.type == "large":
                            asteroides.append(rocks.Rocks(a.x,a.y, "medium"))
                            asteroides.append(rocks.Rocks(a.x,a.y, "medium"))
                        elif a.type == "medium":
                            asteroides.append(rocks.Rocks(a.x,a.y, "small"))
                            asteroides.append(rocks.Rocks(a.x,a.y, "small"))   
                        break                   
                        

                # Fjerner kule etter gitt tid    
                if b.life <= 0 and b in ufo_.bullets:
                    ufo_.bullets.remove(b)
                        

            # Sjekke spillers kuler mot UFO
            for b in player_.bullets:
                if collision(b.x, b.y, ufo_.x, ufo_.y, ufo_.size):
                    debris.create_debris(ufo_.x, ufo_.y, 10)
                    ufo_.state = "dead"
                    player_.score += ufo_.get_ufo_score()
                    


        ## ASTROIDE LOGIKK ##

        # Genererer Asteroider vekk fra senter
        if len(asteroides) == 0 and player_.state == "alive":
            if nextLvlDelay >= 0:
                nextLvlDelay -= 1
            else:
                dw = DISPLAY_WIDTH
                dh = DISPLAY_HEIGHT
                for x in range(stage+3):
                    xSpwn = dw / 2
                    ySpwn = dh / 2
                    while xSpwn - dw / 2 < dw / 4 and ySpwn - dh / 2 < dh /4:
                        xSpwn = random.randrange(0, dw)
                        ySpwn = random.randrange(0, dh)
                    asteroides.append(rocks.Rocks(xSpwn, ySpwn, "large"))
                nextLvlDelay = 30

        for a in asteroides:
            a.update_asteroide()
            if player_.state != "dead":
                if collision(player_.x, player_.y, a.x, a.y, a.size):
                    player_.player_pieces.append(player.DeadPlayer(player_.x, player_.y, 5 * player_.size / (2 * math.cos(math.atan(1 / 3)))))
                    player_.player_pieces.append(player.DeadPlayer(player_.x, player_.y, player_.size))
                    player_.player_pieces.append(player.DeadPlayer(player_.x, player_.y, player_.size / 2))

                    debris.create_debris(player_.x, player_.y, 10)
                    
                    # Spiller dør
                    player_.state = "dead"
                    player_.invisible_dur  = 120
                    player_.spawn_dur = 30
                    player_.lives -= 1
                    player_.resetPlayer()
 
                # Sjekker om spillers kuler treffer astroide
                for b in player_.bullets:
                    if collision(b.x, b.y, a.x, a.y, a.size):
                        player_.bullets.remove(b)
                        debris.create_debris(a.x, a.y, 10)
                        if a.type == "large":
                            player_.score += 20
                            asteroides.append(rocks.Rocks(a.x, a.y, "medium"))
                            asteroides.append(rocks.Rocks(a.x, a.y, "medium"))
                        elif a.type == "medium":
                            player_.score += 50
                            asteroides.append(rocks.Rocks(a.x, a.y, "small"))
                            asteroides.append(rocks.Rocks(a.x, a.y, "small"))
                        else:
                            player_.score += 100
                        asteroides.remove(a)
                        
        
        
        # Ekstra liv
        if player_.score > player_.extra_lives_multiplier * 10000:
            player_.lives += 1
            player_.extra_lives_multiplier += 1
        
        # Tegne spiller
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


        # Is game over
        if player_.lives <= 0:
            gameState = "gameOver"
            if gameOverDelay > 0:
                drawText(x=DISPLAY_WIDTH/3, y=200,size=50, msg="Game Over", color=WHITE, orient="none")
                gameOverDelay -= 1
                
            else:
                highScore.evaluateScore(player_.score)
                gameState = "exit"

        ### Arbiedi
        # Remove player pieces
        for pieces in player_.player_pieces:
            if pieces.pieces_dur <= 0:
                player_.player_pieces.remove(pieces)


        debris.update(SCREEN)
        pygame.display.flip()
        CLOCK.tick(30)

    mainMenu()



if __name__ == "__main__":    
    mainMenu()
    pygame.quit()
    sys.exit()