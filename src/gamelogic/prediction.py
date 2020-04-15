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

def move_to_foundation_advice(tableauPiles, stock, foundationPiles, lowestNeededCard):
    #Give an advice what to do
    for pile in tableauPiles:
        if len(pile.cards) != 0:
            card = pile.frontCard
            if card.value.value <= lowestNeededCard.value:
                for foundPile in foundationPiles:
                    if card.suit == foundPile.suit and card.value == foundPile.nextCard:
                        print("Put the " + card.value.name + " " + card.suit.to_string() + " in the foundation pile")
                        

    #See if other cards can be put in the foundation piles
    

def move_to_foundation_advice_and_do(tableauPiles, stock, foundationPiles, lowestNeededCard):
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
    
    
def free_king_advice(tableauPiles):
    biggestLen = 0 
    targetCard = None
    for pile in tableauPiles:
        if pile.frontCard == None:
            emptyPile = pile
        elif pile.frontCard.value == 13 and len(pile.cards) > biggestLen :
            biggestLen = len(pile.cards) 
            targetCard = pile.frontCard.value
    if targetCard != None:
        print("Put the " + targetCard.name + " of " + targetCard.suit.to_string() + "on the empty tableau pile nr." + emptyPile.number.to_sting())
    return

def look_through_stockPile(stockPile):
    print("Please go through the stock pile, the program will learn the contents, and give best advice.")
    
    return


def twin_is_found(tableauPiles, stockPile):
    for targetCard in stockPile:
        for pile in tableauPiles:
            if targetCard.value == pile.frontCard.value and targetCard.color == pile.frontCard.color:
                for pile in tableauPiles:
                    if pile.frontCard.value == targetCard.value + 1 and pile.frontCard.color != targetCard.color:
                         print("Put the " + targetCard.name + " of " + targetCard.suit.to_string() + " on " + pile.frontCard.name + " of " + pile.frontCard.suit.to_string())
    
    return

def find_biggest_tableau_advise(tableauPiles):
    bigestPile = tableauPiles[0]
    fromPile = tableauPiles[0]
    movePile = []  #Number of cards to move from the bigest pile

    nonVisualCount = 0
    #for pile in tableauPiles:
    for searchBiggest in tableauPiles:
        for pile in tableauPiles:
            if len(pile.cards) != 0:
                if searchBiggest.frontCard.color != pile.frontCard.color and searchBiggest.frontCard.value.value - pile.frontCard.value.value == -1:
                    for cardsInPile in searchBiggest.cards:
                        if cardsInPile.visible == Visible.FALSE:
                            nonVisualCount = nonVisualCount+1
                    if nonVisualCount >= len(bigestPile.cards)-1: 
                        bigestPile = searchBiggest  # The pile with biggest amount of nonVisual cards
                        fromPile = searchBiggest  
                        nonVisualCount = 0  
                
                elif len(searchBiggest.cards) > 1:
                    for cardInPile in searchBiggest.cards:
                        if cardInPile.visible == Visible.TRUE:
                            if cardInPile != searchBiggest.frontCard:
                                if cardInPile.color != pile.frontCard.color and cardInPile.value.value - pile.frontCard.value.value == -1:
                                    bigestPile = searchBiggest
                                    #movePile.append(cardInPile)
                                    fromPile = searchBiggest

                           
    print("Pile with most nonvisible cards: ", bigestPile.number)

    for cards in bigestPile.cards: 
        if cards.visible == Visible.TRUE:   # if they are visible we can add them to the move pile
            #if topCard.value.value - cards.value.value == -1 and topCard.color != cards.color:
            movePile.append(cards)

    cardMoved = 0
    for toPile in tableauPiles:
        if len(movePile) == 0:
            print("No more cards to move")
        else:
            if movePile[0].color != toPile.frontCard.color and movePile[0].value.value - toPile.frontCard.value.value == -1:
                if cardMoved == 0:
                    print("Move " + movePile[0].to_string() + " to " + toPile.frontCard.to_string())
                    choice = input("If you want make this move, press: 1\n")
                    if choice == '1':
                        start_add_to_tableau(movePile, fromPile, toPile)
                        cardMoved = 1
            
    return 

# step 8
def wastepile_to_tableau(wastePile, tableauPiles):
    for tableauPile in tableauPiles:
        # If card matches
        if wastePile.frontCard.value.value - tableauPile.frontCard.value.value == -1 and tableauPile.frontCard.color !=  wastePile.frontCard.color: 
            print("Put the " + wastePile.frontCard.value.name + " of " + wastePile.frontCard.suit.to_string()+ " in the tableau pile containing: " + tableauPile.frontCard.value.name + " of " + tableauPile.frontCard.suit.to_string())
            choice = input("If you want make this move, press: 1\n")
            if choice == '1':
                tableauPile.cards.append(wastePile.frontCard) # Move to tableauPile
                wastePile.cards.pop(len(wastePile.cards) -1) # Remove from wastePile
                if len(wastePile.cards) == 0:
                    wastePile.frontCard = None
                else:
                    wastePile.frontCard = wastePile.cards[LAST_INDEX]

# Step 9
def reshuffle_to_stockpile(wastePile, stockPile):
    # Only use when stockPile is empty
    random.shuffle(wastePile.cards)
    stockPile.cards = wastePile.cards.copy()
    stockPile.frontCard = stockPile.cards[LAST_INDEX]
    wastePile.cards.clear()
    wastePile.frontCard = None