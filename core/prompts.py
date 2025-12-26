from langchain_core.prompts import ChatPromptTemplate

VISION_PROMPT = """Analyze this food image and provide a detailed nutrition estimate.

Instructions:
- Identify the main food item or dish name
- Estimate realistic portion sizes based on visual cues
- Provide comprehensive nutrition breakdown including:
  * Macros: calories, carbs, protein, fat, fiber, sugar (in grams)
  * Minerals: sodium, potassium, calcium, iron (in milligrams)
- Base estimates on standard serving sizes and USDA nutrition data
- Mark the estimate as approximate (estimated: true)

IMPORTANT - Unit formatting:
- Use "g" for macros unit (NOT "grams")
- Use "mg" for minerals unit (NOT "milligrams")
- Use "kcal" for calories unit (NOT "kilocalories")

Be accurate and conservative in estimates. If multiple items are visible, estimate the combined nutrition.
"""

MEAL_GENERATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a nutrition-focused meal planner. Generate concise, flavorful meals
that fit the requested category. Avoid repeating any meal names from previous
days. Each meal must include realistic ingredient quantities and matching
macros/energy values. Use ISO 8601 timestamps supplied.

Rules:
- Respect the requested category exactly: {meal_type}.
- Produce exactly {count} meals.
- Make names unique versus `previous_meals` and within the batch.
- Keep ingredients practical and macros plausible for the described dish.
- If category is "snack", favor quicker, lighter items.
            """,
        ),
        (
            "human",
            """
Previous meal names: {previous_meals}
Requested category: {meal_type}
Count: {count}
Timestamp to use for created_at: {timestamp}
Return JSON matching the schema.
            """,
        ),
    ]
)

CHAT_SYSTEM_PROMPT = "You are a helpful fitness and nutrition assistant. Keep responses concise and practical."
