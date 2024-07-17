from pydantic import BaseModel

class AwardBase(BaseModel):
    year: int
    title: str
    studios: str
    producers: str
    winner: bool

class AwardBaseRequest(AwardBase):
    # Implement the AwardBaseRequest class
    ...

class AwardResponse(AwardBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True  # Add this line to enable from_orm