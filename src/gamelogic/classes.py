from enum import Enum 
import random

NOCARDS = 52
NOCARDS_PLATEAU = 28 # 1+2+3+4+5+6+7=28
cards = []

class Suit(Enum):
    HEARTS = 0
    CLUBS = 1
    DIAMONDS = 2
    SPADES = 3

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

class tableauPile:
    def __init__(self, number):
        self.Cards = []
        self.frontCard = None
        self.number = number

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

    # Make first 28 cards the playing cards in the plateau.
    tableau_piles = []
    card = 0
    for pile in range(1, 8):
        newPile = tableauPile(pile)
        for cardnr in range (1, pile+1):
            currentCard = cards[card]
            currentCard.pile = Pile.TABLEAU 
            print("pile", pile, "card", cardnr) 
            newPile.Cards.append(cards[card])
            card+=1
            print(newPile.Cards[-1].value, newPile.Cards[-1].suit)
        tableau_piles.append(newPile)
        print(len(tableau_piles))    
    print()

    # Make the first seven cards the visible plateau cards.

    for card in range(7):
        cards[card].visible = Visible.TRUE

    # Make the rest of the cards the playing cards in the stockpile.
    for card in range(NOCARDS_PLATEAU, NOCARDS):
        cards[card].pile = Pile.STOCK


def printCards():
    # Print the current state of the deck in the terminal.
    printCounter = 0
    for card in cards:
        print("Card number:", printCounter, card.suit, card.color, card.pile, card.value, card.visible)
        printCounter+=1

# Code runs here
setupTable()
printCards()
