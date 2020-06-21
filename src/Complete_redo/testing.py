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


def setup_table(game):
    
    # Setup a simple deck for testing
    colorSelect = 0
    # Generate a complete deck.
    game.playingCards = []
    for suitSelect in range(NO_SUITS):
        for valueSelect in range(1, 14):
            game.playingCards.append(PlayingCard(Suit(suitSelect), Color(colorSelect), Pile.STOCK, Value(valueSelect), Visible.FALSE))
        # Toggle the color.
        colorSelect+=1
        if colorSelect == 2:
            colorSelect = 0
    # Shuffle the deck.
    
    random.shuffle(game.playingCards)

    # Make first 28 cards the playing cards in the plateau and organize into piles.
    card = 0
    # Make 7 piles
    for pileNumber in range(1, 8):
        currentPile = TableauPile(pileNumber)
        # Make the pile corresponding to the current pilenumber
        for cardNumber in range (1, pileNumber+1):
            currentCard = game.playingCards[card]
            currentCard.pile = Pile.TABLEAU 
            # Make the top card in the pile visible.
            if cardNumber == pileNumber:
                currentCard.visible = Visible.TRUE            
            # Add current card to the current tableau pile and make it the front card ()
            currentPile.cards.append(game.playingCards[card])
            currentPile.frontCard = game.playingCards[card]
            card+=1
        # Add the newly created pile to the tableauPiles array 
        game.tableauPiles.append(currentPile)
        currentPile.frontCard.visible = Visible.TRUE

    # Make the rest of the cards the playing cards in the Stockpile.
    for card in range(NO_CARDS_PLATEAU, NO_CARDS):
        game.playingCards[card].pile = Pile.STOCK
        game.stock.cards.append(game.playingCards[card])
        game.playingCards[card].visible = Visible.TRUE
        game.stock.frontCard =  game.playingCards[card]

    #Initialize the Foundation piles
    for suit in Suit:
        newFoundationPile = FoundationPile(suit)
        newFoundationPile.nextCard = Value.ACE
        game.foundationPiles.append(newFoundationPile)
    #Initialize lowestNeededCard    
    
    newLowestNeededCard(game)

def win_check(game):
    # Check if all cards are visible and thus you game can be won
    check = 0
    for foundation in game.foundationPiles:
        check =check + len(game.foundation.cards)
    for tableau in game.tableauPiles:
        check = check + len(game.tableau.cards)
    if check == 52:
        print("")
        print("  / ____|                           | |     | | \ \   / /        ( )                               | | | | | | | | |\n" 
        + " | |      ___  _ __   __ _ _ __ __ _| |_ ___| |  \ \_/ /__  _   _|/__   _____  __      _____  _ __ | | | | | | | | |\n" 
        + " | |     / _ \| '_ \ / _` | '__/ _` | __/ __| |   \   / _ \| | | | \ \ / / _ \ \ \ /\ / / _ \| '_ \| | | | | | | | |\n" 
        + " | |____| (_) | | | | (_| | | | (_| | |_\__ \_|    | | (_) | |_| |  \ V /  __/  \ V  V / (_) | | | |_|_|_|_|_|_|_|_|\n" 
        + "  \_____|\___/|_| |_|\__, |_|  \__,_|\__|___(_)    |_|\___/ \__,_|   \_/ \___|   \_/\_/ \___/|_| |_(_|_|_|_|_|_|_|_)\n"
        + "                      __/ |                                                                                         \n"
        + "                     |___/                                                                                          ", end="\n")
       # playsound('./fanfare.mp3') #https://www.youtube.com/watch?v=4PIjjmq5cqg
        exit()
        #return 0

def remove_from_tableau_pile(card, tableauPile):
    # Removes a card from the Tableau piles
    tableauPile.cards.remove(card)
    if card == tableauPile.frontCard:
        if len(tableauPile.cards) == 0:
            tableauPile.frontCard = None
        else:
            tableauPile.frontCard = tableauPile.cards[LAST_INDEX]
            tableauPile.frontCard.visible = Visible.TRUE
        
def add_to_goal(card, goalPile, fromPile, game):
    # Don't call this call start_add_to_goal(), but this adds the card to the foundation pile
    goalPile.frontCard = card
    if goalPile.nextCard == Value(13):
        goalPile.nextCard = Value(13)
    else:
        goalPile.nextCard = Value(goalPile.nextCard.value + 1)
    remove_from_tableau_pile(card, fromPile)
    goalPile.cards.append(card)

def start_add_to_goal(card, fromPile, game):
    # The one to call, this checks if the move is legal
    for foundationPile in game.foundationPiles:
        if foundationPile.nextCard == card.value and foundationPile.suit == card.suit:
            add_to_goal(card, foundationPile, fromPile, game)
            newLowestNeededCard(game)
            break
    else:
        print("Illegal move", end=" ")

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
    
    #print("lnc: " + str(game.lowestNeededCard.value) + " smallest: " + str(smallestVal) + " Calc: " + str(Value(smallestVal+3)))

def add_to_tableau(cardList, toPile, fromPile):
    # Move a card from one tableau pile to another
    for card in cardList:        
        remove_from_tableau_pile(card, fromPile)
    toPile.cards.extend(cardList)
    toPile.frontCard = cardList[LAST_INDEX]

def start_add_to_tableau(cardList, fromPile, toPile):
    # The one to call, this checks if the move is legal
    topCard = cardList[0]
    if toPile.frontCard != None:
        if topCard.color != toPile.frontCard.color:
            if (topCard.value.value - toPile.frontCard.value.value == -1):
                add_to_tableau(cardList, toPile, fromPile)
            else:
                print("Wrong value on card")
        else:
            print("Wrong color card")
    elif cardList[0].value.value == 13:
        add_to_tableau(cardList, toPile, fromPile)
    else:
        if cardList[0].value.value == 13:
            add_to_tableau(cardList, toPile, fromPile)
        else:
            print("You can only move a king to an empty pile")


def waste_to_stock(game):   #Reshuffle waste pile to stock pile
    buffer = game.wastePile.cards
    game.wastePile.cards = []
    game.wastePile.frontCard = None
    game.stock.cards.extend(reversed(buffer)) # Need to reverse the array, so that it is in the same order as it started
    game.stock.frontCard = buffer[0]

def stock_to_tableau(game, toPile): #waste_to_tableau(toPile):
    #if len(wastePile.cards) == 0:
    if len(game.stock.cards) == 0:
        print("Stock is empty\n")
        
    else:
        #buffer = wastePile.frontCard
        buffer = game.stock.frontCard
        if buffer.color != toPile.frontCard.color:
            if buffer.value.value - toPile.frontCard.value.value == -1:
                #wastePile.cards.remove(wastePile.frontCard)
                game.stock.cards.remove(game.stock.frontCard)
                
                #if len(wastePile.cards) != 0:
                if len(game.stock.cards) != 0:
                    #wastePile.frontCard = wastePile.cards[LAST_INDEX]
                    #wastePile.frontCard.visible = Visible.TRUE
                    game.stock.frontCard = game.stock.cards[LAST_INDEX]
                    game.stock.frontCard.visible = Visible.TRUE
                else:
                    #wastePile.frontCard = None
                    game.stock.frontCard = None
            
                toPile.cards.append(buffer) #Add to tableau
                toPile.frontCard = buffer
            else:
                print("Wrong value on card")
        else:
            print("Wrong color on card")

def draw_from_stock (game): 
    # Draw card from stock and add it to waste
    if len(game.stock.cards) == 0:
        print("No more cards in stock pile.\n Adding waste pile to stock pile\n")   
        waste_to_stock(game)    #Reshuffle wate pile to stock pile
    else:
        buffer = game.stock.frontCard
        game.stock.cards.remove(game.stock.frontCard)  #Remove frontcard
        if len(game.stock.cards) != 0:
            game.stock.frontCard = game.stock.cards[LAST_INDEX] #New frontcard for stockpile
            game.stock.frontCard.visible = Visible.TRUE
        else:
            game.stock.frontCard = None

        game.wastePile.cards.append(buffer) #Add stock frontcard to wastepile
        game.wastePile.frontCard = buffer   
        game.wastePile.frontCard.visible = Visible.TRUE

        print(game.wastePile.frontCard.to_string(), " has been added to waste pile\n")


def insert_card(cardValue, cardSuit, cardPile, cardColor, inPile):
    # For adding certain cards in testing
    inPile.cards.append(PlayingCard(Suit(cardSuit), Color(cardColor), Pile.TABLEAU, Value(cardValue), Visible.TRUE))

def create_card(cardValue, cardSuit, cardPile, cardColor, cardLeft, cardTop):
    # For adding certain cards in testing
    return PlayingCard(Suit(cardSuit), Color(cardColor), TableauPile(cardPile), Value(cardValue), Visible.TRUE, cardLeft, cardTop)


def print_cards(game):
    # Print the current state of the deck in the terminal.
    print("The entire deck looks like:")
    printCounter = 0
    for card in game.playingCards:
        print("Card number:", printCounter, card.to_string_verbose())
        printCounter+=1

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
            str = str + "0," + game.foundationPiles[i].suit.name + " "
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
                if pile.cards[j].visible == Visible.TRUE:
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

def test_case_solveable_deck(game):

    #Will setup a solveable deck.
    testCards = []
    # Setup a simple deck for testing
    colorSelect = 0
    # Generate a complete deck.
    i = 0
    for suitSelect in range(NO_SUITS):
        for valueSelect in range(1, 14):
            game.playingCards.append(PlayingCard(Suit(suitSelect), Color(colorSelect), Pile.STOCK, Value(valueSelect), Visible.FALSE))
            i += 1
        # Toggle the color.
        colorSelect+=1
        if colorSelect == 2:
            colorSelect = 0
    #The deck for the game
    #               Cardnr:0,  1   2,  3  4   5  6,  7   8  9, 10  11  12  13  14, 15  16  17  18  19  20, 21, 22 23  24  25 26 27, 28  29  30  31  32  33  34  35  36  37  38  39  40  41  42  43  44  45  46  47  48  49  50  51                                        
    intForTestCards = [13, 35, 6, 32, 50, 7, 42, 16, 4, 9, 20, 25, 33, 14, 44, 37, 21, 23, 15, 40, 24, 34, 8, 28, 49, 1, 3, 5,  10, 29, 51, 18, 41, 46, 12, 45, 17, 27, 2,  48, 43, 19, 38, 47, 26, 31, 22, 30, 11, 0,  39, 36]
    for i in intForTestCards:
        testCards.append(game.playingCards[i])
    # Make first 28 cards the playing cards in the plateau and organize into piles.
    card = 0
    # Make 7 piles
    for pileNumber in range(1, 8):
        currentPile = TableauPile(pileNumber)
        # Make the pile corresponding to the current pilenumber
        for cardNumber in range (1, pileNumber+1):
            currentCard = testCards[card]
            currentCard.pile = Pile.TABLEAU 
            # Make the top card in the pile visible.
            if cardNumber == pileNumber:
                currentCard.visible = Visible.TRUE            
            # Add current card to the current tableau pile and make it the front card ()
            currentPile.cards.append(testCards[card])
            currentPile.frontCard = testCards[card]
            card+=1
        # Add the newly created pile to the tableauPiles array 
        game.tableauPiles.append(currentPile)
        currentPile.frontCard.visible = Visible.TRUE

    # Make the rest of the cards the playing cards in the Stockpile.
    for card in range(NO_CARDS_PLATEAU, NO_CARDS):
        testCards[card].pile = Pile.STOCK
        game.stock.cards.append(testCards[card])
        testCards[card].visible = Visible.TRUE
        game.stock.frontCard =  testCards[card]
    
    #Initialize the Foundation piles
    for suit in Suit:
        newFoundationPile = FoundationPile(suit)
        newFoundationPile.nextCard = Value.ACE
        game.foundationPiles.append(newFoundationPile)

    #Initialize lowestNeededCard  
    game.playingCards = testCards  
    newLowestNeededCard(game)
 