import base64
from typing import Union

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from fastapi import UploadFile

from app.core import prompts
from app.core.config import settings
from app.schemas.models import ImageNutritionEstimate

DEFAULT_VISION_MODEL = "gpt-4o"

class NutritionService:
    def __init__(self):
        self.llm = ChatOpenAI(model=DEFAULT_VISION_MODEL, temperature=0.3, api_key=settings.OPENAI_API_KEY)
        self.structured_llm = self.llm.with_structured_output(ImageNutritionEstimate)

    async def analyze_image(self, file_content: bytes, media_type: str = "image/jpeg") -> ImageNutritionEstimate:
        base64_image = base64.b64encode(file_content).decode("utf-8")
        image_url = f"data:{media_type};base64,{base64_image}"
        
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompts.VISION_PROMPT},
                {"type": "image_url", "image_url": {"url": image_url}},
            ]
        )
        
        result: ImageNutritionEstimate = await self.structured_llm.ainvoke([message])
        return result

nutrition_service = NutritionService()
