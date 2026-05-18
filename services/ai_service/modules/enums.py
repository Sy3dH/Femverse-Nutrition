from enum import Enum

class AgentName(Enum):
    NUTRITION = "nutrition"
    NUTRITION_TIP = "nutrition-tip"
    NUTRITION_TEXT_LOGGING = "nutrition-text-logging"
    NUTRITION_IMAGE_LOGGING = "nutrition-image-logging"
    NUTRITION_LABEL_IMAGE_LOGGING = "nutrition-label-image-logging"
    NUTRITION_INSIGHTS = "nutrition-insights"
    # Persona-update agents. Each module has TWO variants — single-log and
    # batch-log — so the route layer can dispatch the right system prompt
    # without the LLM ever seeing the unused mode's rules.
    MENSTRUATION_PERSONA_UPDATE_SINGLE = "menstruation-persona-update-single"
    MENSTRUATION_PERSONA_UPDATE_BATCH = "menstruation-persona-update-batch"
    PREGNANCY_PERSONA_UPDATE_SINGLE = "pregnancy-persona-update-single"
    PREGNANCY_PERSONA_UPDATE_BATCH = "pregnancy-persona-update-batch"
    NUTRITION_PERSONA_UPDATE_SINGLE = "nutrition-persona-update-single"
    NUTRITION_PERSONA_UPDATE_BATCH = "nutrition-persona-update-batch"
    FITNESS_PERSONA_UPDATE_SINGLE = "fitness-persona-update-single"
    FITNESS_PERSONA_UPDATE_BATCH = "fitness-persona-update-batch"


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