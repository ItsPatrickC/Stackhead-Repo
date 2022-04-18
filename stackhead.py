import random
import os
from cardclasses import Deck, Stack, Hand
from cardclasses import values, suits, ranks

import defs
from defs import deal_sh_hand, rules, deal, dealo

clear = lambda: os.system('cls')

#main loop
playerTurn = True
while True:

    # welcome to the game
    print("Welcome to Stackhead!")

    # offer rules, start the game

    rulesyn = str(input("Would you like to know the rules first? y/n"))

    if rulesyn == 'y' or rulesyn == 'Y':
        clear()
        rules()
        input("Press Enter to continue...")
        clear()


    else:
        pass



    deckempty = False #REQ7 1
    gamedeck = Deck()
    gamedeck.shuffle()
    gamestack = Stack()

    # deal out cards to player and opponent
    phand = Hand()
    ohand = Hand()
    deal_sh_hand(phand, gamedeck)
    deal_sh_hand(ohand, gamedeck)

    # show players cards
    print(phand)

    # show opponents face up cards
    ohand.sorthand()
    print("Your opponents face up cards are: ")
    for a in range(0, len(ohand.faceups)):
        print("   ", str(ohand.faceups[a]))

    # show the stack
    #gamestack.starter_card(gamedeck, gamedeck.deal())
    #print("Is this one used?")
    #sval = values[gamestack.all_cards[0].rank]



    def canplay(hand):
        if hand.canplay() < sval:
            return False
        elif hand.canplay() >= sval:
            return True
    def canplay_fu(hand):
        if hand.canplay_fu() < sval:
            return False
        elif hand.canplay() >= sval:
            return True


    #showstack function that displays the stack and shows the sval, partly for presentation and partly for testing
    def showstack(hand):
        gamestack.correct3()
        phand.return3()
        ohand.return3()

        print("The Stack!")
        for a in range(0, len(gamestack.all_cards)):
            print("    ", gamestack.all_cards[a])


        if len(gamestack.all_cards) > 0:
            sval = gamestack.all_cards[0].value
            print(f"Stack Value: {sval}!")
            print(f"Hand value: {hand.canplay()}!") #for testing




    #print("HELLO ", sval)
    #print(f"Starting stack card: {gamestack.all_cards[0]}, {len(gamedeck.all_cards)} cards remaining line 73")

    playing = True

    # main loop
    while playing:
        #correct 3s at the beginning of each turn
        gamestack.correct3()
        phand.return3()
        ohand.return3()

        #check for win conditions each turn
        if phand.win():
            clear()
            print("You got rid of all your cards! You win the game!")
            input("Press Enter to continue...")
            break

        if ohand.win():
            clear()
            print("The opponent used all their cards! They win, better luck next time")
            input("Press Enter to continue...")
            break

        if len(gamedeck.all_cards) == 0: #if the deck runs out of cards, REQ7 2
            deckempty = True

        #print out how many cards in deck (for testing)
        #print(len(gamedeck.all_cards), "cards in deck line 80")

        #set up sval
        if len(gamestack.all_cards) != 0:
            sval = gamestack.all_cards[0].value

        #when it's the players turn

        if playerTurn:

            print("Your turn!")

            if phand.facedowncards(): #check if player has used all cards except facedowns
                print("Use facedown cards!")

            #deal a card if less than 3 in hand and cards still in deck
            #deal(phand,gamedeck) #REQ9 1

            # if a turn begins, and no beginning card, deal one from the deck, if not then player starts game
            if not len(gamestack.all_cards): #check if stack is empty, REQ7 3

                if deckempty: #if deck is empty, prompt player to play a card, REQ8 1
                    print("Deck empty! Play a card")

                    gamestack.all_cards.insert(0, phand.select_card())

                    # check if it's 8
                    if gamestack.eight():  # REQ14 1
                        deal(phand, gamedeck)
                        print("8 skips!")
                        input("Press Enter to continue...")
                        clear()

                        continue

                    # check if it's ten
                    if gamestack.ten():  # REQ15 1
                        deal(phand, gamedeck)
                        print("BURN")
                        # empty the stack
                        while len(gamestack.all_cards) > 0:
                            gamestack.all_cards.pop()

                        input("Press Enter to continue...")
                        clear()
                        continue

                    elif not gamestack.ten():
                        input("Press Enter to continue...")
                        clear()
                        playerTurn = False
                        continue

                    # continue prompt
                    input("Press Enter to continue...")
                    clear()
                    playerTurn = False
                    continue

                # if cards in deck, use top one
                elif not deckempty: #REQ10 1
                    gamestack.starter_card(gamedeck)
                    continue

            # show the stack
            #phand.return3()
            showstack(phand)

            # if the top of the stack is a 7, this section deals with it
            if gamestack.seven(): #REQ13 1
                print("You must play lower than a 7!")

                # need to check if the player actually has anything lower than a 7
                if phand.canplay7() == 100:  # phand returns positively
                    # print("You can play something under a 7!")
                    pass  # is pass right to use?

                else: #if player can't place anything lower thna or equal to 7, tell them and pick up

                    if phand.handempty() and len(phand.faceups): #if hand is empty, but faceup cards not yet used
                        print("Your face up cards: ") #show faceup cards
                        for a in range(0, len(phand.faceups)):
                            print("    ", a, ':', phand.faceups[a])

                    print("You have no cards under 7! Pick up")
                    gamestack.bad_hand(phand)
                    phand.return3()

                    input("Press Enter to continue...")
                    clear()
                    playerTurn = False
                    continue

                gamestack.all_cards.insert(0, phand.select_card())

                if phand.facedowncards(): #if card was played from facedowns
                    if gamestack.comp7() and gamestack.all_cards[0].value not in [2, 3]:
                        print("And it is not playable! Pick up!")
                        gamestack.bad_hand(phand)

                        input("Press Enter to continue...")
                        clear()
                        playerTurn = False
                        continue

                    elif not gamestack.comp7() or gamestack.all_cards[0].value in [2,3]:
                        print("And it is playable!")

                        input("Press Enter to continue...")
                        clear()
                        playerTurn = False
                        continue

                # comp7 returns true if something higher is played on a 7, and sends that card back
                if gamestack.comp7():
                    print("That is not lower than a 7!")
                    gamestack.send_back(phand)
                    phand.return3()
                    # showstack(phand)

                    input("Press Enter to continue...")
                    clear()
                    continue

                if gamestack.compare() and gamestack.all_cards[0].value not in [2,3]:
                    deal(phand,gamedeck) #REQ9 2
                else:
                    deal(phand,gamedeck)#REQ9 3

                if gamestack.multi3():
                    gamestack.correct3()
                    print("The 3 is now a 7! 177")
                    sval = 7

                    input("Press Enter to continue...")
                    clear()
                    playerTurn = False
                    continue

                #immediately check if plaer played a 3
                if gamestack.magic3():
                    gamestack.correct3()
                    print("The 3 is now a 7!")
                    sval = 7

                    input("Press Enter to continue...")
                    clear()
                    playerTurn = False
                    continue

                #check if player played a 4th seven in a row
                if gamestack.burn(): #REQ19 1
                    deal(phand, gamedeck)
                    print(gamestack.all_cards[0].rank, "* 4!!")

                    print("BURN")
                    # empty the stack
                    while len(gamestack.all_cards) > 0:
                        gamestack.all_cards.pop()

                    input("Press Enter to continue...")
                    clear()
                    continue

                # if a 7 is played on a 7, skip to opponent
                if gamestack.multi7():
                    input("Press Enter to continue...")
                    clear()
                    playerTurn = False
                    continue


                # if it returns false, the card is lower and therefore valid to play
                elif not gamestack.comp7():
                    print("That is lower than a 7!")
                    #deal(phand,gamedeck)

                    # if a 3 is played on a 7, might not need this actually
                    if gamestack.all_cards[0].value == 3 and gamestack.all_cards[1].value == 7:
                        gamestack.all_cards[0].value = 7
                        sval = gamestack.all_cards[0].value
                        # showstack(phand)
                        input("Press Enter to continue...")
                        clear()
                        playerTurn = False
                        continue

                    input("Press Enter to continue...")
                    clear()
                    playerTurn = False
                    continue

            # if a ten is played
            if gamestack.ten(): #REQ15 2
                deal(phand, gamedeck)
                print("BURN")

                # empty the stack
                while len(gamestack.all_cards) > 0:
                    gamestack.all_cards.pop()

                input("Press Enter to continue...")
                clear()
                continue

            # test hand, pick up if not playable and skip turn
            if not canplay(phand):
                if phand.handempty() and len(phand.faceups):
                    print("Your face up cards: ")
                    for a in range(0, len(phand.faceups)):
                        print("    ", a, ':', phand.faceups[a])

                print("Cannot play these cards! Pick up")
                gamestack.bad_hand(phand)
                phand.return3()

                input("Press Enter to continue...")
                clear()
                playerTurn = False
                continue

            # if hand is playable
            elif canplay(phand):

                gamestack.all_cards.insert(0, phand.select_card())

                #check if facedown cards are usable, if so use them and evluate
                if phand.facedowncards():
                    if gamestack.compare() and gamestack.all_cards[0].value not in [2, 3]:
                        print("And it is not playable! Pick up!")
                        gamestack.bad_hand(phand)

                        input("Press Enter to continue...")
                        clear()
                        playerTurn = False
                        continue

                    elif not gamestack.compare() or gamestack.all_cards[0].value in [2,3]:
                        print("And it is playable!")

                        if gamestack.ten():  # REQ15 2
                            #deal(phand, gamedeck)
                            print("BURN")

                            # empty the stack
                            while len(gamestack.all_cards) > 0:
                                gamestack.all_cards.pop()

                            input("Press Enter to continue...")
                            clear()
                            continue

                        if gamestack.eight():
                            print("8 skips!")
                            input("Press Enter to continue...")
                            clear()
                            continue


                        input("Press Enter to continue...")
                        clear()
                        playerTurn = False
                        continue

                #deal(phand, gamedeck)#REQ9 4

                #if a 3 is played on another 3, not sure if actually needed now
                if gamestack.multi3(): #REQ12 2
                    gamestack.correct3()
                    print("The 3 is now a", gamestack.all_cards[0].value)
                    sval = gamestack.all_cards[0].value

                    deal(phand, gamedeck)
                    input("Press Enter to continue...")
                    clear()
                    playerTurn = False
                    continue

                #if a card is played for the 4th time in a row
                if gamestack.burn(): #REQ19 2
                    print(gamestack.all_cards[0].rank, "* 4!!")
                    deal(phand, gamedeck)
                    print("BURN")

                    # empty the stack
                    while len(gamestack.all_cards) > 0:
                        gamestack.all_cards.pop()

                    input("Press Enter to continue...")
                    clear()
                    continue

                #check if ten is used, and if that 10 is actually playable on the previous card
                if gamestack.ten() and not gamestack.compare(): #REQ15 3
                    deal(phand, gamedeck)
                    print("BURN")

                    # empty the stack
                    while len(gamestack.all_cards) > 0:
                        gamestack.all_cards.pop()

                    input("Press Enter to continue...")
                    clear()
                    continue

                #if player plays an 8, they get another turn
                if gamestack.eight() and not gamestack.compare(): #REQ14 2
                    deal(phand, gamedeck)
                    print("8 skips!")

                    input("Press Enter to continue...")
                    clear()
                    continue

                # compare the card to the one below, returns true if the card is too low
                if gamestack.compare():
                    # if it's a 2 or 3, then it's playable anywhere
                    if gamestack.magic2(): #REQ11 1
                        sval = gamestack.all_cards[0].value

                        deal(phand, gamedeck)
                        input("Press Enter to continue...")
                        clear()
                        playerTurn = False
                        continue
                        # used to be pass

                    #not sure if this still needs to be here actually
                    elif gamestack.magic3(): #REQ12 1
                        if len(gamestack.all_cards) > 1:
                            gamestack.correct3()
                            print("The 3 is now a", gamestack.all_cards[0].value, "!")
                            sval = gamestack.all_cards[0].value

                            deal(phand, gamedeck)
                            input("Press Enter to continue...")
                            clear()
                            playerTurn = False
                            continue

                    # if it's not playable, send it back
                    else:
                        print("That card is too low!")
                        gamestack.send_back(phand)
                        phand.return3()

                        #print(f"Stack Value: {sval}!")
                        # pass
                        input("Press Enter to continue...")
                        clear()
                        continue

                #deal if necessary
                #deal(phand, gamedeck)#RED9 5

            deal(phand, gamedeck)
            input("Press Enter to continue...")
            clear()
            playerTurn = False
            continue

        # opponents turn
        elif not playerTurn:

            #turncount = 0
            gamestack.correct3()
            ohand.return3()
            ohand.sorthand()

            #show their cards for testing
            '''print("opponents cards")
            for a in range(0, len(ohand.cards)):
                print("    ", a, ':', ohand.cards[a])
            print(len(ohand.cards), "cards!")'''

            print("Opponents turn!")

            #if no cards in the stack
            if not len(gamestack.all_cards): #REQ7 4

                #if no cards in deck
                if deckempty: #REQ8 2
                    print("Deck empty! Opponent will start")

                    gamestack.all_cards.insert(0, ohand.playcard(2))

                    #deal if necessary
                    dealo(ohand, gamedeck)
                    #print("390")

                    #check if opponent played an 8 and it was legal, skip if so
                    if gamestack.eight(): #REQ14 3
                        print("8 skips!")
                        input("Press Enter to continue...")
                        clear()
                        continue

                    if gamestack.ten():  # REQ15 4
                        print("BURN")
                        # empty the stack
                        while len(gamestack.all_cards) > 0:
                            gamestack.all_cards.pop()

                        input("Press Enter to continue...")
                        clear()
                        continue

                    #continue to players turn
                    playerTurn = True
                    continue


                #if deck isn't empty, starter card method starts the round and continues so that opponent has something to play on
                elif not deckempty: #REQ10 2
                    gamestack.starter_card(gamedeck)
                    continue




            # show the stack
            showstack(ohand)

            '''
            test
            if not canplay(ohand):
                print(" UH OH! ")
            '''

            # if the top of the stack is a 7
            if gamestack.seven(): #REQ13 2
                print("Opponent must play lower than a 7!")

                # need to check if the player actually has anything lower than a 7
                if ohand.canplay7() == 100:  # phand returns positively
                    # print("You can play something under a 7!")
                    pass

                #if opponent has nothing to play on a 7, pick up stack and skip to playerturn
                elif not ohand.canplay7():

                    if ohand.handempty() and len(ohand.faceups):
                        print("Opponents face up cards: ")
                        for a in range(0, len(ohand.faceups)):
                            print("    ", a, ':', ohand.faceups[a])

                    print("Opponent has no cards under 7! Picking up")
                    gamestack.bad_hand(ohand)

                    input("Press Enter to continue...")
                    clear()
                    playerTurn = True
                    continue

                # gamestack.all_cards.insert(0,ohand.select_card())
                if int(sval) == 7: #i don't think this needs to be in its own indented block

                    if ohand.facedowncards(): #if facedowns are playable; play them and evlauate
                        gamestack.all_cards.insert(0, ohand.playcard(sval))

                        if not gamestack.comp7() or gamestack.all_cards[0].value in [2,3]:
                            print("And it is playable!")

                        elif gamestack.comp7() and gamestack.all_cards[0].value not in [2,3]:
                            print("And it is not playable! Picking up")
                            gamestack.bad_hand(ohand)

                            input("Press Enter to continue...")
                            clear()
                            playerTurn = True
                            continue

                    else: #otherwise, just default
                        #now using playcard function to select card, fewer lines of code than before
                        gamestack.all_cards.insert(0, ohand.playcard(sval))

                    dealo(ohand,gamedeck)

                    if gamestack.multi3(): #REQ12 3
                        print("The 3 is now a 7! 444")
                        gamestack.correct3()
                        sval = 7
                        input("Press Enter to continue...")
                        clear()
                        playerTurn = True
                        continue

                    #check if opponent played a 3, set that 3 to 7 and continue to playerturn if so
                    if gamestack.magic3(): #REQ12 4
                        gamestack.correct3()
                        gamestack.all_cards[0].value = 7
                        sval = gamestack.all_cards[0].value
                        print("The 3 is now a 7!")

                        input("Press Enter to continue...")
                        clear()
                        playerTurn = True
                        continue

                    #check if oppopnent burns by playing a 4th 7, skip players turn if so
                    if gamestack.burn(): #REQ19 3
                        print(gamestack.all_cards[0].rank, "* 4!!")
                        print("BURN")
                        # empty the stack
                        while len(gamestack.all_cards) > 0:
                            gamestack.all_cards.pop()

                        input("Press Enter to continue...")
                        clear()
                        continue

                    input("Press Enter to continue...")
                    clear()
                    playerTurn = True
                    continue

                # if a 7 is played on a 7, go back
                if gamestack.multi7():
                    input("Press Enter to continue...")
                    clear()
                    playerTurn = True
                    continue

                if len(gamestack.all_cards) > 1:

                    # comp7 returns true if something higher is played on a 7, don't think this actually needs to be
                    #here as opponent won't attempt to play lower than a 7 unless it's 2 or 3, already coded above
                    if gamestack.comp7():
                        print("That is not lower than a 7!")
                        gamestack.send_back(ohand)
                        ohand.return3()
                        # showstack(phand)
                        continue

                    # if it returns false, the card is lower and therefore valid to play
                    elif not gamestack.comp7():
                        print("Opponent played lower than a 7")

                        input("Press Enter to continue...")
                        clear()
                        playerTurn = False
                        continue

            # if a ten is played
            if gamestack.ten(): #REQ15 4
                print("BURN")
                # empty the stack
                while len(gamestack.all_cards) > 0:
                    gamestack.all_cards.pop()

                input("Press Enter to continue...")
                clear()
                continue

            # test hand, pick up if not playable and skip to player turn
            if not canplay(ohand):

                if ohand.handempty() and len(ohand.faceups):
                    print("Opponents face up cards: ")
                    for a in range(0, len(ohand.faceups)):
                        print("    ", a, ':', ohand.faceups[a])

                print("Opponent cannot play any cards! Picking up")
                gamestack.bad_hand(ohand)
                ohand.return3()

                input("Press Enter to continue...")
                clear()
                playerTurn = True
                continue

            # if hand is playable
            elif canplay(ohand):

                #check sval is not a special one
                if int(sval) in [2, 3, 4, 5, 6, 8, 9, 11, 12, 13, 14]:

                    if ohand.facedowncards():
                        gamestack.all_cards.insert(0, ohand.playcard(sval))
                        if not gamestack.compare() or gamestack.all_cards[0].value in [2,3]:
                            print("And it is playable!")

                        elif gamestack.compare() and gamestack.all_cards[0].value not in [2,3]:
                            print("And it is not playable! Picking up")
                            gamestack.bad_hand(ohand)

                            input("Press Enter to continue...")
                            clear()
                            playerTurn = True
                            continue


                    else:
                        # function to select opponents card
                        gamestack.all_cards.insert(0, ohand.playcard(sval))

                    dealo(ohand,gamedeck)

                    if gamestack.multi3(): #if a 3 is played on a 3, somehow messes up without this, REQ12 5
                        gamestack.correct3()
                        print("The 3 is now a", gamestack.all_cards[0].value, "!")
                        sval = gamestack.all_cards[0].value

                        input("Press Enter to continue...")
                        clear()
                        playerTurn = True
                        continue

                    #if opponent plays 4th x in a row
                    if gamestack.burn(): #REQ19 4
                        print(gamestack.all_cards[0].rank, "* 4!!")
                        print("BURN")
                        # empty the stack
                        while len(gamestack.all_cards) > 0:
                            gamestack.all_cards.pop()

                        input("Press Enter to continue...")
                        clear()
                        continue

                    #gamestack.all_cards.insert(0, ohand.select_card())

                    #show cards after playing (for testing purposes)
                    '''print("opponents cards after playing")
                    for a in range(0, len(ohand.cards)):
                        print("    ", a, ':', str(ohand.cards[a]))
                    print(len(ohand.cards), "cards!")'''

                    #if opponent plays a ten legally
                    if gamestack.ten() and not gamestack.compare(): #REQ15 5
                        print("BURN")
                        # empty the stack
                        while len(gamestack.all_cards) > 0:
                            gamestack.all_cards.pop()

                        input("Press Enter to continue...")
                        clear()
                        continue

                    #if opponent plays a legal 8, skip players turn and opponent plays again
                    if gamestack.eight() and not gamestack.compare(): #REQ14 4
                        print("8 skips!")
                        input("Press Enter to continue...")
                        clear()
                        continue

                    #compare the card they played
                    if gamestack.compare():
                        # if it's a 2 or 3, then it's playable anywhere
                        if gamestack.magic2(): #REQ11 2

                            input("Press Enter to continue...")
                            clear()
                            playerTurn = True
                            continue
                            # used to be pass

                        elif gamestack.magic3(): #REQ12 6
                            if len(gamestack.all_cards) > 1:
                                gamestack.correct3()
                                print("The 3 is now a", gamestack.all_cards[0].value, "!")
                                sval = gamestack.all_cards[0].value
                                #values[gamestack.all_cards[0].rank] = sval

                                input("Press Enter to continue...")
                                clear()
                                playerTurn = True
                                continue


            input("Press Enter to continue...")
            clear()
            playerTurn = True

    yn = str(input("Thank you for playing Stackhead! Would you like to play again? y/n"))

    if yn == 'y' or yn == 'Y':
        continue
    else:
        break