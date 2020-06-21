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
    newLowestNeededCard(game)
    #This is "main" for running the AI
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
    #elif foundAdvice == '1':
     #   choice = input("If you wish to do so enter 1: ")    #If the Use wants to do this  
      #  if choice == '1':   
       #     print("Testing for choice!")
    if funcCount == 7:
        print("No moves possible, game unsolvable.")
    #    saveFailedGames(game)

        return 0


#Step 1 and 2
def move_to_foundation_advice(game):                                        #move a card to the foundation pile
    #Give an advice what to do
    for pile in game.tableauPiles:                                          #Go through  the tableau piles 
        if len(pile.cards) != 0 or pile.frontCard != None:                                            # If the pile is not emty
            card = pile.frontCard                                            
            if card.value.value <= game.lowestNeededCard.value:             #If the frontcard is not larger than the lowes needed value    
                for foundPile in game.foundationPiles:                      # go through the foundation piles and see if theres a card that can be added to the foundation piles 
                    if card.suit == foundPile.suit and card.value == foundPile.nextCard:
                        print("Move the " + card.value.name + " " + card.suit.to_string() + " to the foundation pile")
                        return '1'
    if len(game.stock.cards) != 0:                                          # If theres cards in the stockpile 
        pile = game.stock                                               
        for cards in game.stock.cards:                                      # Go through all cards and see if any can be added to the foundations piles
            if cards.value.value <= game.lowestNeededCard.value:
                for foundPiles in game.foundationPiles:
                    if cards.suit == foundPiles.suit and cards.value == foundPiles.nextCard:
                        print("Function 1 og 2")
                        print("Move the " + cards.value.name + " of " + cards.suit.to_string()+ " from stock pile to the foundation pile")
                        return '1'
    return '0'                        
    
#Step 1 and 2 with testing
def move_to_foundation_advice_and_do(game):                                 #move a card to the foundation pile but do it in the game logic so comments in function above
    #Give an advice what to do
    for pile in game.tableauPiles:
        if len(pile.cards) != 0 and pile.frontCard != None:
            card = pile.frontCard
            if card.value.value <= game.lowestNeededCard.value:
                for foundPile in game.foundationPiles:
                    if card.suit == foundPile.suit and card.value == foundPile.nextCard:
                        print("Function 1 og 2")
                        print("Move the " + card.value.name + " of " + card.suit.to_string()+ " to the foundation pile")
                        #choice = input("If you wish to do so enter 1: ")    #If the Use wants to do this  
                        #if choice == '1':   
                        #   start_add_to_goal(card, pile, game)              #run this function
                        return '1'


    if len(game.stock.cards) != 0:
        pile = game.stock
        for cards in game.stock.cards:
            if cards.value.value <= game.lowestNeededCard.value:
                for foundPiles in game.foundationPiles:
                    if cards.suit == foundPiles.suit and cards.value == foundPiles.nextCard:
                        print("Function 1 og 2")
                        print("Move the " + cards.value.name + " of " + cards.suit.to_string()+ " from stock pile to the foundation pile")
                        #choice = input("If you wish to do so enter 1: ")    #If the Use wants to do this 
                        #if choice == '1':
                        #   start_add_to_goal(cards, pile, game)             #run this function
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
        #choice = input("If you wish to do so enter 1: ")
        #if choice == '1': # Choose to execute.
         #   movePile = [] # Card array to the move function.
          #  for card in targetPile.cards: # Take all visible card, eligible to be moved.
           #     if card.visible == Visible.TRUE: 
            #        movePile.append(card)
            #start_add_to_tableau(movePile,targetPile,emptyPile) # The move between tableau piles function is given, the visible cards, the old pile, and the new pile. 
        return '1' 
    else:
        return '0'

#step 4
def find_biggest_tableau_advise(game):  #Find moveable pile with most nonvisual cards
    bigestPile = game.tableauPiles[0]   #Variable that saves the pile with most nonevisual cards
    fromPile = game.tableauPiles[0]
    movePile = []  #Number of cards to move from the bigest pile
    bufferTest = [] #Buffer used to save all visible cards in the current pile

    nonVisualCount = 0
    nVCPrevious = 0

    for searchBiggest in game.tableauPiles: #Current pile
        if searchBiggest.frontCard != None:
            for pile in game.tableauPiles:  #All tableau piles
                if pile.frontCard != None:
                    bufferTest = []
                    if searchBiggest.frontCard.color != pile.frontCard.color and searchBiggest.frontCard.value.value - pile.frontCard.value.value == -1: #Compare tableau piles frontcard
                        for cardsInPile in searchBiggest.cards: #Cards in current pile
                            if cardsInPile.visible == Visible.FALSE:    
                                nonVisualCount = nonVisualCount+1   #Nonvisual cards in current pile
                        if len(bigestPile.cards) != 0:  
                            for cards in bigestPile.cards:      #Cards in current pile with most nonevisual cards
                                if cards.visible == Visible.FALSE:  #Nonvisual cards in biggest pile
                                    nVCPrevious = nVCPrevious+1
                        if nonVisualCount >= nVCPrevious: #COmpare current pile with current biggest pile
                            bigestPile = searchBiggest  # Update the pile with most nonvisual cards
                            fromPile = searchBiggest  
                            nonVisualCount = 0  
                
                    elif len(searchBiggest.cards) > 1:  #If there are more than 1 card in pile
                        for cardInPile in searchBiggest.cards:  
                            if cardInPile.visible == Visible.TRUE:
                                bufferTest.append(cardInPile)   #Buffer used to save all visual cards. Can't move nonvisual cards

                        if bufferTest[0].color != pile.frontCard.color and bufferTest[0].value.value - pile.frontCard.value.value == -1:    #If first cards in pile can be moved
                            bigestPile = searchBiggest
                            fromPile = searchBiggest
                            bufferTest = []

    for cards in bigestPile.cards: 
        if cards.visible == Visible.TRUE:   # if they are visible we can add them to the move pile
            movePile.append(cards)          #We only move cards that are visual

    cardMoved = 0
    if len(movePile) == 0:
        print("No more cards to move in tableau\n") #If there are no more cards to move in tableau
        return '0' 
    else:
        for toPile in game.tableauPiles:
            if toPile.frontCard != None:
                if movePile[0].color != toPile.frontCard.color and movePile[0].value.value - toPile.frontCard.value.value == -1:
                    if cardMoved == 0:
                        print("Function 4")
                        print("Move the " + movePile[0].value.name + " of " + movePile[0].suit.to_string()+ " to " + toPile.frontCard.value.name + " of " + toPile.frontCard.suit.to_string())
                        #choice = input("If you wish to do so enter 1: ")
                        #if choice == '1':
                         #   start_add_to_tableau(movePile, fromPile, toPile)    #Move tableau pile to other tableau pile
                          #  cardMoved = 1
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
                                            #game.stock.frontCard = targetCard # but the targetCard on top of stock
                                            #stock_to_tableau(game, pile) #Move the card into tableau pile.
                                            return '1'
                    else:
                        previousCard = twincard
    return '0'
    
#step 7
def move_from_stock7(game): #Move from stock to tableau if next move is number 4
    cards = []
    for i in game.tableauPiles: #Look through tableauPiles and see if they match with card in stock
        if i.frontCard != None:
            for h in reversed(i.cards): #Find the last visible card in the pile
                if h.visible == Visible.TRUE:
                    cards.append(h)
                    card = cards[-1]    #Last element - last visible card
            if len(game.stock.cards) != 0:
                for j in game.stock.cards:
                    if card.color != j.color and card.value.value - j.value.value == -1: #If they do match, check if the card from stock matches with a card from tableau
                        for tableau in game.tableauPiles:
                            if len(tableau.cards) != 0:
                                if j.color != tableau.frontCard.color and j.value.value - tableau.frontCard.value.value == -1:  #If it does move stock card to tableau
                                    print("Function 7")
                                    print("Move the " + j.value.name + " of " + j.suit.to_string() + " to " + tableau.frontCard.value.name + " of " + tableau.frontCard.suit.to_string())

                                    #choice = input("If you wish to do so enter 1: ")
                                    #if choice == '1':
                                        #game.stock.frontCard = j
                                        #stock_to_tableau(game,tableau)  #Remove from stock and add to tableau
                                    return '1'

                            elif len(tableau.cards) == 0 and j.value.value == 13:   #If there is an empty tableau pile, move out king from stock
                                print("Function 7")
                                print("Move the " + j.value.name + " of " + j.suit.to_string() + "from stock to the empty tableau pile nr. " + str(tableau.number))
                                #choice = input("If you wish to do so enter 1: ")
                                
                                #if choice == '1':
                                 #   game.stock.frontCard = j
                                  #  game.stock.cards.remove(game.stock.frontCard)   #Remove king from stock
                                   # if len(game.stock.cards) != 0:
                                    #    game.stock.frontCard = game.stock.cards[LAST_INDEX] #New frontcard
                                     #   game.stock.frontCard.visible = Visible.TRUE
                                
                                    #else:
                                     #   game.stock.frontCard = None
                                
                                    #tableau.cards.append(j) #Add king to tableau pile
                                    #tableau.frontCard = j   #King is the new frontcard
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
                    #choice = input("If you wish to do so enter 1: ")
                    #if choice == '1':
                    #    game.stock.frontCard = card
                    #    stock_to_tableau(game, tableauPile) # Move to tableauPile
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

def move_to_foundation_advice_without_limit_and_do(game):                           # Move any card that can to the foundation piles
    #Give an advice what to do                                               
    
    for pile in game.tableauPiles:                                                  # Go through  the tableau piles 
        if len(pile.cards) != 0:                                                    # If the pile is not empty
            card = pile.frontCard
            for foundPile in game.foundationPiles:                                  # go through the foundation piles and see if theres a card that can be added to the foundation piles 
                if card.suit == foundPile.suit and card.value == foundPile.nextCard:
                    print("Function 1 og 2")
                    print("Move the " + card.value.name + " of " + card.suit.to_string()+ " to the foundation pile")
                    #choice = input("If you wish to do so enter 1: ")
                    #if choice == '1':
                    #    start_add_to_goal(card, pile, game)
                    return '1'


    if len(game.stock.cards) != 0:                                                  # If theres cards in the stockpile 
        pile = game.stock                                                            
        for cards in game.stock.cards:
            for foundPile in game.foundationPiles: 
                if cards.suit == foundPile.suit and cards.value == foundPile.nextCard:
                    print("Function 1 og 2")
                    print("Move the " + cards.value.name + " of " + cards.suit.to_string()+ " to the foundation pile")
                    #choice = input("If you wish to do so enter 1: ")
                    #if choice == '1':
                    #    start_add_to_goal(cards, pile, game)
                    return '1'
    #return last_ditch_effort(game)

def last_ditch_effort(game):

    cardToBeMoved = None
    for tabPile in game.tableauPiles:               #Go through tableau piles to find an non visible card
        cardToBeMoved = find_first_visible_card(tabPile)
        if cardToBeMoved != 0:
            break             
    #print_table(game)
    suitArray = search_for_suit(game, cardToBeMoved)
    if suitArray == 0:
        cardToBeMoved = find_twin(game, cardToBeMoved)
        suitArray = search_for_suit(game, cardToBeMoved)
    moveThisCard = None
    counter = 0
    if ( suitArray!= 0):
        cardToBeMoved = suitArray[0]
        for card in suitArray[0].pile.cards:
            counter = counter + 1 
            if card.value.value == suitArray[0].value.value and  card.suit.value == suitArray[0].suit.value:
                moveThisCard = suitArray[0].pile.cards[counter]
                moveThisCard.pile = suitArray[0].pile
                break
        if check_moveability(game, moveThisCard, suitArray, counter) == '1':
            return '1'
    # Now we need to find a suit of the opposite color and do the same with 
    # We will use the found pile that is furthest along
    cardToBeMoved = moveThisCard
    counter = 0                     #Move the card after the former moveThisCard 
    for card in cardToBeMoved.pile.cards:
        counter = counter + 1 
        if card.value.value == cardToBeMoved.value.value and  card.suit.value == cardToBeMoved.suit.value:
            moveThisCard = suitArray[0].pile.cards[counter]
            moveThisCard.pile = suitArray[0].pile
            break
    if check_moveability(game, moveThisCard, suitArray, counter) == '1':
        return '1'
        
def find_twin(game, card):
    twin = card
    if card.color == Color.BLACK:
        if card.suit == Suit.C:
            twin.suit = Suit.S
        else:
            twin.suit = Suit.C
    else:
        if card.suit == Suit.H:
            twin.suit = Suit.D
        else:
            twin.suit = Suit.H
    for pile in game.tableauPiles:
        if len(pile.cards) != 0:
            for tabCard in pile.cards:
                if tabCard.value == twin.value and tabCard.color == twin.color and tabCard.suit == twin.suit:
                    tabCard.pile = pile
                    return tabCard




def check_moveability(game, moveThisCard, suitArray, counter):
    for tabPile in game.tableauPiles:
        if len(tabPile.cards) != 0:
            if tabPile.frontCard.color != moveThisCard.color and tabPile.frontCard.value.value == moveThisCard.value.value+1:
                #movePile = []
                #for card in suitArray[0].pile.cards[counter:len(suitArray[0].pile.cards)]:
                 #   movePile.append(card)
                print("Function 9")
                print("Move the " + moveThisCard.value.name + " of " + moveThisCard.suit.to_string()+ " to " + tabPile.frontCard.value.name + " of " + tabPile.frontCard.suit.to_string())
                #choice = input("If you wish to do so enter 1: ")
                #if choice == '1':
                 #   start_add_to_tableau(movePile, suitArray[0].pile, tabPile)    #Move tableau pile to other tableau pile
                return '1'

def find_first_visible_card(tabPile):
    if len(tabPile.cards) != 0:
        if tabPile.cards[0].visible == Visible.FALSE:
            for card in tabPile.cards:          # Find first visible card
                if card.visible.value == 1:
                    return card # This card should be moved                        break
        else:
            return 0
    else:
        return 0


def search_pile_for_card(card, pile):
    if len(pile.cards) != 0:
        for tabcard in pile.cards:
            if tabcard.visible == Visible.TRUE:
                if tabcard.value.value == card.value.value and tabcard.suit.value == card.suit.value:
                    tabcard.pile = pile
                    return tabcard
        return 0        
    else:
        return 0

def search_for_suit(game, card):
    suit = card.suit
    offset = len(game.foundationPiles[card.suit.value].cards)
    suitArray = []
    for cardNum in range (offset, card.value.value):                  #Find all cards untill the target card is found
        curCard = PlayingCard( suit, None, None, Value(cardNum+1), None)
        for tabPile in game.tableauPiles:
            suitCard = search_pile_for_card(curCard, tabPile)
            if suitCard != 0:
                suitArray.append(suitCard)
                break
        if cardNum-offset+1 != len(suitArray):
            return 0
    return suitArray
