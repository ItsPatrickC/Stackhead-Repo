import random
global sval
import os
global magics
#for generating cards/decks
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ( 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':11,
         'Queen':12, 'King':13, 'Ace':14}

clear = lambda: os.system('cls')


class Card:
    '''
    card class
    is a class for card isntances
    '''

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit #+ "(" + str(self.value) + ")"


class Deck:
    '''
    REQ1 is met here

    '''

    def __init__(self):
        # Note this only happens once upon creation of a new Deck
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                # This assumes the Card class has already been defined!
                self.all_cards.append(Card(suit, rank))

    def __str__(self):
        for a in range(0, len(self.all_cards)):
            print(self.all_cards[a])
        return str(len(self.all_cards))

    def shuffle(self):
        #REQ3 is met here
        random.shuffle(self.all_cards)

    def deal(self):
        #REQ2 is met here
        # Note we remove one card from the list of all_cards
        # player.add_card(self.all_cards.pop())
        if len(self.all_cards):
            return self.all_cards.pop()
        else:
            pass


class Hand:
    '''
    REQ6 is met in the following methods:
        canplay()
        canplay7()

    '''

    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.facedowns = []
        self.faceups = []

    def win(self):
        if self.handempty() and not len(self.faceups) and not len(self.facedowns):
            return True
        else:
            return False

    def handempty(self):
        if not len(self.cards):
            return True
        else:
            return False

    def facedowncards(self):
        if self.handempty() and not len(self.faceups):
            #print("These ones!")
            return True
        else:
            return False

    # ranks function will take a card, and return its value, used for the sorthand method
    def ranks(self, card):
        # a = card.rank
        a = card.value
        return a

    def sorthand(self):
        self.cards.sort(key=self.ranks, reverse=True)
        self.faceups.sort(key=self.ranks, reverse=True)
        # using the built in list sort method, but with a key of ranks,
        # this will sort the hand by value

    # this method, checks if a hand has a 3 in it,
    # if so, it resets the 3's value to 3 (as when played, it takes on the value of the card below)
    def return3(self):
        for a in range(0, len(self.cards)):
            # print("return3", self.cards[a].value)
            # print("return3", self.cards[a])
            # print("return3", self.cards[a].rank)
            if self.cards[a].rank == 'Three' or values[self.cards[a].rank] == 3:
                # print("current 3 rank", values[self.cards[a].rank])
                # print("Three!!")
                self.cards[a].value = 3
                # print("new 3 rank", values[self.cards[a].rank])

    def add_card(self, card):
        # used to add cards to the initial hand
        self.cards.append(card)

    def face_ups(self, card):
        # used to add cards to face ups
        self.faceups.append(card)

    def face_downs(self, card):
        # used to add cards to face downs
        self.facedowns.append(card)

    # used to get the maximum value from players hand, 2 or 3 are playable on anything so will return 200 & 300 respectively
    def canplay(self):
        b = 0
        if self.facedowncards():
            b = 1000
        else:
            if self.handempty(): #if no cards in hand
                if len(self.faceups): #but cards in faceups, test for playability
                    for a in range(0, len(self.faceups)):
                        # print(b, "   ", values[self.cards[a].rank])
                        if values[self.faceups[a].rank] >= b:
                            b = values[self.faceups[a].rank]
                        if values[self.faceups[a].rank] == 2:
                            b = 200
                            # print("You have a 2")
                        if values[self.faceups[a].rank] == 3:
                            b = 300
            elif not self.handempty(): #if cards in hand, test for playability
                for a in range(0, len(self.cards)):
                    # print(b, "   ", values[self.cards[a].rank])
                    if values[self.cards[a].rank] >= b:
                        b = values[self.cards[a].rank]
                    if values[self.cards[a].rank] == 2:
                        b = 200
                        # print("You have a 2")
                    if values[self.cards[a].rank] == 3:
                        b = 300

        return b

    # used to test the hand to see if there are any cards equal to or lesser than 7
    def canplay7(self):
        b = 0
        if self.facedowncards():
            b = 100
        else:
            if not self.handempty():
                for a in range(0, len(self.cards)):
                    if values[self.cards[a].rank] <= 7:
                        b = 100
            elif self.handempty():
                if len(self.faceups):
                    for a in range(0, len(self.faceups)):
                        if values[self.faceups[a].rank] <= 7:
                            b = 100

        return b

    # function for the player to select which card to play
    def select_card(self):
        #REQ4 is met here #test comment
        self.sorthand()
        if self.facedowncards():
            print("You must choose from your face down cards:")
            for a in range(0,len(self.facedowns)):
                print("    ", "Hidden card", a)
                if self.facedowns[a].value == 10:
                    print("ten!")
                else:
                    print("not ten")
            self.selection = int(input(f"Which card would you like to play? 0 - {int(len(self.facedowns) - 1)}"))
            print("The hidden card is the", self.facedowns[self.selection], "!")
            return self.facedowns.pop(self.selection)

        else:
            if not self.handempty():
                print("Your hand: ")
                for a in range(0, len(self.cards)):
                    print("    ", a, ':', self.cards[a])

                while True:
                    try:
                        self.selection = int(input(f"Which card would you like to play? 0 - {int(len(self.cards) - 1)}"))
                        # return str(self.cards[self.selection])
                        return self.cards.pop(self.selection)
                        break
                    except:
                        #clear()
                        print("YOU MUST INPUT AN INTEGER BETWEEN 0 AND", int(len(self.cards) - 1))
                        #input("Press Enter to continue...")

            elif self.handempty():
                if len(self.faceups):
                    print("No cards in hand!")
                    print("Your face up cards: ")
                    for a in range(0, len(self.faceups)):
                        print("    ", a, ':', self.faceups[a])
                    self.selection = int(input(f"Which card would you like to play? 0 - {int(len(self.faceups) - 1)}"))
                    return self.faceups.pop(self.selection)

    def summary(self):
        b = ""  # this variable is just used for the return, otherwise calling the __str__ prints out 'None' after everything else
        # is basically the __str__ special function, but too much going on to not throw up type error
        # print(int(len(self.cards)))
        print("Your hand: ")
        for a in range(0, len(self.cards)):
            print("    ", self.cards[a])
        print("Face ups: ")
        for a in range(0, len(self.faceups)):
            print("    ", self.faceups[a])
        print("Face downs: ")
        for a in range(0, len(self.facedowns)):
            print("    ", "<hidden card>")

        # self.return3()
        return b

    def __str__(self):
        # return str of summary function so can easily return more in less lines
        return str(self.summary())

    #function for the opponent to select which card to play
    def playcard(self, sval):
        '''simplified, and more flexible version of the playables method I was using before
        method now takes in sval as an arg, already having determined if it's hand is playable or not (canplay()).
        Also usable for seven() so saves lots of lines of code in the main file

        - Method loops through hand/faceups, appending playable cards to choices list,
        - lowest card from choices is used
        - loop back through cards, remove the one that matches the chosen card'''

        if int(sval) in [2, 3, 4, 5, 6, 8, 9, 11, 12, 13, 14]:

            choices = [] #initiate choices list
            subchoices = [] #initiate subchoices list

            if self.facedowncards():
                print("Opponent will choose from their facedown cards!")
                for a in range(0, len(self.facedowns)): #show how many facedown cards they have
                    print("    ", "Hidden card", a)
                rchoice = random.choice(self.facedowns) #choose one using the random.choice method
                print("Opponent has chosen", rchoice, "!") #print that
                choices.append(rchoice)#put it in choices

                for a in self.facedowns:#remove it from their facedowns
                    if str(a) == str(choices[-1]):
                        # print("MATCH")
                        self.facedowns.remove(a)

                return choices.pop(-1)


            else:

                if not self.handempty():
                    for a in range(0, int(len(self.cards))):  # go through hand and append playable cards
                        if values[self.cards[a].rank] >= sval and values[self.cards[a].rank] not in [2,3]:  # otherwise if playable but not 2 or 3, place in choices
                            choices.append(self.cards[a])
                        elif values[self.cards[a].rank] in [2,3]: #if cards are 2 or 3, place in subchoices
                            subchoices.append(self.cards[a])

                    if len(choices): #if playable cards above 2 or 3, play them
                        print("Opponent plays the", choices[-1], "!")  # play lowest playable card

                    elif not len(choices): #if no playable cards above 2 or 3, take from subchoices
                        choices.append(subchoices[-1])
                        print("Opponent plays the", choices[-1], "!")  # play lowest playable card

                    if len(choices):
                        for a in self.cards:  # go through cards, remove the played card
                            if str(a) == str(choices[-1]):
                                # print("MATCH")
                                self.cards.remove(a)

                elif self.handempty():
                    print("Opponents hand empty!")
                    print("Opponents faceup cards:")
                    for a in self.faceups:
                        print("    ", str(a))

                    for a in range(0, int(len(self.faceups))):  # go through faceups and append playable cards
                        if values[self.faceups[a].rank] >= sval and values[self.faceups[a].rank] not in [2, 3]:
                            choices.append(self.faceups[a])
                        elif values[self.faceups[a].rank] in [2,3]:
                            subchoices.append(self.faceups[a])

                    if len(choices):  # if playable cards above 2 or 3, play them
                        print("Opponent plays the", choices[-1], "!")  # play lowest playable card

                    elif not len(choices):  # if no playable cards above 2 or 3, take from subchoices
                        choices.append(subchoices[-1])
                        print("Opponent plays the", choices[-1], "!")  # play lowest playable card

                    if len(choices):
                        for a in self.cards:  # go through cards, remove the played card
                            if str(a) == str(choices[-1]):
                                # print("MATCH")
                                self.cards.remove(a)

                    for a in self.faceups:  # go through cards, remove the played card
                        if str(a) == str(choices[-1]):
                            # print("MATCH")
                            self.faceups.remove(a)

            return choices.pop(-1)

        elif int(sval) == 7:

            choices = []  # initiate choices list
            subchoices = []  # initiate subchoices list

            if self.facedowncards():
                print("Opponent will choose from their facedown cards!")
                for a in range(0, len(self.facedowns)): #show how many facedown cards they have
                    print("    ", "Hidden card", a)
                rchoice = random.choice(self.facedowns) #choose one using the random.choice method
                print("Opponent has chosen", rchoice, "!") #print that
                choices.append(rchoice)#put it in choices

                for a in self.facedowns:#remove it from their facedowns
                    if str(a) == str(choices[-1]):
                        # print("MATCH")
                        self.facedowns.remove(a)

                return choices.pop(-1)

            else:

                if not self.handempty():
                    for a in range(0, int(len(self.cards))):  # go through hand and append playable cards
                        if values[self.cards[a].rank] <= sval and values[self.cards[a].rank] not in [2,3]:  # otherwise if playable but not 2 or 3, place in choices
                            choices.append(self.cards[a])
                        elif values[self.cards[a].rank] in [2, 3]:  # if cards are 2 or 3, place in subchoices
                            subchoices.append(self.cards[a])

                    if len(choices):  # if playable cards above 2 or 3, play them
                        print("Opponent plays the", choices[-1], "!")  # play lowest playable card

                    elif not len(choices):  # if no playable cards above 2 or 3, take from subchoices
                        choices.append(subchoices[-1])
                        print("Opponent plays the", choices[-1], "!")  # play lowest playable card

                    if len(choices):
                        for a in self.cards:  # go through cards, remove the played card
                            if str(a) == str(choices[-1]):
                                # print("MATCH")
                                self.cards.remove(a)

                elif self.handempty():
                    print("Opponents hand empty!")
                    print("Opponents faceup cards:")
                    for a in self.faceups:
                        print("    ", str(a))

                    for a in range(0, int(len(self.faceups))):  # go through faceups and append playable cards
                        if values[self.faceups[a].rank] <= sval and values[self.faceups[a].rank] not in [2, 3]:
                            choices.append(self.faceups[a])
                        elif values[self.faceups[a].rank] in [2, 3]:
                            subchoices.append(self.faceups[a])

                    if len(choices):  # if playable cards above 2 or 3, play them
                        print("Opponent plays the", choices[-1], "!")  # play lowest playable card

                    elif not len(choices):  # if no playable cards above 2 or 3, take from subchoices
                        choices.append(subchoices[-1])
                        print("Opponent plays the", choices[-1], "!")  # play lowest playable card

                    if len(choices):
                        for a in self.cards:  # go through cards, remove the played card
                            if str(a) == str(choices[-1]):
                                # print("MATCH")
                                self.cards.remove(a)

                    for a in self.faceups:  # go through cards, remove the played card
                        if str(a) == str(choices[-1]):
                            # print("MATCH")
                            self.faceups.remove(a)

            return choices.pop(-1)



class Stack(Deck):  # might need to inherit from hand instead
    '''
    REQ5 is met here in the methods listed below:
        compare()
        comp7()
        bad_hand()
        send_back()
        multi7()
    '''

    def __init__(self):
        # print("Game stack!")
        self.all_cards = []

    # deals a card to the stack to start a round
    def starter_card(self, deck):
        if len(deck.all_cards):
            print(f"Starting stack card: {deck.all_cards[-1]}, {len(deck.all_cards) - 1} cards remaining")
            self.all_cards.append(deck.deal())
            if self.all_cards[0].rank == 'Three':
                self.all_cards[0].value = 3
        else:
            pass



    # function to add card to top of deck
    # needs to take card argument from player hand
    def add_card(self, player, card):
        self.all_cards.append(player.select_card())

    def burn(self):
        if len(self.all_cards) >= 4:

            b = 0
            burn = self.all_cards[0].rank

            for a in self.all_cards:
                if a.rank == burn:
                    b += 1
                elif a.rank != burn:
                    break

            if b == 4:
                return True
            else:
                return False

    # check if top cards are 2 or 3, return true if so
    def magic2(self):
        # 2 just resets the stack, not too complicated
        if values[self.all_cards[0].rank] == 2:
            # print("AAAAAA", values[self.all_cards[0].rank])
            return True

        else:
            return False

    def magic3(self):
        # 3 takes on the value of the card below it
        if values[self.all_cards[0].rank] == 3 or self.all_cards[0].rank == 'Three':
            self.all_cards[0].value = self.all_cards[1].value
            return True

    def correct3(self):
        if len(self.all_cards) > 1:
            if values[self.all_cards[0].rank] == 3 or self.all_cards[0].rank == 'Three':
                self.all_cards[0].value = self.all_cards[1].value
                #print(values[self.all_cards[0].rank])

    def multi3(self):
        if len(self.all_cards) > 1:
            if self.all_cards[0].rank == 'Three' and self.all_cards[1].rank == 'Three':
                return True
            else:
                pass


    def eight(self):
        if len(self.all_cards):
            if values[self.all_cards[0].rank] == 8:
                return True



    def ten(self):
        if len(self.all_cards):
            if values[self.all_cards[0].rank] == 10:
                return True

    # returns true if the top of the stack is 7
    def seven(self):
        # check if there's cards on the stack
        if len(self.all_cards):
            # if so, return true if a 7 is on the top
            if self.all_cards[0].value == 7:
                return True
            else:
                return False

    # compares a card played, against the 7 below it, only used if seven() is true
    def comp7(self):
        # check if cards are in stack
        if len(self.all_cards) > 0:
            # if a card higher than 7 is played, return true, else return false
            if self.all_cards[0].value > self.all_cards[1].value:
                return True
            else:
                pass

    # if a 7 is played on a 7
    def multi7(self):
        if len(self.all_cards) >= 2:
            if values[self.all_cards[0].rank] == 7 and values[self.all_cards[1].rank] == 7:
                return True

    # function for comparing the top card against the second top card
    def compare(self):
        # if rank is lower than the previous card, return true
        if len(self.all_cards):
            if self.all_cards[0].value < self.all_cards[1].value:
                return True

    # not actually used?
    def pick_up(self, player):
        for a in range(0, len(self.all_cards)):
            print(f"{self.all_cards[0]} is lower than {self.all_cards[1]}! You have to pick up!")
            player.cards.append(self.all_cards.pop())

    # is used to give the stack to a player in the event their hand is unplayable
    def bad_hand(self, player):
        for a in range(0, len(self.all_cards)):
            player.cards.append(self.all_cards.pop())

    # used in the event a player tries an unplayable card, it sends it back
    def send_back(self, player):
        player.cards.append(self.all_cards.pop(0))

    def send_back_fu(self, player):
        player.faceups.append(self.all_cards.pop(0))

    # prints the hand
    def summary(self):
        for a in range(0, len(self.all_cards)):
            print(str(self.all_cards[a]))

    # returns a string of summary() to get round the none error
    def __str__(self):
        return str(self.summary())
