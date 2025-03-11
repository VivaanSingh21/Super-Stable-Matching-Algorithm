from flask import Flask, render_template, request, session, jsonify
import networkx as nx
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
import os
import json
from random_preference import generate_preferences
from SUPER_new import stable_super_matching

app = Flask(__name__)
app.secret_key = "secret_key"  #To enable memory

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    n = int(request.form.get("n", 4))  # Default to 4 if no input

    # Generate preferences
    men_prefs, women_prefs = generate_preferences(n)

    # Store preferences in Flask session
    session["men_prefs"] = men_prefs
    session["women_prefs"] = women_prefs

    return render_template("preferences.html", men_prefs=men_prefs, women_prefs=women_prefs)

@app.route("/match", methods=["POST"])
def match():
    # Retrieve stored preferences from session
    men_prefs = session.get("men_prefs")
    women_prefs = session.get("women_prefs")

    if not men_prefs or not women_prefs:  # Handle case if session is empty
        return "Error: No preferences found. Please generate preferences first.", 400

    # Run matching algorithm on the stored preferences
    result = stable_super_matching(men_prefs, women_prefs)

    session["matches"] = result

    return render_template("match_results.html", men_prefs=men_prefs, women_prefs=women_prefs, result=result)


@app.route("/graph")
def graph():
    matches = session.get("matches")
    men_prefs = session.get("men_prefs")
    women_prefs = session.get("women_prefs")

    
    if matches is None:
        return "No stable matching exists. Please generate new preferences and try again.", 400
    

    
    print("DEBUG: Matches structure:", matches)

    # Generate and save the graph
    img_path, edge_info_path = generate_graph(matches, men_prefs, women_prefs)

    return render_template("graph.html", img_path=img_path, edge_info_path=edge_info_path)

def generate_graph(matches, men_preferences, women_preferences):
    """Creates and saves a bipartite graph image for visualization."""
    G = nx.Graph()

    #matches = {woman: man[0] if isinstance(man, list) else man for woman, man in matches.items()}
    men = sorted(men_preferences.keys())   # Ensure men are in order
    women = sorted(women_preferences.keys())
    print(men, women)
    '''
    men = list(sorted(cleaned_matches.values()))# Men as keys
    women = list(sorted(cleaned_matches.keys()))  # Women as keys
    print(cleaned_matches)
    print(men)
    print(women)
    '''
    G.add_nodes_from(men, bipartite=0)  # Men nodes
    G.add_nodes_from(women, bipartite=1)  # Women nodes

    edge_labels = {}

    edges = []

    for woman, man in matches.items():
        if isinstance(man, list):  
            man = man[0]  
        if man in men and woman in women:
            edges.append((man, woman))
            edge_labels[f"{man}-{woman}"] = json.dumps({
                "man": man,
                "woman": woman,
                "man_prefs": men_preferences[man],
                "woman_prefs": women_preferences[woman]
            })
    print(matches)
    print(edges)

    G.add_edges_from(edges)
    static_dir = "static"
    edge_info_path = os.path.join(static_dir, "edge_data.json")
    with open(edge_info_path, "w") as f:
        json.dump(edge_labels, f)

    pos = nx.bipartite_layout(G, men)  # Position nodes in a bipartite layout
    plt.figure(figsize=(5, 3), dpi=150)  # Smaller size, better resolution
    nx.draw(G, pos, with_labels=True, node_color=["lightblue" if node in men else "lightcoral" for node in G.nodes()],
            edge_color="black", font_size=8, node_size=1500, width=1)
    
    img_path = "static/matching_graph.png"
    plt.savefig(img_path)
    plt.close()

    return img_path, edge_info_path 

if __name__ == "__main__":
    app.run(debug=True)
