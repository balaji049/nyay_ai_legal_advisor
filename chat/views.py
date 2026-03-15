# ============================================================
# chat/views.py — All Views (replaces Flask's app.py + auth.py)
# ============================================================
# In Flask: routes were split across app.py and auth.py Blueprint.
# In Django: all views live in one file per app.
#
# KEY DJANGO DIFFERENCES vs Flask:
#   Flask: @app.route("/")           →  Django: path("", views.index) in urls.py
#   Flask: session["user_id"]        →  Django: request.user (built-in!)
#   Flask: @login_required decorator →  Django: @login_required from django.contrib.auth
#   Flask: jsonify({...})            →  Django: JsonResponse({...})
#   Flask: request.get_json()        →  Django: json.loads(request.body)
#   Flask: redirect(url_for("name")) →  Django: redirect(reverse("name"))
#   Flask: render_template("x.html") →  Django: render(request, "chat/x.html", context)

import json
from django.shortcuts           import render, redirect, get_object_or_404
from django.contrib.auth        import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http                import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf                import settings
from groq                       import Groq

from .models import Conversation, Message

# ─── GROQ CLIENT ───────────────────────────────────────────
# Created once at module load — reused across all requests
groq_client = Groq(api_key=settings.GROQ_API_KEY)

SYSTEM_PROMPT = """You are Nyay (meaning "Justice" in Hindi), an expert AI Legal Advisor
specializing exclusively in Indian law. You have comprehensive knowledge of:

AREAS OF EXPERTISE:
- Indian Penal Code (IPC) and its sections
- Code of Criminal Procedure (CrPC)
- Code of Civil Procedure (CPC)
- Constitution of India (all Articles, Fundamental Rights, DPSPs)
- Indian Contract Act, 1872
- Transfer of Property Act, 1882
- Hindu Personal Laws (HMA, HSA, HAMA)
- Muslim Personal Law
- Consumer Protection Act, 2019
- Right to Information Act, 2005
- Protection of Women from Domestic Violence Act, 2005
- POCSO Act, 2012
- IT Act, 2000 and amendments
- Companies Act, 2013
- GST Laws and taxation
- Labour Laws (Factories Act, ESIC, PF, etc.)
- Motor Vehicles Act
- RERA (Real Estate Regulation Act)
- Negotiable Instruments Act (Section 138 cheque bounce)
- Arbitration and Conciliation Act
- Recent landmark Supreme Court and High Court judgments

HOW YOU RESPOND:
1. Always cite specific sections, articles, or acts when relevant
2. Explain legal terms in simple Hindi-English when helpful
3. Give practical step-by-step guidance
4. Mention time limits when relevant
5. Structure complex answers with clear headings

Always end with:
⚖️ *Disclaimer: This is general legal information for educational purposes only.
For your specific situation, please consult a qualified advocate registered with the Bar Council of India.*"""


def call_groq(messages_list):
    """
    Calls Groq API with auto-fallback across models.
    Identical logic to Flask version — Groq SDK works the same regardless of framework.
    Returns: (reply_text, error_message)
    """
    groq_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages_list

    for model_name in settings.GROQ_MODELS:
        try:
            response = groq_client.chat.completions.create(
                model=model_name,
                messages=groq_messages,
                max_tokens=1500,
                temperature=0.7,
            )
            return response.choices[0].message.content, None
        except Exception as e:
            err = str(e)
            is_quota = "429" in err or "rate_limit" in err.lower()
            is_last  = (model_name == settings.GROQ_MODELS[-1])
            if is_quota and not is_last:
                continue
            elif is_quota and is_last:
                return None, "Rate limit reached. Please wait 1 minute and try again."
            else:
                return None, f"API Error: {err}"

    return None, "No response received."


# ════════════════════════════════════════════════════════════
# AUTH VIEWS (replaces auth.py Blueprint from Flask)
# ════════════════════════════════════════════════════════════

def signup_view(request):
    """
    GET  /signup/ → show signup page
    POST /signup/ → create account, auto-login, return JSON

    Flask equivalent: @auth.route("/signup", methods=["GET","POST"])

    Django uses request.method to check GET vs POST.
    Django's User.objects.create_user() handles password hashing automatically!
    No need for werkzeug.security — Django does it built-in.
    """
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "GET":
        return render(request, "chat/signup.html")

    # POST — process signup
    try:
        data     = json.loads(request.body)
        name     = data.get("name",     "").strip()
        email    = data.get("email",    "").strip().lower()
        password = data.get("password", "").strip()
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    # Validation
    if not name or not email or not password:
        return JsonResponse({"error": "All fields are required."}, status=400)
    if len(name) < 2:
        return JsonResponse({"error": "Name must be at least 2 characters."}, status=400)
    if len(password) < 6:
        return JsonResponse({"error": "Password must be at least 6 characters."}, status=400)
    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "This email is already registered. Please log in."}, status=409)

    # Create user — Django hashes the password automatically!
    # create_user() is equivalent to Flask's generate_password_hash()
    user = User.objects.create_user(
        username   = email,          # Django requires username; we use email as username
        email      = email,
        password   = password,       # Django hashes this — never stored as plain text
        first_name = name,
    )

    # Auto-login after signup
    # login() creates a session — equivalent to session["user_id"] = user.id in Flask
    login(request, user)

    return JsonResponse({"success": True, "redirect": "/"})


def login_view(request):
    """
    GET  /login/ → show login page
    POST /login/ → authenticate and login, return JSON

    Flask equivalent: @auth.route("/login", methods=["GET","POST"])

    Django's authenticate() checks email+password and returns the User object.
    Django's login() creates the session entry.
    """
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "GET":
        return render(request, "chat/login.html")

    # POST — process login
    try:
        data     = json.loads(request.body)
        email    = data.get("email",    "").strip().lower()
        password = data.get("password", "").strip()
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not email or not password:
        return JsonResponse({"error": "Email and password are required."}, status=400)

    # Check if email exists first (for a better error message)
    if not User.objects.filter(email=email).exists():
        return JsonResponse({"error": "No account found with this email."}, status=401)

    # authenticate() is Django's equivalent of check_password_hash()
    # It looks up user by username (we use email as username) and verifies hash
    user = authenticate(request, username=email, password=password)

    if user is None:
        return JsonResponse({"error": "Incorrect password. Please try again."}, status=401)

    # login() sets session cookies — equivalent to session["user_id"] = user.id
    login(request, user)

    return JsonResponse({"success": True, "redirect": "/"})


# ════════════════════════════════════════════════════════════
# PAGE VIEWS
# ════════════════════════════════════════════════════════════

@login_required   # Django's built-in decorator — redirects to settings.LOGIN_URL if not logged in
def index(request):
    """
    Main chat page — loads with no active conversation.
    Flask equivalent: @app.route("/") with @login_required custom decorator
    Django provides @login_required built-in — no need to write our own!
    """
    return render(request, "chat/index.html", {
        "user_name":  request.user.first_name or request.user.email,
        "user_email": request.user.email,
    })


@login_required
def load_conversation(request, conv_id):
    """
    Loads the main page with a specific conversation pre-selected.
    get_object_or_404 is a Django shortcut — raises 404 if not found.
    """
    conv = get_object_or_404(Conversation, id=conv_id, user=request.user)
    return render(request, "chat/index.html", {
        "user_name":      request.user.first_name or request.user.email,
        "user_email":     request.user.email,
        "active_conv_id": conv_id,
    })


# ════════════════════════════════════════════════════════════
# API VIEWS — Return JSON, not HTML
# ════════════════════════════════════════════════════════════

@login_required
def api_conversations(request):
    """
    GET  /api/conversations/         → list all conversations (supports ?search=)
    POST /api/conversations/         → create new conversation

    Django handles multiple HTTP methods in one view using request.method check.
    Flask needed separate @app.route(methods=["GET"]) and @app.route(methods=["POST"]).
    """
    if request.method == "GET":
        search = request.GET.get("search", "").strip()

        # Django ORM — no raw SQL!
        # .filter() = WHERE clause
        # | = OR operator in Django Q objects
        from django.db.models import Q, Count

        convs = Conversation.objects.filter(user=request.user)

        if search:
            # Search in title OR in any message content
            convs = convs.filter(
                Q(title__icontains=search) |
                Q(messages__content__icontains=search)
            ).distinct()

        # Annotate with message count, serialize to list of dicts
        convs_data = []
        for c in convs:
            convs_data.append({
                "id":            c.id,
                "title":         c.title,
                "created_at":    c.created_at.isoformat(),
                "updated_at":    c.updated_at.isoformat(),
                "message_count": c.messages.count(),
            })

        return JsonResponse({"conversations": convs_data})

    elif request.method == "POST":
        # Create new empty conversation
        conv = Conversation.objects.create(
            user  = request.user,
            title = "New Conversation",
        )
        return JsonResponse({"id": conv.id, "title": conv.title})

    return JsonResponse({"error": "Method not allowed"}, status=405)


@login_required
def api_conversation_detail(request, conv_id):
    """
    GET    /api/conversations/<id>/  → get messages for a conversation
    DELETE /api/conversations/<id>/  → delete a conversation

    get_object_or_404 automatically returns 404 if conversation doesn't belong to this user.
    """
    conv = get_object_or_404(Conversation, id=conv_id, user=request.user)

    if request.method == "GET":
        messages_data = [
            {
                "role":       m.role,
                "content":    m.content,
                "created_at": m.created_at.isoformat(),
            }
            for m in conv.messages.all()   # Django ORM: related_name="messages"
        ]
        return JsonResponse({
            "conversation": {
                "id":         conv.id,
                "title":      conv.title,
                "updated_at": conv.updated_at.isoformat(),
            },
            "messages": messages_data,
        })

    elif request.method == "DELETE":
        conv.delete()    # Django CASCADE removes all related Messages automatically
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Method not allowed"}, status=405)


@login_required
@require_http_methods(["POST"])
def api_chat(request):
    """
    POST /api/chat/
    Main AI endpoint — identical logic to Flask version.

    Accepts: { "message": "...", "conversation_id": 123 or null }
    Returns: { "reply": "...", "conversation_id": 123, ... }
    """
    try:
        data         = json.loads(request.body)
        user_message = data.get("message", "").strip()
        conv_id      = data.get("conversation_id")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not user_message:
        return JsonResponse({"error": "Empty message"}, status=400)

    # Get or create conversation
    if not conv_id:
        title = user_message[:50] + ("..." if len(user_message) > 50 else "")
        conv  = Conversation.objects.create(user=request.user, title=title)
        is_new = True
    else:
        conv   = get_object_or_404(Conversation, id=conv_id, user=request.user)
        is_new = False

    # Load full message history from DB (context memory!)
    # Django ORM: conv.messages.all() returns all related Message objects
    history = conv.messages.all()
    messages_list = [{"role": m.role, "content": m.content} for m in history]
    messages_list.append({"role": "user", "content": user_message})

    # Call Groq AI
    reply, error = call_groq(messages_list)
    if error:
        return JsonResponse({"error": error}, status=500)

    # Save both messages to DB using Django ORM
    Message.objects.create(conversation=conv, role="user",      content=user_message)
    Message.objects.create(conversation=conv, role="assistant", content=reply)

    # Django auto_now=True on updated_at refreshes it on every conv.save()
    # But Message.objects.create() doesn't touch the conversation, so save manually:
    conv.save()   # This triggers auto_now=True on updated_at

    return JsonResponse({
        "reply":           reply,
        "conversation_id": conv.id,
        "is_new":          is_new,
        "conv_title":      conv.title,
        "message_count":   conv.messages.count(),
    })
