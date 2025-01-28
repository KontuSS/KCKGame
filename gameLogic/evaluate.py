from itertools import combinations

# Card Deck
SUITS = ['H', 'D', 'C', 'S']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Helper to map card rank to numeric value for evaluation
RANK_VALUES = {rank: i for i, rank in enumerate(RANKS, start=2)}

def evaluate_hand(player_cards, community_cards):
    """
    Evaluates the player's hand strength in Texas Hold'em.

    Args:
        player_cards (list of str): List of two cards, e.g., ['10H', 'JH']
        community_cards (list of str): List of five community cards, e.g., ['2C', '3D', '4S', '5H', '6H']

    Returns:
        str: The rank of the hand (e.g., 'Straight', 'Two Pair').
    """
    all_cards = player_cards + community_cards
    all_combinations = combinations(all_cards, 5)  # All possible 5-card combinations

    def parse_cards(cards):
        ranks = sorted([RANK_VALUES[card[:-1]] for card in cards], reverse=True)
        suits = [card[-1] for card in cards]
        return ranks, suits

    def is_flush(suits):
        return max(suits.count(suit) for suit in SUITS) >= 5

    def is_straight(ranks):
        unique_ranks = sorted(set(ranks), reverse=True)
        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i] - unique_ranks[i + 4] == 4:
                return True, unique_ranks[i:i + 5]
        # Handle Ace-low straight
        if set([14, 2, 3, 4, 5]).issubset(set(ranks)):
            return True, [5, 4, 3, 2, 1]
        return False, []

    def get_rank_counts(ranks):
        return {rank: ranks.count(rank) for rank in set(ranks)}

    best_rank = "High Card"

    for combo in all_combinations:
        ranks, suits = parse_cards(combo)
        rank_counts = get_rank_counts(ranks)

        flush = is_flush(suits)
        straight, straight_ranks = is_straight(ranks)

        if flush and straight:
            best_rank = "Straight Flush"
        elif 4 in rank_counts.values():
            best_rank = "Four of a Kind"
        elif sorted(rank_counts.values()) == [2, 3]:
            best_rank = "Full House"
        elif flush:
            best_rank = "Flush"
        elif straight:
            best_rank = "Straight"
        elif 3 in rank_counts.values():
            best_rank = "Three of a Kind"
        elif list(rank_counts.values()).count(2) == 2:
            best_rank = "Two Pair"
        elif 2 in rank_counts.values():
            best_rank = "Pair"

    return best_rank

# Example usage
player_cards = ['10H', 'JH']
community_cards = ['2C', '3D', '4S', '5H', '6H']
print(evaluate_hand(player_cards, community_cards))
