from fastapi import APIRouter, UploadFile, File, HTTPException
from ..shemas.shemas import ResumeUploadResponse
from starlette import status
from ..models.models import ResumeUpload
from ..core.database import db_dependency
from ..utils.auth import user_dependency
from ..utils.utils import extract_pdf
import io


router = APIRouter(
    prefix='/resume',
    tags=['resume upload']
)


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(db: db_dependency, user: user_dependency, file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload PDF file")
    
    content = await file.read()
    try:
        pdf_stream = io.BytesIO(content)
        extracted_text = extract_pdf(pdf_stream)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Failed to extract the file")
    
    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="Empty or unreadable PDF")
    
    resume = ResumeUpload(
        filename=file.filename,
        extracted_text=extracted_text,
        user_id=user.get("user_id")
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)


    return ResumeUploadResponse(id=resume.id, filename=resume.filename)
