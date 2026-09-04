import hashlib
import json
import os
import sqlite3
import urllib.error
import urllib.request
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/auth", tags=["auth"])

GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "storage", "auth.db")
DB_PATH = os.path.abspath(DB_PATH)


def _get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database() -> None:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with _get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT,
                provider TEXT NOT NULL DEFAULT 'local',
                picture TEXT
            )
            """
        )
        conn.commit()


initialize_database()


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register_user(name: str, email: str, password: str | None = None, provider: str = "local", picture: str | None = None) -> dict:
    if not name or not email:
        return {"success": False, "error": "Name and email are required."}

    if provider == "local":
        if not password:
            return {"success": False, "error": "Password is required for local accounts."}
        if len(password) < 8:
            return {"success": False, "error": "Password must be at least 8 characters long."}
        if not any(c.islower() for c in password):
            return {"success": False, "error": "Password must contain at least one lowercase letter."}
        if not any(c.isupper() for c in password):
            return {"success": False, "error": "Password must contain at least one uppercase letter."}
        if not any(c.isdigit() for c in password):
            return {"success": False, "error": "Password must contain at least one number."}

    with _get_connection() as conn:
        existing = conn.execute("SELECT id FROM users WHERE email = ?", (email.lower(),)).fetchone()
        if existing:
            return {"success": False, "error": "An account with this email already exists."}

        password_hash = _hash_password(password) if password else None
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash, provider, picture) VALUES (?, ?, ?, ?, ?)",
            (name.strip(), email.lower(), password_hash, provider, picture),
        )
        user_id = cursor.lastrowid
        user = conn.execute(
            "SELECT id, name, email, provider, picture FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()

        # Return a dictionary that includes the user data both under a
        # ``user`` key (used by the FastAPI ``/signup`` endpoint) **and**
        # top‑level keys ``email`` and ``provider``.  The test suite expects
        # ``register_user`` to expose ``email`` and ``provider`` directly, e.g.:
        # ``user = register_user(...); assert user["email"] == ...``.  By
        # providing the additional top‑level entries we remain backward
        # compatible with existing endpoint logic while satisfying the test
        # expectations.
        user_dict = dict(user)
        return {
            "success": True,
            "user": user_dict,
            "email": user_dict.get("email"),
            "provider": user_dict.get("provider"),
        }


def authenticate_user(email: str, password: str | None = None, provider: str | None = None) -> dict | None:
    with _get_connection() as conn:
        user_row = conn.execute(
            "SELECT id, name, email, password_hash, provider, picture FROM users WHERE email = ?",
            (email.lower(),),
        ).fetchone()

    if not user_row:
        return None

    if provider and user_row["provider"] != provider:
        return None

    if password is not None:
        stored_hash = user_row["password_hash"]
        if not stored_hash or stored_hash != _hash_password(password):
            return None

    return dict(user_row)


@router.get("/me")
def me(request: Request):
    return JSONResponse({"authenticated": False, "user": None})


@router.post("/signup")
def signup(payload: dict):
    result = register_user(
        payload.get("name", ""),
        payload.get("email", ""),
        payload.get("password"),
        provider=payload.get("provider", "local"),
        picture=payload.get("picture"),
    )

    if not result.get("success"):
        return JSONResponse({"authenticated": False, **result}, status_code=400)

    return JSONResponse({"authenticated": True, "user": result["user"]})


@router.post("/login")
def login(payload: dict):
    user = authenticate_user(payload.get("email", ""), payload.get("password"), provider=payload.get("provider"))
    if not user:
        return JSONResponse({"authenticated": False, "error": "Invalid email or password."}, status_code=401)

    return JSONResponse({"authenticated": True, "user": user})


@router.post("/google")
def google_auth(payload: dict):
    access_token = payload.get("access_token") or payload.get("token")

    if not access_token:
        return JSONResponse(
            {"authenticated": False, "error": "No access token provided."},
            status_code=400,
        )

    try:
        request = urllib.request.Request(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            profile = json.loads(response.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
        return JSONResponse(
            {"authenticated": False, "error": f"Google authentication failed: {exc}"},
            status_code=401,
        )

    email = (profile.get("email") or "google.user@example.com").lower()
    user = authenticate_user(email, provider="google")
    if not user:
        result = register_user(
            profile.get("name") or profile.get("given_name") or "Google User",
            email,
            password=None,
            provider="google",
            picture=profile.get("picture"),
        )
        if not result.get("success"):
            return JSONResponse({"authenticated": False, **result}, status_code=400)
        user = result["user"]

    return JSONResponse(
        {
            "authenticated": True,
            "user": {
                "id": user.get("id"),
                "name": user.get("name") or "Google User",
                "email": user.get("email"),
                "picture": user.get("picture"),
                "provider": user.get("provider") or "google",
            },
        }
    )
