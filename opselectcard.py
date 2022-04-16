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

            if not self.handempty():
                for a in range(0, int(len(self.cards))):  # go through hand and append playable cards
                	if values[self.cards[a].rank] in [2,3]:
                		subchoices.append(self.cards[a])
                    elif values[self.cards[a].rank] >= sval and values[self.cards[a].rank] not in [2, 3]:
                        choices.append(self.cards[a])

                if not len(choices):
                	print("Opponent plays the", subchoices[-1], "!")  # play lowest playable card
                	return subchoices.pop(-1)

                else:
                	print("Opponent plays the", choices[-1], "!")  # play lowest playable card

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
                    if values[self.faceups[a].rank] >= sval or values[self.faceups[a].rank] in [2, 3]:
                        choices.append(self.faceups[a])

                print("Opponent plays the", choices[-1], "!")  # play lowest playable card

                for a in self.faceups:  # go through cards, remove the played card
                    if str(a) == str(choices[-1]):
                        # print("MATCH")
                        self.faceups.remove(a)

            return choices.pop(-1)
