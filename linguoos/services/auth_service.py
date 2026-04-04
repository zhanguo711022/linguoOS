from __future__ import annotations

import hashlib
import os
import time

import bcrypt
from jose import JWTError, jwt

from linguoos.storage.sqlite import create_user, get_user_by_email, update_user_last_login

JWT_ALGORITHM = "HS256"


def _get_jwt_secret() -> str:
    secret = os.getenv("JWT_SECRET", "")
    if not secret:
        raise RuntimeError("JWT_SECRET is not set")
    return secret


def _hash_pw(password: str) -> str:
    pre = hashlib.sha256(password.encode()).digest()
    return bcrypt.hashpw(pre, bcrypt.gensalt()).decode()


def _verify_pw(password: str, hashed: str) -> bool:
    pre = hashlib.sha256(password.encode()).digest()
    return bcrypt.checkpw(pre, hashed.encode())


class AuthService:
    def register(self, email: str, password: str) -> int:
        existing = get_user_by_email(email)
        if existing:
            raise ValueError("email already registered")
        password_hash = _hash_pw(password)
        return create_user(email, password_hash)

    def login(self, email: str, password: str) -> str:
        user = get_user_by_email(email)
        if not user or not _verify_pw(password, user["password_hash"]):
            raise ValueError("invalid credentials")
        update_user_last_login(int(user["id"]))
        payload = {"sub": str(user["id"]), "iat": int(time.time())}
        return jwt.encode(payload, _get_jwt_secret(), algorithm=JWT_ALGORITHM)

    def verify_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token, _get_jwt_secret(), algorithms=[JWT_ALGORITHM])
        except JWTError as exc:
            raise ValueError("invalid token") from exc
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("invalid token")
        try:
            return int(user_id)
        except ValueError:
            raise ValueError("invalid token") from None
