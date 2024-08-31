import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

def find_similar_keywords(keywords: List[str], all_review_keywords: List[List[str]], top_n: int = 3) -> List[str]:
    # 키워드 리스트를 문자열로 결합
    keywords_str = ' '.join(keywords)

    # 각 서평의 키워드 리스트를 문자열로 결합
    combined_texts = [' '.join(review_keywords) for review_keywords in all_review_keywords]

    # TF-IDF 벡터화
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform([keywords_str] + combined_texts)

    # 키워드와 모든 서평 간의 코사인 유사도 계산
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # 유사도가 가장 높은 서평의 인덱스 찾기
    most_similar_index = cosine_similarities.argmax()

    # 가장 유사한 서평의 키워드 가져오기
    most_similar_keywords = all_review_keywords[most_similar_index]

    # 입력된 키워드와 가장 유사한 키워드를 포함한 모든 키워드 중에서 TF-IDF 점수를 다시 계산하여 상위 3개를 선택
    all_keywords = keywords + most_similar_keywords
    all_keywords_str = ' '.join(all_keywords)
    all_tfidf_matrix = tfidf.fit_transform([all_keywords_str])

    # 중요도에 따라 상위 n개의 키워드 추출
    feature_names = np.array(tfidf.get_feature_names_out())
    top_indices = np.argpartition(all_tfidf_matrix[0, :].toarray().ravel(), -top_n)[-top_n:]
    top_keywords = feature_names[top_indices].tolist()

    return top_keywords
