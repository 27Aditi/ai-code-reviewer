# ⚡ ReviewPulse AI: AI-Powered Code Reviewer & PR Explainer Bot

An enterprise-ready AI code analysis and Pull Request review application built with **Streamlit** and powered by **Google Gemini** & **OpenAI**.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🌟 Key Features

- **GitHub PR URL Inspection**: Enter any public PR URL to automatically fetch changed files, commit diffs, additions/deletions, and metadata.
- **Git Diff & Raw Code Analysis**: Paste unified diffs or raw source code files directly for instant review.
- **Security & Vulnerability Detection**: Identifies OWASP top 10 risks, SQL/command injections, authorization flaws, and secrets leakage.
- **Persona & Focus Selection**: Toggle between General Review, Strict Security Auditor, Performance Optimization, or Mentorship/Explainer modes.
- **Actionable Suggestions & PR Generator**: Produces formatted before/after replacement blocks and ready-to-copy PR summaries.
- **Report Export**: Download reviews as Markdown with one click.
- **Dual Engine**: Works with Google Gemini (e.g., `gemini-2.0-flash`, `gemini-1.5-pro`) and OpenAI (`gpt-4o`, `gpt-4o-mini`).

---

## 🚀 Live Demo & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-code-reviewer.git
cd ai-code-reviewer
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS / Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run Streamlit App
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## ☁️ Deploying to Streamlit Cloud (Free)

1. Fork or push this repository to your GitHub account.
2. Sign in to [share.streamlit.io](https://share.streamlit.io/).
3. Click **"New App"** and select:
   - **Repository:** `your-username/ai-code-reviewer`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. *(Optional)* Add your secrets in **Advanced Settings -> Secrets**:
   ```toml
   GEMINI_API_KEY = "your-gemini-key"
   OPENAI_API_KEY = "your-openai-key"
   GITHUB_TOKEN = "your-optional-github-token"
   ```
5. Click **Deploy!** 🎉

---

## 🛡️ License
Distributed under the MIT License.
