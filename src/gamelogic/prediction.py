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
    for pile in tableauPiles:
        if len(pile.cards) != 0:
            card = pile.frontCard
            if card.value.value <= lowestNeededCard.value:
                for foundPile in foundationPiles:
                    if card.suit == foundPile.suit and card.value == foundPile.nextCard:
                        print("Put the " + card.value.name + " " + card.suit.to_string() + " in the foundation pile")
                        

    #See if other cards can be put in the foundation piles
    

def give_advice_and_do(tableauPiles, stock, foundationPiles, lowestNeededCard):
    #Give an advice what to do
    for pile in tableauPiles:
        if len(pile.cards) != 0:
            card = pile.frontCard
            if card.value.value <= lowestNeededCard.value:
                for foundPile in foundationPiles:
                    if card.suit == foundPile.suit and card.value == foundPile.nextCard:
                        print("Put the " + card.value.name + " of " + card.suit.to_string()+ " in the foundation pile")
                        choice = input("If you wish to do so enter 1: ")
                        if choice == '1':
                           start_add_to_goal(card, pile, foundPile)
    return

def free_king_advice():
    biggest_len = 0 
    target_card = None
    for pile in tableauPiles:
        if pile.frontCard == None:
            emptyPile = pile
        elif pile.frontCard.value == 13 and len(pile.cards) > biggest_len :
            biggest_len = len(pile.cards) 
            target_card = pile.frontCard.value
    if target_card != None:
        print("Put the " + target_card.name + " of " + target_card.suit.to_string() + "on the empty tableau pile nr." + emptyPile.number.to_sting())
    return

def advise_tableau_to_tableau(tableauPiles, stock, foundationPiles, lowestNeededCard):
    bigestPile = tableauPiles[0]
    nonVisualCount = 0
    for pile in tableauPiles:
        if len(pile.cards) != 0:
            for cardsInPile in pile.cards:
                if cardsInPile.visible == Visible.FALSE:
                    nonVisualCount = nonVisualCount+1
            if nonVisualCount >= len(bigestPile.cards)-1: 
                bigestPile = pile
            nonVisualCount = 0

    for lfPile in tableauPiles:
        if bigestPile.frontCard.color != lfPile.frontCard.color:
            if bigestPile.frontCard.value.value - lfPile.frontCard.value.value == -1:
                print("Move " + bigestPile.frontCard.value.name + " of " + bigestPile.frontCard.to_string() + " to " + lfPile.frontCard.value.name + " of " + lfPile.frontCard.to_string())

                
    print("Biggest pile: ", bigestPile.number)
        #if len(pile.cards) != 0:
            #card = pile.frontCard
