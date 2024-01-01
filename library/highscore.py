import sys
import json
import pygame
import pygame_textinput

from library.utils import *

class HighScore():
    """
    A class representing the high score functionality of the game.
    """

    def __init__(self):
        """
        Initializes the HighScore object.

        Attributes:
        - filepath: The filepath of the high score JSON file.
        - highScore: A list containing the high scores.
        - sortedHighScore: A sorted version of the high scores.
        - pName: A list containing the player's initials.
        - highScoreLoaded: A boolean indicating whether the high scores were successfully loaded.
        """
        self.filepath = "library/highscore.json"
        self.highScore = []
        self.sortedHighScore = []
        self.pName = ["_", "_", "_"]
        self.data = []

        self.loadHighScore()
        
    def loadHighScore(self):
        """
        Loads the high scores from the JSON file.
        """
        try:
            with open(self.filepath, 'r') as file:
                self.data = json.load(file)
            self.highScoreLoaded = True
        except FileNotFoundError:
            self.highScoreLoaded = False
        
        self.highScore = self.data

        if self.highScoreLoaded:
            self.sortHighScore()

    def saveHighScore(self):
        """
        Saves the high scores to the JSON file.
        """
        with open(self.filepath, 'w') as file:
            json.dump(self.highScore, file, indent=4)
    
    def sortHighScore(self):
        """
        Sorts the high scores in descending order based on the score.
        """
        try:
            self.highScore = sorted(self.highScore, key=lambda x: list(x.values())[0], reverse=True)
        except IndexError:
            pass

    def getName(self):
        """
        Get's the player's initials for the high score entry.
        """
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

    def evaluateScore(self, pScore):
        """
        Evaluates if the player's score is a high score and updates the high score list accordingly.

        Parameters:
        - pScore: The player's score to be evaluated.
        """
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