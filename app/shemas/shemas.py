from pydantic import BaseModel, EmailStr


class UserRequest(BaseModel):
    username: str
    email: EmailStr


class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class UserVerification(BaseModel):
    password: str
    new_password: str


class ChatMessageResponse(BaseModel):
    user: str | None = None
    agent: str | None = None


class ChatMessageRequest(BaseModel):
    session_id: int
    message: str


class ChatSessionCreate(BaseModel):
    resume_id: int


class ResumeUploadResponse(BaseModel):
    id: int
    filename:str
