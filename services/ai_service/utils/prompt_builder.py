from typing import Dict, Any
from services.ai_service.utils import prompt_templates
from services.ai_service.modules.enums import AgentName
from typing import Optional


def _build_prompt_context(data: Any) -> Dict[str, Any]:
    """
    Recursively converts Pydantic models to flat dict for prompt formatting.
    """
    if hasattr(data, 'model_dump'):
        context = data.model_dump()
    elif hasattr(data, 'dict'):
        context = data.dict()
    else:
        context = data if isinstance(data, dict) else {}

    for key, value in context.items():

        if hasattr(value, 'model_dump') or hasattr(value, 'dict'):
            nested = value.model_dump() if hasattr(value, 'model_dump') else value.dict()
            context[key] = '\n'.join(f"  {k}: {v}" for k, v in nested.items())

        elif isinstance(value, dict):
            context[key] = '\n'.join(f"  {k}: {v}" for k, v in value.items())

        elif isinstance(value, list):
            context[key] = '\n'.join(f"  - {item}" for item in value)

        elif isinstance(value, bytes):
            context[key] = f"<binary data: {len(value)} bytes>"

    return context

def _get_prompt_template(agent_name: AgentName) -> Optional[str]:
    if agent_name == AgentName.NUTRITION.value:
        return prompt_templates.NUTRITION_AGENT_PROMPT

    elif agent_name == AgentName.NUTRITION_INSIGHTS.value:
        return prompt_templates.NUTRITION_INSIGHTS_PROMPT

    elif agent_name == AgentName.NUTRITION_TEXT_LOGGING.value:
        return prompt_templates.NUTRITION_TEXT_LOGGING_PROMPT

    elif agent_name == AgentName.NUTRITION_IMAGE_LOGGING.value:
        return prompt_templates.NUTRITION_IMAGE_LOGGING_PROMPT

    elif agent_name == AgentName.NUTRITION_LABEL_IMAGE_LOGGING.value:
        return prompt_templates.NUTRITION_LABEL_IMAGE_PROMPT

    return prompt_templates.NUTRITION_AGENT_PROMPT



class PromptBuilder:
    @staticmethod
    def build_prompt(agent_name: AgentName, data: dict) -> str:
        """
        Generic prompt formatter.
        Knows nothing about agents, modules, or data models.
        """

        template = _get_prompt_template(agent_name=agent_name)
        context = _build_prompt_context(data=data)

        print("context", context)

        try:
            return template.format(**context)
        except KeyError as e:
            raise ValueError(f"Missing prompt variable: {e}")

    @staticmethod
    def build_template(agent_name: AgentName) -> str:

        return _get_prompt_template(agent_name=agent_name)