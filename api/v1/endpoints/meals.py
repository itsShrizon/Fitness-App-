from typing import List
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.models import Meal, MealGenerationRequest
from app.services.meal_service import meal_service, MealService

router = APIRouter()

@router.post("/generate", response_model=List[Meal])
async def generate_meals(
    request: MealGenerationRequest,
    service: MealService = Depends(lambda: meal_service)
):
    try:
        return await service.generate_meals(
            meal_type=request.meal_type,
            previous_meal_names=request.previous_meal_names,
            count=request.count
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
