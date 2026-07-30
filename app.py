Here it is — copy everything between the lines:

```python
import json
import os
import io

from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///laws.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ── Optional AI client (graceful if key is missing) ──────────────────────────
try:
    from groq import Groq as _Groq
    _groq_key = os.environ.get("GROQ_API_KEY", "")
    if _groq_key:
        _ai = _Groq(api_key=_groq_key)
        AI_ENABLED = True
    else:
        _ai = None
        AI_ENABLED = False
except ImportError:
    _ai = None
    AI_ENABLED = False

AI_MODEL = "llama-3.3-70b-versatile"

# ── Document parsers (graceful if libs missing) ──────────────────────────────
try:
    import pdfplumber
    PDF_ENABLED = True
except ImportError:
    PDF_ENABLED = False

try:
    from docx import Document as DocxDocument
    DOCX_ENABLED = True
except ImportError:
    DOCX_ENABLED = False


# ════════════════════════════════════════════════════════════════════════════
# Database Models
# ════════════════════════════════════════════════════════════════════════════

class Category(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    slug        = db.Column(db.String(50), unique=True, nullable=False)
    name        = db.Column(db.String(100), nullable=False)
    icon        = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(200))
    laws        = db.relationship("Law", backref="category", lazy=True)
    guides      = db.relationship("Guide", backref="category", lazy=True)


class Law(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    category_id  = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    title        = db.Column(db.String(200), nullable=False)
    statute      = db.Column(db.String(100))
    legal_text   = db.Column(db.Text, nullable=False)
    plain_english= db.Column(db.Text, nullable=False)
    steps        = db.Column(db.Text)
    consequences = db.Column(db.Text)
    warning      = db.Column(db.Text)
    keywords     = db.Column(db.Text)


class CaseStory(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    category_id     = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    summary         = db.Column(db.Text, nullable=False)
    year            = db.Column(db.Integer)
    location        = db.Column(db.String(100))
    outcome         = db.Column(db.Text, nullable=False)
    follow_up_question = db.Column(db.Text)
    keywords        = db.Column(db.Text)


class Guide(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    category_id     = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    slug            = db.Column(db.String(100), unique=True, nullable=False)
    title           = db.Column(db.String(200), nullable=False)
    subtitle        = db.Column(db.String(300))
    icon            = db.Column(db.String(10), nullable=False)
    scenario        = db.Column(db.Text)
    timeline        = db.Column(db.Text)
    checklist       = db.Column(db.Text)
    letter_template = db.Column(db.Text)
    keywords        = db.Column(db.Text)


# ════════════════════════════════════════════════════════════════════════════
# AI Prompts
# ════════════════════════════════════════════════════════════════════════════

TRANSLATE_SYSTEM = """You are a legal document analyst helping everyday people understand legal contracts and statutes.
Analyze the provided text and return ONLY valid JSON — no markdown, no explanation outside the JSON.

Return this exact structure:
{
  "doc_type": "Brief document type (e.g. Rental Agreement, Employment Contract, Statute)",
  "summary": "2–3 sentence plain-English overview at a 5th-grade reading level.",
  "red_flags": ["Concerning item 1", "Concerning item 2"],
  "action_items": ["Thing the user should do 1", "Thing the user should do 2"],
  "clauses": [
    {
      "title": "Short clause name",
      "original": "The original legal text (up to 200 chars, truncate with …)",
      "plain_english": "What this means for you in 1–3 simple sentences.",
      "risk_level": "low|medium|high",
      "why_it_matters": "One sentence on why this clause matters to the user."
    }
  ]
}

Risk levels:
- low: Standard, uncontroversial clause.
- medium: Worth understanding; could affect user's rights.
- high: Potentially harmful; user should consider negotiating or seeking legal advice.

Keep all explanations at a 5th–6th grade reading level. Never give specific legal advice."""

CHAT_SYSTEM = """You are "Lex," a friendly, empathetic AI legal companion built into the Accessible Law platform.
Your job is to help everyday people understand their legal rights — not to give formal legal advice.

Rules:
1. Always speak in plain English at a 5th–6th grade reading level.
2. Be warm, calm, and reassuring — users are often stressed.
3. Never give specific legal advice. Give clear, accurate legal information.
4. Always note that you are not a lawyer and recommend consulting one for serious matters.
5. When relevant, suggest the platform's Translation Engine or Action Guides.
6. Keep responses concise — 3–5 short paragraphs max.
7. End every response with a clear "Next Step" suggestion.
8. If a question involves domestic violence, mental health crisis, or immediate danger, lead with emergency resources first.

Platform features you can reference:
- "Translation Engine" (/translate): Upload a document to get a plain-English breakdown.
- "Action Guides" (/guides): Step-by-step guides for specific situations.
- Legal Aid Alabama: 1-866-456-4995 (free legal help).
- National DV Hotline: 1-800-799-7233."""

LETTER_SYSTEM = """You are a legal document drafter helping everyday people write clear, professional legal correspondence.
Generate a formal but plain-English letter based on the guide type and user's input details.
The letter should:
- Be polite but firm.
- Cite the relevant law or right where applicable.
- Request specific action with a deadline.
- Be ready to print and mail or email.
Return ONLY the letter text — no explanation, no markdown."""


# ════════════════════════════════════════════════════════════════════════════
# Helpers
# ════════════════════════════════════════════════════════════════════════════

def extract_text_from_file(file) -> str:
    filename = file.filename.lower()
    if filename.endswith(".pdf") and PDF_ENABLED:
        with pdfplumber.open(io.BytesIO(file.read())) as pdf:
            return "\n".join(p.extract_text() or "" for p in pdf.pages)
    elif (filename.endswith(".docx") or filename.endswith(".doc")) and DOCX_ENABLED:
        doc = DocxDocument(io.BytesIO(file.read()))
        return "\n".join(p.text for p in doc.paragraphs)
    else:
        return file.read().decode("utf-8", errors="ignore")


def ai_translate(text: str) -> dict:
    truncated = text[:12000]
    response = _ai.chat.completions.create(
        model=AI_MODEL,
        max_tokens=4096,
        messages=[
            {"role": "system", "content": TRANSLATE_SYSTEM},
            {"role": "user", "content": f"Analyze this legal document:\n\n{truncated}"},
        ],
    )
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw)


# ════════════════════════════════════════════════════════════════════════════
# Routes — Pillar 0: Original Alabama Law Browser
# ════════════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    categories = Category.query.all()
    return render_template("index.html", categories=categories)


@app.route("/laws")
def laws_home():
    categories = Category.query.all()
    return render_template("laws_home.html", categories=categories)


@app.route("/category/<slug>")
def category(slug):
    cat = Category.query.filter_by(slug=slug).first_or_404()
    return render_template("category.html", category=cat, laws=cat.laws)


@app.route("/law/<int:law_id>")
def law(law_id):
    entry = Law.query.get_or_404(law_id)
    steps = json.loads(entry.steps) if entry.steps else []
    consequences = json.loads(entry.consequences) if entry.consequences else []
    return render_template("law.html", law=entry, steps=steps, consequences=consequences)


@app.route("/case-finder")
def case_finder():
    return render_template("case_finder.html")


# ════════════════════════════════════════════════════════════════════════════
# Routes — Pillar 1: Translation Engine
# ════════════════════════════════════════════════════════════════════════════

@app.route("/translate")
def translate():
    return render_template("translator.html", ai_enabled=AI_ENABLED)


@app.route("/api/translate", methods=["POST"])
def api_translate():
    if not AI_ENABLED:
        return jsonify({"error": "AI not configured. Set GROQ_API_KEY."}), 503

    text = ""
    if "file" in request.files and request.files["file"].filename:
        try:
            text = extract_text_from_file(request.files["file"])
        except Exception as e:
            return jsonify({"error": f"Could not read file: {e}"}), 400
    elif request.form.get("text"):
        text = request.form["text"]
    elif request.is_json and request.json.get("text"):
        text = request.json["text"]

    if not text or len(text.strip()) < 50:
        return jsonify({"error": "Please provide at least 50 characters of legal text."}), 400

    try:
        result = ai_translate(text)
        return jsonify(result)
    except json.JSONDecodeError:
        return jsonify({"error": "AI returned unexpected format. Please try again."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ════════════════════════════════════════════════════════════════════════════
# Routes — Pillar 2: Scenario Guides
# ════════════════════════════════════════════════════════════════════════════

@app.route("/guides")
def guides():
    all_guides = Guide.query.all()
    categories = Category.query.all()
    return render_template("guides.html", guides=all_guides, categories=categories)


@app.route("/guide/<slug>")
def guide_detail(slug):
    g = Guide.query.filter_by(slug=slug).first_or_404()
    checklist = json.loads(g.checklist) if g.checklist else []
    timeline  = json.loads(g.timeline) if g.timeline else []
    return render_template("guide_detail.html", guide=g,
                           checklist=checklist, timeline=timeline,
                           ai_enabled=AI_ENABLED)


@app.route("/api/generate-letter", methods=["POST"])
def generate_letter():
    if not AI_ENABLED:
        return jsonify({"error": "AI not configured. Set GROQ_API_KEY."}), 503

    data      = request.get_json() or {}
    guide_slug= data.get("guide_slug", "")
    details   = data.get("details", {})

    guide = Guide.query.filter_by(slug=guide_slug).first()
    template  = guide.letter_template if guide else ""

    detail_str = "\n".join(f"{k}: {v}" for k, v in details.items() if v)
    prompt = (
        f"Guide type: {guide.title if guide else guide_slug}\n"
        f"Letter template to adapt:\n{template}\n\n"
        f"User's specific details:\n{detail_str}\n\n"
        "Write the final letter, filling in all details."
    )
    try:
        response = _ai.chat.completions.create(
            model=AI_MODEL,
            max_tokens=1500,
            messages=[
                {"role": "system", "content": LETTER_SYSTEM},
                {"role": "user", "content": prompt},
            ],
        )
        return jsonify({"letter": response.choices[0].message.content.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ════════════════════════════════════════════════════════════════════════════
# Routes — Pillar 3: AI Legal Companion (streaming chat)
# ════════════════════════════════════════════════════════════════════════════

@app.route("/chat")
def chat():
    return render_template("chat.html", ai_enabled=AI_ENABLED)


@app.route("/api/chat", methods=["POST"])
def api_chat():
    if not AI_ENABLED:
        return jsonify({"error": "AI not configured. Set GROQ_API_KEY."}), 503

    data     = request.get_json() or {}
    history  = data.get("history", [])
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return jsonify({"error": "Empty message."}), 400

    messages = [{"role": "system", "content": CHAT_SYSTEM}]
    for msg in history[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_msg})

    def generate():
        try:
            stream = _ai.chat.completions.create(
                model=AI_MODEL,
                max_tokens=1024,
                messages=messages,
                stream=True,
            )
            for chunk in stream:
                text = chunk.choices[0].delta.content or ""
                if text:
                    yield f"data: {json.dumps({'chunk': text})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        yield "data: [DONE]\n\n"

    return Response(stream_with_context(generate()),
                    mimetype="text/event-stream",
                    headers={"X-Accel-Buffering": "no",
                             "Cache-Control": "no-cache"})


# ════════════════════════════════════════════════════════════════════════════
# Existing search + case-finder APIs
# ════════════════════════════════════════════════════════════════════════════

@app.route("/api/match-case", methods=["POST"])
def match_case():
    data = request.get_json()
    user_input = (data.get("query") or "").lower()
    if not user_input:
        return jsonify({"matches": []})

    words = set(user_input.split())
    stories = CaseStory.query.all()
    scored = []
    for story in stories:
        kw = {k.strip() for k in (story.keywords or "").lower().split(",")}
        score = len(words & kw)
        if score > 0:
            scored.append((score, story))

    scored.sort(key=lambda x: x[0], reverse=True)
    results = []
    for _, story in scored[:3]:
        results.append({
            "summary": story.summary,
            "year": story.year,
            "location": story.location,
            "outcome": story.outcome,
            "follow_up": story.follow_up_question,
        })
    return jsonify({"matches": results})


@app.route("/api/search")
def search():
    q = (request.args.get("q") or "").lower().strip()
    if len(q) < 2:
        return jsonify({"results": []})
    results = []
    for entry in Law.query.all():
        haystack = " ".join([entry.title, entry.plain_english,
                             entry.legal_text, entry.keywords or ""]).lower()
        if q in haystack:
            results.append({"id": entry.id, "title": entry.title,
                             "category": entry.category.name,
                             "category_slug": entry.category.slug, "type": "law"})
    for g in Guide.query.all():
        haystack = " ".join([g.title, g.subtitle or "",
                             g.scenario or "", g.keywords or ""]).lower()
        if q in haystack:
            results.append({"slug": g.slug, "title": g.title,
                             "category": g.category.name,
                             "category_slug": g.category.slug, "type": "guide"})
    return jsonify({"results": results[:12]})


def auto_seed():
    db.create_all()
    if Category.query.first() is None:
        import seed_data
        seed_data.seed(db, Category, Law, CaseStory, Guide)

with app.app_context():
    auto_seed()

if __name__ == "__main__":
    app.run(debug=True, port=5050)
```
