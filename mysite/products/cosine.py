import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import ast
import json
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('data/features.csv')
survey_users = pd.read_csv('data/survey_users.csv')
features = df.loc[:, df.columns != 'id']
coffees = df.reset_index(drop=False)
coffees = coffees.rename(columns={"index": "coffeeid"})

# MySQL 연결 정보
mysql_host = 'database-1.cql2hwaazxkg.ap-northeast-2.rds.amazonaws.com'
mysql_user = 'admin'
mysql_password = 'admin1234'
mysql_db = 'team_wondoodoo'

engine = create_engine(f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}")

# 쿼리 작성
review_query = f"SELECT * FROM review;"
users_query = f"SELECT * FROM main_preference;"
try:
    # MySQL에서 데이터 읽어오기
    users = pd.read_sql(users_query,
                        engine)  # ['id', 'caf', 'blend', 'notes', 'sour', 'sweet', 'bitter', 'body', 'user_id']
    users.reset_index(drop=False, inplace=True)
    jsonDec = json.decoder.JSONDecoder()
    users['notes'] = users['notes'].apply(jsonDec.decode)

    ratings = pd.read_sql(review_query,
                          engine)  # 'id', 'Stars', 'content', 'created_date', 'Coffee_id', 'Order_id', 'user_id'
    ratings = ratings[['user_id', 'Coffee_id', 'Stars', 'created_date']]

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    # 연결 닫기
    engine.dispose()

ratings['userid'] = ratings.merge(users, on='user_id')['index']
ratings['coffeeid'] = ratings.merge(coffees, how='left', left_on='Coffee_id', right_on='id')['coffeeid']
ratings.drop(columns=['user_id', 'Coffee_id'], inplace=True)
coffees.drop(columns='id', inplace=True)
users.drop(columns=['user_id', 'id'], inplace=True)
users.rename(columns={"index": "userid"}, inplace=True)


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
    column_mapping = {'바디감': 'body', '신맛': 'sour', '단맛': 'sweet', '쓴맛': 'bitter', '타입_디카페인': 'caf', '타입_블렌드': 'blend',
                      '향료_풍미': '향료'}  # 'notes'
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


DOT = 'dot'
COSINE = 'cosine'


def compute_scores(query_embedding, item_embeddings, measure=DOT):
    """Computes the scores of the candidates given a query.
    Args:
      query_embedding: a vector of shape [k], representing the query embedding.
      item_embeddings: a matrix of shape [N, k], such that row i is the embedding
        of item i.
      measure: a string specifying the similarity measure to be used. Can be
        either DOT or COSINE.
    Returns:
      scores: a vector of shape [N], such that scores[i] is the score of item i.
    """
    u = query_embedding
    V = item_embeddings
    if measure == COSINE:
        V = V / np.linalg.norm(V, axis=1, keepdims=True)
        u = u / np.linalg.norm(u)
    scores = u.dot(V.T)
    return scores


def notes_categorising(data):
    try:
        data['notes'] = data['notes'].apply(ast.literal_eval)
    except ValueError:
        pass
    # Add other keys with initial values
    new_keys = ['꽃', '과일', '달콤함', '허브', '고소함', '향료', '초콜릿']
    for key in new_keys:
        data[key] = 0
    # Iterate through the 'notes' list and add new keys to 'new_dict'
    for index, row in data.iterrows():
        for note in row['notes']:
            data.at[index, note] = 1
    try:
        del data['notes']
    except:
        pass


def similar_user(userid):
    new_user = users[users.index == userid-1]
    new_user.drop(columns='userid', inplace=True)
    notes_categorising(new_user)

    survey_copy = survey_users.copy()
    notes_categorising(survey_copy)

    survey_copy = pd.concat([survey_copy, new_user], ignore_index=True)

    embeddings = survey_copy.values
    cosine_similarity_matrix = cosine_similarity(embeddings, embeddings)

    survey_copy['cosine_similarity'] = cosine_similarity_matrix[-1]
    result_df = survey_copy[survey_copy.index != survey_copy.index[-1]].sort_values(by='cosine_similarity', ascending=False)[:1]
    return result_df.index[0]


def collaborative_rec(model, measure=DOT, exclude_rated=True, k=8, userid=0):
    scores = compute_scores(
        model.embeddings["userid"][userid], model.embeddings["coffeeid"], measure)
    score_key = measure + ' score'
    df_copy = df.copy()
    df_copy[score_key] = list(scores)
    if exclude_rated:
        # remove movies that are already rated
        rated_coffees = ratings[ratings.userid == str(userid)]["coffeeid"].values
        df_copy.reset_index(drop=False, inplace=True)
        df_copy.rename(columns={'index': 'coffeeid'}, inplace=True)
        df_copy = df_copy[df_copy.coffeeid.apply(lambda coffeeid: coffeeid not in rated_coffees)]

    result_df = df_copy.sort_values([score_key], ascending=False).head(k)
    return result_df['id'].tolist()
