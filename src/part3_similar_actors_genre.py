'''
PART 2: SIMILAR ACTROS BY GENRE

Using the imbd_movies dataset:
- Create a data frame, where each row corresponds to an actor, each column represents a genre, and each cell captures how many times that row's actor has appeared in that column’s genre 
- Using this data frame as your “feature matrix”, select an actor (called your “query”) for whom you want to find the top 10 most similar actors based on the genres in which they’ve starred 
- - As an example, select the row from your data frame associated with Chris Hemsworth, actor ID “nm1165110”, as your “query” actor
- Use sklearn.metrics.DistanceMetric to calculate the euclidean distances between your query actor and all other actors based on their genre appearances
- - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.DistanceMetric.html
- Output a CSV continaing the top ten actors most similar to your query actor using cosine distance 
- - Name it 'similar_actors_genre_{current_datetime}.csv' to `/data`
- - For example, the top 10 for Chris Hemsworth are:  
        nm1165110 Chris Hemsworth
        nm0000129 Tom Cruise
        nm0147147 Henry Cavill
        nm0829032 Ray Stevenson
        nm5899377 Tiger Shroff
        nm1679372 Sudeep
        nm0003244 Jordi Mollà
        nm0636280 Richard Norton
        nm0607884 Mark Mortimer
        nm2018237 Taylor Kitsch
- Describe in a print() statement how this list changes based on Euclidean distance
- Make sure your code is in line with the standards we're using in this class
'''

#Write your code below

import os
import json
import pandas as pd
from datetime import datetime
from sklearn.metrics import pairwise_distances

def find_similar_actors():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'imdb_movies.json')
    genre_counts = {}

    with open(data_path, 'r') as f:
        for line in f:
            movie = json.loads(line)
            genres = movie.get("genres", [])
            actors = movie.get("actors", [])
            for actor_id, actor_name in actors:
                if actor_id not in genre_counts:
                    genre_counts[actor_id] = {"name": actor_name}
                for genre in genres:
                    genre_counts[actor_id][genre] = genre_counts[actor_id].get(genre, 0) + 1

    df = pd.DataFrame.from_dict(genre_counts, orient='index').fillna(0)
    names = df['name']
    df_genres = df.drop(columns='name')

    query_id = "nm1165110"
    query_vector = df_genres.loc[query_id].values.reshape(1, -1)

    cosine_distances = pairwise_distances(query_vector, df_genres, metric='cosine')[0]
    df_genres["cosine_distance"] = cosine_distances

    top_10 = df_genres.sort_values("cosine_distance").iloc[1:11]
    top_10["actor_id"] = top_10.index
    top_10["actor_name"] = names[top_10.index]

    out_path = os.path.join(os.path.dirname(__file__), '..', 'data', f'similar_actors_genre_{datetime.now().isoformat()}.csv')
    top_10[["actor_id", "actor_name"]].to_csv(out_path, index=False)
    print("Top 10 similar actors saved to:", out_path)

    euclidean_distances = pairwise_distances(query_vector, df_genres.drop(columns=["cosine_distance"]), metric='euclidean')[0]
    df_genres["euclidean_distance"] = euclidean_distances
    top_10_euclidean = df_genres.sort_values("euclidean_distance").iloc[1:11]
    top_10_euclidean["actor_name"] = names[top_10_euclidean.index]

    print("\nUsing cosine distance, the actors are:")
    print(top_10["actor_name"].tolist())

    print("\nUsing Euclidean distance, the actors are:")
    print(top_10_euclidean["actor_name"].tolist())

    print("\nDescription: Cosine distance compares genre **patterns**, while Euclidean distance compares total **amount** of appearances. So actors who do a similar mix of genres show up with cosine, even if they've done fewer movies.")
