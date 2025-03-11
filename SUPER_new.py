from queue import Queue
from queue import Empty
class Preference:
    """ Class to store a person's preference ranking. """
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight  # Lower weight = Higher preference

    def __repr__(self):
        return f"{self.name}({self.weight})"

def check_duplicate(result_dict):
    """
    Check if any woman has more than one suitor in result_dict.
    If so, return True; otherwise, return False.
    """
    for key in result_dict:
        if len(result_dict[key]) > 1:  # A woman has multiple suitors
            return True
    return False

def fix_duplicates(result_dict, free_men):
    """
    If any woman is engaged to multiple men, add all her suitors back into the queue 
    and reset her engagements to an empty list.
    """
    for woman, suitors in result_dict.items():
        if len(suitors) > 1:  # Woman is engaged to multiple men
            for man in suitors:
                free_men.put(man)  # Add all men back to queue
            
            result_dict[woman] = []  # Reset engagements instead of deleting the key


def initialize_preferences(raw_preferences):
    """
    Converts raw preference lists into a dictionary where each key maps to a list of Preference objects.
    Handles indifference by ensuring equal weights for tied preferences.
    """
    structured_preferences = {}

    for person, preferences in raw_preferences.items():
        structured_preferences[person] = []
        weight = 0  # Start weight from 0

        for group in preferences:
            if isinstance(group, list):  # If there is a tie, assign equal weights
                for item in group:
                    structured_preferences[person].append(Preference(item, weight))
            else:  # Otherwise, assign the next weight
                structured_preferences[person].append(Preference(group, weight))
            weight += 1  # Increment weight for the next preference group

    return structured_preferences

def is_valid_matching(result_dict):
    """
    Checks if every woman is mapped to a unique man.
    Returns True if it's a valid stable matching, otherwise False.
    """
    seen_men = set()  # Store men already assigned
    for woman, men in result_dict.items():
        if len(men) != 1:  # Each woman should have exactly one match
            return False
        if men[0] in seen_men:  # Ensure no duplicate man assignments
            return False
        seen_men.add(men[0])  # Mark man as assigned
    return True

def stable_super_matching(men_preferences, women_preferences):
    # Initialize queue with all men
    free_men = Queue()
    for man in men_preferences.keys():
        free_men.put(man)

    # Initialize d1 (Men's preferences as list of Preference objects)
    d1 = initialize_preferences(men_preferences)

# Initialize d2 (Women's preferences)
    d2 = initialize_preferences(women_preferences)

    # Initialize result dictionary (each woman has an empty list of engaged men)
    result_dict = {woman: [] for woman in women_preferences.keys()}
    #print(d1)
    #print(d2)
   # print(free_men)
    #print(result_dict)
    
    checker =  None
    iterations = 0

    max_iterations = 19
    while (not free_men.empty() and not is_valid_matching(result_dict)) or (checker is None):
        
        iterations+=1

        #Think about why queue may get empty
        try:
            Mx = free_men.get(timeout=5)  # Wait max 5 seconds for an item
        except Empty:
            print("No free men left. Exiting...")
            return None

        for k in d1:
            if len(d1[k])==0:
                return None
                

        # Find the first preference group (weight = 0)
        #women_lst = [pref.name for pref in d1[Mx] if pref.weight == 0] # not pref weight 0 but pop lowest weight
        min_weight = min(pref.weight for pref in d1[Mx])  # Get the lowest weight

        # Step 2: Store all women with that minimum weight
        women_lst = [pref.name for pref in d1[Mx] if pref.weight == min_weight]

        # Step 3: Remove those women from d1[Mx]
        d1[Mx] = [pref for pref in d1[Mx] if pref.weight != min_weight]

        for Wx in women_lst:
            if Mx in [p.name for p in d2[Wx]]:  # If Wx also prefers Mx
                if len(result_dict[Wx]) > 0:  # If Wx is already engaged
                    # Get current lowest weight in result_dict[Wx]
                    current_lowest_weight = min(pref.weight for pref in d2[Wx] if pref.name in result_dict[Wx])

                    # Get Mx's weight in d2[Wx]
                    Mx_weight = next(pref.weight for pref in d2[Wx] if pref.name == Mx)

                    if Mx_weight < current_lowest_weight:  # Mx is strictly better
                        # Free all previous partners
                        for prev_man in result_dict[Wx]:
                            free_men.put(prev_man)

                        result_dict[Wx] = [Mx]  # Replace with Mx

                    elif Mx_weight == current_lowest_weight:  # Mx is equally preferred
                        result_dict[Wx].append(Mx)  # Append Mx

                else:  # Wx is currently free
                    result_dict[Wx].append(Mx)

                # Remove all strictly lesser-preferred men from d2[Wx] (based on weights)
                Wx_new_list = []
                Mx_weight = next(pref.weight for pref in d2[Wx] if pref.name == Mx)  # Find Mx's weight

                for pref in d2[Wx]:
                    
                    if pref.weight > Mx_weight:  # Stop at first strictly worse-ranked man
                        break  
                    else:
                        Wx_new_list.append(pref)

                d2[Wx] = Wx_new_list
            else:
                new_preference_list = []  # Temporary list to store updated preferences

                for p in d1[Mx]:  # Iterate through Mx's preference list
                    if p.name != Wx:  # Only keep women who are NOT Wx
                        new_preference_list.append(p)

                d1[Mx] = new_preference_list  # Update D1[Mx] after filtering


        fix_duplicates(result_dict, free_men)  # Fix duplicates at the end of iteration
        #print("Iteration number", iterations, "Result Dict: ", result_dict)
        #print("Iteration number", iterations, "is valid matching ", is_valid_matching(result_dict))
        #print("Iteration number", iterations, "free_men queue ",list(free_men.queue))
       # print("Iteration number", iterations, "Womens preferences ",d2)
        #print("Iteration number", iterations, "Mens preferences ",d1)

        if is_valid_matching(result_dict):
            break

        '''
        if iterations >= max_iterations:
            print("Loop stopped after 10 iterations.")
            break
        '''

    return result_dict if not check_duplicate(result_dict) else None



#Termination case is when some D1[Mx] becomes empty - so we need to find the condition under which we remove elements from D1[Mx]
men_preferences = {
    'M1': [['W1', 'W2'], 'W3', 'W4'],
    'M2': ['W2', 'W3', 'W1', 'W4'],
    'M3': [['W3', 'W4'], 'W1', 'W2'],
    'M4': ['W4', 'W1','W2','W3']
}

women_preferences = {
    'W1': [['M1', 'M2'], 'M3', 'M4'],
    'W2': ['M2', 'M3', 'M1', 'M4'],
    'W3': [['M3', 'M4'], 'M1', 'M2'],
    'W4': ['M4', 'M1','M2','M3']

}

men_preferences2 = {
    'M1': [['W1', 'W2'], 'W3', 'W4'],
    'M2': [['W1', 'W2'], 'W3', 'W4'],
    'M3': [['W3', 'W4'], 'W1', 'W2'],
    'M4': [['W3', 'W4'], 'W1', 'W2']
}

women_preferences2 = {
    'W1': [['M1', 'M2'], ['M3', 'M4']],
    'W2': [['M1', 'M2'], ['M3', 'M4']],
    'W3': [['M3', 'M4'], ['M1', 'M2']],
    'W4': [['M3', 'M4'], ['M1', 'M2']]
}

men_preferences3 = {
    'M1': [['W1', 'W2'], ['W3', 'W4']],
    'M2': [['W1', 'W2'], ['W3', 'W4']],
    'M3': [['W3', 'W4'], ['W1', 'W2']],
    'M4': [['W3', 'W4'], ['W1', 'W2']]
}

women_preferences3 = {
    'W1': [['M1', 'M2'], ['M3', 'M4']],
    'W2': [['M1', 'M2'], ['M3', 'M4']],
    'W3': [['M3', 'M4'], ['M1', 'M2']],
    'W4': [['M3', 'M4'], ['M1', 'M2']]
}
men_preferences4 = {
    'M1': ['W2','W1'],
    'M2': ['W1', 'W2']
    
}

women_preferences4 = {
    'W1': [['M1', 'M2']],
    'W2': ['M1', 'M2']
}



result = stable_super_matching(men_preferences4, women_preferences4)
print(result)
'''
if result:
    print("\nSuper-Stable Matching Found:")
    for woman, man_list in result.items():
        print(f"{woman} is matched with {man_list}")
else:
    print("\nNo Super-Stable Matching Exists.")
'''