import os

import itertools
import argparse

# Ranks and suits
RANKS = "AKQJT98765432"
SUITS = "shdc"  # spades, hearts, diamonds, clubs

def all_cards():
    return [r + s for r in RANKS for s in SUITS]

CARDS = all_cards()

class Card:
    rank = ''
    suit = ''

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    
    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit
    def __str__(self):        
        return self.rank + self.suit

# Input
# Card Input Are Rank Sorted
def canonical_equivalent(cardSeqL, cardSeqR):
    # Collect All suit in card SeqL
    
    canonicalSeqL = []
    for suit in SUITS:
        canonicalSeqL.append('')

    for card in cardSeqL:
        canonicalSeqL[SUITS.index(card.suit)] += card.rank

    canonicalSeqL.sort()

    canonicalSeqR = []
    for suit in SUITS:
        canonicalSeqR.append('')

    for card in cardSeqR:
        canonicalSeqR[SUITS.index(card.suit)] += card.rank
    
    canonicalSeqR.sort()
    
    if canonicalSeqL == canonicalSeqR:
        return True
    else:
        return False

def sub(rank, rankIdx, cardSeqs, list_of_cardSeqs):
    if rankIdx == len(rank):
        for cardSeq in list_of_cardSeqs:
            if canonical_equivalent(cardSeqs, cardSeq):
                return
        list_of_cardSeqs.append(cardSeqs)
        return
    for suit in SUITS:
        card = Card(rank[rankIdx], suit)
        if card in cardSeqs:
            continue
        else:
            sub(rank, rankIdx + 1, cardSeqs + [card], list_of_cardSeqs)
    return

# Rank is unique
# Given a rank combination, generate all possible suit combinations and apply 
# canonical_suits to get the canonical flop representation
# For example, for rank combination (A, A, K), we generate all suit combinations:
# AAA: sss, ssh, shs, shh, shd, ssd
# In the order of 'shcd'

# Canonic rule. 
#   The first card is always spade. Because of the rank uniqueness, we can always assign the first card to spade.
#    The second card is always heart. Because of the rank uniqueness, we can always assign the second card to heart.
def canonical_flops(rank):
    list_of_cardSeqs = []
    sub(rank, 0, [], list_of_cardSeqs)

    return list_of_cardSeqs

def main():
    parser = argparse.ArgumentParser(description="gen.py argment")
    
    parser.add_argument("--input", type=str, required=False)

    args = parser.parse_args()
    print("input:", args.input)

    total_rank_list = []
    for rank in itertools.combinations_with_replacement(RANKS, 3):
        total_rank_list.append(rank)
    
    canonical_flop_list = []
    for rank in total_rank_list:
        flops = canonical_flops(rank)
        canonical_flop_list.append(flops)
    
    res = ''
    for flopList in canonical_flop_list:
        for flop in flopList:
            for card in flop:
                res += str(card)
            res += "\n"
    
    s = ''
    with open("1755CanonicFlops.txt", "r", encoding="utf-8") as f:
        s = f.read()

    if(s != res):
        print("Error: Generated flops do not match the expected flops.")
    else:
        print("Success: Generated flops match the expected flops.")
        
    # Write to file, one flop per line
    os.makedirs("flops", exist_ok=True)
    with open("flops\\flops_1755.txt", "w") as f:
        f.write(res)
            
if __name__ == "__main__":
    main()