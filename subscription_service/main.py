from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import Subscription
from schemas import SubscriptionCreate, SubscriptionResponse
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/subscriptions/", response_model=SubscriptionResponse)
async def get_subscriptions(db: AsyncSession = Depends(get_db)):
    logger.debug(f"Received request to get all subscriptions")

    results = await db.execute(select(Subscription))

    subscriptions = results.scalars().all()

    return subscriptions


@app.post("/subscriptions/", response_model=SubscriptionResponse)
async def create_subscription(sub: SubscriptionCreate, db: Session = Depends(get_db)):
    logger.debug(f"Received payload: {sub}")
    # Check if the email already exists
    result = await db.execute(select(Subscription).where(Subscription.email == sub.email))
    existing_subscription = result.scalars().first()
    if existing_subscription:
        raise HTTPException(status_code=400, detail="Email already subscribed")

    # Create new subscription
    new_subscription = Subscription(email=sub.email)
    db.add(new_subscription)
    try:
        await db.commit()
        await db.refresh(new_subscription)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=500, detail="Error while saving subscription")

    return new_subscription


@app.get("/")
def read_root():
    return {"message": "Welcome to Subscription Service"}
