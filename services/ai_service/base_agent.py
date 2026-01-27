from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Tuple, Any
from services.ai_service.gemini_service import GeminiLLMService

class BaseAgent(ABC):
    def __init__(self, llm_service: GeminiLLMService):
        self.llm = llm_service

    @abstractmethod
    async def run(self, **kwargs):
        pass

    from pydantic import BaseModel
    from typing import Type, Optional

    def query_llm(
            self,
            prompt: str,
            history: Optional[List[str]] = None,
            is_json_response: bool = True,
            temperature: float = 0.7,
            image_bytes: Optional[bytes] = None,
            image_mime_type: str = "image/jpeg",
            output_schema: Optional[Type[BaseModel]] = None  # <-- Add this
    ) -> Tuple[Dict[str, Any] | str, Optional[str]]:
        """
        Sends a prompt to the LLM (Gemini) and optionally includes an image for multimodal input.

        :param prompt: Prompt string for the model.
        :param history: Optional list of previous context strings.
        :param is_json_response: Whether the response should be parsed as JSON.
        :param temperature: Sampling temperature.
        :param image_bytes: Optional image bytes for multimodal models.
        :param image_mime_type: MIME type of the image (default: "image/jpeg").
        :param output_schema: Optional Pydantic model for structured output.
        :return: Tuple of (response, error). Response is JSON if is_json_response=True.
        """
        return self.llm.send_prompt(
            prompt=prompt,
            history_context=history,
            is_json_response=is_json_response,
            temperature=temperature,
            image_bytes=image_bytes,
            image_mime_type=image_mime_type,
            output_schema=output_schema
        )
