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
import cv2 as cv

PADDING = 2

# Method to highlight a specified card on screen
def highlight_card(frame, card): #Takes the fram to print on and card in question.
    cv.rectangle(frame, (card.left-PADDING, card.top-PADDING), (card.left+WIDTH_OF_CARD, card.top+HEIGHT_OF_CARD), (0, 255, 255),thickness=2)
    #Use opencv2 to call the rectangle method, specify rectangle boundaries, color and thickness

def highlight_pile(frame, pile, number): # Method to highlight a specified pile and pile type on screen
    if pile == "tableau":
        cv.rectangle(frame, ((CARD_WIDTH*number)+PADDING,CARD_HEIGHT+PADDING), ((CARD_WIDTH*(number+1))-PADDING,RESOLUTION_Y-PADDING),(0, 255, 255),thickness=2)
    elif pile == "foundation":
        cv.rectangle(frame,(CARD_WIDTH*(number+3)+PADDING,PADDING),(CARD_WIDTH*(number+4)-PADDING, CARD_HEIGHT-PADDING),(0, 255, 255),thickness=2)
    elif pile == "stock":
        cv.rectangle(frame,(PADDING,PADDING), (CARD_WIDTH-PADDING,CARD_HEIGHT-PADDING),(0, 255, 255),thickness=2)

# Method to print the advice of the gamelogic on screen
def print_advice(frame, advice): # Takes frame to print on and advice to display
    cv.putText(frame, advice, (90,CARD_HEIGHT-20), cv.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), thickness=2)
    # Specify the text with advice argument, coordinates, font, color etc. 

# Method to draw up the game table on screen.
def print_grid(frame): # Takes the frame to print on.
    # Top line
    cv.line(frame,(0,CARD_HEIGHT),(RESOLUTION_X,CARD_HEIGHT),(0,0,255),thickness=2)
    # Bottom lines
    for line in range(7):
        cv.line(frame,(CARD_WIDTH*line,0),(CARD_WIDTH*line,RESOLUTION_Y),(0,0,255),thickness=2)
    
# Method to identify if the stock pile is empty based on level of contour in top left square. 
def stockpile_is_empty(frame, game): # Works on a well focussed image
    stockpileFrame = frame[0:CARD_HEIGHT,0:CARD_WIDTH] #Define the stockpile frame(top left square)
    stockpileFrameGrey = cv.cvtColor(stockpileFrame, cv.COLOR_BGR2GRAY) # Convert the frame to a gray color space
    _, thresh = cv.threshold(stockpileFrameGrey, 127, 255, 0)   # Filters out pixels outside of the range from 127 to 255. 
                                                                # Returns binary picture, 0 on the pixels outside of the range and 1 for the pixels inside.
    contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) #Finds the contour of a binary image.
    if len(contours) > STOCKPILE_THRESHOLD or game.stock.frontCard != None: #If the contour is bigger than our specified threshold the stock pile is not empty
        return False
    elif len(contours) < STOCKPILE_THRESHOLD and game.stock.frontCard == None: # Otherwise empty.
        return True        

# Method to see if a king is on top of non-visual cards. Works the same as the stock_is_empty
def king_is_on_card(frame, game, card): 
    kingFrame = frame[card.top-50:card.top,card.left:card.left+WIDTH_OF_CARD]
    kingFrameGrey = cv.cvtColor(kingFrame, cv.COLOR_BGR2GRAY)
    _, thresh = cv.threshold(kingFrameGrey, 127, 255, 0)
    contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if len(contours) > KING_THRESHOLD:
        return True
    elif len(contours) < KING_THRESHOLD:
        return False  

# Method to generate advice for the user.  
def give_advice(game, stockIsEmpty, frame): # Takes the game object, value for whether stock is empty and the frame to print on.
    newLowestNeededCard(game) #Updates the lowest needed card for the foundation piles.
    foundAdvice = '0' # Variables see if an advice has been found, only one advice can be generated per iteration. 
    #funcCount = 0     # 

    print_grid(frame) # Print the game table

    # Every possible move, will now be calculated in a prioritised way. If a possible move is found, '1' is returned and the advice is given.
    # Each priority is represented with a function call as seen below.

    #Step 1 and 2:
    if foundAdvice == '0':
       foundAdvice = move_to_foundation_advice_and_do(game, frame)
   
    #Step 3
    if foundAdvice == '0':
        foundAdvice = free_king_advice(game, frame)
    
    #Step 4
    if foundAdvice == '0':
        foundAdvice = find_biggest_tableau_advise(game, frame)
    
    #Step 5 is already imnplemented in step 10
     
    # Step 6 
    if foundAdvice == '0':
        foundAdvice = twin_is_found(game, frame)
    
    # Step 7
    if foundAdvice == '0':
        foundAdvice = move_from_stock7(game, frame)

    # Step 8
    if foundAdvice == '0':
        foundAdvice = stockpile_to_tableau(game, frame)
    
    # Step 9
    if foundAdvice == '0':
        if stockIsEmpty:
            foundAdvice = move_to_foundation_advice_without_limit_and_do(game, frame)

    # Step 10
    if foundAdvice == '0':
        foundAdvice = draw_a_card_from_stock(game, frame)

    if foundAdvice == '0':
        print("No moves possible. Game unsolvable.")
        print_advice(frame, "No moves possible. Game unsolvable.")
        return 0                       
    
#Step 1 and 2 
# Method will see if a card in stock or tableau is needed in the foundationPile, based on game.lowestNeededCard.
def move_to_foundation_advice_and_do(game, frame):
    for pile in game.tableauPiles: # Go through each tableau
        if len(pile.cards) != 0 and pile.frontCard != None: # If the pile is not empty
            card = pile.frontCard                           #check if the frontcard of the pile is smaller or equal tot he lowest needed card in foundation.
            if card.value.value <= game.lowestNeededCard.value: 
                for foundPile in game.foundationPiles:  # For each foundation pile 
                    if card.suit == foundPile.suit and card.value == foundPile.nextCard: # if the card is the same suit of the pile and is the next needed card in the pile
                        print("Function 1 og 2: Move card to foundation")                  # Give the advise to move the card.
                        print("Move the " + card.value.name + " of " + card.suit.to_string()+ " to the " + NUMBER_ARRAY[foundPile.suit.value] + " foundation pile")
                        highlight_card(frame, card) #Highlight the card and foundation pile in question. And print the advice on screen.
                        highlight_pile(frame, "foundation", foundPile.suit.value) 
                        print_advice(frame, "Move the " + card.value.name + " of " + card.suit.to_string()+ " to the " + NUMBER_ARRAY[foundPile.suit.value] + " foundation pile")
                        return '1'
    if game.stock.frontCard != None: # Do the same for the stock card.
        card = game.stock.frontCard
        if card.value.value <= game.lowestNeededCard.value:
            for foundPiles in game.foundationPiles:
                if card.suit == foundPiles.suit and card.value == foundPiles.nextCard:
                    print("Function 1 og 2: Move card to foundation")
                    print("Move the " + card.value.name + " of " + card.suit.to_string()+ " from stock pile to the foundation pile")
                    highlight_card(frame, card)
                    highlight_pile(frame, "foundation", foundPile.suit.value)
                    return '1'
    return '0'
    
#Step 3
# Metohd to move the king from the tableau pile with the most non-visible cards to an empty space.
def free_king_advice(game, frame): 
    biggestLen = 0      # Measure of pile with the biggest amount of non visible cards.
    emptyPile = None    # The pile ready to have a king placed.
    targetCard = None   # The king
    choice = None       # User choice
    for pile in game.tableauPiles: # Check if any tableau is empty by finding a pile with no frontcard.
        if not pile.cards: # if the pile.cards is empty
            emptyPile = pile
        else:                       # If the pile is not empty, we can check if it has a king ready to be moved.
            for card in pile.cards:                 # Find the king
                if card.value.value == 13 and king_is_on_card(frame, game, card): # if the card is a king and is not on top of non visual cards
                    if card.top > biggestLen : # Try and pick the king that is furthest down the game table as it is most likely the king on top of most non visual cards.
                        biggestLen = card.top
                        targetCard = card
    if targetCard != None and emptyPile != None: # If a king and an empty pile is found
        print("Function 3: Move king")                      # Give the advice
        print("Move the " + targetCard.value.name + " of " + targetCard.suit.to_string()+ " to the empty tableau pile nr. " + str(emptyPile.number))
        highlight_card(frame, targetCard)
        highlight_pile(frame, "tableau", emptyPile.number-1)
        king_is_on_card(frame, game, targetCard)
        print_advice(frame,"Move the " + targetCard.value.name + " of " + targetCard.suit.to_string()+ " to the empty tableau pile nr. " + str(emptyPile.number))
        return '1' 
    else:
        return '0'

# Step 4
# Method to find moves from one tableau to another
def find_biggest_tableau_advise(game, frame):  
    targetPile = None  # the pile to move to
    biggestLen = 0 # value of the biggest top coordinate of a movable card
    card = None  # the card to move

    for tabPile in game.tableauPiles: # for each tableau pile we iterate thourgh every other
        if tabPile.frontCard != None and len(tabPile.cards) > 0: #as long as the pile is not empty
            for pile in game.tableauPiles:  
                if pile.frontCard != None and len(tabPile.cards) > 0:
                    #In the case that a pile with only one card is moveable:
                    if tabPile.frontCard.color != pile.frontCard.color and tabPile.frontCard.value.value - pile.frontCard.value.value == -1 and len(tabPile.cards) < 2:
                        if biggestLen < tabPile.frontCard.top: # Try and chose the card with most non visual cards
                            biggestLen = tabPile.frontCard.top
                            targetPile = pile
                            card = tabPile.frontCard
                    #In the case that the entire pile is moveable.
                    if tabPile.cards[0].value.value - pile.frontCard.value.value == -1 and tabPile.cards[0].color != pile.frontCard.color:
                        if biggestLen < tabPile.cards[0].top:
                            biggestLen = tabPile.cards[0].top
                            targetPile = pile
                            card = tabPile.cards[0]
    if card != None and targetPile != None: # If a moveable card/pile is found, give advice
        print("Function 4: Move tableau card/pile")
        print("Move the " + card.value.name + " of " + card.suit.to_string()+ " to " + targetPile.frontCard.value.name + " of " + targetPile.frontCard.suit.to_string()) 
        highlight_card(frame, card)
        highlight_pile(frame, "tableau", targetPile.number-1)
        print_advice(frame, "Move the " + card.value.name + " of " + card.suit.to_string()+ " to " + targetPile.frontCard.value.name + " of " + targetPile.frontCard.suit.to_string())
        return '1'
    return '0'

# Step 6
# Method to move a card from stockpile to tableau pile if the same value and color of the card is already in a tableau pile on another card
def twin_is_found(game, frame):
    targetCard = None
    if game.stock.frontCard != None:
        targetCard = game.stock.frontCard # Need to check for frontcard in stock 
        for twinpile in game.tableauPiles: # And for each card, in each tableau pile.
            if twinpile.frontCard != None: # If the tableau pile is not empty.
                for twincard in twinpile.cards: # try to find a visible card of same color and value as target card.
                    if targetCard.value.value == twincard.value.value and targetCard.color == twincard.color:
                        for pile in game.tableauPiles: # When all requirements have been meet, we check all other tableau piles for a place for the targetCard
                            if pile.frontCard != None and pile != twinpile:
                                if pile.frontCard.value.value == targetCard.value.value + 1 and pile.frontCard.color != targetCard.color:
                                    print("Function 6: find twin card and add to tableau") # Give advice
                                    print("Move the " + targetCard.value.name + " of " + targetCard.suit.to_string() + " to " + pile.frontCard.value.name + " of " + pile.frontCard.suit.to_string()) 
                                    highlight_card(frame, targetCard)
                                    highlight_pile(frame, "tableau", pile.number-1)
                                    print_advice(frame, "Move the " + targetCard.value.name + " of " + targetCard.suit.to_string() + " to " + pile.frontCard.value.name + " of " + pile.frontCard.suit.to_string())
                                    return '1'
    return '0'
    
# Step 7
# Method to move from stock to tableau if the next move is step 4
def move_from_stock7(game, frame):
    card = None
    targetPile = None
    if game.stock.frontCard != None: 
        stockCard = game.stock.frontCard  # First we go through each tableau pile to find a card/pile that can be moved on top of the stock card.
        for tabPile in game.tableauPiles:
            if len(tabPile.cards) != 0:
                #Check frontcard
                if tabPile.frontCard.color != stockCard.color and tabPile.frontCard.value.value - stockCard.value.value == -1: #If they do match, check if the card from stock matches with a card from tableau
                    for tableau in game.tableauPiles: # Now to see if the stock card can be placed
                        if len(tableau.cards) != 0:
                            # Check frontcard
                            if stockCard.color != tableau.frontCard.color and stockCard.value.value - tableau.frontCard.value.value == -1:  #If it does move stock card to tableau
                                card = stockCard
                                targetPile = tableau
                            # Check top card
                            elif stockCard.color != tableau.frontCard.color and stockCard.value.value - tableau.cards[0].value.value == -1:
                                card = stockCard
                                targetPile = tableau
                # Check top card
                elif tabPile.cards[0].color != stockCard.color and tabPile.cards[0].value.value - stockCard.value.value == -1:
                    for tableau in game.tableauPiles: # Now to see if the stock card can be placed
                        if len(tableau.cards) != 0:
                            # Check frontcard
                            if stockCard.color != tableau.frontCard.color and stockCard.value.value - tableau.frontCard.value.value == -1:  #If it does move stock card to tableau
                                card = stockCard
                                targetPile = tableau
                            # Check top card
                            elif stockCard.color != tableau.frontCard.color and stockCard.value.value - tableau.cards[0].value.value == -1:
                                card = stockCard
                                targetPile = tableau
            #If the pile is empty the stock card is a king.
            elif len(tabPile.cards) == 0 and stockCard.value.value == 13:   #If there is an empty tableau pile, move out king from stock
                for tableau in game.tableauPiles: # Now to see if a card in tableau can be put on the card
                    if len(tableau.cards) != 0:
                        # Check top card
                        if stockCard.color != tableau.frontCard.color and stockCard.value.value - tableau.frontCard.value.value == -1:  #If it does move stock card to tableau
                            card = stockCard
                            targetPile = tableau
                        # Check top card
                        elif stockCard.color != tableau.frontCard.color and stockCard.value.value - tableau.cards[0].value.value == -1:
                            card = stockCard
                            targetPile = tableau
        if card != None and targetPile != None:# If a card and targetPile is found, give advice
            print("Function 7")
            print("Move the " + stockCard.value.name + " of " + stockCard.suit.to_string() + " from stock to " + targetPile.frontCard.value.name + " of " + targetPile.frontCard.suit.to_string())
            highlight_card(frame, stockCard)
            highlight_pile(frame, "tableau", targetPile.number-1)
            print_advice(frame, "Move the " + stockCard.value.name + " of " + stockCard.suit.to_string() + " from stock to " + targetPile.frontCard.value.name + " of " + targetPile.frontCard.suit.to_string())
            return '1'
    return '0'

# Step 8
# Method to move anything from stock to tableau pile.
def stockpile_to_tableau(game, frame):
    card = None
    targetPile = None
    if game.stock.frontCard != None:
        card = game.stock.frontCard
        for tableauPile in game.tableauPiles: # Go through each tableau pile to see if the stock card can be put there.  
            if tableauPile.frontCard != None and len(tableauPile.cards) > 0:
                if card.value.value - tableauPile.frontCard.value.value == -1 and tableauPile.frontCard.color != card.color: 
                    targetPile = tableauPile
            elif card.value.value == 13: # If it was an empty pile and the stock card was a king.
                    targetPile = tableauPile
    if card != None and targetPile != None: # If a card and targetPile is found, give advice
        print("Function 8: Move any card from stock to tableau")
        print("Move the " + card.value.name + " of " + card.suit.to_string()+ " to to the tableau pile containing: " + targetPile.frontCard.value.name + " of " + targetPile.frontCard.suit.to_string())
        highlight_card(frame, card)
        highlight_pile(frame, "tableau", targetPile.number-1)
        print_advice(frame, "Move the " + card.value.name + " of " + card.suit.to_string()+ " to to the tableau pile containing: " + targetPile.frontCard.value.name + " of " + targetPile.frontCard.suit.to_string())
        return '1'
    return '0'


# Step 9
# Method that moves any card that can to the foundation piles
def move_to_foundation_advice_without_limit_and_do(game, frame):  
    card = None
    targetPile = None                      
    for pile in game.tableauPiles:# Go through the tableau piles 
        if len(pile.cards) != 0:  # If the pile is not empty
            tabCard = pile.frontCard
            for foundPile in game.foundationPiles: # go through the foundation piles and see if theres a card that can be added to the foundation piles 
                if card.suit == foundPile.suit and card.value == foundPile.nextCard:
                    targetPile = foundPile
                    card = tabCard
    if game.stock.frontCard != None: # See if the stock card can be added to a foundation pile.
        stockCard = game.stock.frontCard
        for foundPiles in game.foundationPiles:
            if card.suit == foundPiles.suit and card.value == foundPiles.nextCard:
                targetPile = foundPile
                card = stockCard
    if card != None and targetPile != None: # If a card and targetPile is found, give advice
        print("Function 9: Move to foundation without a limit")
        print("Move the " + card.value.name + " of " + card.suit.to_string()+ " from stock pile to the foundation pile")
        highlight_card(frame, card)
        highlight_pile(frame, "foundation", targetPile.suit.value)
        print_advice(frame, "Move the " + card.value.name + " of " + card.suit.to_string()+ " from stock pile to the foundation pile")
        return '1'
    return '0'

# Step 5 and 10
# Method that checks if the stock pile is empty and it gives the advice to pull from stock.
def draw_a_card_from_stock(game, frame):
    if not stockpile_is_empty(frame, game):
        print("Please draw from stock")
        highlight_pile(frame, "stock", 0)
        print_advice(frame, "Please draw from stock")
        return '1'
    else:
        return '0'


