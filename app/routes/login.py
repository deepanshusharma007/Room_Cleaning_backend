from fastapi import APIRouter, HTTPException
from app.database import supabase
from app.utils.security import verify_password
from app.auth import create_access_token, create_refresh_token
from jose import jwt
from app.config import JWT_SECRET, JWT_ALGORITHM

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/admin-login")
def admin_login(username: str, password: str):

    response = supabase.table("admins") \
        .select("*") \
        .eq("username", username) \
        .execute()

    if not response.data:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    admin = response.data[0]

    if not verify_password(password, admin["password_hash"]):

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token({
        "admin_id": admin["id"]
    })

    refresh_token = create_refresh_token({
        "admin_id": admin["id"]
    })

    session_data = {
        "admin_id": admin["id"],
        "refresh_token": refresh_token,
        "is_active": True
    }

    supabase.table("auth_sessions").insert(session_data).execute()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh")
def refresh_token(refresh_token: str):

    try:

        payload = jwt.decode(
            refresh_token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
        )

        session = supabase.table("auth_sessions") \
            .select("*") \
            .eq("refresh_token", refresh_token) \
            .eq("is_active", True) \
            .execute()

        if not session.data:
            raise HTTPException(
                status_code=401,
                detail="Session expired or logged out"
            )

        new_access_token = create_access_token({
            "admin_id": payload["admin_id"]
        })

        return {
            "access_token": new_access_token
        }

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )
    

@router.post("/logout")
def logout(refresh_token: str):

    supabase.table("auth_sessions") \
        .update({"is_active": False}) \
        .eq("refresh_token", refresh_token) \
        .execute()

    return {
        "message": "Logged out successfully"
    }