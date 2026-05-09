import re
from collections import defaultdict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load knowledge base
with open("college_data.txt", "r", encoding="utf-8") as f:
    corpus = [line.strip() for line in f if line.strip()]


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    for key, value in synonyms.items():
        text = re.sub(rf"\b{re.escape(key)}\b", value, text)

    return re.sub(r"\s+", " ", text).strip()


# Better TF-IDF (n-grams improve matching)
vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 3),
    sublinear_tf=True,
)

# Synonym dictionary (VERY IMPORTANT)
synonyms = {
    "tnu": "the neotia university",
    "college": "university",
    "hostel": "residential facility",
    "hostels": "residential facility",
    "mess": "dining housing hostel food",
    "food": "dining mess",
    "fees": "fee structure",
    "fee": "fee structure",
    "cost": "fee structure",
    "price": "fee structure",
    "scholarship": "scholarships financial aid",
    "scholarships": "scholarships financial aid",
    "placement": "job placement",
    "placements": "job placement",
    "package": "salary placement",
    "salary": "salary placement",
    "companies": "recruiters",
    "recruiter": "recruiters",
    "recruiters": "recruiters",
    "courses": "programs",
    "course": "programs",
    "programmes": "programs",
    "programs": "programs",
    "admission": "admissions application entrance eligibility",
    "apply": "admissions application",
    "eligibility": "eligibility criteria",
    "btech": "b tech b.tech engineering",
    "bca": "bachelor computer application",
    "bba": "business administration management",
    "bpharm": "bachelor pharmacy",
    "b pharm": "bachelor pharmacy",
    "nautical": "nautical science maritime",
    "marine": "maritime marine engineering",
    "law": "legal studies ba llb bba llb",
    "contact": "phone email address admissions contact",
    "address": "campus address contact",
    "documents": "documents verification admission",
}

search_corpus = [clean_text(line) for line in corpus]
X = vectorizer.fit_transform(search_corpus)

category_terms = {
    "fees": {"fee", "fees", "cost", "semester", "payment", "scholarship", "scholarships"},
    "admissions": {"admission", "admissions", "apply", "application", "entrance", "test", "eligibility", "documents"},
    "courses": {"course", "courses", "program", "programs", "btech", "bca", "bba", "bpharm", "pharmacy", "law", "marine", "nautical"},
    "hostel": {"hostel", "hostels", "mess", "residential", "dining", "campus", "gym", "medical", "ragging"},
    "placements": {"placement", "placements", "recruiter", "recruiters", "salary", "package", "internship", "companies"},
    "contact": {"contact", "phone", "email", "address", "number", "enquiry"},
}

course_focus_terms = {
    "btech": {"b.tech", "b tech", "btech", "engineering", "cse"},
    "bca": {"bca", "bachelor of computer application"},
    "bba": {"bba", "business administration", "management"},
    "bpharm": {"b.pharm", "b pharm", "bpharm", "pharmacy"},
    "pharmacy": {"pharmacy", "b.pharm", "b pharm", "bpharm"},
    "nautical": {"nautical", "b.sc. nautical", "bsc nautical", "maritime"},
    "marine": {"marine", "maritime"},
    "law": {"law", "legal", "llb", "ba llb", "bba llb"},
    "biotechnology": {"biotechnology", "biotech", "integrated sciences"},
    "nursing": {"nursing", "gnm"},
    "hostel": {"hostel", "hostels", "residential", "dining"},
}


def matched_categories(cleaned_query):
    words = set(cleaned_query.split())
    return [name for name, terms in category_terms.items() if words & terms]


def matched_course_focus(cleaned_query):
    words = set(cleaned_query.split())
    matches = []

    for name, terms in course_focus_terms.items():
        normalized_terms = {clean_text(term) for term in terms}
        if name in words or words & normalized_terms:
            matches.append(name)

    return matches


def boosted_scores(cleaned_query):
    user_vec = vectorizer.transform([cleaned_query])
    scores = cosine_similarity(user_vec, X)[0]

    categories = matched_categories(cleaned_query)
    if not categories:
        return scores

    boosts = defaultdict(float)
    for index, line in enumerate(search_corpus):
        line_words = set(line.split())
        for category in categories:
            if line_words & category_terms[category]:
                boosts[index] += 0.08

    for index, boost in boosts.items():
        scores[index] += boost

    for focus in matched_course_focus(cleaned_query):
        terms = course_focus_terms[focus]
        for index, original_line in enumerate(corpus):
            line = original_line.lower()
            if any(term in line for term in terms):
                scores[index] += 0.15

    return scores


def shorten_fact(text, max_length=175):
    if len(text) <= max_length:
        return text

    cut_at = text.rfind(", and ", 0, max_length)
    if cut_at == -1:
        cut_at = text.rfind(", ", 0, max_length)
    if cut_at == -1:
        cut_at = text.rfind(" ", 0, max_length)

    if cut_at == -1:
        return text[:max_length].rstrip() + "..."

    return text[:cut_at].rstrip() + "..."


def format_answer(responses, categories=None):
    if not responses:
        return ""

    categories = categories or []
    max_items = 3 if len(responses) > 2 else len(responses)

    # Most fee/admission answers feel better with fewer, denser facts.
    if any(category in categories for category in {"fees", "admissions", "contact"}):
        max_items = min(max_items, 2)

    selected = [shorten_fact(response) for response in responses[:max_items]]

    if len(selected) == 1:
        return selected[0]

    return "\n".join(f"- {fact}" for fact in selected)


def category_priority(response, categories):
    text = clean_text(response)
    priority = 0

    priority_terms = {
        "fees": {"fee", "semester", "total", "payment", "scholarship"},
        "admissions": {"admission", "apply", "application", "entrance", "provisional", "eligibility"},
        "placements": {"placement", "salary", "recruiters", "companies", "internship", "average", "highest"},
        "hostel": {"hostel", "residential", "dining", "mess", "warden", "campus facilities"},
        "courses": {"course", "courses", "school", "programs", "eligibility"},
        "contact": {"contact", "email", "address", "phone", "enquiry"},
    }

    for category in categories:
        priority += sum(1 for term in priority_terms.get(category, set()) if term in text)

    return priority


def chatbot_response(user_input):
    user_input = clean_text(user_input)

    if not user_input:
        return "Please ask me about TNU courses, fees, admissions, hostel, scholarships, placements, or contact details."

    greetings = {"hi", "hello", "hey", "good morning", "good evening"}
    if user_input in greetings:
        return "Hello! Ask me about The Neotia University courses, fees, admissions, hostel, scholarships, placements, or contact details."

    similarity = boosted_scores(user_input)

    top_indices = similarity.argsort()[-6:][::-1]
    best_score = similarity[top_indices[0]]

    if best_score < 0.12:
        return "I couldn't find exact info. Try asking about TNU courses, fees, admissions, hostel, scholarships, placements, or contact details."

    responses = []
    seen = set()
    focus_matches = matched_course_focus(user_input)
    categories = matched_categories(user_input)

    for index in top_indices:
        if similarity[index] < 0.10:
            continue

        response = corpus[index]
        if focus_matches:
            lower_response = response.lower()
            is_focused = any(
                any(term in lower_response for term in course_focus_terms[focus])
                for focus in focus_matches
            )
            if not is_focused and len(responses) < 2:
                continue

        normalized = clean_text(response)

        if normalized in seen:
            continue

        responses.append(response)
        seen.add(normalized)

        if len(responses) == 3:
            break

    responses.sort(key=lambda response: category_priority(response, categories), reverse=True)

    return format_answer(responses, categories)
