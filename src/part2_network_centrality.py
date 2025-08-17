'''
PART 2: NETWORK CENTRALITY METRICS

Using the imbd_movies dataset
- Build a graph and perform some rudimentary graph analysis, extracting centrality metrics from it. 
- Below is some basic code scaffolding that you will need to add to
- Tailor this code scaffolding and its stucture to however works to answer the problem
- Make sure the code is inline with the standards we're using in this class 
'''

import numpy as np
import pandas as pd
import networkx as nx
import json
import os
from datetime import datetime

# Build the graph
g = nx.Graph()

# Set up your dataframe(s) -> the df that's output to a CSV should include at least the columns 'left_actor_name', '<->', 'right_actor_name'

def compute_network_centrality():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'imdb_movies.json')
with open(data_path, 'r') as in_file:
        # Don't forget to comment your code
        for line in in_file:
            # Don't forget to include docstrings for all functions

            # Load the movie from this line
  this_movie = json.loads(line)

            # Create a node for every actor
    for actor_id, actor_name in this_movie.get('actors', []):
                # add the actor to the graph    
         g.add_node(actor_id, name=actor_name)

            # Iterate through the list of actors, generating all pairs
            ## Starting with the first actor in the list, generate pairs with all subsequent actors
            ## then continue to second actor in the list and repeat

            i = 0 #counter
            for left_actor_id, left_actor_name in this_movie.get('actors', []): for right_actor_id, right_actor_name in this_movie['actors'][i+1:]:

                    # Get the current weight, if it exists
                    if g.has_edge(left_actor_id, right_actor_id):
                        g[left_actor_id][right_actor_id]['weight'] += 1
                    else:
                        # Add an edge for these actors
                        g.add_edge(left_actor_id, right_actor_id, weight=1) 
                     i += 1

    # Print the info below
    print("Nodes:", len(g.nodes))
    print("Edges:", len(g.edges))

    # Print the 10 the most central nodes
    deg_cent = nx.degree_centrality(g)  top_10 = sorted(deg_cent.items(), key=lambda x: x[1], reverse=True)[:10]

    # Prepare the dataframe
    output_data = []
    for actor_id, centrality in top_10: actor_name = g.nodes[actor_id]['name']
   output_data.append({"actor_id": actor_id, "actor_name": actor_name, "centrality": centrality})
 df = pd.DataFrame(output_data)

    # Output the final dataframe to a CSV named 'network_centrality_{current_datetime}.csv' to `/data`
    out_path = os.path.join(os.path.dirname(__file__), '..', 'data', f'network_centrality_{datetime.now().isoformat()}.csv')
    df.to_csv(out_path, index=False)
    print("Top 10 central actors saved to:", out_path)

