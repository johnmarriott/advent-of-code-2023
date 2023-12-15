#!/usr/bin/env python

# big idea:
# turn each line into hand = (strength, cards, values, bid) where 
# strength is the strength of the hand type (high card = 1, ..., four of a kind = 7)
# cards is the character value of the card
# values is the numeric value of the card (see face_card_values)
# and bid is as defined
#
# then ascending sort by strength/cards[0] .. cards[4] and the score is sort rank * bid

import fileinput
import pprint
from collections import Counter

# a ten is a "face card" here
face_card_values = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
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

def strength_of_values(values):
    frequencies = Counter(values) # turns `[13, 10, 3, 3, 2]` into `Counter({3: 2, 13: 1, 10: 1, 2: 1})`
    frequency_list = sorted(list(frequencies.values())) # list and sort it into [1,1,2,2]
    frequency_string = ','.join(str(x) for x in frequency_list) # turn it into "1,1,2,2"
    strength = value_strengths[frequency_string]

    return strength

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

    strength = strength_of_values(values)

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