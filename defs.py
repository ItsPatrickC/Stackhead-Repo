#function to deal a stackhead hand to a given player
def deal_sh_hand(player,deck):
    #REQ2 is met here
    player.add_card(deck.deal())
    player.add_card(deck.deal())
    player.add_card(deck.deal())
    player.face_ups(deck.deal())
    player.face_ups(deck.deal())
    player.face_ups(deck.deal())
    player.face_downs(deck.deal())
    player.face_downs(deck.deal())
    player.face_downs(deck.deal())

def rules():
    print("These are the rules of Stackhead")
    print("When a card is played, the next player must play a card on top!")
    print("The card played on top must be of equal or greater value than the card below")
    print("If the player has no card that is equal to or greater, they must pick up the stack")
    print("and add it to their hand!")
    print("There are a few exceptions though!")
    print("A 2 can be played on anything, resetting the stack")
    print("A 3 is invisible, acting the same as the card below it")
    print("A 7 means the next player must play a lower card")
    print("An 8 skips the next turn")
    print("A 10 burns, taking the cards in the stack out of the game")


def deal(hand,deck):

    # and less than 3 cards in hand, deal a card
    while len(hand.cards) < 3 and len(deck.all_cards):
        print(f"dealing you the {deck.all_cards[-1]}, {len(deck.all_cards)-1} cards remaining")
        hand.add_card(deck.deal())
    #print(len(hand.cards), "in ur hand")

def dealo(hand,deck):

    # and less than 3 cards in hand, deal a card
    while len(hand.cards) < 3 and len(deck.all_cards):
        print(f"dealing opponent the {deck.all_cards[-1]}, {len(deck.all_cards)-1} cards remaining")
        hand.add_card(deck.deal())
    print(len(hand.cards), "in opponents hand")
