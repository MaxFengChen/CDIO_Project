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

def give_advice(tableauPiles, stock, foundationPiles, lowestNeededCard, wastePile):
    foundAdvice = '0'
    #Step 1 and 2:
    foundAdvice = move_to_foundation_advice_and_do(tableauPiles, stock, foundationPiles, lowestNeededCard)
    #Step 3
    if foundAdvice == '0':
       foundAdvice = free_king_advice(tableauPiles)
    #Step #4
    if foundAdvice == '0':
        foundAdvice = find_biggest_tableau_advise(tableauPiles)
    #Step 5 is already imnplemented as program knows stock
    #Step 6 
    if foundAdvice == '0':
        foundAdvice = twin_is_found(tableauPiles, stock)
    #Step 7
    if foundAdvice == '0':
        foundAdvice = move_from_stock7(tableauPiles, stock)
    #Step 8
    if foundAdvice == '0':
        foundAdvice = stockpile_to_tableau(stock, tableauPiles)

#Step 1 and 2
def move_to_foundation_advice(tableauPiles, stock, foundationPiles, lowestNeededCard):
    #Give an advice what to do
    for pile in tableauPiles:
        if len(pile.cards) != 0:
            card = pile.frontCard
            if card.value.value <= lowestNeededCard.value:
                for foundPile in foundationPiles:
                    if card.suit == foundPile.suit and card.value == foundPile.nextCard:
                        print("Put the " + card.value.name + " " + card.suit.to_string() + " in the foundation pile")
                        return '1'
    return '0'                        
    
#Step 1 and 2 with testing
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
                        return '1'


    if len(stock.cards) != 0:
        for cards in stock.cards:
            if cards.value.value <= lowestNeededCard.value:
                for foundPiles in foundationPiles:
                    if cards.suit == foundPiles.suit and cards.value == foundPiles.nextCard:
                        print("Put the " + cards.value.name + " of " + cards.suit.to_string()+ " in the foundation pile")
                        print("Test funktion 1 og 2")
                        choice = input("If you wish to do so enter 1: ")
                        if choice == '1':
                           start_add_to_goal(cards, stock, foundPiles)
                        return '1'
    return '0'
    
#Step 3 
def free_king_advice(tableauPiles):
    biggestLen = 0 
    emptyPile = None
    targetCard = None
    targetPile = None
    choice = None
    for pile in tableauPiles:
        if pile.frontCard == None:
            emptyPile = pile
        else:
            for card in pile.cards:
                if card.visible == Visible.TRUE and card.value.value == 13: 
                    if len(pile.cards) > biggestLen :
                        biggestLen = len(pile.cards) 
                        targetPile = pile
                        targetCard = card
    if targetPile != None and emptyPile != None:
        print("Put the " + targetCard.to_string() + " on the empty tableau pile nr. " + str(emptyPile.number))
        choice = input("If you want make this move, press: 1 \n")
        if choice == '1':
            movePile = []
            for card in targetPile.cards:
                if card.visible == Visible.TRUE:
                    movePile.append(card)
            start_add_to_tableau(movePile,targetPile,emptyPile)
        return '1' 
    else:
        return '0'

#step 4
def find_biggest_tableau_advise(tableauPiles):
    bigestPile = tableauPiles[0]
    fromPile = tableauPiles[0]
    movePile = []  #Number of cards to move from the bigest pile

    nonVisualCount = 0
    #for pile in tableauPiles:
    for searchBiggest in tableauPiles:
        if searchBiggest.frontCard != None:
            for pile in tableauPiles:
                if pile.frontCard != None:
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

                           
    #print("Pile with most nonvisible cards: ", bigestPile.number)
    for cards in bigestPile.cards: 
        if cards.visible == Visible.TRUE:   # if they are visible we can add them to the move pile
            movePile.append(cards)

    cardMoved = 0
    if len(movePile) == 0:
        print("No more cards to move in tableau")
        return '0' 
    else:
        for toPile in tableauPiles:
            if toPile.frontCard != None:
                if movePile[0].color != toPile.frontCard.color and movePile[0].value.value - toPile.frontCard.value.value == -1:
                    if cardMoved == 0:
                        print("Move " + movePile[0].to_string() + " to " + toPile.frontCard.to_string())
                        print("Funktion 4")
                        choice = input("If you want make this move, press: 1\n")
                        if choice == '1':
                            start_add_to_tableau(movePile, fromPile, toPile)
                            cardMoved = 1
                        return '1'
            
    return '0'

#Step 5
def look_through_stockPile(stockPile):
    print("Please go through the stock pile, the program will learn the contents, and give best advice.")
    return

#Step 6
def twin_is_found(tableauPiles, stockPile):
    for targetCard in stockPile.cards:
        for pile in tableauPiles:
            if pile.frontCard != None:
                if targetCard.value.value == pile.frontCard.value.value and targetCard.color == pile.frontCard.color:
                    for pile in tableauPiles:
                        if pile.frontCard != None:
                            if pile.frontCard.value.value == targetCard.value.value + 1 and pile.frontCard.color != targetCard.color:
                                print("Funktion 6")
                                print("Put the " + targetCard.value.name + " of " + targetCard.suit.to_string() + " on " + pile.frontCard.value.name + " of " + pile.frontCard.suit.to_string()) 
                                stockPile.frontCard = targetCard
                                stock_to_tableau(stockPile, pile)
                                return '1'
    return '0'
    
#step 7
def move_from_stock7(tableauPile, stockPile):
    for i in tableauPile: #Look through tableauPiles and see if they match with card in stock
        for h in i.cards:
            if len(stock.cards) != 0 and h.visible == Visible.TRUE:
                for j in stockPile.cards:
                    if h.color != j.color and h.value.value - j.value.value == -1: #If they do check if the card from stock matches with a card from tableau
                        for tableau in tableauPile:
                            if len(tableau.cards) != 0:
                                #if cards.color != tableau.frontCard.color and cards.value.value - tableau.frontCard.value.value == -1:
                                if j.color != tableau.frontCard.color and j.value.value - tableau.frontCard.value.value == -1:
                                    print("Move " + j.to_string() + " to " + tableau.frontCard.to_string())
                                    print("Funktion 7")
                                    choice = input("Press 1 if you want to make this move\n")
                                    if choice == '1':
                                        stockPile.frontCard = j
                                        stock_to_tableau(stockPile,tableau)
                                    return '1'
    return '0'


# step 8
def stockpile_to_tableau(stockPile, tableauPiles):
    for card in stockPile.cards:
        for tableauPile in tableauPiles:
            if tableauPile.frontCard != None:
            # If card matches
                if card.value.value - tableauPile.frontCard.value.value == -1 and tableauPile.frontCard.color !=  card.color: 
                    print("Put the " + card.value.name + " of " + card.suit.to_string()+ " in the tableau pile containing: " + tableauPile.frontCard.value.name + " of " + tableauPile.frontCard.suit.to_string())
                    print("Funktion 8")
                    choice = input("If you want make this move, press: 1\n")
                    if choice == '1':
                        stock.frontCard = card
                        stock_to_tableau(stockPile, tableauPile) # Move to tableauPile
                    return '1'
    return '0'

# Step 9
def reshuffle_to_stockpile(wastePile, stockPile):
    # Only use when stockPile is empty
    random.shuffle(wastePile.cards)
    stockPile.cards = wastePile.cards.copy()
    stockPile.frontCard = stockPile.cards[LAST_INDEX]
    wastePile.cards.clear()
    wastePile.frontCard = None