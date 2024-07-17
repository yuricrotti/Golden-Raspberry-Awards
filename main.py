from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
import os
import sys
from models.models import Award
from database.database import engine, Base, get_db, SessionLocal
from repositories.repositories import AwardRepository
from schemas.schemas import AwardBaseRequest, AwardResponse
import logging

from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup (lifespan)")

    # Create a new session
    db: Session = SessionLocal()

    try:
        # get current working directory
        cwd = os.getcwd()
        dir_data = os.path.join(cwd, "data", "movielist.csv")

        # Load data into the database when the application starts
        AwardRepository.save_from_csv(db, dir_data)

        yield
    finally:
        # Clean up resources here, like closing database connections
        logger.info("Application shutdown (lifespan)")
        db.close()


app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Message": "Welcome to the Awards API"}

@app.get("/api/awards/winner_interval", response_model=dict)
def read_root():

    db: Session = SessionLocal()

    response = AwardRepository.get_winner(db)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Winner Intervals not found"
        )

    return response


@app.post(
    "/api/awards", response_model=AwardResponse, status_code=status.HTTP_201_CREATED
)
def create(request: AwardBaseRequest, db: Session = Depends(get_db)):
    award = AwardRepository.save(db, Award(**request.dict()))
    return AwardResponse.from_orm(award)


@app.get("/api/awards", response_model=list[AwardResponse])
def find_all(db: Session = Depends(get_db)):
    awards = AwardRepository.find_all(db)
    return [AwardResponse.from_orm(award) for award in awards]


@app.get("/api/awards/{id}", response_model=AwardResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    award = AwardRepository.find_by_id(db, id)
    if award is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Award not found"
        )
    return AwardResponse.from_orm(award)


@app.put("/api/awards/{id}", response_model=AwardResponse)
def update(id: int, request: AwardBaseRequest, db: Session = Depends(get_db)):
    if not AwardRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Award not found"
        )
    award = Award(**request.dict())
    award.id = id
    AwardRepository.save(db, award)
    return AwardResponse.from_orm(award)


@app.delete("/api/awards/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    if not AwardRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Award not found"
        )
    AwardRepository.delete_by_id(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
