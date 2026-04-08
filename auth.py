import streamlit as st
import bcrypt
import json
import os

USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")


def _load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}


def _save_users(users: dict):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def sign_up(username: str, password: str, full_name: str) -> tuple[bool, str]:
    users = _load_users()
    if username in users:
        return False, "Username already exists."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    users[username] = {
        "hashed_password": hash_password(password),
        "full_name": full_name,
        "favorites": [],
    }
    _save_users(users)
    return True, "Account created successfully!"


def login(username: str, password: str) -> tuple[bool, str]:
    users = _load_users()
    if username not in users:
        return False, "Username not found."
    if not verify_password(password, users[username]["hashed_password"]):
        return False, "Incorrect password."
    st.session_state["logged_in"] = True
    st.session_state["username"] = username
    st.session_state["full_name"] = users[username]["full_name"]
    st.session_state["favorites"] = users[username].get("favorites", [])
    return True, "Logged in successfully!"


def logout():
    for key in ["logged_in", "username", "full_name", "favorites"]:
        st.session_state.pop(key, None)


def is_logged_in() -> bool:
    return st.session_state.get("logged_in", False)


def add_favorite(prop_id: int):
    users = _load_users()
    username = st.session_state.get("username")
    if username and username in users:
        favs = users[username].get("favorites", [])
        if prop_id not in favs:
            favs.append(prop_id)
            users[username]["favorites"] = favs
            st.session_state["favorites"] = favs
            _save_users(users)


def remove_favorite(prop_id: int):
    users = _load_users()
    username = st.session_state.get("username")
    if username and username in users:
        favs = users[username].get("favorites", [])
        favs = [f for f in favs if f != prop_id]
        users[username]["favorites"] = favs
        st.session_state["favorites"] = favs
        _save_users(users)


def get_favorites() -> list:
    return st.session_state.get("favorites", [])