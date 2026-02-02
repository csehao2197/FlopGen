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

def canonical_flop(flop):
    """
    Given a 3-card flop (iterable of 'Rs' strings), return its canonical
    representative under all suit permutations and card reorderings.
    """
    # All permutations of suits (4! = 24)
    suit_perms = []
    for perm_suits in itertools.permutations(SUITS):
        perm_map = dict(zip(SUITS, perm_suits))
        suit_perms.append(perm_map)

    reps = []
    for perm in suit_perms:
        # Apply suit permutation
        permuted = [apply_suit_perm(c, perm) for c in flop]
        # Sort cards in a consistent way: by rank index, then suit index
        permuted_sorted = sorted(
            permuted,
            key=lambda c: (RANKS.index(c[0]), SUITS.index(c[1]))
        )
        reps.append("".join(permuted_sorted))

    # Canonical representative is lexicographically smallest representation
    return min(reps)

def main():
    parser = argparse.ArgumentParser(description="gen.py argment")
    
    parser.add_argument("--input", type=str, required=False)

    args = parser.parse_args()
    print("input:", args.input)

    unique_flops = set()

    # Generate all unordered 3-card combinations from the 52-card deck
    for flop in itertools.combinations(CARDS, 3):
        key = canonical_flop(flop)
        unique_flops.add(key)

    # We expect 1755 unique canonical flops
    print(f"Number of canonical flops: {len(unique_flops)}")

    # Sort them lexicographically for stable output
    #sorted_flops = sorted(unique_flops)
    sorted_flops = unique_flops

    # Write to file, one flop per line
    with open("flops_1755.txt", "w") as f:
        for rep in sorted_flops:
            # rep is like '2s3h4d' (three cards concatenated)
            # Optionally insert spaces between cards for readability
            cards = [rep[i:i+2] for i in range(0, 6, 2)]
            f.write("".join(cards) + "\n")

if __name__ == "__main__":
    main()