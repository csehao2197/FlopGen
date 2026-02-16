import os

import itertools
import argparse

# Part 1: Generate all card sequences of length n from 52 cards
# Part 2: Convert a card sequence to its canonical form.
#         The signature of a card sequence is first by its rank signature, then by its suit signature.
#         Because we can swap suit, so it is easier to think from the suit perspective.
#         In the order of spade, heart, diamond, club, if we can find a conversion map that map the 
#         cards to the form that space always gets more cards if it is equivilent, spades always get the 
#         highest rank. 

# Ranks and suits
RANKS = "AKQJT98765432"
SUITS = "shdc"  # spades, hearts, diamonds, clubs

def gen_all_cards():
    return [r + s for r in RANKS for s in SUITS]

def gen_all_card_objects():
    cards = []
    for r in RANKS:
        for s in SUITS:
            cards.append(Card(r, s))
    return cards

CARDS = gen_all_cards()

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

def parse_card(card_str):
    rank = card_str[0]
    suit = card_str[1]
    return Card(rank, suit)

def parse_card_seq(card_seq_str):
    card_seq = []
    for i in range(0, len(card_seq_str), 2):
        card_str = card_seq_str[i:i+2]
        card_seq.append(parse_card(card_str))
    return card_seq

def to_canonic_seq(cardSeq):
    ret = []

    sortedCardSeq = sorted(cardSeq, key=lambda x: RANKS.index(x.rank) * 10 + SUITS.index(x.suit))

    suit_to_card_seq_map = [[], [], [], []]
    for card in sortedCardSeq:
        suit_to_card_seq_map[SUITS.index(card.suit)].append(card)
    # we set up rule that only assign the smallest suit to the order of shcd.
    # if the count is a tie, we compare the highest card of the suit, with 
    # order [rank, suit shcd]

    suit_to_card_seq_map.sort(key=lambda x: (len(x), RANKS.index(x[0].rank) if len(x) > 0 else -1, SUITS.index(x[0].suit) if len(x) > 0 else -1), reverse=True)


    for idx in range(len(suit_to_card_seq_map)):
        for card in suit_to_card_seq_map[idx]:
            ret.append(Card(card.rank, SUITS[idx]))

    sortedRet = sorted(ret, key=lambda x: RANKS.index(x.rank) * 10 + SUITS.index(x.suit))
    return sortedRet

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
    
def canonical_equivalent_2(cardSeqL, cardSeqR):
    return to_canonic_suit(cardSeqL) == to_canonic_suit(cardSeqR)

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

def all_card_seq_sub(all_cards, idx, length, cardSeq, list_of_cardSeqs):
    
    if len(cardSeq) == length:
        list_of_cardSeqs.append(cardSeq)
        return

    if(idx >= len(all_cards)):
        return
    
    all_card_seq_sub(all_cards, idx + 1, length, cardSeq + [all_cards[idx]], list_of_cardSeqs)
    all_card_seq_sub(all_cards, idx + 1, length, cardSeq, list_of_cardSeqs)
    
    return

def all_card_seq(length):
    list_of_cardSeqs = []
    all_cards = gen_all_card_objects()
    all_card_seq_sub(all_cards, 0, length, [], list_of_cardSeqs)
    return list_of_cardSeqs

def main():

    print ("Test1: Test generate canoiclal card sequence from card sequence")
    print ("Test card sequence 2sKd7h should generate canonical card sequence Ks7h2d")
    carnoical_card_seq = to_canonic_seq(parse_card_seq("2sKd7h"))
    print ("Generated Canonical card sequence:", ''.join(str(card) for card in carnoical_card_seq))
    print ("Expected canonical card sequence: Ks7h2d")
    
    print ("Test card sequence 7hQdQc should generate canonical card sequence QsQh7d")
    carnoical_card_seq = to_canonic_seq(parse_card_seq("7hQdQc"))
    print ("Generated Canonical card sequence:", ''.join(str(card) for card in carnoical_card_seq))
    print ("Expected canonical card sequence: QsQh7d")

    print ("Test card sequence JcQc2c should generate canonical card sequence QsJs2s")
    carnoical_card_seq = to_canonic_seq(parse_card_seq("JcQc2c"))
    print ("Generated Canonical card sequence:", ''.join(str(card) for card in carnoical_card_seq))
    print ("Expected canonical card sequence: QsJs2s")

    print ("Test card sequence AcAdKd should generate canonical card sequence KsAdQd")
    carnoical_card_seq = to_canonic_seq(parse_card_seq("AcAdKd"))
    print ("Generated Canonical card sequence:", ''.join(str(card) for card in carnoical_card_seq))
    print ("Expected canonical card sequence: AsAhKs")

    print ("Test card sequence AcAdKc should generate canonical card sequence KsAdQd")
    carnoical_card_seq = to_canonic_seq(parse_card_seq("AcAdKc"))
    print ("Generated Canonical card sequence:", ''.join(str(card) for card in carnoical_card_seq))
    print ("Expected canonical card sequence: AsAhKs")

    print ("Test card sequence 2sKd7h7dQdQsJcQc2c should generate canonical card sequence Ks7h2d")
    carnoical_card_seq = to_canonic_seq(parse_card_seq("2sKd7h7dQd5cQsJcQc2c"))
    print ("Generated Canonical card sequence:", ''.join(str(card) for card in carnoical_card_seq))
    print ("Expected canonical card sequence: KhQsQhQdJs7h7c5s2s2d")
    print ("The rule now is use the highest count suit then highest rank first")

    print ("Test2: Test all card sequence generated from 52 cards")
    card_seq_1 = all_card_seq(1)
    print ("Generated card sequence of length 1:", len(card_seq_1))
    print ("Expected card sequence of length 1:", 52)
    card_seq_2 = all_card_seq(2)
    print ("Generated card sequence of length 2:", len(card_seq_2))
    print ("Expected card sequence of length 2:", 1326)
    card_seq_3 = all_card_seq(3)
    print ("Generated card sequence of length 3:", len(card_seq_3))
    print ("Expected card sequence of length 3:", 22100)

    print ("Test2: Test generate 1755 canonical flops using canonical equivalent function")
    print ("Generate all flops sequences")
    flops = all_card_seq(3)

    cardnical_flop_set = set()
    for flop in flops:
        canonic_flop = to_canonic_seq(flop)
        cardnical_flop_set.add(''.join(str(card) for card in canonic_flop))

    print ("Generated canonical flops:", len(cardnical_flop_set))
    print ("Expected canonical flops:", 1755)

    # ok it is different. meaning AsAdKd and AsAdKs are converted to 
    # different canonic flops
    # we need a rule like the hightest rank smaller set always get spade first.
    # for each rank, we assign the suit in the order of spade, heart, diamond, club.
    # with the order of count of suit of this card in this seq. 
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