#!/usr/bin/env python

# big idea:
# turn each line into hand = (strength, cards, values, bid) where 
# strength is the strength of the hand type (high card = 1, ..., four of a kind = 7)
# cards is the character value of the card
# values is the numeric value of the card (see face_card_values)
# and bid is as defined
#
# then ascending sort by strength/cards[0] .. cards[4] and the score is sort rank * bid
#
# for part 2:
# do JJJJJ directly
# if a hand has 1--4 Js, rank the hand as if Js are highest-valued card in hand

import fileinput
import pprint
from collections import Counter

# a ten is a "face card" here
face_card_values = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 1,
    "T": 10
}

value_strengths = {
    "1,1,1,1,1": 1, # high card
    "1,1,1,2": 2, # one pair
    "1,2,2": 3, # two pair
    "1,1,3": 4, # three of a kind
    "2,3": 5, # full house
    "1,4": 6, # four of a kind
    "5": 7 # five of a kind
}

def wildcard_strength_of_values(values):
    if not face_card_values["J"] in values: # there are no wild cards in the hand
        strength = strength_of_values(values)
        return strength
    elif values == [face_card_values["J"]] * 5: # special case for five wild cards
        return value_strengths["5"]
    else: # there are between one and four wild cards
        # given these hand types, the best version of this hand is the one
        # with all wildcards turned into the highest-valued card of
        # the highest-frequency card in the hand

        frequencies_values = frequencies_values_of_values(values)
        max_frequency = sorted(frequencies_values.keys(), reverse=True)[0]
        max_frequency_max_value = sorted(frequencies_values[max_frequency], reverse=True)[0]

        if max_frequency_max_value == face_card_values["J"]:
            # for a hand like 234JJ, don't want to see J as the max freq max value to use
            # go to next index of frequencies_values since if J was first in sorted
            # frequencies_values there isn't another one behind it
            max_frequency = sorted(frequencies_values.keys(), reverse=True)[1]
            max_frequency_max_value = sorted(frequencies_values[max_frequency], reverse=True)[0]

        # change wildcards to the strength-maximizing value
        for i in range(len(values)):
            if values[i] == face_card_values["J"]:
                values[i] = max_frequency_max_value

        # rate the hand with wildcards as max values
        strength = strength_of_values(sorted(values, reverse=True))
        return strength

def strength_of_values(values):
    frequencies = Counter(values) # turns `[13, 10, 3, 3, 2]` into `Counter({3: 2, 13: 1, 10: 1, 2: 1})`
    frequency_list = sorted(list(frequencies.values())) # list and sort it into [1,1,2,2]
    frequency_string = ','.join(str(x) for x in frequency_list) # turn it into "1,1,2,2"
    strength = value_strengths[frequency_string]
    return strength

def frequencies_values_of_values(values):
    """
    get frequencies values of a list of values:
    
    [13, 10, 3, 3, 2] turns into [{2: [3], 1: [2, 10, 13]}]
    [5, 5, 6, 6, 3] turns into [{2: [5, 6], 1: [3]}]
    
    also get strength because it was here in the code,
    it would be cleaner if this were refactored
    """
    frequencies = Counter(values) # turns `[13, 10, 3, 3, 2]` into `Counter({3: 2, 13: 1, 10: 1, 2: 1})`

    # for each frequency (once, twice, ...) track the face value of cards of this frequency
    # so that we can then order within that frequency (e.g., a two pair is ordered KK883 not 88KK3)
    frequencies_values = {}
    for key, value in frequencies.items():
        if value in frequencies_values:
            frequencies_values[value].append(key)
        else:
            frequencies_values[value] = [key]

    return  frequencies_values

hands = []
for line in fileinput.input():
    info = line.split(" ")
    cards = list(info[0])
    bid = int(info[1])

    values = []
    for card in cards:
        if card.isnumeric():
            value = int(card)
        else:
            value = face_card_values[card]
        values.append(value)

    strength = wildcard_strength_of_values(values.copy())

    hands.append({
        "strength": strength,
        "cards": cards,
        "values": values,
        "bid": bid
    })

# sort by least to most important key 
hands.sort(key=lambda x: x["values"][4])
hands.sort(key=lambda x: x["values"][3])
hands.sort(key=lambda x: x["values"][2])
hands.sort(key=lambda x: x["values"][1])
hands.sort(key=lambda x: x["values"][0])
hands.sort(key=lambda x: x["strength"])

for i in range(len(hands)):
    rank = i + 1
    hands[i]["rank"] = rank
    hands[i]["winnings"] = rank * hands[i]["bid"]

total_winnings = sum([hand["winnings"] for hand in hands])

pprint.pprint(hands, compact=True, sort_dicts=False)

print(total_winnings)