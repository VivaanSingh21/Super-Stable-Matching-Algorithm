import random
from SUPER_new import stable_super_matching

def generate_preferences(n):
    """
    Generates random preference dictionaries for `n` men and `n` women.
    Each man ranks all women, and each woman ranks all men.
    Some rankings may include ties.
    
    Returns:
        men_preferences (dict): Each man's preference list (with possible ties).
        women_preferences (dict): Each woman's preference list (with possible ties).
    """
    men = [f"M{i+1}" for i in range(n)]
    women = [f"W{i+1}" for i in range(n)]
    
    men_preferences = {}
    women_preferences = {}

    # Generate random preferences for men
    for man in men:
        ranked_women = random.sample(women, len(women))  # Shuffle women for random order
        men_preferences[man] = create_tied_preferences(ranked_women)  # Convert to tied list
       # print("Ranked woman list", ranked_women)
    
    # Generate random preferences for women
    for woman in women:
        ranked_men = random.sample(men, len(men))  # Shuffle men for random order
        women_preferences[woman] = create_tied_preferences(ranked_men)  # Convert to tied list
    
    return men_preferences, women_preferences


def create_tied_preferences(ranked_list):
    """
    Converts a ranked list into a preference list with some possible ties.
    Randomly decides whether to introduce ties in the ranking.
    
    Args:
        ranked_list (list): A shuffled list of preferences.
    
    Returns:
        list: A list of preferences, where some items may be grouped into sublists (indicating ties).
    """
    tied_preferences = []
    i = 0
    while i < len(ranked_list):
        if i < len(ranked_list) - 1 and random.random() < 0.2:  # 30% chance of creating a tie
            tied_preferences.append([ranked_list[i], ranked_list[i+1]])  # Tie between two
            i += 2  # Skip the next one since it's tied
        else:
            tied_preferences.append(ranked_list[i])  # Single ranking
            i += 1
    return tied_preferences

# Example Usage:
n = 4 # Number of men and women
'''
men_preferences, women_preferences = generate_preferences(n)
print(generate_preferences(n))

print("Men's Preferences:")
for man, prefs in men_preferences.items():
    print(f"{man}: {prefs}")

print("\nWomen's Preferences:")
for woman, prefs in women_preferences.items():
    print(f"{woman}: {prefs}")
'''

men_preferences, women_preferences = generate_preferences(n)
print(men_preferences, women_preferences)
print(stable_super_matching(men_preferences, women_preferences))