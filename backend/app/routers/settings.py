from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.config import get_settings
from app.database import get_session
from app.models import AppSetting, AppSettingUpsert, utc_now

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("")
def list_settings(session: Session = Depends(get_session)) -> dict[str, object]:
    runtime = get_settings()
    user_settings = session.exec(select(AppSetting).order_by(AppSetting.key)).all()
    return {
        "runtime": {
            "environment": runtime.environment,
            "database_url": runtime.database_url,
            "chroma_path": runtime.chroma_path,
            "llm_model": runtime.llm_model,
            "embedding_model": runtime.embedding_model,
        },
        "user_settings": user_settings,
    }


@router.put("/{key}", response_model=AppSetting)
def upsert_setting(
    key: str,
    payload: AppSettingUpsert,
    session: Session = Depends(get_session),
) -> AppSetting:
    existing = session.exec(select(AppSetting).where(AppSetting.key == key)).first()
    if existing is None:
        existing = AppSetting(key=key, value=payload.value)
    else:
        existing.value = payload.value
        existing.updated_at = utc_now()
    session.add(existing)
    session.commit()
    session.refresh(existing)
    return existing
