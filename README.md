# Super-Stable-Matching-Algorithm
Super Stable Matching Algorithm

NOTE: TO run the webpage, run python3 graphical_interface.py      


This project implements Super Stable Matching, based on Robert W. Irving's paper on Stable Marriage with Indifference. The goal is to find a stable pairing where no two participants strictly prefer each other over their assigned match.
 
1. Algorithm - stable_super_matching
The function takes two dictionaries of men’s and women’s preferences, where each preference is stored as a Preference object with:
•	name: The preferred person.
•	weight: Ranking (0 = most preferred).

Setup
•	Men are placed in a queue.
•	Preferences are stored in dictionaries, handling ties.
•	A result dictionary tracks engagements.

Matching Process
•	Each free man proposes to his highest-ranked available woman.
•	A woman tentatively accepts all equally ranked proposals and rejects lower ones.
•	If she was engaged to a lower-ranked man, he is released back into the queue.

Final Adjustments
•	Women remove strictly lower-ranked men.
•	If a man has no options left, no super stable match exists.

Completion
•	The process repeats until all men are matched or no proposals can be made.
•	The function returns the final stable match or None if no match exists.
 
2. Random Input Generation
The function generate_preferences(n):
•	Creates n men and women.
•	Randomizes preference lists.
•	Introduces ties randomly 20% chance(Intentionally low to observe more stable matchings)
•	Stores preferences for consistent matching.
 
3. Front-End Implementation (Flask)
   
A Flask web interface lets users:
1.	Generate preferences.
2.	Run the matching algorithm.
3.	View results as a bipartite graph.
   
Graph Visualization
•	Built with NetworkX and Matplotlib.
•	Men and women are positioned separately.
•	Edges represent final matches.
•	Graph is saved and displayed in the interface.

Edge Interaction (Click to Show Preferences)
•	Clicking a match opens a popup showing:
o	The man’s and woman’s full preference lists.
o	Preference data is stored in a JSON file.
o	Clicking an edge retrieves the relevant data.
