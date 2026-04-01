# Nyay AI - Legal Advisor for India

> AI-powered legal assistant grounded in Indian law. Every response is constrained to the knowledge base or the uploaded document. Zero hallucinations by design.

[![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.x-green?style=flat-square)](https://djangoproject.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-orange?style=flat-square)](https://console.groq.com)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue?style=flat-square)](https://postgresql.org)
[![Live](https://img.shields.io/badge/Live-Demo-brightgreen?style=flat-square)](https://nyay-ai-legal-advisor.onrender.com)

**[Live Demo](https://nyay-ai-legal-advisor.onrender.com)** | **[LinkedIn](https://linkedin.com/in/balaji-bhairwad)** | **[GitHub](https://github.com/balaji049)**

---

## Screenshots


![Nyay AI Chat Interface](ADD_SCREENSHOT_URL_HERE)

---

## What this project does

Nyay AI is a full-stack legal assistant that answers questions about Indian law
in plain language. It covers IPC sections, CrPC procedures, tenant rights,
employment law, and contract review.

Most people cannot afford a lawyer for everyday legal doubts. Nyay fills that
gap by giving clear, grounded answers without hallucinating legal citations
that do not exist.

The core design decision: the AI is not allowed to answer from general
knowledge alone. Every response is constrained to the legal knowledge base
or the specific document the user uploads. If the answer is not there, the
system says so.

---

## Two modes of operation

### 1. General legal chat

Ask questions about Indian law in plain language. The system loads the full
conversation history from PostgreSQL before every response, so context
carries across multiple sessions. You never have to repeat yourself.

Covers:
- Indian Penal Code (IPC) sections and offences
- Code of Criminal Procedure (CrPC)
- Tenant rights and rental disputes
- Employment law and wrongful termination
- Contract review and clause explanation
- FIR generation with correct section references
- IPC section lookup by number or keyword
- PDF export of any consultation

### 2. Document-aware chat (RAG)

Upload a contract, legal notice, or any PDF. The system extracts the content
using PyMuPDF and constrains the AI to answer strictly from that document.
General knowledge is explicitly blocked in the prompt.

Use this for:
- Understanding what a rental agreement actually says
- Checking if a job offer letter has unusual clauses
- Reviewing a legal notice before responding to it

The prompt injection for document mode:

```
Answer only using the content from the document provided below.
Do not use any general knowledge. If the answer is not in the
document, say: "I could not find this in the document."
```

This matters in a legal context. A hallucinated IPC section number or a
fabricated contract clause can cause real harm.

---

## Engineering decisions

### Model fallback chain

The primary model is LLaMA 3.3 70B via Groq API. If it hits a rate limit,
the system silently falls back to LLaMA 3.1 8B, then Gemma 2 9B. The user
never sees an error. This was a deliberate production decision built into
the Groq client wrapper.

```
Request arrives
      |
      v
Try LLaMA 3.3 70B
      |
   success? --> return response
      |
   rate limit?
      |
      v
Try LLaMA 3.1 8B
      |
   success? --> return response
      |
   rate limit?
      |
      v
Try Gemma 2 9B --> return response
```

### Persistent conversation memory

The full conversation history is loaded from PostgreSQL before every API
call. Most demo chatbots reset on every message. Legal consultations span
multiple sessions. Nyay keeps the entire thread intact.

### SQLite locally, PostgreSQL in production

Local development uses Django's default SQLite for zero-setup. Production
on Render uses PostgreSQL. The switch is handled entirely via the
DATABASE_URL environment variable and dj-database-url, so no code changes
are needed between environments.

---

## Tech stack

| Layer          | Technology                                           |
|----------------|------------------------------------------------------|
| Backend        | Python 3.10, Django                                  |
| AI inference   | Groq API (LLaMA 3.3 70B + LLaMA 3.1 8B + Gemma 2 9B)|
| Document RAG   | PyMuPDF (text extraction from uploaded PDFs)         |
| Database       | PostgreSQL (production), SQLite (local dev)          |
| Frontend       | HTML, CSS, JavaScript                                |
| Auth           | Django built-in authentication                       |
| Deployment     | Render                                               |

---

## Project structure

```
nyay_ai_legal_advisor/
|
+-- manage.py
+-- requirements.txt
+-- .env                         # never commit this
+-- .env.example                 # safe to commit, no real keys
|
+-- nyay_project/
|   +-- settings.py
|   +-- urls.py
|   +-- wsgi.py
|
+-- chat/
    +-- models.py                # Conversation and Message models
    +-- views.py                 # Chat logic, Groq API calls, fallback chain
    +-- urls.py
    +-- templates/chat/
        +-- index.html           # Main chat UI
        +-- login.html
        +-- signup.html
```

---

## How to run locally

```bash
# Clone
git clone https://github.com/balaji049/nyay_ai_legal_advisor.git
cd nyay_ai_legal_advisor

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate          # macOS and Linux
.\venv\Scripts\activate           # Windows PowerShell

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the root folder:

```
SECRET_KEY=your_django_secret_key_here
GROQ_API_KEY=gsk_your_groq_key_here
```

For local dev, SQLite is used automatically. No DATABASE_URL needed.

```bash
# Run migrations
python manage.py makemigrations chat
python manage.py migrate

# Start the server
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

---

## Getting a Groq API key

1. Go to [console.groq.com](https://console.groq.com) and sign up (free)
2. Click API Keys, then Create API Key
3. Copy the key immediately. It starts with `gsk_` and is shown only once
4. Paste it into your `.env` file

---

## Deploying to production (Render)

1. Push the repo to GitHub
2. Create a new Web Service on Render, connect the repo
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn nyay_project.wsgi`
5. Add environment variables in Render dashboard:

```
SECRET_KEY=your_production_secret_key
GROQ_API_KEY=gsk_your_groq_key
DATABASE_URL=postgresql://...      # from Render PostgreSQL add-on
```

Render's PostgreSQL add-on provides the DATABASE_URL automatically when
you attach it to the service.

---

## Request flow

```
User message
      |
      v
Load full conversation history from PostgreSQL
      |
      v
Document uploaded? -- YES --> PyMuPDF extracts text --> inject as context
                  -- NO  --> use general legal knowledge prompt
      |
      v
Call Groq API (LLaMA 3.3 70B)
      |
      v
Rate limit hit? -- YES --> LLaMA 3.1 8B --> Gemma 2 9B
               -- NO  --> use response
      |
      v
Save new messages to PostgreSQL
      |
      v
Render in chat UI
```

---

## What I want to improve

- Hindi, Telugu, and Tamil language support. Most people with legal questions
  in Telangana are not thinking in English.
- Source highlighting: show the exact sentence in the uploaded document that
  the answer came from.
- Voice input for accessibility.
- Find a nearby advocate using location and Bar Council data.

---

## Disclaimer

Nyay AI provides general legal information, not legal advice. For anything
serious, consult a lawyer registered with the Bar Council of India.

---

## Author

**Balaji Bhairwad**
B.Tech, Computer Science and Engineering (AI and ML)
Malla Reddy Engineering College, Hyderabad

[LinkedIn](https://linkedin.com/in/balaji-bhairwad) | [GitHub](https://github.com/balaji049) | [Live Demo](https://nyay-ai-legal-advisor.onrender.com)

---

*Built because most people cannot afford a lawyer for every small legal doubt.*
