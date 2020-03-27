from enum import Enum 
import random

NOCARDS = 52
NOCARDS_PLATEAU = 28 # 1+2+3+4+5+6+7=28

cards = []
tableau_piles = []
foundations_piles = []

class Suit(Enum):
    # HEARTS = 0
    # CLUBS = 1
    # DIAMONDS = 2
    # SPADES = 3
    H = 0
    C = 1
    D = 2
    S = 3

class Color(Enum):
    RED = 0
    BLACK = 1

class Pile(Enum):
    STOCK = 0
    TABLEAU = 1
    FOUNDATION= 2
    WASTE = 3

class Value(Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    KNIGHT = 11
    QUEEN = 12
    KING = 13

class Visible(Enum):
    FALSE = 0
    TRUE = 1

class Playing_Card:
    def __init__(self, suit, color, pile, value, visible):
        self.suit = suit
        self.color = color
        self.pile = pile
        self.value = value
        self.visible = visible
    
    def getCardString(self):
        if self.visible == 1:
            if self.value.value < 10:
                return str(0) + str(self.value.value) + "," + str(self.suit.name)
            else:
                return str(self.value.value) + "," + str(self.suit.name)
        else:
            return "###" 

class tableauPile:
    def __init__(self, number):
        self.Cards = []
        self.frontCard = None
        self.number = number

class stockPile:
    def __init__(self):
        self.Cards = []
        self.frontCard = None

class foundationPile:
    def __init__(self, suit):
        self.Cards = []
        self.frontCard = None
        self.suit = suit

stock = stockPile()

def setupTable():
    # Setup a simple deck for testing
    colorSelect = 0

    # Generate a complete deck.
    for suitSelect in range(4):
        for valueSelect in range(1, 14):
            cards.append(Playing_Card(Suit(suitSelect), Color(colorSelect), Pile.STOCK, Value(valueSelect), Visible.FALSE))

        # Toggle the color.
        colorSelect+=1
        if colorSelect == 2:
            colorSelect = 0

    # Shuffle the deck.
    random.shuffle(cards)

    # Make first 28 cards the playing cards in the plateau and organize into piles.
    print("Each pile looks like:")
    card = 0
    for pile in range(1, 8):
        newPile = tableauPile(pile)
        for cardnr in range (1, pile+1):
            currentCard = cards[card]
            currentCard.pile = Pile.TABLEAU 
            print("pile", pile, "card", cardnr) 
            # Make the top card in the pile visible.
            if cardnr == pile:
                currentCard.visible = Visible.TRUE 
            newPile.Cards.append(cards[card])
            newPile.frontCard = cards[card]
            card+=1
            print(newPile.Cards[-1].value, newPile.Cards[-1].suit, newPile.Cards[-1].visible)
        tableau_piles.append(newPile)
        newPile.frontCard.visible = 1
        print("Size of the pile:", len(tableau_piles),"\n")
    # Make the rest of the cards the playing cards in the stockpile.
    #stock = stockPile()
    
    for card in range(NOCARDS_PLATEAU, NOCARDS):
        cards[card].pile = Pile.STOCK
        stock.Cards.append(cards[card])
        cards[card].visible = 1
        stock.frontCard =  cards[card]

    #Initialize the Foundation piles
    for suit in Suit:
        newFoundationPile = foundationPile(suit)
        foundations_piles.append(newFoundationPile)

def printCards():
    # Print the current state of the deck in the terminal.
    print("The entire deck looks like:")
    printCounter = 0
    for card in cards:
        print("Card number:", printCounter, card.suit, card.color, card.pile, card.value, card.visible)
        printCounter+=1

# Code runs here
def printTable():
    # Print first line with Stock pile and the Foundation piles
    print("The playing table looks like:\n")
    str = ""
    if stock.frontCard == None:
        str = "0,X     "
    else:
        str = stock.frontCard.getCardString() + "     "

    for i in range(len(foundations_piles)):
        if foundations_piles[i].frontCard == None:
            str = str + "0," + foundations_piles[i].suit.name + "  "
        else:
            str = str + foundations_piles[i].frontCard.getCardString() + " "
            
    print(str,"\n")
    str = ""

    # Print Tableau piles
    for j in range(len(tableau_piles)):
        for pile in tableau_piles:
            if len(pile.Cards) > j :
               str = str + pile.Cards[j].getCardString() + "  "
            else:
                str = str + "     "
        print(str,)
        str = ""
    print()
    
setupTable()
#printCards()
printTable()
