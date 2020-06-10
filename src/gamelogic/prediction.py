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
    round = 0
    print("Round " + str(round) + ". ")
    round = round +1 
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
                        print("Put the " + card.value.name + " " + card.suit.to_string() + " in the foundation pile")
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
                        print("Funktion 1 og 2")
                        print("Put the " + card.value.name + " of " + card.suit.to_string()+ " in the foundation pile")
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
                        print("Put the " + cards.value.name + " of " + cards.suit.to_string()+ " in the foundation pile")
                        print("Test funktion 1 og 2")
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
        print("Funktion 3")
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
def find_biggest_tableau_advise(game):
    bigestPile = game.tableauPiles[0]   #currently biggest pile
    fromPile = game.tableauPiles[0]     #the pile to be moved from
    movePile = []  #Number of cards to move from the bigest pile

    nonVisualCount = 0
    nVCPrevious = 0
    #for pile in tableauPiles:
    for searchBiggest in game.tableauPiles:             #currently pile
        if searchBiggest.frontCard != None:
            for pile in game.tableauPiles:
                if pile.frontCard != None:
                    if searchBiggest.frontCard.color != pile.frontCard.color and searchBiggest.frontCard.value.value - pile.frontCard.value.value == -1:
                        for cardsInPile in searchBiggest.cards:         #Find number of nonvisual cards
                            if cardsInPile.visible == Visible.FALSE:       
                                nonVisualCount = nonVisualCount+1       
                        if len(bigestPile.cards) != 0:                  #
                            for cards in bigestPile.cards:              #fIND NUMBER OF NONVISUAL CARDS IN THE CURRENTLY BIGGEST pile 
                                if cards.visible == Visible.FALSE:
                                    nVCPrevious = nVCPrevious+1
                        if nonVisualCount >= nVCPrevious:               #if there's more nonvisual cards in currently pile, update this to be the biggest pile 
                            bigestPile = searchBiggest                  # The pile with biggest amount of nonVisual cards
                            fromPile = searchBiggest  
                            nonVisualCount = 0  
                
                    elif len(searchBiggest.cards) > 1:
                        for cardInPile in searchBiggest.cards:
                            if cardInPile.visible == Visible.TRUE:
                                #if cardInPile != searchBiggest.frontCard:
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
        for toPile in game.tableauPiles:
            if toPile.frontCard != None:
                if movePile[0].color != toPile.frontCard.color and movePile[0].value.value - toPile.frontCard.value.value == -1:
                    if cardMoved == 0:
                        print("Funktion 4")
                        print("Move " + movePile[0].to_string() + " to " + toPile.frontCard.to_string())
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
def twin_is_found(game):
    for targetCard in game.stock.cards:
        for pile in game.tableauPiles:
            if pile.frontCard != None:
                if targetCard.value.value == pile.frontCard.value.value and targetCard.color == pile.frontCard.color:
                    for pile in game.tableauPiles:
                        if pile.frontCard != None:
                            if pile.frontCard.value.value == targetCard.value.value + 1 and pile.frontCard.color != targetCard.color:
                                print("Funktion 6")
                                print("Put the " + targetCard.value.name + " of " + targetCard.suit.to_string() + " on " + pile.frontCard.value.name + " of " + pile.frontCard.suit.to_string()) 
                                game.stock.frontCard = targetCard
                                stock_to_tableau(game, pile)
                                return '1'
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
                                    print("Funktion 7")
                                    print("Move " + j.to_string() + " to " + tableau.frontCard.to_string())
                                    choice = input("Press 1 if you want to make this move\n")
                                    if choice == '1':
                                        game.stock.frontCard = j
                                        stock_to_tableau(game,tableau)
                                        return '1'
                            elif len(tableau.cards) == 0 and j.value.value == 13:
                                print("Move " + j.to_string())
                                choice = input("Press 1 if you want to make this move\n")
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
                    print("Funktion 8")
                    print("Put the " + card.value.name + " of " + card.suit.to_string()+ " in the tableau pile containing: " + tableauPile.frontCard.value.name + " of " + tableauPile.frontCard.suit.to_string())
                    choice = input("If you want make this move, press: 1\n")
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
                    print("Funktion 1 og 2")
                    print("Put the " + card.value.name + " of " + card.suit.to_string()+ " in the foundation pile")
                    choice = input("If you wish to do so enter 1: ")
                    if choice == '1':
                        start_add_to_goal(card, pile, game)
                    return '1'


    if len(game.stock.cards) != 0:
        pile = game.stock
        for cards in game.stock.cards:
            if cards.value.value <= game.lowestNeededCard.value:
                if cards.suit == game.foundPile.suit and cards.value == game.foundationPiles.nextCard:
                    print("Put the " + cards.value.name + " of " + cards.suit.to_string()+ " in the foundation pile")
                    print("Test funktion 1 og 2")
                    choice = input("If you wish to do so enter 1: ")
                    if choice == '1':
                        start_add_to_goal(cards, pile, game)
                    return '1'
    return '0'