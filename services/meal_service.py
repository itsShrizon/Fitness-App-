from datetime import datetime, timezone
from typing import List, Sequence

from langchain_openai import ChatOpenAI

from app.core import prompts
from app.core.config import settings
from app.schemas.models import ALLOWED_MEAL_TYPES, Meal, MealList

DEFAULT_MODEL = "gpt-4o-mini" # Corrected from gpt-4.1-mini

class MealService:
    def __init__(self):
        self.llm = ChatOpenAI(model=DEFAULT_MODEL, temperature=0.7, api_key=settings.OPENAI_API_KEY)
        self.chain = prompts.MEAL_GENERATION_PROMPT | self.llm.with_structured_output(MealList)

    async def generate_meals(
        self,
        meal_type: str,
        previous_meal_names: Sequence[str],
        count: int = 3,
    ) -> List[Meal]:
        normalized_type = meal_type.strip().lower()
        if normalized_type not in ALLOWED_MEAL_TYPES:
            raise ValueError(f"meal_type must be one of {sorted(ALLOWED_MEAL_TYPES)}")
        
        previous_list = [name.strip() for name in previous_meal_names if name.strip()]
        timestamp = datetime.now(timezone.utc).isoformat()

        # Invoke chain
        result: MealList = await self.chain.ainvoke(
            {
                "meal_type": normalized_type,
                "previous_meals": previous_list or ["none"],
                "count": count,
                "timestamp": timestamp,
            }
        )
        return result.meals

meal_service = MealService()
