from django.test import TestCase
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Create your tests here.
def most_similar(idx, top_n=10):
    df = pd.read_csv('../../wondoofin.csv')
    test = pd.read_csv('../../features.csv', index_col='id')
    test = test.loc[:, test.columns != 'id']
    embeddings = test.values
    cosine_similarity_matrix = cosine_similarity(embeddings, embeddings)

    df_copy = df.copy()

    df_copy['cosine_similarity'] = cosine_similarity_matrix[idx]
    return df_copy.sort_values(by='cosine_similarity', ascending=False)[:top_n]
