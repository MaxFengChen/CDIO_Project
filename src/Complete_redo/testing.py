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

from classes import *
import random
from colorama import Fore, Back, Style
from playsound import playsound

def win_check(game):
    # Check if all cards are visible and thus you game can be won

    for foundation in game.foundationPiles:
        if foundation.frontCard != None:
            if foundation.frontCard.value.value == 13:
                print("")
                print("  / ____|                           | |     | | \ \   / /        ( )                               | | | | | | | | |\n" 
                + " | |      ___  _ __   __ _ _ __ __ _| |_ ___| |  \ \_/ /__  _   _|/__   _____  __      _____  _ __ | | | | | | | | |\n" 
                + " | |     / _ \| '_ \ / _` | '__/ _` | __/ __| |   \   / _ \| | | | \ \ / / _ \ \ \ /\ / / _ \| '_ \| | | | | | | | |\n" 
                + " | |____| (_) | | | | (_| | | | (_| | |_\__ \_|    | | (_) | |_| |  \ V /  __/  \ V  V / (_) | | | |_|_|_|_|_|_|_|_|\n" 
                + "  \_____|\___/|_| |_|\__, |_|  \__,_|\__|___(_)    |_|\___/ \__,_|   \_/ \___|   \_/\_/ \___/|_| |_(_|_|_|_|_|_|_|_)\n"
                + "                      __/ |                                                                                         \n"
                + "                     |___/                                                                                          ", end="\n")
                playsound('./fanfare.mp3') #https://www.youtube.com/watch?v=4PIjjmq5cqg
                exit()
            #return 0

def add_to_goal(card, goalPile, game):
    # Don't call this call start_add_to_goal(), but this adds the card to the foundation pile
    goalPile.frontCard = card
    if goalPile.nextCard == Value(13):
        goalPile.nextCard = Value(13)
    else:
        goalPile.nextCard = Value(goalPile.nextCard.value + 1)
    goalPile.cards.append(card)

def start_add_to_goal(card, foundPile, game):
    # The one to call, this checks if the move is legal
    if foundPile.nextCard == card.value and foundPile.suit == card.suit:
        add_to_goal(card, foundPile, game)
        newLowestNeededCard(game)

def newLowestNeededCard(game):
    #checks the foundation piles and will maybe set a new lowestNeededCard
    if (game.foundationPiles[0].frontCard != None) and (game.foundationPiles[1].frontCard != None) and (game.foundationPiles[2].frontCard != None) and (game.foundationPiles[3].frontCard != None):
        smallestVal = game.foundationPiles[0].frontCard.value.value
        for pile in game.foundationPiles:
            if pile.frontCard.value.value < smallestVal:
                smallestVal = pile.frontCard.value.value
    else:
        smallestVal = 0
    
    if smallestVal+2 > 13:
        game.lowestNeededCard = Value(13)
    else:
        game.lowestNeededCard = Value(smallestVal+2)

def create_card(cardValue, cardSuit, cardPile, cardColor, cardLeft, cardTop):
    # For adding certain cards in testing
    return PlayingCard(Suit(cardSuit), Color(cardColor), TableauPile(cardPile), Value(cardValue), cardLeft, cardTop)

def print_table(game):
    print(f"{Back.GREEN}") # Add a background color to the 
    # Print first line with Stock pile and the Foundation piles
    str = ""
    if game.stock.frontCard == None:
        str = "0,X     "
    else:
        # Add coloring to the stock pile
        if game.stock.frontCard.suit.get_color() == Color.BLACK:
            stringColor = f"{Fore.BLACK}"
        elif game.stock.frontCard.suit.get_color() == Color.RED:
            stringColor = f"{Fore.RED}"
        str = str + stringColor

        str = str + game.stock.frontCard.to_string() + "     "
    for i in range(len(game.foundationPiles)):
        # Add coloring to the foundation piles
        if game.foundationPiles[i].suit.get_color() == Color.BLACK:
            stringColor = f"{Fore.BLACK}"
        elif game.foundationPiles[i].suit.get_color() == Color.RED:
            stringColor = f"{Fore.RED}"
        str = str + stringColor

        if game.foundationPiles[i].frontCard == None:
            str = str + "00," + game.foundationPiles[i].suit.name + " "
        else:
            str = str + game.foundationPiles[i].frontCard.to_string() + " "
    
    print(str,"\n")
    str = ""

    # Print Tableau piles
    l = 0
    for pile in game.tableauPiles: 
        if len(pile.cards) > l:
            l = len(pile.cards) 
    for j in range(l):
        for pile in game.tableauPiles:
            if len(pile.cards)> l :
                l = len(pile.cards)
            if len(pile.cards) > j:
                # Add coloring to the plateau cards
                if pile.cards[j].suit.get_color() == Color.BLACK:
                    stringColor = f"{Fore.BLACK}"
                elif pile.cards[j].suit.get_color() == Color.RED:
                    stringColor = f"{Fore.RED}"
                else:
                    stringColor = f"{Fore.LIGHTWHITE_EX}"
                str = str + stringColor
                str = str + pile.cards[j].to_string() + " "
            else:
                str = str + "     "
        print(str)
        str = ""
    # Remove all coloring
    print(f"{Style.RESET_ALL}")
