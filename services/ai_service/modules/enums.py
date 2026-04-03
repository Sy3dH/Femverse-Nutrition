from enum import Enum

class AgentName(Enum):
    NUTRITION = "nutrition"
    NUTRITION_TIP = "nutrition-tip"
    NUTRITION_TEXT_LOGGING = "nutrition-text-logging"
    NUTRITION_IMAGE_LOGGING = "nutrition-image-logging"
    NUTRITION_LABEL_IMAGE_LOGGING = "nutrition-label-image-logging"
    NUTRITION_INSIGHTS = "nutrition-insights"
    MENSTRUATION_PERSONA_UPDATE = "menstruation-persona-update"
    PREGNANCY_PERSONA_UPDATE = "pregnancy-persona-update"
    NUTRITION_PERSONA_UPDATE = "nutrition-persona-update"
    FITNESS_PERSONA_UPDATE = "fitness-persona-update"


class PlanType(Enum):
    STANDARD_BALANCED = "standard_balanced"
    WEIGHT_LOSS = "weight_loss"
    WEIGHT_GAIN = "weight_gain"
    PCOS_FRIENDLY = "pcos_friendly"
    PREGNANCY_T1 = "pregnancy_t1"
    PREGNANCY_T2 = "pregnancy_t2"
    PREGNANCY_T3 = "pregnancy_t3"
    POSTPARTUM = "postpartum"
    PRECONCEPTION = "preconception"
    GLUTEN_FREE = "gluten_free"
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    DIABETIC_LOW_GI = "diabetic_low_gi"
    WEDDING_PREP = "wedding_prep"
    EXAM_BRAIN_BOOST = "exam_brain_boost"
    HIGH_PROTEIN_ATHLETIC = "high_protein_athletic"

class AgentModuleEnum(Enum):
    NUTRITION = "nutrition"
    PERSONA = "persona"