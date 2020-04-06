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
from testing import *
from classes import *

def give_advice(tableauPiles, stock, foundationPiles, lowestNeededCard):
    #Give an advice what to do
    #See if there's any Aces that can be added to the foundations
    if stock.frontCard.value is Value(1):
        print("Put the ace in the foundation pile")
        return
    for pile in tableauPiles:
        if len(pile.cards) != 0:
            card = pile.frontCard 
            if card.value is Value(1):
                print("Put the ace of " + card.suit + "in the foundation pile")
                return
            if card.value < lowestNeededCard.value:
                for foundPile in foundationPiles:
                    if card.suit is foundPile.suit and card is foundPile.nextCard:
                        print("Put the " + card.value +  " of " + card.suit + "in the foundation pile")
        

    #See if other cards can be put in the foundation piles
    
    
    

def give_advice_and_do(tableauPiles, stock, foundationPiles, lowestNeededCard):
    #Give an advice what to do
    #See if there's any Aces that can be added to the foundations
    if stock.frontCard.value is Value(1):
        print("Put the ace in the foundation pile")
        return
    for pile in tableauPiles:
        if len(pile.cards) != 0:
            card = pile.frontCard
            if card.value is Value(1):
                print("Put the ace in the foundation pile.")
                choice = input("If you wish to do so enter 1.")
                if choice is '1':
                    start_add_to_goal(card, pile,foundationPiles)
                return
            if card.value.value <= lowestNeededCard.value:
                for foundPile in foundationPiles:
                    print(card.suit, card.value, foundPile.suit, foundPile.nextCard.value)
                    if card.suit is foundPile.suit and card.value is foundPile.nextCard:
                        print("Put the " + card.value.name +  " of " + card.suit.name + "in the foundation pile")
                        choice = input("If you wish to do so enter 1.")
                        if choice is '1':
                            start_add_to_goal(card, pile, foundPile)
    
    
