import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


# Create your tests here.
def most_similar(coffee_id, top_n=10):
    df = pd.read_csv('data/features.csv')
    test = df.loc[:, df.columns != 'id']
    embeddings = test.values
    cosine_similarity_matrix = cosine_similarity(embeddings, embeddings)

    df_copy = df.copy()
    idx = df[df['id'] == coffee_id].index[0]

    df_copy['cosine_similarity'] = cosine_similarity_matrix[idx]
    # result_df = df_copy.sort_values(by='cosine_similarity', ascending=False)[:top_n]
    result_df = df_copy[df_copy['id'] != coffee_id].sort_values(by='cosine_similarity', ascending=False)[:top_n]
    return result_df['id'].tolist()
