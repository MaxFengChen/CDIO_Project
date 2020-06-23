#          .x+=:.                     ..    .         s                   .                        
#     z`    ^%              x .d88"    @88>      :8                  @88>                          
#        .   <k        u.    5888R     %8P      .88                  %8P      .u    .              
#      .@8Ned8"  ...ue888b   '888R      .      :888ooo       u        .     .d88B :@8c       .u    
#    .@^%8888"   888R Y888r   888R    .@88u  -*8888888    us888u.   .@88u  ="8888f8888r   ud8888.  
#   x88:  `)8b.  888R I888>   888R   ''888E`   8888    .@88 "8888" ''888E`   4888>'88"  :888'8888. 
#   8888N=*8888  888R I888>   888R     888E    8888    9888  9888    888E    4888> '    d888 '88%" 
#    %8"    R88  888R I888>   888R     888E    8888    9888  9888    888E    4888>      8888.+"    
#     @8Wou 9%  u8888cJ888    888R     888E   .8888Lu= 9888  9888    888E   .d888L .+   8888L      
#   .888888P`    "*888*P"    .888B .   888&   ^%888*   9888  9888    888&   ^"8888*"    '8888c. .+ 
#   `   ^"F        'Y"       ^*888%    R888"    'Y"    "888*""888"   R888"     "Y"       "88888%   
#                              "%       ""              ^Y"   ^Y'     ""                   "YP'    
#    
#   62410 CDIO-Projekt F20 - Solitaire solver
#   https://github.com/MaxTheScrub/CDIO_Project 
#
#   Group 7:                                    
#   Henrik Peter Warncke s184801                
#   Max Feng Chen Bjørnsen s184811              
#   Jeppe Møller Bak s164871                    
#   Adam Aron Edelsten s173057                  
#   Tobias Lauge Borgstrøm s184810              
#   Tobias Ladefoged Jensen s184815             
#   Markus Repnak Jacobsen s184808              
#   Ajs Ritsmer Stormholt s174517               
#
#   Naming convention: https://www.python.org/dev/peps/pep-0008/                       
#   Class names: PascalCase                         
#   Function names: snake_case                       
#   Variables: camelCase
#   Objects: camelCase                        
#   Constants: SCREAMING_SNAKE_CASE    

from enum import Enum 

NO_CARDS = 52 # Number of cards
NO_SUITS = 4 # Number of different card suits
NO_CARDS_PLATEAU = 28 # Number of cards in tablea piles from start
LAST_INDEX = -1       # Used in some cases to get last index
NUMBER_ARRAY = ("FIRST", "SECOND", "THIRD", "FOURTH", "FIFTH", "SIXTH", "SEVENTH") # Used to print advices
CARD_WIDTH = 280 # Width of piles in frames
CARD_HEIGHT = 350  # Height of piles in frames
WIDTH_OF_CARD = 140  # Width of cards in frames
HEIGHT_OF_CARD = 190 # Height of cards in frames
RESOLUTION_X = 1920 #Frame resolution
RESOLUTION_Y = 1080
STOCKPILE_THRESHOLD = 500 # Threshold used to see if stock pile is empty
KING_THRESHOLD = 50 # Threshold used to see if the king is on top of a non visual card
CONFIDENCE_THRESHOLD = 0.80 # Threshold of level of confidence the computer vision needs to have in the card. 

#Class of the different card suits
class Suit(Enum):
    # HEARTS = 0
    # CLUBS = 1
    # DIAMONDS = 2
    # SPADES = 3
    H = 0
    C = 1
    D = 2
    S = 3
    #Method to get color of suit
    def get_color(self):
        if self == Suit.H:
            return Color.RED
        if self == Suit.C:
            return Color.BLACK
        if self == Suit.D:
            return Color.RED
        if self == Suit.S:
            return Color.BLACK
    #Method to get the suit printed
    def to_string(self):
        if self == Suit.H:
            return "HEARTS"
        elif self == Suit.C:
            return "CLUBS"
        elif self == Suit.D:
            return "DIAMONDS"
        elif self == Suit.S:
            return "SPADES"

#Class for the different card colors
class Color(Enum):
    RED = 0
    BLACK = 1

#Class for the different types of piles of solitaire
class Pile(Enum):
    STOCK = 0
    TABLEAU = 1
    FOUNDATION= 2

# Class for the different card values
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

#Class for playing cards
class PlayingCard:
    def __init__(self, suit, color, pile, value, left, top):
        self.suit = suit
        self.color = color
        self.pile = pile
        self.value = value
        self.left = left # left coordinate in frame
        self.top = top # top coordinate in frame
        self.ID = self.to_string()
    
    # Method to print value and suit of card
    def to_string(self):
        if self.value.value < 10:
            return str(0) + str(self.value.value) + "," + str(self.suit.name)
        else:
            return str(self.value.value) + "," + str(self.suit.name)

    #Method to get the verbose of the playing card
    def to_string_verbose(self):
        return str(self.suit.name) + " " + str(self.color.name) + " " + str(self.pile.name) + " " + str(self.value.value)

#Class for tableau piles
class TableauPile:
    def __init__(self, number):
        self.cards = []
        self.frontCard = None
        self.number = number # which number tableau piles is it counting left to right

#Class for stock pile
class StockPile:
    def __init__(self):
        self.cards = []
        self.frontCard = None

# Class for foundation piles
class FoundationPile:
    def __init__(self, suit):
        self.cards = []
        self.frontCard = None
        self.nextCard = None
        self.suit = suit

#Class for the solitaire game
class Game:
    def __init__(self):
        self.playingCards = []
        self.tableauPiles = []
        self.foundationPiles = []
        self.stock = StockPile()
        self.lowestNeededCard = Value(2)
