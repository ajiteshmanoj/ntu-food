from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class ReviewCreate(BaseModel):
    stall_id: int = Field(..., gt=0)
    order_id: Optional[int] = Field(None, gt=0)
    rating: float = Field(..., ge=1.0, le=5.0, description="Rating must be between 1 and 5")
    comment: Optional[str] = Field(None, max_length=1000)

    @validator('rating')
    def validate_rating(cls, v):
        if v < 1.0 or v > 5.0:
            raise ValueError('Rating must be between 1.0 and 5.0')
        return round(v, 1)  # Round to 1 decimal place

class ReviewUpdate(BaseModel):
    rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    comment: Optional[str] = Field(None, max_length=1000)

    @validator('rating')
    def validate_rating(cls, v):
        if v is not None and (v < 1.0 or v > 5.0):
            raise ValueError('Rating must be between 1.0 and 5.0')
        return round(v, 1) if v else v

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    stall_id: int
    order_id: Optional[int] = None
    rating: float
    comment: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReviewWithUser(ReviewResponse):
    user_name: str
    user_email: str

    class Config:
        from_attributes = True

class StallRatingStats(BaseModel):
    stall_id: int
    average_rating: float
    total_reviews: int
    rating_distribution: dict  # {1: count, 2: count, ...}

    class Config:
        from_attributes = True
