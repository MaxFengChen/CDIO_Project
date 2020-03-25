from enum import Enum 

class Suits(Enum):
    HEARTS = 1
    DIAMONDS = 2
    CLUBS = 3
    SPADES = 4

class Color(Enum):
    RED = 1
    BLACK = 2

class Pile(Enum):
    STOCK = 1
    TABLEAU = 2
    FOUNDATION= 3
    WASTE = 4

class Value(Enum):
    A = 1
    ONE = 1
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


