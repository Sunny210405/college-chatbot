import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Load knowledge base
with open("college_data.txt", "r", encoding="utf-8") as f:
    display_corpus = [line.strip() for line in f if line.strip()]

corpus = [line.lower() for line in display_corpus]

# Better TF-IDF (n-grams improve matching)
vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
)

X = vectorizer.fit_transform(corpus)

# Synonym dictionary
synonyms = {
    "tnu": "the neotia university",
    "college": "university",
    "hostel": "residential facility",
    "hostels": "residential facility",
    "fees": "fee structure",
    "fee": "fee structure",
    "cost": "fee structure",
    "scholarship": "financial aid",
    "placement": "job placement",
    "placements": "job placement",
    "package": "salary",
    "companies": "recruiters",
    "courses": "programs",
    "course": "programs",
    "btech": "b tech engineering cse",
    "bca": "bachelor computer application",
    "bba": "bba business administration humanities management",
    "bpharm": "bachelor pharmacy",
}

topic_terms = {
    "fees": {"fee", "fees", "cost", "semester", "total"},
    "placements": {"placement", "placements", "salary", "package", "recruiters", "companies", "internship"},
    "hostel": {"hostel", "hostels", "residential", "mess", "dining"},
    "admissions": {"admission", "admissions", "apply", "entrance", "eligibility"},
    "courses": {"course", "courses", "program", "programs", "school"},
}

focus_terms = {
    "btech": {"b.tech", "b tech", "btech", "cse", "engineering"},
    "bba": {"bba", "bba hons", "business administration", "humanities and management"},
    "bca": {"bca", "computer application"},
    "bpharm": {"b.pharm", "b pharm", "bpharm", "pharmacy"},
    "hostel": {"hostel", "hostels", "residential"},
    "nautical": {"nautical", "maritime"},
    "law": {"law", "llb", "legal"},
}


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # Replace common synonyms so student-style questions still match.
    for key, value in synonyms.items():
        text = text.replace(key, value)

    return text


def short_answer(responses, max_sentences=2, max_chars=430):
    answer = " ".join(responses)

    if len(responses) > max_sentences:
        answer = " ".join(responses[:max_sentences])

    if len(answer) <= max_chars:
        return answer

    cut_at = answer.rfind(". ", 0, max_chars)
    if cut_at != -1:
        return answer[: cut_at + 1]

    cut_at = answer.rfind(" ", 0, max_chars)
    if cut_at == -1:
        return answer[:max_chars].rstrip() + "..."

    return answer[:cut_at].rstrip() + "..."


def query_topics(cleaned_query):
    words = set(cleaned_query.split())
    return [topic for topic, terms in topic_terms.items() if words & terms]


def query_focus(cleaned_query):
    words = set(cleaned_query.split())
    matches = []

    for focus, terms in focus_terms.items():
        cleaned_terms = {clean_text(term) for term in terms}
        if focus in words or words & cleaned_terms or any(term in cleaned_query for term in cleaned_terms):
            matches.append(focus)

    return matches


def ranked_scores(cleaned_query):
    user_vec = vectorizer.transform([cleaned_query])
    scores = cosine_similarity(user_vec, X)[0]
    topics = query_topics(cleaned_query)
    focuses = query_focus(cleaned_query)

    for index, line in enumerate(corpus):
        words = set(line.split())
        matched_topic = False
        matched_focus = False

        for topic in topics:
            if words & topic_terms[topic]:
                scores[index] += 0.22
                matched_topic = True

        for focus in focuses:
            if any(term in line for term in focus_terms[focus]):
                scores[index] += 0.08
                matched_focus = True

        if matched_topic and matched_focus:
            scores[index] += 0.28

    return scores


def chatbot_response(user_input, current_course=None):
    user_input_clean = clean_text(user_input)
    
    # Check if user is asking about fees but hasn't mentioned a specific course
    if any(word in user_input_clean for word in ["fee", "cost", "price", "charge"]):
        courses = ["btech", "bca", "bba", "bpharm", "nursing", "law", "nautical", "agriculture", "fisheries"]
        course_mentioned = any(course in user_input_clean for course in courses)
        
        # If no course mentioned in current query, but we have context from previous conversation
        if not course_mentioned and current_course:
            # Append course context to the query for better search results
            user_input_clean = user_input_clean + " " + current_course.lower()
        elif not course_mentioned:
            return "Which course's fee structure would you like to know about? We offer B.Tech, BCA, BBA, B.Pharmacy, B.Nursing, BA LLB, B.Sc. Nautical Science, B.Sc. Agriculture, and B.Sc. Fisheries Science. Please specify the course name."

    similarity = ranked_scores(user_input_clean)

    # Use the old simple top-match behavior, but keep answers compact.
    top_indices = similarity.argsort()[-3:][::-1]
    best_score = similarity[top_indices[0]]

    if best_score < 0.15:
        return "I couldn't find exact info. Try asking about courses, fees, admissions, hostel, placements, or facilities."

    focuses = query_focus(user_input)
    topics = query_topics(user_input)
    responses = []

    for i in top_indices:
        if similarity[i] <= 0.1:
            continue

        response = display_corpus[i]

        if focuses:
            lower_response = response.lower()
            is_focused = any(
                any(term in lower_response for term in focus_terms[focus])
                for focus in focuses
            )
            if not is_focused:
                continue

        responses.append(response)

    if not responses:
        responses = [
            display_corpus[i]
            for i in top_indices
            if similarity[i] > 0.1
        ]

    if "fees" in topics:
        responses.sort(key=lambda response: "has a semester fee" not in response.lower())

    return short_answer(responses, max_chars=520)
