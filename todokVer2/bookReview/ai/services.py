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
    "불평/불만": "이 부분에서 불편함을 느끼셨다면, 어떤 점이 특히 그랬나요?",
    "환영/호의": "어떤 장면에서 환영받는 기분이 들었나요? 특별히 기억에 남는 순간이 있으신가요?",
    "감동/감탄": "이 장면이 감동적으로 다가온 이유가 무엇인가요? 어떤 부분이 깊은 인상을 남겼나요?",
    "지긋지긋": "이 상황에서 지겨움을 느끼셨다면, 어떤 이유 때문일까요?",
    "고마움": "어떤 부분에서 감사함을 느끼셨나요? 그 장면이 특별히 기억에 남는 이유가 있나요?",
    "슬픔": "이 장면이 슬프게 느껴진 이유는 무엇인가요? 마음에 남는 장면이 있었나요?",
    "화남/분노": "어떤 부분에서 화가 나셨나요? 그 장면이 어떤 감정을 불러일으켰는지 궁금합니다.",
    "존경": "주인공에게 존경심을 느끼신 이유가 무엇인가요? 어떤 행동이 인상 깊으셨나요?",
    "기대감": "어떤 장면이 기대감을 주었나요? 그 기대가 이야기 전개에 어떤 영향을 미쳤는지 궁금합니다.",
    "우쭐댐/무시함": "이 부분에서 우쭐해지셨다면, 어떤 일이 그런 감정을 불러일으켰나요?",
    "안타까움/실망": "이 장면이 안타깝거나 실망스럽게 느껴진 이유는 무엇인가요?",
    "비장함": "이 순간에서 비장함을 느끼셨나요? 어떤 점이 그 감정을 자아냈는지 궁금합니다.",
    "의심/불신": "이 부분에서 의심이나 불신을 느끼신 이유가 무엇인가요?",
    "뿌듯함": "이 장면이 뿌듯함을 주었다면, 어떤 점이 그렇게 느끼게 했나요?",
    "편안/쾌적": "이 부분에서 편안함을 느끼셨나요? 그 감정이 들게 한 장면이 있었나요?",
    "신기함/관심": "어떤 장면이 신기하거나 흥미로웠나요? 특별히 주목한 점이 있으신가요?",
    "아껴주는": "이 장면에서 따뜻함이나 배려를 느끼셨다면, 어떤 이유 때문인가요?",
    "부끄러움": "이 장면이 부끄럽게 느껴진 이유가 있을까요?",
    "공포/무서움": "이 장면에서 두려움을 느끼셨다면, 무엇이 특히 무서웠나요?",
    "절망": "이 부분에서 절망감을 느끼셨나요? 그 감정이 어떤 장면에서 가장 크게 다가왔나요?",
    "한심함": "이 장면이 한심하게 느껴진 이유가 무엇인가요?",
    "역겨움/징그러움": "어떤 부분이 역겨움을 불러일으켰나요? 그 감정이 특히 강하게 느껴진 이유는 무엇인가요?",
    "짜증": "이 장면에서 짜증이 나셨나요? 어떤 점이 특히 그랬는지 말씀해 주세요.",
    "어이없음": "이 부분이 어이없게 느껴졌다면, 그 이유는 무엇일까요?",
    "패배/자기혐오": "이 장면이 패배감이나 자기혐오를 불러일으켰나요? 어떤 점에서 그렇게 느끼셨나요?",
    "귀찮음": "이 장면이 귀찮게 느껴졌다면, 그 이유가 무엇인지 궁금합니다.",
    "힘듦/지침": "이 장면에서 피로감을 느끼셨나요? 무엇이 특히 힘들게 다가왔나요?",
    "즐거움/신남": "이 부분에서 즐거움이나 신남을 느끼셨나요? 어떤 점이 그 감정을 자아냈나요?",
    "깨달음": "이 장면이 주는 깨달음이 있으셨나요? 무엇을 새롭게 알게 되었는지 궁금합니다.",
    "죄책감": "이 부분이 죄책감을 느끼게 했다면, 어떤 이유 때문이었나요?",
    "증오/혐오": "이 장면에서 증오나 혐오를 느끼셨다면, 어떤 점이 그랬는지 설명해 주세요.",
    "흐뭇함(귀여움/예쁨)": "이 장면이 귀엽거나 흐뭇하게 다가왔다면, 어떤 점에서 그렇게 느끼셨나요?",
    "당황/난처": "어떤 장면이 당황스럽게 다가왔나요? 그 상황이 특별히 난처했던 이유는 무엇인가요?",
    "경악": "이 장면이 경악스럽게 느껴진 이유는 무엇인가요?",
    "부담/안 내킴": "이 부분에서 부담감이나 꺼림칙함을 느끼셨다면, 어떤 점이 그랬나요?",
    "서러움": "이 장면에서 서러움을 느끼셨다면, 그 이유는 무엇인가요?",
    "재미없음": "어떤 부분이 재미없게 느껴지셨나요? 그 이유를 설명해 주실 수 있나요?",
    "불쌍함/연민": "이 장면이 불쌍하거나 연민을 불러일으켰다면, 그 이유가 무엇인가요?",
    "놀람": "어떤 장면이 놀랍게 다가왔나요? 그 놀라움이 이야기에 어떤 영향을 주었는지 궁금합니다.",
    "행복": "이 장면에서 행복감을 느끼셨다면, 어떤 점이 그 감정을 불러일으켰나요?",
    "불안/걱정": "이 장면이 불안하거나 걱정스럽게 느껴진 이유가 무엇인가요?",
    "기쁨": "어떤 장면에서 기쁨을 느끼셨나요? 그 기쁨이 어떤 의미를 주었나요?",
    "안심/신뢰": "이 부분에서 안심하거나 신뢰를 느끼셨다면, 어떤 점이 특히 그렇게 느껴지게 했나요?"
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
