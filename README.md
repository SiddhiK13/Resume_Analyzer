# 📄 AI Resume Analyzer

An AI-powered web app that analyzes your resume against a job description and gives instant feedback — including ATS score, skill gaps, strengths, and predicted interview questions.

Built with Python, Groq LLaMA AI, and Streamlit.

---

## 🚀 Live Demo

> Upload your resume PDF + paste any job description → get AI feedback in seconds

---

## ✨ Features

- 📊 ATS Compatibility Score (out of 100)
- 💪 Top 3 strengths from your resume
- 🔍 Top 3 skill gaps for the role
- ✏️ 3 specific resume improvements
- 🎯 3 predicted interview questions

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core programming language |
| Groq API (LLaMA 3.3 70B) | AI analysis engine |
| pdfplumber | PDF text extraction |
| Streamlit | Web app interface |

---

## ⚙️ How to Run Locally

### 1. Clone the repository

git clone https://github.com/YOUR-USERNAME/ai-resume-analyzer.git
cd ai-resume-analyzer

### 2. Install dependencies

pip install -r requirements.txt

### 3. Get your free Groq API key
- Go to [console.groq.com](https://console.groq.com)
- Sign up for free
- Create an API key

### 4. Add your API key
Open `app.py` and replace line 4:
```python
client = Groq(api_key="your-groq-key-here")
```

### 5. Run the app

streamlit run app.py

Open your browser at `http://localhost:8501`

---

## 📸 How to Use

1. Upload your resume as a PDF
2. Paste the job description you are applying for
3. Click **Analyze My Resume**
4. Get detailed AI feedback instantly

---

## 👨‍💻 Author

**Siddhi Kshirsagar**
- LinkedIn: https://www.linkedin.com/in/siddhi-kshirsagar04/
- GitHub: https://github.com/SiddhiK13

---

## 📌 Note

This project was built as part of my AI/ML portfolio to demonstrate skills in API integration, NLP, and full-stack Python development.
