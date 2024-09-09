import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple

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

    # 입력 키워드와 유사한 상위 키워드를 튜플로 리턴
    return top_keywords, most_similar_keywords


from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline

model_name = "searle-j/kote_for_easygoing_people"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

pipe = TextClassificationPipeline(
    model=model,
    tokenizer=tokenizer,
    device=0, # gpu number, -1 if cpu used
    return_all_scores=True,
    function_to_apply='sigmoid'
)

# 감정 레이블에 대한 기본 질문 템플릿
emotion_questions = {
    "불평/불만": "불편함을 느끼신 부분이 있으셨던 것 같아요. 어떤 점이 특히 그랬나요?",
    "환영/호의": "환영받는 기분을 느끼셨던 순간이 있나요? 특별히 기억에 남는 장면이 있었나요?",
    "감동/감탄": "감동을 받으신 부분이 있었던 것 같아요. 어떤 점에서 깊은 인상을 받으셨나요?",
    "지긋지긋": "지겨움을 느끼셨을 때, 그 이유가 무엇이라고 생각하셨나요?",
    "고마움": "감사함을 느끼신 부분이 있었던 것 같은데, 그 순간이 특별히 기억에 남는 이유가 무엇인가요?",
    "슬픔": "슬프게 다가온 장면이 있나요? 어떤 부분에서 특히 슬픔을 느끼셨나요?",
    "화남/분노": "화가 나셨던 순간이 있나요? 그 장면이 어떤 감정을 자아냈는지 궁금해요.",
    "존경": "주인공에게 존경심을 느끼신 부분이 있었나요? 어떤 행동이 가장 인상 깊었나요?",
    "기대감": "기대감을 느끼게 했던 장면이 있나요? 그 기대가 이야기 전개에 어떤 영향을 미쳤는지 궁금합니다.",
    "우쭐댐/무시함": "우쭐해지셨거나 무시당하는 느낌을 받으셨을 때, 그 이유가 무엇인가요?",
    "안타까움/실망": "안타깝거나 실망스러웠던 장면이 있었나요? 그 감정이 어떻게 생겼는지 알고 싶어요.",
    "비장함": "비장함을 느끼셨던 순간이 있나요? 어떤 점이 그 감정을 불러일으켰나요?",
    "의심/불신": "의심이나 불신을 느끼신 장면이 있었나요? 그 이유는 무엇이었나요?",
    "뿌듯함": "뿌듯함을 느끼신 순간이 있었다면, 그 이유는 무엇이었나요?",
    "편안/쾌적": "편안함이나 쾌적함을 느끼셨던 부분이 있었나요? 그 순간이 어떤 영향을 주었나요?",
    "신기함/관심": "신기하거나 흥미를 느끼셨던 장면이 있었다면, 무엇이 특별히 흥미로웠나요?",
    "아껴주는": "따뜻함이나 배려를 느끼셨던 순간이 있었나요? 그 이유는 무엇이었나요?",
    "부끄러움": "부끄러움을 느끼셨던 순간이 있다면, 어떤 이유에서였나요?",
    "공포/무서움": "두려움을 느끼셨던 순간이 있었나요? 그 두려움이 어디에서 비롯된 건가요?",
    "절망": "절망감을 느끼셨을 때, 어떤 장면이 가장 크게 다가왔나요?",
    "한심함": "한심하다는 생각이 들었던 장면이 있었나요? 그 이유는 무엇이었나요?",
    "역겨움/징그러움": "역겨움이나 징그러움을 느끼셨을 때, 어떤 점이 가장 불쾌했나요?",
    "짜증": "짜증을 느끼셨던 순간이 있었나요? 어떤 점이 가장 짜증스럽게 느껴졌나요?",
    "어이없음": "어이없다고 느끼셨던 순간이 있었나요? 그 감정이 왜 생겼는지 궁금합니다.",
    "패배/자기혐오": "패배감이나 자기혐오를 느끼셨다면, 어떤 점에서 그런 감정을 느끼셨나요?",
    "귀찮음": "귀찮음을 느끼셨던 장면이 있었다면, 그 이유는 무엇이었나요?",
    "힘듦/지침": "피로감을 느끼셨던 장면이 있었나요? 어떤 점에서 특히 힘들게 다가왔나요?",
    "즐거움/신남": "즐거움이나 신남을 느끼셨던 순간이 있다면, 그 감정을 불러일으킨 이유가 무엇이었나요?",
    "깨달음": "새로운 깨달음을 얻으셨던 장면이 있나요? 그 깨달음이 어떤 영향을 주었나요?",
    "죄책감": "죄책감을 느끼셨던 장면이 있었다면, 어떤 이유에서였나요?",
    "증오/혐오": "증오나 혐오를 느끼셨던 순간이 있었나요? 그 감정이 생긴 이유가 궁금합니다.",
    "흐뭇함(귀여움/예쁨)": "귀엽거나 흐뭇한 감정을 느끼셨던 순간이 있었나요? 그 순간이 어떤 영향을 주었나요?",
    "당황/난처": "당황스럽거나 난처했던 장면이 있었다면, 그 이유는 무엇이었나요?",
    "경악": "경악을 느끼셨던 순간이 있었다면, 어떤 장면에서 그런 감정이 생겼나요?",
    "부담/안 내킴": "부담감이나 꺼림칙함을 느끼셨던 순간이 있었나요? 그 이유는 무엇이었나요?",
    "서러움": "서러움을 느끼셨던 장면이 있었나요? 어떤 점에서 그런 감정을 느끼셨나요?",
    "재미없음": "재미없다고 느끼셨던 부분이 있었다면, 그 이유는 무엇인가요?",
    "불쌍함/연민": "불쌍하거나 연민을 느끼셨던 장면이 있었나요? 그 감정이 생긴 이유는 무엇이었나요?",
    "놀람": "놀라움을 느끼셨던 장면이 있었다면, 그 놀라움이 어떤 영향을 주었나요?",
    "행복": "행복감을 느끼셨던 순간이 있나요? 그 행복을 자아낸 장면이 무엇이었나요?",
    "불안/걱정": "불안하거나 걱정되었던 순간이 있었다면, 그 이유는 무엇이었나요?",
    "기쁨": "기쁨을 느끼셨던 장면이 있었다면, 그 감정이 어떤 의미를 가졌나요?",
    "안심/신뢰": "안심하거나 신뢰를 느끼셨던 순간이 있었나요? 그 감정이 어떻게 생겼는지 궁금합니다."
}

# 감정 분석을 바탕으로 질문 생성
def generate_questions(text, top_n=3):
    pipe_output = pipe(text)[0]
    
    # 상위 N개의 감정 레이블 추출
    sorted_emotions = sorted(pipe_output, key=lambda x: x["score"], reverse=True)[:top_n]
    
    questions = []
    for emotion in sorted_emotions:
        label = emotion["label"]
        score = emotion["score"]
        
        # 해당 감정에 대한 질문이 존재하면 추가
        if label in emotion_questions:
            questions.append(emotion_questions[label])
            # print(f"{label} (Score: {score:.2f})")
    
    return questions
