from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

ALLOWED_MEAL_TYPES = {"breakfast", "lunch", "dinner", "snack"}


class Ingredient(BaseModel):
    name: str
    quantity: float
    unit: str


class RecipeStep(BaseModel):
    step: int
    instruction: str


class Serving(BaseModel):
    size: float
    unit: str


class NutritionUnit(BaseModel):
    macros: str = Field(default="g", description="Unit for macronutrients")
    minerals: str = Field(default="mg", description="Unit for minerals")
    calories: str = Field(default="kcal", description="Unit for calories")


class MacroUnits(BaseModel):
    macros: str = Field("g", description="Unit for macronutrients")
    energy: str = Field("kcal", description="Unit for energy")


class Macros(BaseModel):
    carbs: float
    fats: float
    protein: float


class ExtendedMacros(BaseModel):
    calories: float
    carbs: float
    protein: float
    fat: float
    fiber: float
    sugar: float


class Minerals(BaseModel):
    sodium: float
    potassium: float
    calcium: float
    iron: float


class Nutrition(BaseModel):
    units: MacroUnits = Field(default_factory=MacroUnits)
    macros: Macros
    energy: float


class ImageNutrition(BaseModel):
    unit: NutritionUnit = Field(default_factory=NutritionUnit)
    macros: ExtendedMacros
    minerals: Minerals


class Meal(BaseModel):
    id: str | None = None  # Optional for generation input/output if needed
    name: str
    description: str
    category: str
    serving: Serving
    nutrition: Nutrition
    ingredients: List[Ingredient]
    recipe: List[RecipeStep]
    tags: List[str]
    image_url: str | None = None
    created_at: str | None = None


class MealList(BaseModel):
    meals: List[Meal]


class ImageNutritionEstimate(BaseModel):
    name: str
    estimated: bool = Field(default=True)
    nutrition: ImageNutrition


# --- Request Schemas ---

class ChatRequest(BaseModel):
    message: str
    history: List[dict] | None = None
    context: dict | None = None

class MealGenerationRequest(BaseModel):
    meal_type: str
    previous_meal_names: List[str] = []
    count: int = 3
