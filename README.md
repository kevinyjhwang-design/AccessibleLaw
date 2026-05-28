# Accessible Law

Most people can't afford a lawyer — but everyone deserves to understand their rights. Accessible Law is a free web app that translates legal documents into plain English, walks you through your options step by step, and lets you ask an AI legal companion anything, anytime.

Built specifically for Alabama residents.

---

## What it does

**Translate a document** — Upload a lease, contract, or legal notice and get a plain-English breakdown of every clause. Red flags are highlighted so you know what to watch out for.

**Action Guides** — Step-by-step checklists for real situations: getting your security deposit back, fighting an eviction, disputing unpaid wages, and more. Each guide includes a timeline and a letter generator that writes a ready-to-send letter with your details filled in.

**Ask Lex** — An AI legal companion you can talk to in plain words, any time of day. No legal jargon needed. Lex explains your rights, answers follow-up questions, and points you to next steps.

**Browse Alabama Laws** — Search laws by topic (housing, employment, family, criminal) and read what each law actually means for you — not just what it says.

**Story Match** — Describe your situation and find similar cases where people won, along with how they did it.

---

## Running it locally

**1. Install dependencies**
```bash
pip3 install flask flask-sqlalchemy pdfplumber python-docx google-genai
```

**2. Get a free Gemini API key**

Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey) → Create API key in new project. It's free, no credit card needed.

**3. Add your key**
```bash
echo 'GEMINI_API_KEY=your-key-here' > .env
```

**4. Set up the database**
```bash
python3 seed_data.py
```

**5. Start the app**
```bash
source .env && python3 app.py
```

Then open [http://localhost:5050](http://localhost:5050).

> No API key? The app still works — AI features are off, but guides, law browsing, and search all run fine.

---

## Stack

| Layer | Tools |
|---|---|
| Backend | Python, Flask, SQLite |
| AI | Google Gemini (`gemini-2.0-flash`) |
| Document parsing | pdfplumber, python-docx |
| Frontend | HTML, CSS, Vanilla JS |
| Real-time chat | Server-Sent Events (SSE) |
| Offline support | Progressive Web App (PWA) |

---

## Project structure

```
alabama-legal-aid/
├── app.py                  # routes, models, AI calls
├── seed_data.py            # populates the database
├── requirements.txt
├── templates/              # Jinja2 HTML templates
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
    ├── manifest.json
    └── sw.js
```

---

## Disclaimer

This app provides legal **information**, not legal advice. Lex is not a lawyer. For anything serious, please talk to a real attorney.

**Free legal help in Alabama:**
- Legal Aid Alabama — [1-866-456-4995](tel:18664564995)
- Alabama DV Hotline — [1-800-650-6522](tel:18006506522)
- National DV Hotline — [1-800-799-7233](tel:18007799233)
