import json
import pygame


from library.utils import *


class HighScore():
    def __init__(self):
        self.filepath = "library/highscore.json"
        self.highScore = []
        self.sortedHighScore = []
        self.pName = ["_", "_", "_"]

        try:
            self.loadHighScore()
            self.highScoreLoaded = True
        except FileNotFoundError:
            self.highScoreLoaded = False
        
        if self.highScoreLoaded:
            self.sortHighScore()
        
    def loadHighScore(self):
        with open(self.filepath, 'r') as file:
            data = json.load(file)
        self.highScore = data

    def saveHighScore(self):
        with open(self.filepath, 'w') as file:
            json.dump(self.highScore, file, indent=4)
    
    def sortHighScore(self):
        try:
            self.highScore = sorted(self.highScore, key=lambda x: list(x.values())[0], reverse=True)
        except IndexError:
            pass

    def getName(self):
        manager = pygame_textinput.TextInputManager(validator=lambda input: len(input) <= 3)
        textInput = pygame_textinput.TextInputVisualizer(manager=manager)

        # Highscore loop
        running = True
        while running:
            SCREEN.fill(BLACK)
            drawText("POENGSUMMEN DIN ER EN AV DE TI BESTE.", DISPLAY_WIDTH/10, 60, 30, WHITE, orient="left")
            drawText("SKRIV SKRIV INN TRE INITIALER.", DISPLAY_WIDTH/10, 90, 30, WHITE, orient="left")
            drawText("TRYKK ENTER NÅR DU ER FERIDG.", DISPLAY_WIDTH/10, 120, 30, WHITE, orient="left")
            drawText(self.pName[0], DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2, 30, WHITE)
            drawText(self.pName[1], DISPLAY_WIDTH/2+20, DISPLAY_HEIGHT/2, 30, WHITE)
            drawText(self.pName[2], DISPLAY_WIDTH/2+40, DISPLAY_HEIGHT/2, 30, WHITE)
            
            events = pygame.event.get() 
            textInput.update(events)

            if len(textInput.value) == 1:
                self.pName = [textInput.value[0], "_", "_"]
            elif len(textInput.value) == 2:
                self.pName = [textInput.value[0], textInput.value[1], "_"]
            elif len(textInput.value) == 3:
                self.pName = [textInput.value[0], textInput.value[1], textInput.value[2]]
            else:
                self.pName = ["_", "_", "_"]

            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False
                        break

            pygame.display.update()
        if self.pName == ["_", "_", "_"]:
            self.pName = [" "," "," "]


    # Sjekker om poengsummen er en highscore
    def evaluateScore(self, pScore):
        break_flag = False

        if len(self.highScore) > 0:
            for hs in self.highScore:
                if break_flag:
                    break
                for key, value in hs.items():
                    if pScore > value:
                        self.getName()
                        self.highScore.insert(self.highScore.index(hs), {''.join(self.pName):pScore})
                        break_flag = True
                        break
                    elif len(self.highScore) < 10:
                        self.getName()
                        self.highScore.append({''.join(self.pName):pScore})
                        break_flag = True
                        break
            if len(self.highScore) >= 11:
                self.highScore.pop()
        else:
            self.getName()
            self.highScore.append({''.join(self.pName):pScore})
                          
        self.sortHighScore()
        self.saveHighScore()