from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from typing import List
from ..models.models import ResumeUpload, CareerChatSession, CareerChatMessage
from datetime import datetime, timezone
from ..core.database import db_dependency
from ..utils.auth import user_dependency
from ..shemas.shemas import ChatMessageResponse, ChatMessageRequest, ChatSessionCreate
from ..services.agent import CareerAgent


router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.post("/start", response_model=int)
async def start_chat_session(user: user_dependency, db: db_dependency, resume_id):
    resume = db.query(ResumeUpload).filter_by(id= resume_id, user_id=user.get("user_id")).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    session = CareerChatSession(resume_id=resume.id, started_at=datetime.now(timezone.utc))
    db.add(session)
    db.commit()
    db.refresh(session)
    return session.id


@router.post("/send", response_model=ChatMessageResponse)
async def send_message(chat_request: ChatMessageRequest, db: db_dependency, user: user_dependency):
    session = db.query(CareerChatSession).filter_by(id=chat_request.session_id).first()
    if not session or session.resume.user_id != user.get("user_id"):
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    user_message = CareerChatMessage(
        session_id=session.id,
        content=chat_request.message,
        role="user",
        timestamp=datetime.now(timezone.utc)
    )

    db.add(user_message)


    resume_text = session.resume.extracted_text
    history = sorted(session.messages, key=lambda x: x.timestamp)[-10:]
    history = [
        {"role": "user" if msg.role == "user" else "assistant", "content": msg.content}
        for msg in session.messages
    ]
    summery = "Hi I am a good AI eng and good person I love AI and Volleyball"
    agent = CareerAgent(user.get("username"), resume_text, summery)
    response = agent.chat(chat_request.message, history)

    agent_msg = CareerChatMessage(
        session_id=session.id,
        role="agent",
        content=response,
        timestamp=datetime.now(timezone.utc)
    )
    db.add(agent_msg)
    db.commit()

    return ChatMessageResponse(agent=response)


@router.get("/{session_id}/history", status_code=status.HTTP_200_OK, response_model=List[ChatMessageResponse])
async def get_chat_history(session_id: int, user: user_dependency, db: db_dependency):
    session = db.query(CareerChatSession).filter_by(id=session_id).first()
    if not session or session.resume.user_id != user.get("user_id"):
        raise HTTPException(status_code=404, detail="Session not found")
    
    messages = session.messages
    return[ChatMessageResponse(agent=msg.content) if msg.role == "agent" else ChatMessageResponse(user=msg.content) for msg in messages]
