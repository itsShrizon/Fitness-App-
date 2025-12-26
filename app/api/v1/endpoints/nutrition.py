from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.schemas.models import ImageNutritionEstimate
from app.services.nutrition_service import nutrition_service, NutritionService

router = APIRouter()

@router.post("/analyze-image", response_model=ImageNutritionEstimate)
async def analyze_image(
    file: UploadFile = File(...),
    service: NutritionService = Depends(lambda: nutrition_service)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        content = await file.read()
        return await service.analyze_image(content, media_type=file.content_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
