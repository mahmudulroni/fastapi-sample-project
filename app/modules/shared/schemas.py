from sqlmodel import SQLModel

# ------------------------
# Global Message Schemas
# ------------------------


class Message(SQLModel):
    message: str
