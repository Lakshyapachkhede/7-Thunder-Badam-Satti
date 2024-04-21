import pygame
import random
import time
import sys
from buttons import Button


pygame.init()

FPS = 60
WIDTH, HEIGHT = 1366, 768


YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)


CARD_SIZE = (80, 120)
HOVER_CARD_SIZE = (120, 180)

FONT = pygame.font.Font(r"E:\projects\games\7-Thunder\assets\fonts\Boniro.ttf", 40)
# FONT.set_bold(True)

clock = pygame.time.Clock()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("7-Thunder")

background_img = pygame.image.load(r"E:\projects\games\7-Thunder\assets\img\back.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT)).convert_alpha()

arrow_img = pygame.image.load(r"E:\projects\games\7-Thunder\assets\img\arrow.png")
arrow_img = pygame.transform.scale(arrow_img, (30, 54)).convert_alpha()



groups = ["h", "s", "c", "d"]
cardList = []
for group in groups:
    for i in range(1, 14):
        cardList.append(group + str(i))

boardCardValueXcoordinateDict = {
    1:263,
    2:323,
    3:383,
    4:443,
    5:503,
    6:563,
    7:623,
    8:683,
    9:743,
    10:803,
    11:863,
    12:923,
    13:983,
}

boardCardGroupYcoordinateDict = {
    "c":200, 
    "d":300,
    "h":400,
    "s":500
}

boardCardDict = {
    "h": {"top":-1, "bottom":-1},
    "d": {"top":-1, "bottom":-1},
    "s": {"top":-1, "bottom":-1},
    "c": {"top":-1, "bottom":-1}
}

boardCardsList = []


class Card:
    def __init__(self, group, value, img, x, y):
        self.group = group
        self.value = value
        self.img = pygame.transform.scale(pygame.image.load(img), CARD_SIZE).convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.img, (self.rect.x, self.rect.y))

    def isMouseOver(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouseX, mouseY) and Player.canPlayCard(self):
            self.drawBorder(GREEN)
            return True
        elif self.rect.collidepoint(mouseX, mouseY):
            self.drawBorder(RED)
            return True
        return False
    
    def drawBorder(self, color):
        pygame.draw.rect(window, color, (self.rect.x - 3, self.rect.y - 3, self.img.get_width() + 6, self.img.get_height() + 6), 4)


    def rotateCard(self, angle):
        self.img = pygame.transform.rotate(self.img, angle)

    def toBoardCard(self):
        return BoardCard(self.group, self.value, self.img, boardCardValueXcoordinateDict[self.value], boardCardGroupYcoordinateDict[self.group])


class BoardCard(Card):
    def __init__(self, group, value, img, x, y):
        super().__init__(group, value, fr"E:\projects\games\7-Thunder\assets\img\Cards\{group}\{value}.png",  x, y)
        self.img = pygame.transform.rotate(self.img, 90)






class Player:
    """Player Class for game Players"""
    def __init__(self, cards, playerNumber,color, name):
        self.cards = sorted(cards, key=self.custom_sort)
        self.playerNumber = playerNumber
        self.objCards = []
        self.color = color
        self.name = name
        self.lastPlayedCard = None




    @staticmethod
    def custom_sort(card):
        # Define the order of card groups
        group_order = {'h': 2, 'c': 0, 's': 3, 'd': 1}
        # Extract the card group and value from the card string
        group = card[0]
        value = int(card[1:])
        # Sort first by card group, then by card value
        return (group_order[group], value)


    def initCards(self):
        y = 628
        x = 163
        for card in self.cards:
            group = card[0]
            value = int(card[1:])
            img = fr"E:\projects\games\7-Thunder\assets\img\Cards\{group}\{value}.png"
            card = Card(group, value, img, x, y)
            x+=80
            self.objCards.append(card)

    def drawCards(self):
        if self.lastPlayedCard:
            self.lastPlayedCard.drawBorder(self.color)
        prevCard = None
        for card in self.objCards:
            if self.playerNumber == 1 or self.playerNumber == 3:
                if prevCard != None:
                    if not ((prevCard.rect.x + 163) == card.rect.x):
                        card.rect.x = prevCard.rect.x + CARD_SIZE[0]
                else:
                    card.rect.x = 163 #for first card
            elif self.playerNumber == 2 or self.playerNumber == 4:
                if prevCard != None:
                    if not ((prevCard.rect.y + 40) == card.rect.y):
                        card.rect.y = prevCard.rect.y + 40
                else:
                    card.rect.y = 104 #for first card

            prevCard = card
            card.draw()


    def selectCard(self):
        passButton = Button(10, 20, 100, 50, RED, BLUE, YELLOW, YELLOW, "Pass")
        for card in self.objCards:

            if (card.isMouseOver() and pygame.mouse.get_pressed()[0]):
                card.drawBorder(GREEN)
                if self.playMove(card):
                    time.sleep(0.1)
                    return True
        passButton.activate_button(window)

        if (passButton.activate_button(window) == True) and self.canPass():
            time.sleep(0.1)
            return True
    
    def canPlayCard(self, card):
            if card.value == 7 and card.group == "h":
                return True
            
            if boardCardDict["h"]["top"] != - 1:
                if card.value == 7 and boardCardDict[card.group]["top"] == -1:
                    return True
                
                if (card.value == boardCardDict[card.group]["top"] + 1 ) or (card.value == boardCardDict[card.group]["bottom"]  - 1):
                    return True
    
            return False
    
    @staticmethod
    def canPlayCard(card):
            if card.value == 7 and card.group == "h":
                return True
            
            if boardCardDict["h"]["top"] != - 1:
                if card.value == 7 and boardCardDict[card.group]["top"] == -1:
                    return True
                
                if (card.value == boardCardDict[card.group]["top"] + 1 ) or (card.value == boardCardDict[card.group]["bottom"]  - 1):
                    return True
    
            return False
    

    def playMove(self, card):
        if boardCardDict[card.group]["top"] == -1:
            if card.value == 7 and card.group == "h":
                boardCardDict["h"]["top"] = 7
                boardCardDict["h"]["bottom"] = 7
                self.objCards.remove(card)
                boardCard = card.toBoardCard()
                self.lastPlayedCard = boardCard
                boardCardsList.append(boardCard)
                return True


            elif card.value == 7 and boardCardDict["h"]["top"] != -1:
                boardCardDict[card.group]["top"] = 7
                boardCardDict[card.group]["bottom"] = 7
                self.objCards.remove(card)
                boardCard = card.toBoardCard()
                self.lastPlayedCard = boardCard
                boardCardsList.append(boardCard)
                return True


        else:
            if boardCardDict[card.group]["top"] + 1 == card.value:
                boardCardDict[card.group]["top"]+=1
                self.objCards.remove(card)
                boardCard = card.toBoardCard()
                self.lastPlayedCard = boardCard
                boardCardsList.append(boardCard)
                return True


            elif boardCardDict[card.group]["bottom"] - 1 == card.value :
                boardCardDict[card.group]["bottom"]-=1
                self.objCards.remove(card)
                boardCard = card.toBoardCard()
                self.lastPlayedCard = boardCard
                boardCardsList.append(boardCard)
                return True
        time.sleep(0.1)    #time.sleep(0.1) for slowing selection of cards 
        
    def findStopCards(self):
        stopCardsList = []
        for group in groups:
            highest = None
            lowest = None

            for card in self.objCards:
                if card.group == group:
                    if highest is None or card.value > highest.value:
                        highest = card
                    if lowest is None or card.value < lowest.value:
                        lowest = card
    
            stopCardsList.append(highest)
            stopCardsList.append(lowest)
        return stopCardsList
    

    def checkWin(self):
        if len(self.objCards) == 0:
            return True
        
    def canPass(self):
        if self.haveCard("h", 7):
            return False
        if self.haveCard("s", 7) or self.haveCard("c", 7) or self.haveCard("d", 7) :
            return False

        for card in self.objCards:
                if (boardCardDict[card.group]["top"] != -1):
                    if ((boardCardDict[card.group]["top"] + 1) == card.value or (boardCardDict[card.group]["bottom"] - 1) == card.value):
                        return False
        return True      
    
    def haveCard(self, group, value):
        for card in self.objCards:
            if card.group == group and card.value == value:
                return True
        
        return False
        
class AiPlayer(Player):
    """Ai Player Class for game Players"""
    def __init__(self, cards, playerNumber, color, name):
        super().__init__(cards, playerNumber, color, name)
        if self.playerNumber == 2:
            self.fixCoordinate = 20
            self.incrementCoordinate = 104
            self.incrementvalue = 40
        elif self.playerNumber == 3:
            self.fixCoordinate = 20
            self.incrementCoordinate = 163
            self.incrementvalue = 80
        elif self.playerNumber == 4:
            self.fixCoordinate = 1226
            self.incrementCoordinate = 104
            self.incrementvalue = 40

            self.stopCards = []


    def initCards(self):
        for card in self.cards:
            group = card[0]
            value = int(card[1:])
            img = fr"E:\projects\games\7-Thunder\assets\img\rszCardBack.png" #change png to rszCardBack for hidden
            card = Card(group, value, img, self.fixCoordinate if self.playerNumber!=3 else self.incrementCoordinate,
                         self.fixCoordinate if self.playerNumber==3 else self.incrementCoordinate)
            if self.playerNumber != 3:
                card.rotateCard(-90)
            self.incrementCoordinate+=self.incrementvalue
            self.objCards.append(card)


    def selectCard(self):

        """
        Best Move Strategy:
        1. If canPass, then sleep for 3 seconds and return True.
        2. Check if there's a 7 of hearts and play it if found.
        3. Check for stop cards. If found, play the highest card greater than the highest stop card
           or play the lowest card smaller than the lowest stop card.
        4. If no stop cards are found, play the highest card not in the stop cards list.
        """
        thinking_time = random.uniform(1.0, 1.5)  # Random delay between 1 and 3 seconds
        time.sleep(thinking_time)
        if self.canPass():
            return True


        canPlayCards = []

        for card in self.objCards:
            if card.value == 7 and card.group == "h":
                self.playMove(card)

                return True
            
            if self.canPlayCard(card) and (card not in self.stopCards):
                canPlayCards.append(card)

        if len(canPlayCards) == 0:
            for card in self.stopCards:
                if self.canPlayCard(card):
                    canPlayCards.append(card)


        for card in canPlayCards:
            if card == None:
                canPlayCards.remove(card)


            

        # Play the middle card from the list of playable cards
        if len(canPlayCards) != 0:
            card_to_play = canPlayCards[len(canPlayCards) // 2]
            if self.playMove(card_to_play):
                canPlayCards.remove(card_to_play)
                if card_to_play in self.stopCards:
                    self.stopCards.remove(card_to_play)
                return True

        return False  # No valid move found


    
def renderText(msg, x, y, color):
    fontLabel = FONT.render(msg, 1, color)
    window.blit(fontLabel, (x, y))


def drawBoardCards():
    for card in boardCardsList:
        card.draw()

def shuffleCards():
    random.shuffle(cardList)

shuffleCards()

def checkFirstTurn():
    global arrow_img
    for number, player in enumerate(playerList):
        if player.haveCard("h", 7):
            arrow_img = pygame.transform.rotate(arrow_img, -90 * number)
            return number






def showTurn():
    if turn == 0:
        window.blit(arrow_img, (180, 550))
    elif turn == 1:
        window.blit(arrow_img, (160, 150))
    elif turn == 2:
        window.blit(arrow_img, (180, 160))
    elif turn == 3:
        window.blit(arrow_img, (1160, 150))


cards = [cardList[0:13], cardList[13:26], cardList[26:39], cardList[39:52]]

player1 = Player(cards[0], 1, RED, "RED")
player2 = AiPlayer(cards[1], 2, BLUE, "BLUE")
player3 = AiPlayer(cards[2], 3, GREEN, "GREEN")
player4 = AiPlayer(cards[3], 4, YELLOW, "YELLOW")

playerList = [player1, player2, player3, player4]

for player in playerList:
    player.initCards()
    player.stopCards = player.findStopCards()


def showName():
    for player in playerList:
        if player.playerNumber == 1:
            renderText(player.name, 220, 560, player.color)
        if player.playerNumber == 2:
            name = FONT.render(player.name, 1, player.color)
            name = pygame.transform.rotate(name, -90)
            window.blit(name, (160, 220))

        if player.playerNumber == 3:
            renderText(player.name, 220, 170, player.color)
        if player.playerNumber == 4:
            name = FONT.render(player.name, 1, player.color)
            name = pygame.transform.rotate(name, -90)
            window.blit(name, (1160, 190))


quitButton = Button(1250, 20, 100, 50, RED, BLUE, YELLOW, YELLOW, "Quit", pygame.quit)
turn = checkFirstTurn()

# def winScreen(player)


def main():
    global turn, arrow_img
    run = True
    while run:
        clock.tick(FPS)
        window.blit(background_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False



        drawBoardCards()
        for player in playerList:
            player.drawCards()
            if player.checkWin():
                # winScreen(player)
                pass
            
        if playerList[turn].selectCard():
            if turn == 3:
                turn = 0
                arrow_img = pygame.transform.rotate(arrow_img, -90)

            elif turn < 3:
                arrow_img = pygame.transform.rotate(arrow_img, -90)
                turn+=1


        showTurn()
        showName()

        # renderText("Hello", 200, 200, RED)
        quitButton.activate_button(window)


        pygame.display.flip()


if __name__ == '__main__':

    main()

    pygame.quit()
    sys.exit()