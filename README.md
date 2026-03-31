# 📄 AI Resume Reviewer

A professional AI-powered web app that analyzes your resume against a job description and gives instant, structured feedback including a match score, strengths, gaps and quick fixes.

🔗 **Live Demo:** https://ai-resume-reviewer-rjfbacdeeg6ei4smv3gso8.streamlit.app

---

## ✨ Features

- **Match Score** — Get a score out of 10 showing how well your resume fits the job
- **Strengths** — See what your resume does well for the specific role
- **Gaps** — Find out what is missing compared to the job requirements
- **Quick Fixes** — Get 3 specific changes to make your resume stronger
- **PDF Upload** — Upload your resume as a PDF or paste it as text
- **Clean UI** — Professional dark theme built for a great user experience

---

## 🛠️ Built With

- [Python](https://python.org)
- [Streamlit](https://streamlit.io)
- [Groq API](https://console.groq.com) (LLaMA 3.3 70B)
- [PyPDF2](https://pypdf2.readthedocs.io)
- [python-dotenv](https://pypi.org/project/python-dotenv)

---

## 🚀 Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/saipraneethp7/ai-resume-reviewer.git
cd ai-resume-reviewer
```

**2. Create a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your API key**

Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free Groq API key at https://console.groq.com

**5. Run the app**
```bash
streamlit run app.py
```

---

## 📁 Project Structure
```
ai-resume-reviewer/
├── app.py              # Main Streamlit app
├── requirements.txt    # Python dependencies
├── .env                # API key (not committed)
├── .gitignore          # Ignored files
└── README.md           # Project documentation
```

---

## 👤 Author

**Sai Praneeth**
- GitHub: [@saipraneethp7](https://github.com/saipraneethp7)
- University: UMKC, CS Class of 2026

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).