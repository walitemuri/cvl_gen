from io import BytesIO
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter,File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import schemas, oauth2, models
from .. database import get_db
import PyPDF2
from typing import Annotated

router = APIRouter(tags=["Resume Requests"],
                   prefix="/resume")


#Get Resume by ID
@router.get("/{id}", response_model=schemas.ResumeOut)
def get_resume(id: int , current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    user_resume = db.query(models.Resume).filter(models.Resume.id == id).first()
    if not user_resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Resume {id} not found."
        )
    if current_user.resume_id != user_resume.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to resume.")
    return user_resume


@router.post("/", response_model=schemas.ResumeOut)
async def create_user_resume(file: UploadFile = File(None), current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    if current_user.resume_id != None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only one resume per user at a time.")
    if not file:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail=f"No file."
        )
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only PDF files are allowed.",
        )
    pdf_reader = PyPDF2.PdfReader(BytesIO(await file.read()))
    content = ""
    for page in range(len(pdf_reader.pages)):
        content += pdf_reader.pages[page].extract_text()
    new_resume = models.Resume(resume_string=content)
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)
    current_user.resume_id = new_resume.id
    db.commit()
    return new_resume

@router.delete("/{id}")
def delete_resume(id: int, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    query = db.query(models.Resume).filter(models.Resume.id == id)
    deleted_resume = query.first()
    if not deleted_resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Resume {id} not found.")
    if current_user.resume_id != deleted_resume.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to delete.")
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)