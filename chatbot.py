import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load knowledge base
with open("college_data.txt", "r", encoding="utf-8") as f:
    corpus = [line.strip().lower() for line in f if line.strip()]

# Better TF-IDF (n-grams improve matching)
vectorizer = TfidfVectorizer(
    stop_words='english',
    ngram_range=(1, 2)   # BIG upgrade
)

X = vectorizer.fit_transform(corpus)

# Synonym dictionary (VERY IMPORTANT)
synonyms = {
    "tnu": "the neotia university",
    "college": "university",
    "hostel": "residential facility",
    "fees": "fee structure",
    "placement": "job placement",
    "companies": "recruiters",
    "courses": "programs"
}

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Replace synonyms
    for key, value in synonyms.items():
        text = text.replace(key, value)

    return text

def chatbot_response(user_input):
    user_input = clean_text(user_input)

    user_vec = vectorizer.transform([user_input])
    similarity = cosine_similarity(user_vec, X)[0]

    # Get top 3 matches instead of 1
    top_indices = similarity.argsort()[-3:][::-1]
    best_score = similarity[top_indices[0]]

    if best_score < 0.15:
        return "I couldn't find exact info. Try asking about courses, placements, hostel, campus, or facilities."

    # Combine top results (makes answers richer)
    responses = [corpus[i] for i in top_indices if similarity[i] > 0.1]

    return " ".join(responses).capitalize()