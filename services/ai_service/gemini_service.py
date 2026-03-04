import os
import json
import logging
from google import genai
from google.oauth2 import service_account
from typing import List, Dict, Optional, Any
from google.genai.types import GenerateContentConfig
from services.ai_service.config.constants import (
    GEMINI_LLM_MODEL,
    GEMINI_EMBEDDING_MODEL,
    FITNESS_FINE_TUNED_MODEL_ENDPOINT
)
from services.ai_service.cache.gemini_cache_registry import GeminiCacheRegistry
from dotenv import load_dotenv


load_dotenv()
logger = logging.getLogger("celery")

VERTEX_AI_CREDS_PATH = os.getenv("VERTEX_AI_CREDENTIALS_PATH")
VERTEX_AI_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
VERTEX_AI_LOCATION = os.getenv("LOCATION_VERTEX_AI", "us-central1")

GEMINI_PRICING = {
    # model substring -> (input_per_1m, output_per_1m, cached_input_per_1m)
    "gemini-2.5-pro":        (1.25,  10.00, 0.31),
    "gemini-2.5-flash":      (0.30,   2.50, 0.075),
    "gemini-2.5-flash-lite": (0.10,   0.40, 0.025),
    "gemini-2.0-flash-lite": (0.075,  0.30, 0.01875),
    "gemini-2.0-flash":      (0.10,   0.40, 0.025),
    "gemini-1.5-pro":        (1.25,   5.00, 0.3125),
    "gemini-1.5-flash":      (0.075,  0.30, 0.01875),
}

def build_gemini_history_context(
        history: List[Dict[str, str]],
        max_turns: int = 5
) -> List[str]:
    """
    Builds a formatted list of previous interactions for Gemini API, limited to max_turns.

    :param history: List of dicts with 'role' and 'content'.
                    Example: [{'role': 'user', 'content': 'Hi'}, {'role': 'assistant', 'content': 'Hello'}]
    :param max_turns: Number of last conversation turns to include.
    :return: List of formatted strings like "User: message", "Assistant: message"
    """
    if not history:
        return []

    trimmed_history = history[:max_turns]
    formatted_history = []

    for entry in trimmed_history:
        role = entry.get("role", "").strip().lower()
        content = entry.get("content", "").strip()

        if role == "model":
            role = "assistant"  # normalize

        if role and content:
            formatted = f"{role.capitalize()}: {content}"
            formatted_history.append(formatted)

    return formatted_history


def _get_gemini_cost(model_identifier: str, input_tokens: int, output_tokens: int,
                     cached_tokens: int) -> float | None:
    """Calculate the cost in USD for a Gemini API call, or None if model pricing is unknown."""
    model_lower = model_identifier.lower()
    pricing = next((v for k, v in GEMINI_PRICING.items() if k in model_lower), None)
    if pricing is None:
        return None
    input_price, output_price, cached_price = pricing
    non_cached_input = max(0, input_tokens - cached_tokens)
    return (
            (non_cached_input * input_price / 1_000_000)
            + (cached_tokens * cached_price / 1_000_000)
            + (output_tokens * output_price / 1_000_000)
    )


class GeminiLLMService:
    def __init__(
            self,
            model_name: str = GEMINI_LLM_MODEL,
            embedding_model_name: str = GEMINI_EMBEDDING_MODEL,
            is_fine_tuned: bool = False,
            fine_tuned_model_endpoint: Optional[str] = None
    ):
        """
        Initialize Gemini service with Vertex AI using the new Google Gen AI SDK.

        Args:
            model_name: The LLM model to use (base model or fine-tuned model name)
            embedding_model_name: The embedding model to use
            is_fine_tuned: Whether the model is a fine-tuned model
            fine_tuned_model_endpoint: Full endpoint path for fine-tuned models
                                     Format: "projects/{PROJECT_NUMBER}/locations/{LOCATION}/models/{MODEL_ID}"
        """
        self.model = model_name
        self.embedding_model = embedding_model_name
        self.is_fine_tuned = is_fine_tuned
        self.fine_tuned_model_endpoint = fine_tuned_model_endpoint

        credentials = service_account.Credentials.from_service_account_file(VERTEX_AI_CREDS_PATH)

        # Add required scopes for Vertex AI and Generative AI
        scopes = [
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/generative-language'
        ]
        self.credentials = credentials.with_scopes(scopes)

        self.client = genai.Client(
            vertexai=True,
            project=VERTEX_AI_PROJECT_ID,
            location=VERTEX_AI_LOCATION,
            credentials=self.credentials
        )

        if self.is_fine_tuned and self.fine_tuned_model_endpoint:
            self.model_identifier = self.fine_tuned_model_endpoint
            logger.info(f"Initialized fine-tuned Gemini model: {self.fine_tuned_model_endpoint}")
        else:
            self.model_identifier = model_name
            logger.info(f"Initialized base Gemini model: {model_name} using Google Gen AI SDK")

        self.cache_registry = GeminiCacheRegistry(
            client=self.client,
            model=self.model_identifier,
        )

    def send_prompt(
            self,
            prompt: str,
            history_context: Optional[List[str]] = None,
            is_json_response: bool = True,
            temperature: float = 0.7,
            image_bytes: Optional[bytes] = None,
            image_mime_type: str = "image/jpeg",
            output_schema: Optional[Any] = None,
            cached_content_name: Optional[str] = None,
    ) -> tuple[None, str] | None | tuple[Any, None] | tuple[str | None, None]:
        """
        Sends a prompt to the Gemini model with optional structured output.

        :param prompt:               The user's current message.
        :param history_context:      Formatted prior turns from build_gemini_history_context().
        :param is_json_response:     Whether to parse and return a JSON response.
        :param temperature:          Sampling temperature.
        :param image_bytes:          Optional raw image bytes to include in the request.
        :param image_mime_type:      MIME type of image_bytes.
        :param output_schema:        Optional Pydantic model for structured output validation.
        :param cached_content_name:  Full Gemini cache resource name
                                     ("projects/.../cachedContents/ID").
                                     When provided, the cached system prompt is injected by
                                     Gemini automatically — do NOT re-send it in contents.
        """
        try:
            prompt_list = [f"User: {prompt}"]
            contents = history_context + prompt_list if history_context else prompt_list

            # Add image to contents if provided
            if image_bytes:
                from google.genai.types import Part
                image_part = Part.from_bytes(data=image_bytes, mime_type=image_mime_type)
                contents = [image_part] + contents

            # Build config
            config_params = {
                "temperature": temperature,
                "response_mime_type": "application/json" if (is_json_response or output_schema) else "text/plain"
            }

            if output_schema:
                config_params["response_schema"] = output_schema

            # Wire in the server-side cache when provided.
            # Gemini injects the cached system prompt on its side —
            # no need to include it in contents.
            if cached_content_name:
                config_params["cached_content"] = cached_content_name

            config = GenerateContentConfig(**config_params)

            if not is_json_response and not output_schema:
                response = self.client.models.generate_content(
                    model=self.model_identifier,
                    contents=contents,
                    config=config
                )
                self._log_cache_usage(response)
                return response.text, None

            # JSON parsing with retries
            max_retries = 3
            response = None

            for attempt in range(1, max_retries + 1):
                response = self.client.models.generate_content(
                    model=self.model_identifier,
                    contents=contents,
                    config=config
                )

                self._log_cache_usage(response)

                try:
                    parsed = json.loads(response.text)

                    # Validate with Pydantic if schema provided
                    if output_schema:
                        validated = output_schema(**parsed)
                        return validated.model_dump(), None

                    return parsed, None

                except json.JSONDecodeError as je:
                    logger.warning(
                        f"[Gemini JSON Parse] Attempt {attempt}/{max_retries} failed: {je}. "
                        f"model={self.model_identifier}, "
                        f"response_text={response.text[:500]}"
                    )
                    if attempt == max_retries:
                        logger.error(
                            f"[Gemini JSON Parse] Exhausted retries. Unable to parse JSON response after {max_retries} attempts. "
                            f"model={self.model_identifier}"
                        )
                        return None, "Failed to parse JSON response from LLM"
                except Exception as validation_error:
                    logger.error(f"[Pydantic Validation] Failed: {validation_error}")
                    return None, f"Schema validation failed: {str(validation_error)}"

            return None

        except Exception as e:
            logger.error(f"Error occurred during llm response generation. Error={str(e)}")
            return None, str(e)

    # Gemini API pricing per 1M tokens (USD) — update as needed
    # Source: https://ai.google.dev/gemini-api/docs/pricing
    GEMINI_PRICING = {
        # model substring -> (input_per_1m, output_per_1m, cached_input_per_1m)
        "gemini-2.5-pro": (1.25, 10.00, 0.31),
        "gemini-2.5-flash": (0.30, 2.50, 0.075),
        "gemini-2.5-flash-lite": (0.10, 0.40, 0.025),
        "gemini-2.0-flash-lite": (0.075, 0.30, 0.01875),
        "gemini-2.0-flash": (0.10, 0.40, 0.025),
        "gemini-1.5-pro": (1.25, 5.00, 0.3125),
        "gemini-1.5-flash": (0.075, 0.30, 0.01875),
    }

    def _log_cache_usage(self, response) -> None:
        """
        Log cached token counts and estimated cost from the response usage metadata.
        A non-zero cached_content_token_count confirms the cache was hit
        and those tokens were billed at the discounted rate.
        """
        try:
            usage = getattr(response, "usage_metadata", None)
            if usage is None:
                return

            cached_tokens = getattr(usage, "cached_content_token_count", 0) or 0
            input_tokens = getattr(usage, "prompt_token_count", 0) or 0
            output_tokens = getattr(usage, "candidates_token_count", 0) or 0
            total_tokens = getattr(usage, "total_token_count", 0) or 0

            cost = _get_gemini_cost(self.model_identifier, input_tokens, output_tokens, cached_tokens)
            cost_part = f", cost=${cost:.6f}" if cost is not None else ""

            if cached_tokens:
                print(
                    f"[Gemini Cache] HIT — cached_tokens={cached_tokens}, "
                    f"input_tokens={input_tokens}, output_tokens={output_tokens}, "
                    f"total_tokens={total_tokens}, model={self.model_identifier}{cost_part}"
                )
            else:
                print(
                    f"[Gemini Cache] No cache hit — "
                    f"input_tokens={input_tokens}, output_tokens={output_tokens}, "
                    f"total_tokens={total_tokens}, model={self.model_identifier}{cost_part}"
                )
        except Exception as e:
            logger.warning(f"[Gemini Cache] Failed to read usage_metadata: {e}")

    def get_embeddings(self, text: str) -> List[float]:
        """
        Generates an embedding vector for the given text using the Gemini Embedding model.
        Note: Embeddings typically use base models, not fine-tuned models.

        :param text: The input text to embed.
        :return: A list of floats representing the embedding vector.
        """
        if not text:
            return []

        try:
            response = self.client.models.embed_content(
                model=self.embedding_model,  # Always use base embedding model
                contents=text
            )

            if response.embeddings:
                return response.embeddings[0].values
            return []

        except Exception as e:
            logger.error(f"Error occurred during generating embeddings. Error={str(e)}")
            return []

    @classmethod
    def create_fine_tuned_service(
            cls,
            fine_tuned_model_endpoint: str,
            model_name: str = "fine-tuned-model",
            embedding_model_name: str = GEMINI_EMBEDDING_MODEL
    ) -> 'GeminiLLMService':
        """
        Factory method to create a GeminiLLMService instance for fine-tuned models.

        Args:
            fine_tuned_model_endpoint: Full endpoint path for the fine-tuned model
                                     Format: "projects/{PROJECT_NUMBER}/locations/{LOCATION}/models/{MODEL_ID}"
            model_name: Descriptive name for the fine-tuned model
            embedding_model_name: The embedding model to use (typically base model)

        Returns:
            GeminiLLMService instance configured for fine-tuned model
        """
        return cls(
            model_name=model_name,
            embedding_model_name=embedding_model_name,
            is_fine_tuned=True,
            fine_tuned_model_endpoint=fine_tuned_model_endpoint
        )

    def get_model_info(self) -> Dict[str, str]:
        """
        Returns information about the current model configuration.

        Returns:
            Dictionary with model information
        """
        return {
            "model_type": "fine-tuned" if self.is_fine_tuned else "base",
            "model_name": self.model,
            "model_identifier": self.model_identifier,
            "embedding_model": self.embedding_model,
            "project_id": VERTEX_AI_PROJECT_ID,
            "location": VERTEX_AI_LOCATION
        }


gemini_service = GeminiLLMService()

fitness_gemini_service = GeminiLLMService.create_fine_tuned_service(
    fine_tuned_model_endpoint=FITNESS_FINE_TUNED_MODEL_ENDPOINT,
    model_name="fitness-fine-tuned-model"
)


def get_gemini_service() -> GeminiLLMService:
    """Get the default base Gemini service instance."""
    return gemini_service


def get_fitness_gemini_service() -> GeminiLLMService:
    """Get the fitness fine-tuned Gemini service instance."""
    return fitness_gemini_service