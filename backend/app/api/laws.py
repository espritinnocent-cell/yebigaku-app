from app.database import get_session
from app.models import LawArticle
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

router = APIRouter(prefix="/api/laws", tags=["Laws"])


@router.get("/", response_model=list[LawArticle])
def get_laws(
    law_name: str | None = None,
    session: Session = Depends(get_session),
):
    """保存されている条文一覧を取得する（法律名での絞り込みも可能）"""
    query = select(LawArticle)
    if law_name:
        query = query.where(LawArticle.law_name == law_name)
    return session.exec(query).all()


@router.get("/{law_id}", response_model=LawArticle)
def get_law_by_id(law_id: int, session: Session = Depends(get_session)):
    """指定されたIDの条文詳細を取得する"""
    article = session.get(LawArticle, law_id)
    if not article:
        raise HTTPException(status_code=404, detail="指定された条文が見つかりません。")
    return article
