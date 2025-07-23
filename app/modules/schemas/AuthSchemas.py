from sqlmodel import SQLModel


# ------------------------
# Auth Token Schemas
# ------------------------

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None  # Typically holds the user ID or email
