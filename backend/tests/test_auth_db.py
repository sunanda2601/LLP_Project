import os

from app.routes import auth


def test_register_and_login_persist_user(tmp_path, monkeypatch):
    db_path = tmp_path / "auth.db"
    monkeypatch.setattr(auth, "DB_PATH", db_path)

    auth.initialize_database()

    # Weak password should fail
    weak_res = auth.register_user("Ada Lovelace", "ada@example.com", "weak")
    assert weak_res.get("success") is False

    user = auth.register_user("Ada Lovelace", "ada@example.com", "Secret123")
    assert user["email"] == "ada@example.com"
    assert user["provider"] == "local"

    authenticated = auth.authenticate_user("ada@example.com", "Secret123")
    assert authenticated is not None
    assert authenticated["email"] == "ada@example.com"

    duplicate = auth.register_user("Ada Lovelace", "ada@example.com", "Secret123")
    assert duplicate["success"] is False
