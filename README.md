# Accessible Law 🏛️

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=flat-square&logo=flask)
![Gemini](https://img.shields.io/badge/Google_Gemini-AI-orange?style=flat-square&logo=google)
![PWA](https://img.shields.io/badge/PWA-enabled-purple?style=flat-square)

> Most people can't afford a lawyer, but everyone deserves to understand their rights.

Accessible Law is a free web app for Alabama residents. Upload a contract, get a plain-English breakdown. Follow step-by-step action guides for real situations like evictions and unpaid wages. Or just ask Lex, the AI legal companion, anything you want in plain words.

---

## ✨ Features

| | Feature | What it does |
|---|---|---|
| 📄 | **Translation Engine** | Upload a PDF, Word doc, or paste text. Get a plain-English summary, red flags highlighted, and every clause explained simply. |
| 📋 | **Action Guides** | Step-by-step checklists for evictions, unpaid wages, security deposits, and more. Generates a ready-to-send letter with your details filled in. |
| 🤖 | **Ask Lex AI** | Chat with an AI legal companion anytime. No legal jargon needed. Powered by Google Gemini. |
| ⚖️ | **Alabama Law Browser** | Browse laws by topic and read what each one actually means for you. |
| 🔍 | **Story Match** | Describe your situation and find similar cases where people won. |

---

## 🚀 Getting Started

### 1. Install dependencies
```bash
pip3 install flask flask-sqlalchemy pdfplumber python-docx google-genai
```

### 2. Get a free Gemini API key
Head to [aistudio.google.com/apikey](https://aistudio.google.com/apikey) and click **Create API key in new project**. Free, no credit card needed.

### 3. Add your key
```bash
echo 'GEMINI_API_KEY=your-key-here' > .env
```

### 4. Seed the database
```bash
python3 seed_data.py
```

### 5. Run it
```bash
source .env && python3 app.py
```

Open [http://localhost:5050](http://localhost:5050) and you're in.

> 💡 No API key? The app still runs. AI features are just turned off.

---

## 🗂️ Project Structure

```
alabama-legal-aid/
├── app.py                  # routes, models, AI calls
├── seed_data.py            # populates the database
├── requirements.txt
├── templates/              # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── translator.html
│   ├── chat.html
│   ├── guide_detail.html
│   ├── law.html
│   └── ...
└── static/
    ├── css/
    │   ├── styles.css
    │   └── translator.css
    ├── js/
    │   ├── app.js
    │   ├── chat.js
    │   ├── translator.js
    │   └── guide.js
    ├── manifest.json       # PWA manifest
    └── sw.js               # service worker
```

---

## 🛠️ Tech Stack

- **Backend** -- Python, Flask, SQLAlchemy, SQLite
- **AI** -- Google Gemini (`gemini-2.0-flash`)
- **Document parsing** -- pdfplumber, python-docx
- **Frontend** -- HTML, CSS, Vanilla JS
- **Real-time chat** -- Server-Sent Events (SSE)
- **Offline support** -- Progressive Web App (PWA)

---

## ⚠️ Disclaimer

This app gives legal **information**, not legal advice. Lex is not a lawyer. For anything serious, please talk to a real attorney.

**Free legal help in Alabama:**
- 📞 Legal Aid Alabama -- [1-866-456-4995](tel:18664564995)
- 📞 Alabama DV Hotline -- [1-800-650-6522](tel:18006506522)
- 📞 National DV Hotline -- [1-800-799-7233](tel:18007992733)
