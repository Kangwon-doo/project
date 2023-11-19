import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('data/features.csv')
features = df.loc[:, df.columns != 'id']


# Create your tests here.
def most_similar(coffee_id, top_n=10):
    embeddings = features.values
    cosine_similarity_matrix = cosine_similarity(embeddings, embeddings)

    df_copy = df.copy()
    idx = df[df['id'] == coffee_id].index[0]

    df_copy['cosine_similarity'] = cosine_similarity_matrix[idx]
    result_df = df_copy[df_copy['id'] != coffee_id].sort_values(by='cosine_similarity', ascending=False)[:top_n]
    return result_df['id'].tolist()


def cos_recommendation(user_input, top_n=4):
    column_mapping = {'바디감': 'body', '신맛': 'sour', '단맛': 'sweet', '쓴맛': 'bitter', '타입_디카페인': 'caf', '타입_블렌드': 'blend','향료_풍미':'향료'}  # 'notes'
    df.rename(columns=column_mapping, inplace=True)
    # Create a new dictionary
    new_dict = user_input.copy()
    # Add other keys with initial values
    new_keys = ['꽃', '과일', '달콤함', '허브', '고소함', '향료', '초콜릿']
    for key in new_keys:
        new_dict[key] = 0
    # Iterate through the 'notes' list and add new keys to 'new_dict'
    for note in user_input.get('notes', []):
        new_dict[note] = 1
    try:
        del new_dict['notes']
    except:
        pass

    df_copy = df.copy()
    df_copy.loc[len(df)] = new_dict
    features_df = df_copy[
        ['body', 'sour', 'sweet', 'bitter', 'caf', 'blend', '꽃', '과일', '허브', '달콤함', '고소함', '향료', '초콜릿']]  # '타입_싱글오리진'

    embeddings = features_df.values
    cosine_similarity_matrix = cosine_similarity(embeddings, embeddings)
    
    df_copy['cosine_similarity'] = cosine_similarity_matrix[-1]
    result_df = df_copy[df_copy['id'].notna()].sort_values(by='cosine_similarity', ascending=False)[:top_n]
    return result_df['id'].tolist()
