from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from passlib.context import CryptContext
import mysql.connector
import joblib
from sklearn.metrics.pairwise import cosine_similarity
import textwrap
import os

# ---------------- CONFIG ----------------
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "Pradeesh@12345"
DB_NAME = "users_auth"

SESSION_SECRET = "replace_this_with_a_long_random_secret"  # change for prod

MODEL_PATH = "policy_vectorizer.pkl"
MATRIX_PATH = "policy_tfidf_matrix.pkl"

# ---------------- APP SETUP ----------------
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------------- PASSWORD HASH ----------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    password = (password or "")[:72]
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password = (plain_password or "")[:72]
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

# ---------------- DB HELPERS ----------------
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

def init_db():
    # create database if doesn't exist, then table
    try:
        conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS)
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Warning creating DB (may already exist):", e)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

init_db()

# ---------------- LOAD MODEL (optional) ----------------
model_loaded = False
if os.path.exists(MODEL_PATH) and os.path.exists(MATRIX_PATH):
    try:
        vectorizer = joblib.load(MODEL_PATH)
        data = joblib.load(MATRIX_PATH)
        tfidf_matrix = data["matrix"]
        df = data["df"]
        model_loaded = True
        print("Model pickles loaded.")
    except Exception as e:
        print("Failed to load model pickles:", e)
        model_loaded = False
else:
    model_loaded = False

def search_policies_real(query: str, top_k: int = 5):
    if not model_loaded:
        # fallback example result
        return [
            {
                "scheme_name": "Startup India",
                "schemeCategory": "Entrepreneurship",
                "level": "National",
                "score": 0.91,
                "summary": "A Government initiative to promote startups.",
                "eligibility": "Registered startups",
                "benefits": "Tax exemptions, mentorship",
                "application": "Apply on Startup India portal",
                "documents": "Company registration, PAN",
                "tags": "startup, innovation"
            }
        ]

    qvec = vectorizer.transform([query.lower()])
    sims = cosine_similarity(qvec, tfidf_matrix).flatten()
    idxs = sims.argsort()[::-1][:top_k]
    results = []
    for idx in idxs:
        row = df.iloc[idx]
        summary = ""
        if "details" in row and isinstance(row["details"], str):
            summary = textwrap.shorten(row["details"], width=250, placeholder="...")
        results.append({
            "scheme_name": row.get("scheme_name", "Unknown Scheme"),
            "schemeCategory": row.get("schemeCategory", ""),
            "level": row.get("level", ""),
            "summary": summary,
            "benefits": row.get("benefits", ""),
            "eligibility": row.get("eligibility", ""),
            "application": row.get("application", ""),
            "documents": row.get("documents", ""),
            "tags": row.get("tags", ""),
            "score": round(float(sims[idx]), 3)
        })
    return results

# ---------------- ROUTES ----------------

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "msg": ""})

@app.post("/signup", response_class=HTMLResponse)
async def signup(request: Request, username: str = Form(...), password: str = Form(...)):
    username = username.strip()
    if not username or not password:
        return templates.TemplateResponse("signup.html", {"request": request, "msg": "Provide username & password."})
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cur.fetchone():
            cur.close(); conn.close()
            return templates.TemplateResponse("signup.html", {"request": request, "msg": "Username already exists."})
        hashed = get_password_hash(password)
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed))
        conn.commit()
        cur.close(); conn.close()
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    except Exception as e:
        return templates.TemplateResponse("signup.html", {"request": request, "msg": f"DB error: {e}"})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "msg": ""})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close(); conn.close()
    except Exception as e:
        return templates.TemplateResponse("login.html", {"request": request, "msg": f"DB error: {e}"})

    if not user or not verify_password(password, user["password"]):
        return templates.TemplateResponse("login.html", {"request": request, "msg": "Invalid username or password."})

    # store minimal user info in session
    request.session["user"] = {"id": user["id"], "username": user["username"]}
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

@app.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    # render your provided index.html (it expects 'results' and 'user')
    return templates.TemplateResponse("index.html", {"request": request, "results": None, "user": user})

@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = Form(...)):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    results = search_policies_real(query, top_k=5)
    return templates.TemplateResponse("index.html", {"request": request, "results": results, "user": user, "query": query})
