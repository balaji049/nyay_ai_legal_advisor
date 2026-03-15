# ⚖️ NYAY – AI Legal Advisor for India

Ever tried Googling a legal question in India and ended up more confused than before? That's exactly why I built NYAY.

Most people can't afford a lawyer for every small doubt — *"Can my landlord do this?"*, *"What are my rights if I get fired?"*, *"Is this contract clause even legal?"*. NYAY gives you a place to ask those questions in plain language and actually get a useful answer.

It's built with Django and powered by Groq's LLaMA model. The big thing that makes it different from just prompting ChatGPT: **it remembers your conversation**. Every message is saved to a database and reloaded before each response, so the AI always has full context — no repeating yourself.

---

## What it can do

- Ask anything about Indian laws, rights, or legal procedures and get a clear explanation
- Pick up right where you left off — conversations are saved and searchable
- Works across multiple accounts, each with their own private history
- Falls back across multiple Groq models automatically if one hits a rate limit
- Comes with a clean dark/light mode UI and typing indicators so it feels like a real chat

---

## Tech I used

| | |
|---|---|
| Backend | Django (Python 3.10) |
| AI | Groq API — LLaMA 3.3 70B primary, LLaMA 3.1 8B + Gemma 2 9B as fallbacks |
| Database | SQLite via Django ORM |
| Frontend | Plain HTML, CSS, JavaScript |
| Auth | Django's built-in authentication |
| Config | python-dotenv |

---

## How it works under the hood

Nothing fancy, but it works really well:
```
User sends a message
      ↓
Django loads the full conversation history from SQLite
      ↓
Entire history + new message sent to Groq API
      ↓
AI responds with full context of everything said before
      ↓
New messages saved back to SQLite
      ↓
Response shown in browser
```

The context memory is the core feature. Without it, the AI treats every message as a fresh question. With it, you can have a real back-and-forth like you would with an actual advisor.

---

## Project structure
```
nyay-django/
│
├── manage.py                  ← Django's entry point
├── requirements.txt
├── .env                       ← your API keys go here (never commit this)
├── db.sqlite3                 ← auto-created when you migrate
│
├── nyay_project/
│   ├── settings.py            ← all config lives here
│   ├── urls.py                ← master URL router
│   └── wsgi.py
│
└── chat/
    ├── models.py              ← database tables as Python classes
    ├── views.py               ← all the route logic
    ├── urls.py
    ├── admin.py
    ├── migrations/
    └── templates/chat/
        ├── index.html         ← main chat UI
        ├── login.html
        └── signup.html
```

---

## Running it locally

### 1. Install Python 3.10
Grab it from [python.org](https://www.python.org/downloads/release/python-3100/). On Windows, make sure you check **Add Python to PATH** during setup.

### 2. Windows only — allow scripts to run
Open PowerShell and run this once:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Clone the repo
```bash
git clone https://github.com/balaji049/nyay_ai_legal_advisor.git
cd nyay_ai_legal_advisor
```

### 4. Set up a virtual environment
```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```
Once active, you'll see `(venv)` at the start of your terminal line.

### 5. Upgrade pip and install dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Get your Groq API key
1. Go to [console.groq.com](https://console.groq.com) and sign up
2. Click **API Keys → Create API Key**
3. Copy it immediately — it starts with `gsk_...` and you only see it once

### 7. Create your `.env` file
Make a file called `.env` in the root folder (same level as `manage.py`):
```env
SECRET_KEY=your_django_secret_key_here
GROQ_API_KEY=gsk_your_groq_key_here
```
This file is already in `.gitignore` — don't remove it from there.

### 8. Set up the database
```bash
python manage.py makemigrations chat
python manage.py migrate
```
`makemigrations` reads your models and creates migration files. `migrate` actually builds the tables in `db.sqlite3`.

### 9. Start the server
```bash
python manage.py runserver
```
Then open **http://127.0.0.1:8000** in your browser. (Django uses port 8000, not 5000.)

---

## Admin panel

Want to poke around the database through a UI? Create a superuser:
```bash
python manage.py createsuperuser
```
Then visit `/admin/` while the server is running.

---

## What I want to add next

- 🎤 Voice input so you can just speak your question
- 📄 Upload a document and have the AI explain what it means
- 🌍 Hindi, Telugu, Tamil support — most people asking legal questions aren't thinking in English
- 📍 A map to find nearby lawyers if you need to take things further
- 📱 A proper mobile app

---

## Disclaimer

NYAY gives you **general legal information**, not legal advice. It's meant to help you understand your situation, not replace a qualified advocate. For anything serious, please consult a lawyer registered with the Bar Council of India.

---

## About

Built by **Balaji Bhairwad** as part of my B.Tech in AI & ML.  
GitHub: [github.com/balaji049](https://github.com/balaji049)

If this helped you, a ⭐ on the repo would mean a lot!
