from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List
from app.database.database import get_db
from app.models.review import Review
from app.models.stall import Stall
from app.models.order import Order, OrderStatus
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse, ReviewWithUser, StallRatingStats
from app.routes.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(
    review: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new review for a stall"""
    # Verify stall exists
    stall = db.query(Stall).filter(Stall.id == review.stall_id).first()
    if not stall:
        raise HTTPException(status_code=404, detail="Stall not found")

    # If order_id is provided, verify the order belongs to the user and is completed
    if review.order_id:
        order = db.query(Order).filter(
            Order.id == review.order_id,
            Order.user_id == current_user.id
        ).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if order.stall_id != review.stall_id:
            raise HTTPException(status_code=400, detail="Order is not from this stall")
        if order.status != OrderStatus.COMPLETED:
            raise HTTPException(status_code=400, detail="Can only review completed orders")

        # Check if review already exists for this order
        existing_review = db.query(Review).filter(Review.order_id == review.order_id).first()
        if existing_review:
            raise HTTPException(status_code=400, detail="Review already exists for this order")

    # Check if user has already reviewed this stall (without order)
    if not review.order_id:
        existing_review = db.query(Review).filter(
            Review.user_id == current_user.id,
            Review.stall_id == review.stall_id,
            Review.order_id.is_(None)
        ).first()
        if existing_review:
            raise HTTPException(status_code=400, detail="You have already reviewed this stall")

    # Create review
    db_review = Review(
        user_id=current_user.id,
        stall_id=review.stall_id,
        order_id=review.order_id,
        rating=review.rating,
        comment=review.comment
    )

    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    # Update stall average rating
    update_stall_rating(review.stall_id, db)

    return db_review

@router.get("/stall/{stall_id}", response_model=List[ReviewWithUser])
def get_stall_reviews(
    stall_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get all reviews for a stall"""
    stall = db.query(Stall).filter(Stall.id == stall_id).first()
    if not stall:
        raise HTTPException(status_code=404, detail="Stall not found")

    reviews = db.query(Review).options(
        joinedload(Review.user)
    ).filter(Review.stall_id == stall_id).order_by(Review.created_at.desc()).offset(skip).limit(limit).all()

    # Format response with user information
    result = []
    for review in reviews:
        result.append({
            "id": review.id,
            "user_id": review.user_id,
            "stall_id": review.stall_id,
            "order_id": review.order_id,
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at,
            "updated_at": review.updated_at,
            "user_name": review.user.name,
            "user_email": review.user.ntu_email
        })

    return result

@router.get("/stall/{stall_id}/stats", response_model=StallRatingStats)
def get_stall_rating_stats(
    stall_id: int,
    db: Session = Depends(get_db)
):
    """Get rating statistics for a stall"""
    stall = db.query(Stall).filter(Stall.id == stall_id).first()
    if not stall:
        raise HTTPException(status_code=404, detail="Stall not found")

    reviews = db.query(Review).filter(Review.stall_id == stall_id).all()

    if not reviews:
        return {
            "stall_id": stall_id,
            "average_rating": 0.0,
            "total_reviews": 0,
            "rating_distribution": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        }

    total_rating = sum(r.rating for r in reviews)
    average_rating = round(total_rating / len(reviews), 1)

    # Calculate rating distribution
    rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for review in reviews:
        rating_int = round(review.rating)
        if rating_int in rating_distribution:
            rating_distribution[rating_int] += 1

    return {
        "stall_id": stall_id,
        "average_rating": average_rating,
        "total_reviews": len(reviews),
        "rating_distribution": rating_distribution
    }

@router.get("/user/my-reviews", response_model=List[ReviewResponse])
def get_user_reviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all reviews by the current user"""
    reviews = db.query(Review).filter(Review.user_id == current_user.id).order_by(Review.created_at.desc()).all()
    return reviews

@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(
    review_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific review"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a review (only by the review author)"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this review")

    if review_update.rating is not None:
        review.rating = review_update.rating
    if review_update.comment is not None:
        review.comment = review_update.comment

    db.commit()
    db.refresh(review)

    # Update stall average rating
    update_stall_rating(review.stall_id, db)

    return review

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a review (only by the review author)"""
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this review")

    stall_id = review.stall_id
    db.delete(review)
    db.commit()

    # Update stall average rating
    update_stall_rating(stall_id, db)

    return None

def update_stall_rating(stall_id: int, db: Session):
    """Helper function to update stall's average rating"""
    reviews = db.query(Review).filter(Review.stall_id == stall_id).all()

    if reviews:
        average_rating = sum(r.rating for r in reviews) / len(reviews)
        stall = db.query(Stall).filter(Stall.id == stall_id).first()
        if stall:
            stall.rating = round(average_rating, 1)
            db.commit()
    else:
        stall = db.query(Stall).filter(Stall.id == stall_id).first()
        if stall:
            stall.rating = 0.0
            db.commit()
