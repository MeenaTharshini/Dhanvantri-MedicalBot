from flask import Flask, render_template, request, redirect, url_for, session
from medicalbot import get_medical_response
from herbs import HERB_DB
from werkzeug.security import generate_password_hash, check_password_hash
import json, uuid, os, random
from datetime import datetime
from core.ai_engine import ai_response
from database import connect, create_tables
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask import jsonify
from health.dashboard import get_dashboard_data

from health.checkins import save_checkin, get_recent_checkins, create_checkin_table
from health.profile import get_profile, save_profile, create_profile_table
app = Flask(__name__)
app.secret_key = "dhanvantri_secret"

# ---------------- EMAIL CONFIG ---------------- #
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.secret_key)

# ---------------- PATHS ---------------- #
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, "chat_history.json")
USERS_FILE = os.path.join(BASE_DIR, "users.json")

# ---------------- DAILY CONTENT ---------------- #
DAILY_TIPS = [
    "Drink warm water after waking up",
    "Practice 10 minutes of pranayama daily",
    "Eat seasonal fruits",
    "Sleep before 10:30 PM",
    "Drink turmeric milk for immunity"
]

YOGA_POSES = [
    "Surya Namaskar – boosts energy",
    "Vrikshasana – improves balance",
    "Bhujangasana – strengthens spine",
    "Anulom Vilom – improves breathing",
    "Tadasana – improves posture"
]

# ---------------- INIT ---------------- #
def init_files():
    for file in [HISTORY_FILE, USERS_FILE]:
        if not os.path.exists(file):
            with open(file, "w") as f:
                json.dump([], f)

# ---------------- CHAT STORAGE ---------------- #
def format_date(date_str):
    try:
        chat_date = datetime.strptime(date_str, "%d %b %Y").date()
    except:
        return date_str

    today = datetime.now().date()
    if chat_date == today:
        return "Today"
    elif (today - chat_date).days == 1:
        return "Yesterday"
    return chat_date.strftime("%d %b %Y")

def load_chats():
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as f:
        chats = json.load(f)

    if "user" in session:
        chats = [c for c in chats if c.get("user") == session["user"]]

    for c in chats:
        c["display_date"] = format_date(c.get("created_at", ""))

    return chats

def save_chats(chats):
    if not os.path.exists(HISTORY_FILE):
        all_chats = []
    else:
        with open(HISTORY_FILE, "r") as f:
            all_chats = json.load(f)

    all_chats = [c for c in all_chats if c.get("user") != session.get("user")]
    all_chats = chats + all_chats

    with open(HISTORY_FILE, "w") as f:
        json.dump(all_chats, f, indent=4)

@app.route("/profile", methods=["GET", "POST"])
def profile():

    # Check whether the user is logged in
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    create_profile_table()

    if request.method == "POST":

        data = {
            "age": request.form.get("age") or None,
            "gender": request.form.get("gender"),
            "wellness_goal": request.form.get("wellness_goal"),
            "activity_level": request.form.get("activity_level"),
            "sleep_hours": request.form.get("sleep_hours") or None,
            "dietary_preference": request.form.get("dietary_preference"),
            "wellness_interest": request.form.get("wellness_interest")
        }

        save_profile(user_id, data)

        return redirect(url_for("profile", saved="1"))

    profile_data = get_profile(user_id)

    message = None

    if request.args.get("saved") == "1":
        message = "🌿 Your wellness profile has been saved successfully."

    return render_template(
        "profile.html",
        profile=profile_data,
        message=message
    )

# ---------------- HERBS ---------------- #
def suggest_herbs(text):
    text = text.lower()
    suggested = []

    for herb, data in HERB_DB.items():
        if any(use in text for use in data["uses"]):
            suggested.append(herb.title())

    return suggested

def generate_chat_title(user_input):
    """
    Generate a short, intelligent title based on the user's
    actual intention rather than copying the beginning of
    the message.
    """

    text = user_input.lower().strip()

    # =========================================================
    # 🚨 MEDICAL EMERGENCIES
    # =========================================================

    emergency_patterns = [
        "vomiting blood",
        "vomit blood",
        "throwing up blood",
        "coughing blood",
        "spitting blood",
        "blood in vomit",
        "severe bleeding",
        "heavy bleeding",
        "unconscious",
        "not breathing",
        "difficulty breathing",
        "can't breathe",
        "cannot breathe",
        "chest pain",
        "heart attack",
        "stroke",
        "seizure",
        "severe allergic reaction",
        "anaphylaxis",
        "poisoning",
        "overdose",
        "suicide attempt",
        "suicidal",
        "severe injury",
        "major accident"
    ]

    if any(pattern in text for pattern in emergency_patterns):
        return "🚨 Medical Emergency"


    # =========================================================
    # 🩺 COMMON SYMPTOMS
    # =========================================================

    symptom_titles = {

        "stomach pain": "Stomach Pain",
        "stomach ache": "Stomach Pain",
        "abdominal pain": "Abdominal Pain",
        "belly pain": "Stomach Pain",

        "fever": "Fever Guidance",

        "cough": "Cough Guidance",

        "cold": "Cold & Sneezing",
        "sneezing": "Cold & Sneezing",
        "runny nose": "Cold & Sneezing",

        "headache": "Headache Relief",
        "migraine": "Headache & Migraine",

        "allergy": "Allergy Guidance",
        "allergic": "Allergy Guidance",

        "sore throat": "Sore Throat",

        "vomiting": "Vomiting & Nausea",
        "vomit": "Vomiting & Nausea",
        "nausea": "Nausea & Vomiting",

        "diarrhea": "Digestive Problems",
        "loose motion": "Digestive Problems",

        "constipation": "Constipation",

        "back pain": "Back Pain",
        "neck pain": "Neck Pain",
        "joint pain": "Joint Pain",

        "tooth pain": "Tooth Pain",
        "toothache": "Tooth Pain",

        "dizziness": "Dizziness",
        "vertigo": "Dizziness & Vertigo",

        "fatigue": "Fatigue & Low Energy",
        "tired": "Fatigue & Low Energy",
        "exhausted": "Fatigue & Low Energy",

        "insomnia": "Sleep Problems",
        "can't sleep": "Sleep Problems",
        "cannot sleep": "Sleep Problems",
        "not sleeping": "Sleep Problems",

        "period pain": "Menstrual Pain",
        "period cramps": "Menstrual Pain",
        "menstrual": "Menstrual Health"
    }

    for keyword, title in symptom_titles.items():
        if keyword in text:
            return title


    # =========================================================
    # 🧠 MENTAL WELLNESS
    # =========================================================

    if any(word in text for word in [
        "anxiety",
        "anxious",
        "panic attack",
        "panic"
    ]):
        return "Stress & Anxiety"

    if any(word in text for word in [
        "stress",
        "stressed",
        "overwhelmed",
        "tension"
    ]):
        return "Stress Management"

    if any(word in text for word in [
        "sad",
        "unhappy",
        "lonely",
        "depressed",
        "depression"
    ]):
        return "Emotional Wellbeing"


    # =========================================================
    # 🌿 AYURVEDA / TRADITIONAL WELLNESS
    # =========================================================

    if "ayurveda" in text or "ayurvedha" in text:
        return "About Ayurveda"

    if "siddha" in text:
        return "About Siddha Medicine"

    if "yoga" in text:
        return "Yoga & Wellness"

    if "meditation" in text:
        return "Meditation & Mindfulness"

    if "pranayama" in text:
        return "Pranayama & Breathing"


    # =========================================================
    # 🍎 LIFESTYLE / WELLNESS
    # =========================================================

    if any(word in text for word in [
        "diet",
        "nutrition",
        "healthy food",
        "what should i eat",
        "what can i eat"
    ]):
        return "Healthy Diet & Nutrition"

    if any(word in text for word in [
        "weight loss",
        "lose weight",
        "losing weight"
    ]):
        return "Weight Management"

    if any(word in text for word in [
        "exercise",
        "workout",
        "fitness"
    ]):
        return "Fitness & Exercise"

    if any(word in text for word in [
        "sleep",
        "sleeping"
    ]):
        return "Sleep & Rest"


    # =========================================================
    # 🌿 HERBS / NATURAL REMEDIES
    # =========================================================

    if any(word in text for word in [
        "herb",
        "herbal",
        "turmeric",
        "ginger",
        "neem",
        "tulsi",
        "ashwagandha",
        "aloe vera"
    ]):
        return "Herbs & Natural Remedies"


    # =========================================================
    # 📚 KNOWLEDGE QUESTIONS
    # =========================================================

    if "what is ayurveda" in text:
        return "About Ayurveda"

    if "what is siddha" in text:
        return "About Siddha Medicine"

    if any(word in text for word in [
        "what is",
        "what are",
        "explain",
        "meaning of",
        "difference between",
        "how does"
    ]):
        return "Health Information"


    # =========================================================
    # 👋 GREETINGS
    # =========================================================

    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    if any(
        text == greeting or text.startswith(greeting + " ")
        for greeting in greetings
    ):
        return "Greeting"


    # =========================================================
    # 🤖 AI FALLBACK
    # =========================================================

    try:

        prompt = f"""
You are a conversation-title generator.

Read the user's complete message and determine its MAIN INTENT.

User message:
{user_input}

Create a short title that summarizes the topic.

Rules:
- Use 2 to 5 words only.
- Do NOT copy the beginning of the user's message.
- Do NOT answer the question.
- Do NOT explain anything.
- Do NOT use quotation marks.
- Do NOT use a period.
- Focus on the main health topic or intention.
- Return ONLY the title.

Examples:

"I am vomiting a lot of blood. What should I do?"
Medical Emergency

"My stomach hurts after eating"
Stomach Pain

"Why do I keep feeling tired?"
Fatigue & Low Energy

"What are the benefits of turmeric?"
Turmeric Benefits

"How can I reduce stress before exams?"
Stress Management
"""

        ai_title = ai_response(prompt)

        # Clean AI output
        title = ai_title.strip()

        # Remove markdown / quotes if AI adds them
        title = title.replace('"', "")
        title = title.replace("'", "")
        title = title.replace("*", "")
        title = title.replace("#", "")

        # Only take first non-empty line
        lines = [
            line.strip()
            for line in title.splitlines()
            if line.strip()
        ]

        if lines:
            title = lines[0]

        # Prevent excessively long AI titles
        if len(title) > 45:
            title = title[:45].rsplit(" ", 1)[0]

        return title or "Health Chat"

    except Exception as e:

        print("AI TITLE ERROR:", e)

        return "Health Chat"
# ---------------- AUTH ---------------- #
@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"].strip().lower()
        password = generate_password_hash(request.form["password"])

        conn = connect()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        existing = cur.fetchone()

        if existing:
            error = "User already exists"
        else:
            cur.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password)
            )
            conn.commit()
            return redirect(url_for("login"))

        conn.close()

    return render_template("signup.html", error=error)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = connect()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session["user"] = username
            session["user_id"] = user[0]

            return redirect(url_for("home"))
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)

    return redirect(url_for("login"))

# ---------------- CHAT ROUTES ---------------- #
@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    chats = load_chats()

    if not chats:
        return redirect(url_for("new_chat"))

    return redirect(url_for("chat", chat_id=chats[0]["id"]))

@app.route("/new")
def new_chat():
    if "user" not in session:
        return redirect(url_for("login"))

    chats = load_chats()
    chat_id = str(uuid.uuid4())

    chats.insert(0, {
        "id": chat_id,
        "user": session["user"],
        "title": "New Chat",
        "messages": [],
        "created_at": datetime.now().strftime("%d %b %Y")
    })

    save_chats(chats)

    return redirect(url_for("chat", chat_id=chat_id))
@app.route("/checkin", methods=["GET", "POST"])
def checkin():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    create_checkin_table()

    if request.method == "POST":

        data = {
            "sleep_hours": request.form.get("sleep_hours"),
            "energy": request.form.get("energy"),
            "mood": request.form.get("mood"),
            "stress": request.form.get("stress"),
            "hydration": request.form.get("hydration"),
            "activity_minutes": request.form.get("activity_minutes"),
            "notes": request.form.get("notes", "").strip()
        }

        save_checkin(user_id, data)

        return redirect(url_for("checkin", saved="1"))

    message = None

    if request.args.get("saved") == "1":
        message = "🌿 Today's wellness check-in has been saved."

    recent_checkins = get_recent_checkins(user_id)

    return render_template(
        "checkin.html",
        message=message,
        checkins=recent_checkins
    )

# ---------------- DASHBOARD ---------------- #

@app.route("/dashboard")
def dashboard():

    # User must be logged in
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    # Get dashboard information
    dashboard_data = get_dashboard_data(user_id)

    return render_template(
        "dashboard.html",
        profile=dashboard_data["profile"],
        checkins=dashboard_data["checkins"],
        user=session.get("user")
    )

@app.route("/delete/<chat_id>")
def delete_chat(chat_id):
    if "user" not in session:
        return redirect(url_for("login"))

    chats = load_chats()
    chats = [c for c in chats if c["id"] != chat_id]

    save_chats(chats)
    return redirect(url_for("home"))

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    message = None

    if request.method == "POST":
        email = request.form["email"]

        conn = connect()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cur.fetchone()

        if user:
            # Generate token
            token = serializer.dumps(email, salt="reset-password")

            reset_link = url_for("reset_password", token=token, _external=True)

            # Send email
            msg = Message("Password Reset - Dhanvantri",
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[email])

            msg.body = f"Click to reset your password:\n{reset_link}"

            mail.send(msg)

            message = "Reset link sent to your email 🌿"
        else:
            message = "Email not found"

        conn.close()

    return render_template("forgot.html", message=message)

@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = serializer.loads(token, salt="reset-password", max_age=300)
    except:
        return "❌ Invalid or expired link"

    if request.method == "POST":
        new_password = generate_password_hash(request.form["password"])

        conn = connect()
        cur = conn.cursor()

        cur.execute("UPDATE users SET password=? WHERE email=?",
                    (new_password, email))
        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("reset.html")
# ---------------- MAIN CHAT ---------------- #
@app.route("/chat/<chat_id>", methods=["GET"])
def chat(chat_id):

    chats = load_chats()
    chat = next((c for c in chats if c["id"] == chat_id), None)

    if not chat:
        return redirect(url_for("home"))

    return render_template(
        "index.html",
        chats=load_chats(),
        current_chat=chat,
        user=session.get("user"),
        tip=random.choice(DAILY_TIPS),
        yoga=random.choice(YOGA_POSES)
    )
@app.route("/chat", methods=["POST"])
def chat_api():

    try:
        data = request.get_json(silent=True) or {}

        chat_id = data.get("chat_id")
        user_input = data.get("question", "").strip()

        print("\n========== CHAT REQUEST ==========")
        print("CHAT ID:", chat_id)
        print("QUESTION:", user_input)

        if not chat_id:
            print("ERROR: Missing chat_id")
            return jsonify({
                "reply": "Chat ID is missing."
            }), 400

        if not user_input:
            print("ERROR: Empty question")
            return jsonify({
                "reply": "Please enter a question."
            }), 400

        chats = load_chats()

        chat = next(
            (c for c in chats if c.get("id") == chat_id),
            None
        )

        if not chat:
            print("ERROR: Chat not found:", chat_id)

            return jsonify({
                "reply": "Chat not found."
            }), 404

        history = chat.get("messages", [])

        print("Calling AI...")

        # IMPORTANT
        answer = ai_response(
            user_input=user_input,
            history=history
        )

        print("AI RESPONSE:", answer)

        if not answer:
            answer = "I could not generate a response."

        # ---------------- USER MESSAGE ----------------

        chat["messages"].append({
            "role": "user",
            "content": user_input,
            "time": datetime.now().strftime("%H:%M")
        })

        # ---------------- BOT MESSAGE ----------------

        chat["messages"].append({
            "role": "bot",
            "content": str(answer),
            "time": datetime.now().strftime("%H:%M")
        })

        # ---------------- TITLE ----------------

        if chat.get("title") == "New Chat":
            try:
                chat["title"] = generate_chat_title(user_input)
            except Exception as title_error:
                print("TITLE ERROR:", title_error)
                chat["title"] = "Health Chat"

        save_chats(chats)

        print("CHAT SAVED SUCCESSFULLY")
        print("=================================\n")

        return jsonify({
            "reply": str(answer),
            "title": chat["title"],
            "chat_id": chat["id"]
        })

    except Exception as e:

        print("\n========== CHAT ERROR ==========")
        print(type(e).__name__)
        print(str(e))
        import traceback
        traceback.print_exc()
        print("================================\n")

        return jsonify({
            "reply": "AI service error. Check the Flask terminal."
        }), 500
# ---------------- RUN ---------------- #
if __name__ == "__main__":
    init_files()
    create_tables()
    create_profile_table()
    create_checkin_table()

    app.run(debug=True)