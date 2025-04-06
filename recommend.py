from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def Recommendation(Skills, dataset, val):
    df = pd.read_csv(dataset)
    skills = ""
    recommended = set()
    for i in Skills:
        skills += (i+" ")
    # print("skills:",skills)
    # print(len(df.index)+1)
    df.loc[len(df.index)] = [(len(df.index)+1), "Present skills", skills]
    x = df['Skills']
    tfidf = TfidfVectorizer()
    x = tfidf.fit_transform(x)
    similarity_score = cosine_similarity(x)
    recommendation_score = list(enumerate(similarity_score[len(df.index)-1]))
    # print(recommendation_score)
    sorted_similar_exams = sorted(
        recommendation_score, key=lambda x: x[1], reverse=True)
    # print(sorted_similar_exams)
    i = 0
    while len(recommended) < 5 and i < len(sorted_similar_exams) and sorted_similar_exams[i][1] > 0:
        index = sorted_similar_exams[i][0]
        suggest = df.iloc[index][val]
        i += 1
        if (suggest != "Present skills"):
            # print(suggest)
            recommended.add(suggest)
    recommended = list(recommended)
    if (len(recommended) < 5):
        for i in range(len(recommended)-5):
            recommended.append(" ")
    # print(recommended)
    return recommended


def RecommendExam(WSkills, dataset, val):
    # print("exms")
    return Recommendation(WSkills, dataset, val)


def RecommendJob(SSkills, dataset, val):
    # print("jobs")
    return Recommendation(SSkills, dataset, val)


# print('Top 5 Exams suggested for You:')
WSkills = ["coding", "aptitude", "English"]
dataset = 'Exam_Recommendation.csv'
val = 'Exam Name'
RecommendExam(WSkills, dataset, val)

# print('Top 5 Jobs suggested for You:')
SSkills = ["coding", "aptitude", "English"]
dataset = 'job_recommendation.csv'
val = 'job'
RecommendJob(SSkills, dataset, val)
