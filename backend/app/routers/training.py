from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import TrainingPlan, TrainingPlanCreate

router = APIRouter(prefix="/training-plans", tags=["training plans"])


@router.get("", response_model=list[TrainingPlan])
def list_training_plans(session: Session = Depends(get_session)) -> list[TrainingPlan]:
    return list(
        session.exec(select(TrainingPlan).order_by(TrainingPlan.created_at.desc())).all()
    )


@router.post("", response_model=TrainingPlan)
def create_training_plan(
    payload: TrainingPlanCreate, session: Session = Depends(get_session)
) -> TrainingPlan:
    plan = TrainingPlan.model_validate(payload)
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan


@router.get("/{plan_id}", response_model=TrainingPlan)
def read_training_plan(
    plan_id: int, session: Session = Depends(get_session)
) -> TrainingPlan:
    plan = session.get(TrainingPlan, plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Training plan not found")
    return plan
