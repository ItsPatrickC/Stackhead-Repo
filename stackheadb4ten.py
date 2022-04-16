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
    '''
    rulesyn = str(input("Would you like to know the rules first? y or n"))

    if rulesyn == 'y' or rulesyn == 'Y':
        rules()

    else:
        pass
    '''


    deckempty = False
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


    def showstack(hand):
        print("The Stack!")
        for a in range(0, len(gamestack.all_cards)):
            print("    ", gamestack.all_cards[a])

        if len(gamestack.all_cards) > 0:
            sval = values[gamestack.all_cards[0].rank]
            print(f"Stack Value: {sval}!")
            print(f"Hand value: {hand.canplay()}!")


    #print("HELLO ", sval)
    #print(f"Starting stack card: {gamestack.all_cards[0]}, {len(gamedeck.all_cards)} cards remaining line 73")

    playing = True

    # main loop
    while playing:

        if len(gamedeck.all_cards) == 0: #if the deck runs out of cards
            deckempty = True

        #print out how many cards in deck (for testing)
        print(len(gamedeck.all_cards), "cards in deck line 80")

        #set up sval, and make sure 3 is correct
        if len(gamestack.all_cards) != 0:
            sval = values[gamestack.all_cards[0].rank]

            if values[gamestack.all_cards[0].rank] == 3:
                print("something to see here")
                # check if there is actually a card below it first
                if len(gamestack.all_cards) > 1:
                    values[gamestack.all_cards[0].rank] = values[gamestack.all_cards[1].rank]
                    sval = values[gamestack.all_cards[1].rank]
                    print("3 corrected")
                else:
                    #print("nothing to see here")
                    pass

        #when it's the players turn
        if playerTurn:

            print("Your turn!")

            #deal a card if less than 3 in hand and cards still in deck
            if len(gamestack.all_cards) > 0:
                deal(phand,gamedeck)

            # if a turn begins, and no beginning card, deal one from the deck, if not then player starts game
            if not len(gamestack.all_cards): #check if stack is empty

                if deckempty: #if deck is empty, prompt player to play a card
                    print("Deck empty! Play a card")
                    gamestack.all_cards.insert(0, phand.select_card())

                    #check if it's ten
                    if gamestack.ten():
                        print("BURN")
                        # empty the stack
                        while len(gamestack.all_cards) > 0:
                            gamestack.all_cards.pop()
                        continue
                    elif not gamestack.ten():
                        input("Press Enter to continue...")
                        clear()
                        playerTurn = False
                        continue

                    input("Press Enter to continue...")
                    clear()
                    playerTurn = False
                    continue

                elif not deckempty: #if cards in deck, use top one
                    gamestack.starter_card(gamedeck)
                    #sval = values[gamestack.all_cards[0].rank]
                    #print(len(gamedeck.all_cards), "cards in deck")
                    continue

            # show the stack
            phand.return3()
            showstack(phand)

            # if the top of the stack is a 7, this section deals with it
            if gamestack.seven():
                print("You must play lower than a 7!")


                # need to check if the player actually has anything lower than a 7
                if phand.canplay7() == 100:  # phand returns positively
                    # print("You can play something under a 7!")
                    pass  # is pass right to use?
                else:
                    print("You have no cards under 7! Pick up")
                    gamestack.bad_hand(phand)
                    phand.return3()
                    continue

                gamestack.all_cards.insert(0, phand.select_card())

                '''if gamestack.ten():
                    print("BURN")
                    # empty the stack
                    while len(gamestack.all_cards) > 0:
                        gamestack.all_cards.pop()
                    continue
                elif not gamestack.ten():
                    playerTurn = False
                    continue'''

                # if a 7 is played on a 7, go back
                if gamestack.multi7():
                    input("Press Enter to continue...")
                    clear()
                    playerTurn = False
                    continue

                # comp7 returns true if something higher is played on a 7
                if gamestack.comp7():
                    print("That is not lower than a 7!")
                    gamestack.send_back(phand)
                    phand.return3()
                    # showstack(phand)
                    continue

                # if it returns false, the card is lower and therefore valid to play
                elif not gamestack.comp7():
                    print("That is lower than a 7!")
                    if len(phand.cards) < 3 and not deckempty:  # deal a card if less than 3 in hand
                        deal(phand,gamedeck)
                        #phand.add_card(gamedeck.deal())

                    # if a 3 is played on a 7
                    if values[gamestack.all_cards[0].rank] == 3 and values[gamestack.all_cards[1].rank] == 7:
                        values[gamestack.all_cards[0].rank] = 7
                        sval = values[gamestack.all_cards[0].rank]
                        # showstack(phand)
                        input("Press Enter to continue...")
                        clear()
                        playerTurn = False
                        continue

                    input("Press Enter to continue...")
                    clear()
                    playerTurn = False
                    continue

                # if a 3 is played on a 7

            # if a ten is played
            if gamestack.ten():
                print("BURN")
                # empty the stack
                while len(gamestack.all_cards) > 0:
                    gamestack.all_cards.pop()
                continue

            # test hand, pick up if not playable and put a new starting card down
            if not canplay(phand):
                print("Cannot play these cards! Pick up")
                gamestack.bad_hand(phand)
                phand.return3()
                if not deckempty:
                    gamestack.starter_card(gamedeck)
                elif deckempty:
                    print("Play a card!")
                    gamestack.all_cards.insert(0, phand.select_card())
                    if gamestack.ten():
                        print("BURN")
                        # empty the stack
                        while len(gamestack.all_cards) > 0:
                            gamestack.all_cards.pop()
                        continue
                    '''elif not gamestack.ten():
                        playerTurn = False
                        continue'''

                #print(len(gamedeck.all_cards), "cards in deck")

                input("Press Enter to continue...")
                clear()
                playerTurn = False
                continue

            # if hand is playable
            elif canplay(phand):

                # player plays card
                gamestack.all_cards.insert(0, phand.select_card())

                #check if ten is used, and if that 10 is actually playable on the previous card
                if gamestack.ten() and not gamestack.compare():
                    print("BURN")
                    # empty the stack
                    while len(gamestack.all_cards) > 0:
                        gamestack.all_cards.pop()
                    continue
                '''elif not gamestack.ten():
                    playerTurn = False
                    continue'''

                # compare the card to the one below, returns true if the card is too low
                if gamestack.compare():
                    # if it's a 2 or 3, then it's playable anywhere
                    if gamestack.magics():
                        sval = values[gamestack.all_cards[0].rank]
                        print("The SVAL is now ", values[gamestack.all_cards[0].rank],"----", sval)

                        input("Press Enter to continue...")
                        clear()
                        playerTurn = False
                        continue
                        # used to be pass

                    # if it's not playable, send it back
                    else:
                        print("That card is too low!")
                        gamestack.send_back(phand)
                        phand.return3()
                        print(f"Stack Value: {sval}!")
                        # pass
                        continue

                deal(phand, gamedeck)

                # as long as there are still cards in the deck, and less than 3 in hand, deal a card
                if len(gamestack.all_cards) > 0:
                    if len(phand.cards) < 3 and not deckempty:
                        deal(phand,gamedeck)
                        #phand.add_card(gamedeck.deal())
                # continue

            # update sval as the stack will have a new card on top
            sval = values[gamestack.all_cards[0].rank]
            # phand.sorthand()
            # canplay(phand)

            '''if len(phand.cards) < 3 and len(gamedeck.all_cards) > 0:  # deal a card if less than 3 in hand
                print(f"dealing you the {gamedeck.all_cards[-1]}, {len(gamedeck.all_cards) - 1} cards remaining")
                phand.add_card(gamedeck.deal())'''

            if len(gamestack.all_cards) > 0:
                deal(phand,gamedeck)

            input("Press Enter to continue...")
            clear()
            playerTurn = False
            continue

        # opponents turn
        elif not playerTurn:

            #show their cards for testing
            '''print("opponents cards")
            for a in range(0, len(ohand.cards)):
                print("    ", a, ':', ohand.cards[a])
            print(len(ohand.cards), "cards!")'''

            ohand.return3()
            ohand.sorthand()

            print("Opponents turn!")

            if len(gamestack.all_cards):
                dealo(ohand,gamedeck)

            if not len(gamestack.all_cards):

                if deckempty:
                    print("Deck empty!")
                    playables = []  # init playables list

                    for a in range(0, len(ohand.cards)):  # loop thru hand and place in list

                        playables.append(ohand.cards.pop(0))

                    for b in range(0, len(playables)):  # loop thru playables list
                        if values[playables[b].rank] <= sval or values[playables[b].rank] in [2, 3]:  # check if playable on 7
                            pass
                        elif values[playables[b].rank] > sval:  # if not, place them back in hand
                            ohand.cards.append(playables.pop(b))
                            playables.insert(0, "placeholder")

                    print("Opponent plays the", playables[-1], "!")
                    gamestack.all_cards.insert(0, playables.pop(-1))

                    for a in playables:
                        if a != "placeholder":
                            ohand.cards.append(a)

                    dealo(ohand, gamedeck)

                elif not deckempty:
                    gamestack.starter_card(gamedeck)
                    #sval = values[gamestack.all_cards[0].rank]
                    continue

            # show the stack
            ohand.return3()
            showstack(ohand)
            if not canplay(ohand):
                print(" UH OH! ")

            # if the top of the stack is a 7, this section deals with it
            if gamestack.seven():
                print("Opponent must play lower than a 7!")

                # need to check if the player actually has anything lower than a 7
                if ohand.canplay7() == 100:  # phand returns positively
                    # print("You can play something under a 7!")
                    pass  # is pass right to use?

                #if opponent has nothing to play on a 7, pick up stack
                elif not ohand.canplay7():
                    print("Opponent has no cards under 7! Picking up")
                    gamestack.bad_hand(ohand)
                    ohand.return3()

                    input("Press Enter to continue...")
                    clear()
                    playerTurn = True
                    continue

                # gamestack.all_cards.insert(0,ohand.select_card())
                if int(sval) == 7:

                    playables = [] #init playables list

                    for a in range(0,len(ohand.cards)): #loop thru hand and place in list

                        playables.append(ohand.cards.pop(0))

                    for b in range(0,len(playables)): #loop thru playables list
                        if values[playables[b].rank] <= sval or values[playables[b].rank] in [2,3]: #check if playable on 7
                            pass
                        elif values[playables[b].rank] > sval: #if not, place them back in hand
                            ohand.cards.append(playables.pop(b))
                            playables.insert(0,"placeholder")

                    print("Opponent plays the", playables[-1], "!")
                    gamestack.all_cards.insert(0, playables.pop(-1))

                    for a in playables:
                        if a != "placeholder":
                            ohand.cards.append(a)

                    dealo(ohand,gamedeck)

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

                    # comp7 returns true if something higher is played on a 7
                    if gamestack.comp7():
                        print("That is not lower than a 7!")
                        gamestack.send_back(ohand)
                        ohand.return3()
                        # showstack(phand)
                        continue

                    # if it returns false, the card is lower and therefore valid to play
                    elif not gamestack.comp7():
                        print("Opponent played lower than a 7")

                        # if a 3 is played on a 7
                        if values[gamestack.all_cards[0].rank] == 3 and values[gamestack.all_cards[1].rank] == 7:
                            values[gamestack.all_cards[0].rank] = 7
                            sval = values[gamestack.all_cards[0].rank]
                            # showstack(phand)

                            input("Press Enter to continue...")
                            clear()
                            playerTurn = False
                            continue

                        #else:
                            #showstack(ohand)

                        input("Press Enter to continue...")
                        clear()
                        playerTurn = True
                        continue

            # if a ten is played
            if gamestack.ten():
                print("BURN")
                # empty the stack
                while len(gamestack.all_cards) > 0:
                    gamestack.all_cards.pop()
                continue

            # test hand, pick up if not playable and put a new starting card down
            if not canplay(ohand):
                print("Opponent cannot play any cards! Picking up")
                gamestack.bad_hand(ohand)
                ohand.return3()
                if not deckempty:
                    gamestack.starter_card(gamedeck)
                    #print(len(gamedeck.all_cards), "cards in deck")
                    # pass
                elif deckempty:
                    sval = 1
                    # print("Play a card!")
                    # gamestack.all_cards.insert(0,ohand.select_card())

                    playables = []
                    for a in range(0, len(ohand.cards)):
                        # print(ohand.cards[a])
                        # print(values[ohand.cards[a].rank])

                        # playables.append(values[ohand.cards[a].rank])
                        playables.append(ohand.cards.pop(0))



                    '''
                    showing what the opponent can play, used for testing
                    print("Opponent can play: ")
                    for a in playables:
                        print("    ", a)
                    '''
                    # print(min(playables))
                    # print()

                    print("Opponent plays the", playables[0], "!")

                    gamestack.all_cards.insert(0, playables.pop(-1))

                    while len(playables):
                        ohand.cards.append(playables.pop())

                    print("opponents cards after playing")
                    for a in range(0, len(ohand.cards)):
                        print("    ", a, ':', ohand.cards[a])
                    print(len(ohand.cards), "cards!")

                    if gamestack.ten():
                        print("BURN")
                        # empty the stack
                        while len(gamestack.all_cards) > 0:
                            gamestack.all_cards.pop()
                        continue
                    '''elif not gamestack.ten():
                        playerTurn = True
                        continue
                        '''



                input("Press Enter to continue...")
                clear()
                playerTurn = True
                continue

            # if hand is playable
            elif canplay(ohand):

                if int(sval) in [2, 3, 4, 5, 6, 8, 9, 11, 12, 13, 14]:

                    #inititalise list
                    playables = []
                    for a in range(0, len(ohand.cards)): #loop through cards

                        playables.append(ohand.cards.pop(0)) #put in playables

                    for b in range(0,len(playables)): #loop through playables, decide whether to keep or not
                        if values[playables[b].rank] >= sval or values[playables[b].rank] in [2,3]: #if playable
                            #print(playables[b], "is usable!") #leave in playables
                            pass
                        elif values[playables[b].rank] < sval: #if not
                            #print(playables[b], "is not usable!")
                            ohand.cards.append(playables.pop(b)) #place back in playerhand
                            playables.insert(0,"placeholder") #insert placeholder to avoid index error next go around

                    #opponent plays card
                    print("Opponent plays the", playables[-1], "!")
                    gamestack.all_cards.insert(0, playables.pop(-1))

                    #go thru playables, send back to hand if not a placeholder
                    for a in playables:
                        if a != "placeholder":
                            #print("HELLO", a)
                            ohand.cards.append(a)

                    #deal if necessary
                    dealo(ohand,gamedeck)

                    #show cards after playing (for testing purposes)
                    '''print("opponents cards after playing")
                    for a in range(0, len(ohand.cards)):
                        print("    ", a, ':', str(ohand.cards[a]))
                    print(len(ohand.cards), "cards!")'''

                    #if opponent plays a ten
                    if gamestack.ten():
                        print("BURN")
                        # empty the stack
                        while len(gamestack.all_cards) > 0:
                            gamestack.all_cards.pop()
                        continue
                    '''elif not gamestack.ten():
                        playerTurn = True
                        continue'''

                    #compare the card they played
                    if gamestack.compare():
                        # if it's a 2 or 3, then it's playable anywhere
                        if gamestack.magics():
                            sval = values[gamestack.all_cards[0].rank]
                            print("The SVAL is now ", values[gamestack.all_cards[0].rank],"----", sval)

                            input("Press Enter to continue...")
                            clear()
                            playerTurn = True
                            continue
                            # used to be pass
                        # if it's not playable, send it back

                if len(gamestack.all_cards) > 1:
                    if gamestack.compare():
                        # if it's a 2 or 3, then it's playable anywhere
                        if gamestack.magics():
                            sval = values[gamestack.all_cards[0].rank]
                            print("The SVAL is now ", values[gamestack.all_cards[0].rank],"----", sval)

                            input("Press Enter to continue...")
                            clear()
                            playerTurn = True
                            continue
                            # used to be pass
                        # if it's not playable, send it back


            # update sval as the stack will have a new card on top
            sval = values[gamestack.all_cards[0].rank]
            # phand.sorthand()
            # canplay(phand)

            input("Press Enter to continue...")
            clear()
            playerTurn = True
