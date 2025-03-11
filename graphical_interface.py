from flask import Flask, render_template, request, session, jsonify
import networkx as nx
import matplotlib
matplotlib.use("Agg")  # Use a non-GUI backend for Matplotlib
import matplotlib.pyplot as plt
import os
import json
from random_preference import generate_preferences
from SUPER_new import stable_super_matching

app = Flask(__name__)
app.secret_key = "secret_key"  # Enables session storage for user data

# Homepage route - Renders the main index page
@app.route("/")
def index():
    return render_template("index.html")

# Generates random preferences for men and women
@app.route("/generate", methods=["POST"])
def generate():
    n = int(request.form.get("n", 4))  # Default to 4 if no input

    # Generate preferences
    men_prefs, women_prefs = generate_preferences(n)

    # Store preferences in Flask session
    session["men_prefs"] = men_prefs
    session["women_prefs"] = women_prefs

    return render_template("preferences.html", men_prefs=men_prefs, women_prefs=women_prefs)

# Runs the stable matching algorithm based on stored preferences
@app.route("/match", methods=["POST"])
def match():
    # Retrieve stored preferences from session
    men_prefs = session.get("men_prefs")
    women_prefs = session.get("women_prefs")

    if not men_prefs or not women_prefs:  # Handle case if session is empty
        return "Error: No preferences found. Please generate preferences first.", 400

    # Run the stable matching algorithm
    result = stable_super_matching(men_prefs, women_prefs)

    # Store the matches in session
    session["matches"] = result

    return render_template("match_results.html", men_prefs=men_prefs, women_prefs=women_prefs, result=result)

# Generates and displays the bipartite graph visualization of the matching
@app.route("/graph")
def graph():
    matches = session.get("matches")
    men_prefs = session.get("men_prefs")
    women_prefs = session.get("women_prefs")

    if matches is None:
        return "No stable matching exists. Please generate new preferences and try again.", 400

    print("DEBUG: Matches structure:", matches)

    # Generate and save the graph image
    img_path, edge_info_path = generate_graph(matches, men_prefs, women_prefs)

    return render_template("graph.html", img_path=img_path, edge_info_path=edge_info_path)

# Function to generate a bipartite graph visualization of the matching
def generate_graph(matches, men_preferences, women_preferences):
    """Creates and saves a bipartite graph image for visualization."""
    G = nx.Graph()

    # Extract sorted lists of men and women
    men = sorted(men_preferences.keys())  
    women = sorted(women_preferences.keys())  

    print("Men:", men)
    print("Women:", women)

    # Add nodes for men and women to the graph
    G.add_nodes_from(men, bipartite=0)  
    G.add_nodes_from(women, bipartite=1)  

    edge_labels = {}
    edges = []

    # Create edges from matches
    for woman, man in matches.items():
        if isinstance(man, list):  
            man = man[0]  # Extract first element if it's a list

        if man in men and woman in women:
            edges.append((man, woman))
            edge_labels[f"{man}-{woman}"] = json.dumps({  # Convert key to string for JSON
                "man": man,
                "woman": woman,
                "man_prefs": men_preferences[man],
                "woman_prefs": women_preferences[woman]
            })

    print("DEBUG: Matches:", matches)
    print("DEBUG: Edges:", edges)

    # Add edges to the graph
    G.add_edges_from(edges)

    # Ensure static directory exists
    static_dir = "static"
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

    # Save edge info for interactive display
    edge_info_path = os.path.join(static_dir, "edge_data.json")
    with open(edge_info_path, "w") as f:
        json.dump(edge_labels, f)

    # Position nodes in a bipartite layout
    pos = nx.bipartite_layout(G, men)

    # Resize the figure for a better fit
    plt.figure(figsize=(5, 3), dpi=150)  
    nx.draw(G, pos, with_labels=True, node_color=["lightblue" if node in men else "lightcoral" for node in G.nodes()],
            edge_color="black", font_size=8, node_size=1500, width=1)

    # Save the graph image
    img_path = os.path.join(static_dir, "matching_graph.png")
    plt.savefig(img_path)
    plt.close()

    return img_path, edge_info_path  # Return graph image path and edge info path

# Runs the Flask app
if __name__ == "__main__":
    app.run(debug=True)
