# 🎓 College AI Chatbot

An intelligent FAQ chatbot built for **The Neotia University**, designed to answer student queries related to courses, placements, campus facilities, and more using **TF-IDF-based Natural Language Processing**.

---

## 🚀 Features

* 🧠 TF-IDF + Cosine Similarity based response system
* 📚 Knowledge-based chatbot using custom dataset
* 🎨 Modern dark-themed UI with animations
* ⚡ Fast and lightweight (no external APIs required)
* 🔄 Typing animation for realistic responses

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit** (Frontend + UI)
* **Scikit-learn** (TF-IDF Vectorization)
* **NumPy**
* **HTML + CSS** (Custom styling)

---

## 🧠 How It Works

1. User enters a query
2. Text is cleaned and processed
3. TF-IDF vectorization converts text into numerical form
4. Cosine similarity finds the closest matching answer
5. Top relevant responses are returned

---

## 📂 Project Structure

```
college-chatbot/
│── streamlit_app.py     # UI + App logic  
│── chatbot.py           # TF-IDF chatbot logic  
│── college_data.txt     # Knowledge base  
│── requirements.txt     # Dependencies  
│── README.md            # Documentation  
```

---

## ▶️ Run Locally

```bash
git clone https://github.com/Sunny210405/college-chatbot.git
cd college-chatbot
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

## 🌐 Live Demo

*(Add your Streamlit deployment link here once deployed)*

---

## 📌 Example Queries

* "What courses are offered?"
* "Does the university provide hostel facilities?"
* "What is the placement rate?"
* "Top recruiters?"

---

## 🎯 Future Improvements

* 🔍 Better semantic search (embeddings)
* 🌐 Integration with live college website
* 📄 PDF/document-based chatbot
* 🧠 Context-aware conversations

---

## 👨‍💻 Author

**Anindya Jana**
B.Tech CSE (AI & ML)
GitHub: https://github.com/Sunny210405

---

## 📜 License

This project is licensed under the MIT License.
