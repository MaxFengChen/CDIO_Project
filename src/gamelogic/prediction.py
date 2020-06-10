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
    
#Step 3 
def free_king_advice(game):
    biggestLen = 0 
    emptyPile = None
    targetCard = None
    targetPile = None
    choice = None
    for pile in game.tableauPiles:
        if pile.frontCard == None:
            emptyPile = pile
        else:
            if pile.cards[0].visible == Visible.FALSE :
                for card in pile.cards:
                    if card.visible == Visible.TRUE and card.value.value == 13:   
                        if len(pile.cards) > biggestLen :
                            biggestLen = len(pile.cards) 
                            targetPile = pile
                            targetCard = card
    if targetPile != None and emptyPile != None:
        print("Function 3")
        print("Move the " + targetCard.value.name + " of " + targetCard.suit.to_string()+ " to the empty tableau pile nr. " + str(emptyPile.number))
        choice = input("If you wish to do so enter 1: ")
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
                        choice = input("If you wish to do so enter 1: ")
                        if choice == '1':
                            start_add_to_tableau(movePile, fromPile, toPile)    #Move tableau pile to other tableau pile
                            cardMoved = 1
                        return '1'
            
    return '0'

#Step 5
def look_through_stockPile(stockPile):
    print("Please go through the stock pile, the program will learn the contents, and give best advice.")
    return

#Step 6
def twin_is_found(game):
    for targetCard in game.stock.cards:
        for pile in game.tableauPiles:
            if pile.frontCard != None:
                if targetCard.value.value == pile.frontCard.value.value and targetCard.color == pile.frontCard.color:
                    for pile in game.tableauPiles:
                        if pile.frontCard != None:
                            if pile.frontCard.value.value == targetCard.value.value + 1 and pile.frontCard.color != targetCard.color:
                                print("Function 6")
                                print("Move the " + targetCard.value.name + " of " + targetCard.suit.to_string() + " to " + pile.frontCard.value.name + " of " + pile.frontCard.suit.to_string()) 
                                game.stock.frontCard = targetCard
                                stock_to_tableau(game, pile)
                                return '1'
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

                                    choice = input("If you wish to do so enter 1: ")
                                    if choice == '1':
                                        game.stock.frontCard = j
                                        stock_to_tableau(game,tableau)  #Remove from stock and add to tableau
                                        return '1'

                            elif len(tableau.cards) == 0 and j.value.value == 13:   #If there is an empty tableau pile, move out king from stock
                                print("Function 7")
                                print("Move the " + j.value.name + " of " + j.suit.to_string() + "from stock to the empty tableau pile nr. " + str(tableau.number))
                                choice = input("If you wish to do so enter 1: ")
                                
                                if choice == '1':
                                    game.stock.frontCard = j
                                    game.stock.cards.remove(game.stock.frontCard)   #Remove king from stock
                                    if len(game.stock.cards) != 0:
                                        game.stock.frontCard = game.stock.cards[LAST_INDEX] #New frontcard
                                        game.stock.frontCard.visible = Visible.TRUE
                                
                                    else:
                                        game.stock.frontCard = None
                                
                                    tableau.cards.append(j) #Add king to tableau pile
                                    tableau.frontCard = j   #King is the new frontcard
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