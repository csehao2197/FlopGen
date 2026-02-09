import os

import itertools
import argparse

# Ranks and suits
RANKS = "AKQJT98765432"
SUITS = "shdc"  # spades, hearts, diamonds, clubs

def all_cards():
    return [r + s for r in RANKS for s in SUITS]

CARDS = all_cards()

def apply_suit_perm(card, perm):
    """Apply a suit permutation (dict) to a single card."""
    rank, suit = card[0], card[1]
    return rank + perm[suit]

def canonical_suits(suits):
    suit_order = {}
    suit_index = 0
    for s in suits:
        if s not in suit_order:
           suit_order[s] = SUITS[suit_index]
           suit_index += 1
    for s in SUITS:
        if s not in suit_order:
            suit_order[s] = SUITS[suit_index]
            suit_index += 1
    # """Map suits to a canonical order: s -> s, h -> h, d -> d, c -> c"""
    # suit_order = {'s': 's', 'h': 'h', 'd': 'd', 'c': 'c'}
    suits_mapped = [suit_order[s] for s in suits]
    return suits_mapped

def canonical_flops(rank):
    ret = []
    # sss ssh shs shh shd 
    list_of_perms = ['sss', 'ssh', 'shs', 'shh', 'shd']
    
    for perm in list_of_perms:
        flop = zip(rank, perm)
        flop_cards = [r + s for r, s in flop]
        card_dups = len(set(flop_cards)) < 3
        if card_dups:
            continue
        ret.append("".join(flop_cards)) 
    if(len(ret) == 3):
        # AAB
        ret = [ret[0], ret[2]]
    return ret

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

    print(f"Number of total rank combinations: {len(total_rank_list)}")
    print(f"Number of total canonical_flop_list: {len(canonical_flop_list)}")

    ret = list(itertools.chain(*canonical_flop_list))
    print(f"Number of total canonical flops: {len(ret)}")
    
    res = map("".join, ret)
    
    # Write to file, one flop per line
    os.makedirs("flops", exist_ok=True)
    with open("flops\\flops_1755.txt", "w") as f:
        for rep in res:
            f.write(rep + "\n")
            
if __name__ == "__main__":
    main()