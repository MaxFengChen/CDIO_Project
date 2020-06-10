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
# 
from testing import *
from classes import *
from SavingGames import *

def give_advice(game):
    foundAdvice = '0'
    funcCount = 0
    #Step 1 and 2:
    if foundAdvice == '0':
        foundAdvice = move_to_foundation_advice_and_do(game)
    #Step 3
    if foundAdvice == '0':
        funcCount = funcCount + 1
        foundAdvice = free_king_advice(game)
    #Step #4
    if foundAdvice == '0':
        funcCount = funcCount + 1
        foundAdvice = find_biggest_tableau_advise(game)
    #Step 5 is already imnplemented as program knows stock
    #Step 6 
    if foundAdvice == '0':
        funcCount = funcCount + 1
        foundAdvice = twin_is_found(game)
    #Step 7
    if foundAdvice == '0':
        funcCount = funcCount + 1
        foundAdvice = move_from_stock7(game)
    #Step 8
    if foundAdvice == '0':
        funcCount = funcCount + 1
        foundAdvice = stockpile_to_tableau(game)
    #Step 9
    if foundAdvice == '0':
        funcCount = funcCount + 1
        foundAdvice = move_to_foundation_advice_without_limit_and_do(game)
    if foundAdvice == '0':
        funcCount = funcCount + 1
    if funcCount == 7:
        print("No moves possible, game unsolvable.")
        saveFailedGames(game)

        return 0


#Step 1 and 2
def move_to_foundation_advice(game):
    #Give an advice what to do
    for pile in game.tableauPiles:
        if len(pile.cards) != 0:
            card = pile.frontCard
            if card.value.value <= game.lowestNeededCard.value:
                for foundPile in game.foundationPiles:
                    if card.suit == foundPile.suit and card.value == foundPile.nextCard:
                        print("Move the " + card.value.name + " " + card.suit.to_string() + " to the foundation pile")
                        return '1'
    return '0'                        
    
#Step 1 and 2 with testing
def move_to_foundation_advice_and_do(game):
    #Give an advice what to do
    for pile in game.tableauPiles:
        if len(pile.cards) != 0:
            card = pile.frontCard
            if card.value.value <= game.lowestNeededCard.value:
                for foundPile in game.foundationPiles:
                    if card.suit == foundPile.suit and card.value == foundPile.nextCard:
                        print("Function 1 og 2")
                        print("Move the " + card.value.name + " of " + card.suit.to_string()+ " to the foundation pile")
                        choice = input("If you wish to do so enter 1: ")
                        if choice == '1':
                           start_add_to_goal(card, pile, game)
                        return '1'


    if len(game.stock.cards) != 0:
        pile = game.stock
        for cards in game.stock.cards:
            if cards.value.value <= game.lowestNeededCard.value:
                for foundPiles in game.foundationPiles:
                    if cards.suit == foundPiles.suit and cards.value == foundPiles.nextCard:
                        print("Function 1 og 2")
                        print("Move the " + cards.value.name + " of " + cards.suit.to_string()+ " from stock pile to the foundation pile")
                        choice = input("If you wish to do so enter 1: ")
                        if choice == '1':
                           start_add_to_goal(cards, pile, game)
                        return '1'
    return '0'
    
#Step 3, is to move the king from the tableau pile with the most non-visible cards to an empty space.
def free_king_advice(game): 
    biggestLen = 0      # Measure of pile with the biggest amount of non visible cards.
    emptyPile = None    # The pile ready to have a king placed.
    targetCard = None   # The king
    targetPile = None   # The pile that the king is in.
    choice = None       # User choice
    for pile in game.tableauPiles: # Check if any tableau is empty by finding a pile with no frontcard.
        if pile.frontCard == None: 
            emptyPile = pile
        else:                       # If the pile is not empty, we can check if it has a king ready to be moved.  
            if pile.cards[0].visible == Visible.FALSE : # We are only interested in a king that is on top of non-visible cards
                for card in pile.cards:                 # Find the king
                    if card.visible == Visible.TRUE and card.value.value == 13:   
                        if len(pile.cards) > biggestLen : # If the king is found update the variables.
                            biggestLen = len(pile.cards) 
                            targetPile = pile
                            targetCard = card
    if targetPile != None and emptyPile != None: # If a king and an empty pile is found
        print("Function 3")                      # Instructions:
        print("Move the " + targetCard.value.name + " of " + targetCard.suit.to_string()+ " to the empty tableau pile nr. " + str(emptyPile.number))
        choice = input("If you wish to do so enter 1: ")
        if choice == '1': # Choose to execute.
            movePile = [] # Card array to the move function.
            for card in targetPile.cards: # Take all visible card, eligible to be moved.
                if card.visible == Visible.TRUE: 
                    movePile.append(card)
            start_add_to_tableau(movePile,targetPile,emptyPile) # The move between tableau piles function is given, the visible cards, the old pile, and the new pile. 
        return '1' 
    else:
        return '0'

#step 4
def find_biggest_tableau_advise(game):
    biggestPile = game.tableauPiles[0] 
    fromPile = game.tableauPiles[0]
    movePile = []  #Number of cards to move from the biggest pile
    bufferTest = []
    nonVisualCount = 0
    nVCPrevious = 0
    #for pile in tableauPiles:
    for searchBiggest in game.tableauPiles:
        if searchBiggest.frontCard != None:
            for pile in game.tableauPiles:
                if pile.frontCard != None:
                    bufferTest = []
                    if searchBiggest.frontCard.color != pile.frontCard.color and searchBiggest.frontCard.value.value - pile.frontCard.value.value == -1:
                        if biggestPile == None:
                            biggestPile = searchBiggest  # The pile with biggest amount of nonVisual cards
                            fromPile = searchBiggest  
                            nonVisualCount = 0
                        for cardsInPile in searchBiggest.cards:
                            if cardsInPile.visible == Visible.FALSE:
                                nonVisualCount = nonVisualCount+1   #Nonvisual cards in current pile
                        if len(biggestPile.cards) != 0:
                            for cards in biggestPile.cards:
                                if cards.visible == Visible.FALSE:  #Nonvisual cards in biggest pile
                                    nVCPrevious = nVCPrevious+1
                        if nonVisualCount >= nVCPrevious: #COmpare current pile with current biggest pile
                            biggestPile = searchBiggest  # The pile with biggest amount of nonVisual cards
                            fromPile = searchBiggest  
                            nonVisualCount = 0  
                    elif len(searchBiggest.cards) > 1:
                        for cardInPile in searchBiggest.cards:
                            if cardInPile.visible == Visible.TRUE:
                                bufferTest.append(cardInPile)
                        #if cardInPile != searchBiggest.frontCard:
                        if bufferTest[0].color != pile.frontCard.color and bufferTest[0].value.value - pile.frontCard.value.value == -1:    #Moves entire pile
                            biggestPile = searchBiggest
                            fromPile = searchBiggest
                            bufferTest = []

                           
    #print("Pile with most nonvisible cards: ", biggestPile.number)
    if biggestPile != None:
        for cards in biggestPile.cards: 
            if cards.visible == Visible.TRUE:   # if they are visible we can add them to the move pile
                movePile.append(cards)

    cardMoved = 0
    if len(movePile) == 0:
        print("No more cards to move in tableau\n")
        return '0' 
    else:
        for toPile in game.tableauPiles:
            if toPile.frontCard != None:
                if movePile[0].color != toPile.frontCard.color and movePile[0].value.value - toPile.frontCard.value.value == -1:
                    if cardMoved == 0:
                        print("Function 4")
                        print("Move the " + movePile[0].value.name + " of " + movePile[0].suit.to_string()+ " to " + toPile.frontCard.value.name + " of " + toPile.frontCard.suit.to_string())
                        choice = input("If you wish to do so enter 1: ")
                        if choice == '1':
                            start_add_to_tableau(movePile, fromPile, toPile)
                            cardMoved = 1
                        return '1'
            
    return '0'

#Step 5, is a step for the user. This step will give the application the knowledge of the entire stockpile, to give advise from.
def look_through_stockPile(stockPile):
    print("Please go through the stock pile, the program will learn the contents, and give best advice.")
    return

#Step 6, is to move a card from stockpile to tableau pile if the same value and color of the card is already in a tableau pile on a visible card
def twin_is_found(game):
    previousCard = None 
    for targetCard in game.stock.cards: # Need to check for every card in stock 
        for twinpile in game.tableauPiles: # And for each crad, each tableau pile.
            if twinpile.frontCard != None: # If the tableau pile is not empty
                previousCard = None
                for twincard in twinpile.cards: # For each card in the pile, we try to find a visible card of same color and value as target card.
                    if previousCard != None:    # Important is at the card must lie on top of a visible card.
                        if previousCard.visible == Visible.TRUE: 
                            previousCard = twincard 
                            if targetCard.value.value == twincard.value.value and targetCard.color == twincard.color and twincard.visible == Visible.TRUE:
                                for pile in game.tableauPiles: # When all requirements have been meet, we check all other tableau piles for a place for the targetCard
                                    if pile.frontCard != None and pile != twinpile:
                                        if pile.frontCard.value.value == targetCard.value.value + 1 and pile.frontCard.color != targetCard.color:
                                            print("Function 6") #Instructions
                                            print("Move the " + targetCard.value.name + " of " + targetCard.suit.to_string() + " to " + pile.frontCard.value.name + " of " + pile.frontCard.suit.to_string()) 
                                            game.stock.frontCard = targetCard # but the targetCard on top of stock
                                            stock_to_tableau(game, pile) #Move the card into tableau pile.
                                            return '1'
                    else:
                        previousCard = twincard
    return '0'
    
#step 7
def move_from_stock7(game):
    cards = []
    for i in game.tableauPiles: #Look through tableauPiles and see if they match with card in stock
        if i.frontCard != None:
            for h in reversed(i.cards): #Find the last visible card in the pile
                if h.visible == Visible.TRUE:
                    cards.append(h)
                    card = cards[-1]
            if len(game.stock.cards) != 0:
                for j in game.stock.cards:
                    if card.color != j.color and card.value.value - j.value.value == -1: #If they do check, check if the card from stock matches with a card from tableau
                        for tableau in game.tableauPiles:
                            if len(tableau.cards) != 0:
                                if j.color != tableau.frontCard.color and j.value.value - tableau.frontCard.value.value == -1:
                                    print("Function 7")
                                    print("Move the " + j.value.name + " of " + j.suit.to_string() + " to " + tableau.frontCard.value.name + " of " + tableau.frontCard.suit.to_string())

                                    choice = input("If you wish to do so enter 1: ")
                                    if choice == '1':
                                        game.stock.frontCard = j
                                        stock_to_tableau(game,tableau)
                                        return '1'
                            elif len(tableau.cards) == 0 and j.value.value == 13:
                                print("Function 7")
                                print("Move the " + j.value.name + " of " + j.suit.to_string() + "from stock to the empty tableau pile nr. " + str(tableau.number))
                                choice = input("If you wish to do so enter 1: ")
                                if choice == '1':
                                    game.stock.frontCard = j
                                    game.stock.cards.remove(game.stock.frontCard)
                                    if len(game.stock.cards) != 0:
                                        game.stock.frontCard = game.stock.cards[LAST_INDEX]
                                        game.stock.frontCard.visible = Visible.TRUE
                                    else:
                                        game.stock.frontCard = None
                                
                                    tableau.cards.append(j)
                                    tableau.frontCard = j
                                    return '1'

    return '0'


# step 8
def stockpile_to_tableau(game):
    for card in game.stock.cards:
        for tableauPile in game.tableauPiles:
            if tableauPile.frontCard != None:
            # If card matches
                if card.value.value - tableauPile.frontCard.value.value == -1 and tableauPile.frontCard.color !=  card.color: 
                    print("Function 8")
                    print("Move the " + card.value.name + " of " + card.suit.to_string()+ " to the tableau pile containing: " + tableauPile.frontCard.value.name + " of " + tableauPile.frontCard.suit.to_string())
                    choice = input("If you wish to do so enter 1: ")
                    if choice == '1':
                        game.stock.frontCard = card
                        stock_to_tableau(game, tableauPile) # Move to tableauPile
                    return '1'
    return '0'

# Step 9
def reshuffle_to_stockpile(game):
    # Only use when stockPile is empty
    print("reshuffle stockpile")
    # random.shuffle(game.wastePile.cards)
    # game.stock.cards = game.wastePile.cards.copy()
    # game.stock.frontCard = game.stock.cards[LAST_INDEX]
    # game.wastePile.cards.clear()
    # game.wastePile.frontCard = None

def move_to_foundation_advice_without_limit_and_do(game):
    #Give an advice what to do
    
    for pile in game.tableauPiles:
        if len(pile.cards) != 0:
            card = pile.frontCard
            for foundPile in game.foundationPiles:
                if card.suit == foundPile.suit and card.value == foundPile.nextCard:
                    print("Function 1 og 2")
                    print("Move the " + card.value.name + " of " + card.suit.to_string()+ " to the foundation pile")
                    choice = input("If you wish to do so enter 1: ")
                    if choice == '1':
                        start_add_to_goal(card, pile, game)
                    return '1'


    if len(game.stock.cards) != 0:
        pile = game.stock
        for cards in game.stock.cards:
            if cards.value.value <= game.lowestNeededCard.value:
                if cards.suit == game.foundPile.suit and cards.value == game.foundationPiles.nextCard:
                    print("Function 1 og 2")
                    print("Move the " + cards.value.name + " of " + cards.suit.to_string()+ " to the foundation pile")
                    choice = input("If you wish to do so enter 1: ")
                    if choice == '1':
                        start_add_to_goal(cards, pile, game)
                    return '1'
    return '0'