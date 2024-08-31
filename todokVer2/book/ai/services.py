import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import string
from konlpy.tag import Komoran

# Stopwords 로드
with open('korean_stopwords.txt', 'r') as f:
    list_file = f.readlines()
stopwords = list([item.strip() for item in list_file])
stopwords.extend(['나는', '작가', '저자', '주인공', '독서', '문장', '내용', '이제', '오늘', '올해'])

# Komoran 객체 초기화
komoran = Komoran()

# 정규화 함수
def preprocess(text):
    text = text.strip()
    text = re.compile('<.*?>').sub('', text)
    text = re.compile('[%s]' % re.escape(string.punctuation)).sub(' ', text)
    text = re.sub('\s+', ' ', text)
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'[^\w\s]', ' ', str(text).strip())
    text = re.sub(r'\d', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

# 명사/영단어 추출 함수
def final(text):
    n = []
    word = komoran.nouns(text)
    p = komoran.pos(text)
    for pos in p:
        if pos[1] in ['SL']:
            word.append(pos[0])
    for w in word:
        if len(w) > 1 and w not in stopwords:
            n.append(w)
    return " ".join(n)

# 전처리 함수
def preprocess_text(text):
    return final(preprocess(text))

# extract_keywords 함수 구현
def extract_keywords(text: str, top_n: int = 4) -> list:
    # 단일 텍스트를 처리하기 위해 DataFrame 생성
    df = pd.DataFrame({'description': [text]})
    
    # 텍스트 전처리
    df['description_clean'] = df['description'].apply(preprocess_text)
    
    # TF-IDF 분석
    tfidf = TfidfVectorizer()
    X = tfidf.fit_transform(df['description_clean'])
    
    # 중요한 단어 추출
    feature_names = np.array(tfidf.get_feature_names_out())
    top_indices = np.argpartition(X[0, :].toarray().ravel(), -top_n)[-top_n:]
    important_words = feature_names[top_indices].tolist()
    
    return important_words
