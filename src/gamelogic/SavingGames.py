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
   
def saveFailedGames(game):
    numVariablePath = "src/gamelogic/FailedGames/numberVariable"
    failedGamePath = "src/gamelogic/FailedGames/failedGame"

    num = open(numVariablePath, "rt")
    currentNumber = str(int(num.read()) +1)
    num.close()
    num = open(numVariablePath, "wt")
    num.write(currentNumber)
    num.close()
    failedGamePath = failedGamePath + currentNumber + ".txt"
    Savegame = open(failedGamePath, "wt")
    for card in game.playingCards:
        cardString = str(card.suit.value) + ", " + str(card.value.value )
        Savegame.write(cardString + "\n")
    Savegame.close()
    print("Game saved as " + failedGamePath)

def reloadFailedGame(game):
    failedGamePath = "src/gamelogic/FailedGames/failedGame"

    gamenumber = input("Enter the save number you want to reload.")
    failedGamePath = failedGamePath + gamenumber + ".txt"

    fGame = open(failedGamePath, "r")
    try:
        fGame = open(failedGamePath, "r")
    except FileNotFoundError:
        print('File does not exist.')
        exit()
    fGameLines = fGame.readlines()
    fGame.close()
    cardArray = []

    for line in fGameLines:
        lineArr = line.split(", ")
        suit = int(lineArr[0])
        value = int(lineArr[1].replace('\n', ""))
        if suit == 0 or suit == 1:
            color = 0
        else:
            color = 1
        cardArray.append(PlayingCard(Suit(suit), Color(color), Pile.STOCK, Value(value), Visible.FALSE))
    game.playingCards = cardArray
    
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
