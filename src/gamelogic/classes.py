from enum import Enum 

class Suit(Enum):
    HEARTS = 0
    DIAMONDS = 1
    CLUBS = 2
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
    
card = Playing_Card(Suits.HEARTS, Color.RED, Pile.STOCK, Value.SEVEN, Visible.TRUE)

print(card.suit, card.color, card.pile, card.value, card.visible)


