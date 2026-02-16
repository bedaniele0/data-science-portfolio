"""
============================================================================
auth.py - Authentication & Authorization para Fraud Detection API
============================================================================
Sistema de autenticación con JWT y API Keys

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Metodología: DVP-PRO
============================================================================
"""

import base64
import hashlib
import json
import os
import time
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Optional

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from pydantic import BaseModel

# ============================================================================
# CONFIGURATION
# ============================================================================

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# ============================================================================
# MODELS
# ============================================================================

class Token(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token payload data."""
    username: Optional[str] = None
    scopes: list = []


class User(BaseModel):
    """User model."""
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


# ============================================================================
# PASSWORD FUNCTIONS
# ============================================================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica password contra hash."""
    return hashed_password == get_password_hash(plain_password)


def get_password_hash(password: str) -> str:
    """Genera hash de password."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# ============================================================================
# JWT FUNCTIONS
# ============================================================================

def _sign(payload: str) -> str:
    return sha256((payload + SECRET_KEY).encode("utf-8")).hexdigest()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token firmado (no JWT estándar) usando HMAC-SHA256.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": int(expire.timestamp())})
    payload = base64.urlsafe_b64encode(json.dumps(to_encode).encode("utf-8")).decode("utf-8")
    signature = _sign(payload)
    return f"{payload}.{signature}"


def decode_access_token(token: str) -> TokenData:
    """
    Decodifica y valida el token firmado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload_b64, signature = token.split(".")
        if signature != _sign(payload_b64):
            raise credentials_exception

        payload = json.loads(base64.urlsafe_b64decode(payload_b64.encode("utf-8")))
        username: str = payload.get("sub")
        exp_ts = payload.get("exp", 0)
        if not username or time.time() > exp_ts:
            raise credentials_exception

        return TokenData(username=username)
    except Exception:
        raise credentials_exception


# ============================================================================
# AUTHENTICATION DEPENDENCIES
# ============================================================================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Security(security)
) -> User:
    """
    Obtiene usuario actual; exige credenciales.
    """
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    token_data = decode_access_token(token)

    user = User(
        username=token_data.username,
        email=f"{token_data.username}@example.com",
        full_name=token_data.username.title(),
        disabled=False
    )
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Retorna usuario activo; falla si está deshabilitado.
    """
    if current_user is None or current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


# ============================================================================
# API KEY AUTHENTICATION
# ============================================================================

async def verify_api_key(
    api_key: Optional[str] = Security(api_key_header)
) -> bool:
    """
    Verifica API Key desde header.

    Args:
        api_key: API key desde header X-API-Key

    Returns:
        True si API key es válida

    Raises:
        HTTPException si API key es inválida
    """
    # Check if API key auth is enabled
    if not os.getenv("ENABLE_API_KEY_AUTH", "false").lower() == "true":
        return True

    valid_api_key = os.getenv("API_KEY")

    if not valid_api_key:
        # No API key configured, allow access
        return True

    if api_key is None or api_key != valid_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
            headers={"WWW-Authenticate": "API-Key"},
        )

    return True


# ============================================================================
# OPTIONAL AUTHENTICATION (JWT OR API KEY)
# ============================================================================

async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security),
    api_key: Optional[str] = Security(api_key_header)
) -> Optional[User]:
    """
    Optional authentication - acepta JWT o API Key.

    Args:
        credentials: JWT Bearer credentials
        api_key: API Key header

    Returns:
        User si autenticación exitosa, None si no hay credenciales
    """
    # Try JWT first
    if credentials:
        try:
            return await get_current_user(credentials)
        except HTTPException:
            pass

    # Try API Key
    if api_key:
        try:
            await verify_api_key(api_key)
            return User(username="api_key_user", email="api@example.com")
        except HTTPException:
            pass

    # No authentication provided
    return None


# ============================================================================
# MOCK USER DATABASE (Replace with real DB in production)
# ============================================================================

fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "email": "admin@frauddetection.com",
        "hashed_password": get_password_hash("admin123"),
        "disabled": False,
    },
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@frauddetection.com",
        "hashed_password": get_password_hash("test123"),
        "disabled": False,
    }
}


def authenticate_user(username: str, password: str) -> Optional[User]:
    """
    Autentica usuario con username y password.

    Args:
        username: Username
        password: Password en texto plano

    Returns:
        User si autenticación exitosa, None si falla
    """
    user_dict = fake_users_db.get(username)

    if not user_dict:
        return None

    if not verify_password(password, user_dict["hashed_password"]):
        return None

    return User(**user_dict)
