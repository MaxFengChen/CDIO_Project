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

playingCards = []
tableauPiles = []
foundationsPiles = []
stock = StockPile()
wastePile = WastePile()
lowestNeededCard = Value.TWO

def setup_table():
    # Setup a simple deck for testing
    colorSelect = 0
    # Generate a complete deck.
    for suitSelect in range(NO_SUITS):
        for valueSelect in range(1, 14):
            playingCards.append(PlayingCard(Suit(suitSelect), Color(colorSelect), Pile.STOCK, Value(valueSelect), Visible.FALSE))
        # Toggle the color.
        colorSelect+=1
        if colorSelect == 2:
            colorSelect = 0
    # Shuffle the deck.
    random.shuffle(playingCards)

    # Make first 28 cards the playing cards in the plateau and organize into piles.
    card = 0
    # Make 7 piles
    for pileNumber in range(1, 8):
        currentPile = TableauPile(pileNumber)
        # Make the pile corresponding to the current pilenumber
        for cardNumber in range (1, pileNumber+1):
            currentCard = playingCards[card]
            currentCard.pile = Pile.TABLEAU 
            # Make the top card in the pile visible.
            if cardNumber == pileNumber:
                currentCard.visible = Visible.TRUE            
            # Add current card to the current tableau pile and make it the front card ()
            currentPile.cards.append(playingCards[card])
            currentPile.frontCard = playingCards[card]
            card+=1
        # Add the newly created pile to the tableauPiles array 
        tableauPiles.append(currentPile)
        currentPile.frontCard.visible = Visible.TRUE

    # Make the rest of the cards the playing cards in the Stockpile.
    for card in range(NO_CARDS_PLATEAU, NO_CARDS):
        playingCards[card].pile = Pile.STOCK
        stock.cards.append(playingCards[card])
        playingCards[card].visible = Visible.TRUE
        stock.frontCard =  playingCards[card]

    #Initialize the Foundation piles
    for suit in Suit:
        newFoundationPile = FoundationPile(suit)
        newFoundationPile.nextCard = Value.ACE
        foundationsPiles.append(newFoundationPile)

def win_check():
    # Check if all cards are visible and thus you game can be won
    check = 0
    for card in playingCards:
        if card.visible == Visible.FALSE:
            check = 1
    if check == 0:
        print("Congrats you have won!", end="\n")

def remove_from_tableau_pile(card, tableauPile):
    # Removes a card from the Tableau piles
    tableauPile.cards.remove(card)
    if card == tableauPile.frontCard:
        if len(tableauPile.cards) == 0:
            tableauPile.frontCard = None
        else:
            tableauPile.frontCard = tableauPile.cards[LAST_INDEX]
            tableauPile.frontCard.visible = Visible.TRUE
        
def add_to_goal(card, goalPile, fromPile):
    # Don't call this call start_add_to_goal(), but this adds the card to the foundation pile
    goalPile.frontCard = card
    goalPile.nextCard = Value(goalPile.nextCard.value + 1)
    remove_from_tableau_pile(card, fromPile)
    goalPile.cards.append(card)

def start_add_to_goal(card, fromPile, foundationPiles):
    # The one to call, this checks if the move is legal
    for foundationPile in foundationsPiles:
        if foundationPile.nextCard == card.value and foundationPile.suit == card.suit:
            add_to_goal(card, foundationPile, fromPile)
            break
    else:
        print("Illegal move", end=" ")

def add_to_tableau(cardList, toPile, fromPile):
    # Move a card from one tableau pile to another
    for card in cardList:
        remove_from_tableau_pile(card, fromPile)
    toPile.cards.extend(cardList)    
    print("\n")

def start_add_to_tableau(cardList, fromPile, toPile):
    # The one to call, this checks if the move is legal
    topCard = cardList[0]
    if topCard.color != toPile.frontCard.color:
        if topCard.value.value - toPile.frontCard.value.value == -1:
            add_to_tableau(cardList, toPile, fromPile)

        else:
            print("Wrong value on card")
    else:
        print("Wrong color card")

def waste_to_stock():
    # Add entire waste pile to stock pile
    buffer = wastePile.cards
    wastePile.cards = []
    wastePile.frontCard = None
    
    stock.cards.extend(reversed(buffer)) # Need to reverse the array, so that it is in the same order as it started
    stock.frontCard = buffer[0]

def waste_to_tableau(toPile):
    if len(wastePile.cards) == 0:
        print("Wastepile is empty\n")
        
    else:
        buffer = wastePile.frontCard
        if buffer.color != toPile.frontCard.color:
            if buffer.value.value - toPile.frontCard.value.value == -1:
                wastePile.cards.remove(wastePile.frontCard)
                if len(wastePile.cards) != 0:
                    wastePile.frontCard = wastePile.cards[LAST_INDEX]
                    wastePile.frontCard.visible = Visible.TRUE
                else:
                    wastePile.frontCard = None
            
                toPile.cards.append(buffer)
                toPile.frontCard = buffer
            else:
                print("Wrong value on card")
        else:
            print("Wrong color on card")

def draw_from_stock (): 
    # Draw card from stock and add it to waste
    if len(stock.cards) == 0:
        print("No more cards in stock pile.\n Adding waste pile to stock pile\n")   
        waste_to_stock()
    else:
        buffer = stock.frontCard
        stock.cards.remove(stock.frontCard)
        if len(stock.cards) != 0:
            stock.frontCard = stock.cards[LAST_INDEX]
            stock.frontCard.visible = Visible.TRUE
        else:
            stock.frontCard = None

        wastePile.cards.append(buffer)
        wastePile.frontCard = buffer
        wastePile.frontCard.visible = Visible.TRUE

        print(wastePile.frontCard.to_string(), " has been added to waste pile\n")


def insert_card(cardValue, cardSuit, cardPile, cardColor, inPile):
    # For adding certain cards in testing
    inPile.cards.append(PlayingCard(Suit(cardSuit), Color(cardColor), Pile.TABLEAU, Value(cardValue), Visible.TRUE))

def print_cards():
    # Print the current state of the deck in the terminal.
    print("The entire deck looks like:")
    printCounter = 0
    for card in playingCards:
        print("Card number:", printCounter, card.to_string_verbose())
        printCounter+=1

def print_table():
    print(f"{Back.GREEN}{Style.BRIGHT}") # Add a background color to the 
    # Print first line with Stock pile and the Foundation piles
    str = ""
    if stock.frontCard == None:
        str = "0,X     "
    else:
        # Add coloring to the stock pile
        if stock.frontCard.suit.get_color() == Color.BLACK:
            stringColor = f"{Fore.BLACK}"
        elif stock.frontCard.suit.get_color() == Color.RED:
            stringColor = f"{Fore.RED}"
        str = str + stringColor

        str = str + stock.frontCard.to_string() + "     "
    for i in range(len(foundationsPiles)):
        # Add coloring to the foundation piles
        if foundationsPiles[i].suit.get_color() == Color.BLACK:
            stringColor = f"{Fore.BLACK}"
        elif foundationsPiles[i].suit.get_color() == Color.RED:
            stringColor = f"{Fore.RED}"
        str = str + stringColor

        if foundationsPiles[i].frontCard == None:
            str = str + "0," + foundationsPiles[i].suit.name + " "
        else:
            str = str + foundationsPiles[i].frontCard.to_string() + " "
    
    print(str,"\n")
    str = ""

    # Print Tableau piles
    for j in range(len(tableauPiles)):
        for pile in tableauPiles:
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

