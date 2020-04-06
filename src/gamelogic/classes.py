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

NO_CARDS = 52
NO_SUITS = 4
NO_CARDS_PLATEAU = 28 # 1+2+3+4+5+6+7=28
LAST_INDEX = -1

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

class PlayingCard:
    def __init__(self, suit, color, pile, value, visible):
        self.suit = suit
        self.color = color
        self.pile = pile
        self.value = value
        self.visible = visible
    
    def to_string(self):
        if self.visible == Visible.TRUE:
            if self.value.value < 10:
                return str(0) + str(self.value.value) + "," + str(self.suit.name)
            else:
                return str(self.value.value) + "," + str(self.suit.name)
        else:
            return "####"

    def to_string_verbose(self):
        return str(self.suit.name) + " " + str(self.color.name) + " " + str(self.pile.name) + " " + str(self.value.value) + " " + str(self.visible.name)

class TableauPile:
    def __init__(self, number):
        self.cards = []
        self.frontCard = None
        self.number = number

class StockPile:
    def __init__(self):
        self.cards = []
        self.frontCard = None

class WastePile:
    def __init__(self):
        self.cards = []
        self.frontCard = None

class FoundationPile:
    def __init__(self, suit):
        self.cards = []
        self.frontCard = None
        self.nextCard = None
        self.suit = suit
        