from services.ai_service.resolvers.base_resolver import BaseInputResolver
from typing import Optional, Dict, Any

class NutritionTipInputResolver(BaseInputResolver):

    async def resolve(
        self,
        user_id: str,
        date: Optional[int] = None
    ) -> Dict[str, Any]:

        # DB access (backend-owned)
        # user = await user_repo.get(user_id)
        # health = await health_repo.get_latest(user_id, date)
        # prefs = await nutrition_pref_repo.get(user_id)

        return {
            "bmi": health.bmi,
            "bmr": health.bmr,
            "country": user.country,
            "food_prefs": prefs.food_prefs,
            "allergies": prefs.allergies,
            "health_goals": prefs.health_goals,
            "target_weight": prefs.target_weight,
            "location": user.location,
            "plan_type": prefs.plan_type,
        }
