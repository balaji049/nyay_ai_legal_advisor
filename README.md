# ⚖️ NYAY – AI Legal Advisor for India

> AI-powered legal advisor built with Django and Groq LLM that helps users understand Indian laws, rights, and legal procedures through conversational AI with persistent context memory.

---

## 📌 Project Overview

Access to reliable legal information in India is often expensive and difficult for common citizens. Many AI chatbots provide generic answers and forget previous messages, making conversations inconsistent.

**NYAY solves this by:**
- 🤖 Providing AI-powered legal explanations specialized for Indian law
- 🧠 Maintaining conversation memory so the AI understands context
- 💾 Allowing users to save and revisit past conversations
- 🔐 Using Django's secure authentication and ORM for full-stack development

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 AI Legal Q&A | Ask questions about Indian laws, rights, and procedures |
| 🧠 Persistent Memory | Full conversation history reloaded for context-aware responses |
| 🔐 User Authentication | Secure signup / login with Django's auth system |
| 💬 Saved Conversations | Sidebar to browse and resume past chat sessions |
| 🔍 Search Conversations | Quickly find previous discussions by keyword |
| 🗑 Delete Conversations | Remove unwanted chat sessions |
| ⚡ Multi-Model Fallback | Groq auto-falls back across LLaMA and Gemma models |
| 🌙 Dark / Light Mode | Toggle theme for comfortable reading |
| 🔒 CSRF Protection | Django middleware guards all form submissions |
| 🧑‍💻 Admin Panel | Django admin for managing users and conversations |
| ⌛ Typing Indicator | Real-time visual feedback while AI responds |
| 📌 Quick Suggestions | One-click common legal question prompts |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10 |
| Backend Framework | Django |
| ORM / Auth | Django ORM + Django Authentication |
| Frontend | HTML5, CSS3, JavaScript |
| AI Provider | Groq API |
| Primary Model | LLaMA 3.3 70B |
| Fallback Models | LLaMA 3.1 8B · Gemma 2 9B |
| Database | SQLite (via Django ORM, auto-created) |
| Config / Secrets | python-dotenv (.env file) |

---

## 🏗️ System Architecture
```
User Browser
      │
      ▼
Frontend (HTML + JavaScript)
      │
      ▼
Django Views
      │
      ├── Load full conversation history from SQLite
      │
      ▼
Groq AI API  (LLaMA 3.3 70B → fallback if needed)
      │
      ▼
AI Response generated with full context
      │
      ▼
New messages stored in SQLite
      │
      ▼
Response returned to browser
```

The app stores every message in the database and reloads the full history before each API call — giving the AI complete context awareness across sessions.

---

## 📂 Project Structure
```
nyay-django/
│
├── manage.py                  ← Django command-line entry point
├── requirements.txt           ← All Python dependencies
├── .env                       ← GROQ_API_KEY + SECRET_KEY  (never commit!)
├── .gitignore
├── db.sqlite3                 ← Auto-created after migrate
│
├── nyay_project/              ← Django project config
│   ├── __init__.py
│   ├── settings.py            ← All configuration
│   ├── urls.py                ← Master URL router
│   └── wsgi.py                ← Production deployment entry point
│
└── chat/                      ← Main Django app
    ├── __init__.py
    ├── models.py              ← Database tables as Python classes
    ├── views.py               ← Route handlers (chat, auth, API)
    ├── urls.py                ← App-level URL patterns
    ├── admin.py               ← Register models in Django admin
    ├── migrations/            ← Auto-generated SQL migration files
    └── templates/
        └── chat/
            ├── index.html     ← Main chat UI
            ├── login.html     ← Login page
            └── signup.html    ← Signup + disclaimer modal
```

---

## ⚙️ Installation Guide

### 1. Install Python 3.10
Download from [python.org](https://www.python.org/downloads/release/python-3100/) and ensure **Add Python to PATH** is checked during installation.

### 2. Allow Script Execution — Windows only
Run once in PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Clone the Repository
```bash
git clone https://github.com/balaji049/nyay_ai_legal_advisor.git
cd nyay_ai_legal_advisor
```

### 4. Create a Virtual Environment
```bash
python -m venv venv
```
Activate it:
```bash
# Windows
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```
You should see `(venv)` at the start of your terminal prompt.

### 5. Upgrade pip
```bash
python -m pip install --upgrade pip
```

### 6. Install Dependencies
```bash
pip install -r requirements.txt
```

### 7. Get a Free Groq API Key
1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up with Google or email
3. Click **API Keys** → **Create API Key** → give it a name
4. Copy the key immediately — it starts with `gsk_...` and is shown **only once**

### 8. Configure Environment Variables
Create a `.env` file in the project root (same folder as `manage.py`):
```env
SECRET_KEY=your_django_secret_key_here
GROQ_API_KEY=gsk_your_groq_key_here
```
> ⚠️ Never commit this file to Git. It is already listed in `.gitignore`.

### 9. Run Database Migrations
```bash
python manage.py makemigrations chat
python manage.py migrate
```

| Command | What it does |
|---|---|
| `makemigrations chat` | Reads `models.py` and creates migration blueprint files |
| `migrate` | Executes those blueprints and creates tables in `db.sqlite3` |

### 10. Start the Development Server
```bash
python manage.py runserver
```
Open your browser at: **http://127.0.0.1:8000**

> 📝 Django defaults to port **8000**, not 5000 like Flask.

---

## 🤖 Groq Multi-Model Fallback

| Priority | Model | Notes |
|---|---|---|
| 1 — Primary | LLaMA 3.3 70B | Best accuracy for legal reasoning |
| 2 — Fallback | LLaMA 3.1 8B | Faster, lighter responses |
| 3 — Fallback | Gemma 2 9B | Additional redundancy |

---

## 🧑‍💻 Django Admin Panel

Create a superuser to access the admin panel at `/admin/`:
```bash
python manage.py createsuperuser
```

---

## 🚀 Future Improvements

- 🎤 Voice-based legal assistant
- 📄 Legal document analysis (OCR)
- 🌍 Multi-language support — Hindi, Telugu, Tamil
- 📍 Nearby lawyer finder using maps API
- 📱 Mobile app integration
- 📊 Admin analytics dashboard

---

## ⚠️ Legal Disclaimer

This project provides **general legal information for educational purposes only**. It does not constitute legal advice and should not replace consultation with a qualified advocate registered with the Bar Council of India.

---

## 👨‍💻 Author

**Balaji Bhairwad**  
B.Tech – Artificial Intelligence & Machine Learning  
GitHub: [github.com/balaji049](https://github.com/balaji049)

---

⭐ If you found this project useful, please consider **starring the repository**!
