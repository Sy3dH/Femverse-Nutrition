import logging
from services.ai_service.config.constants import DEFAULT_CACHE_TTL
from datetime import datetime, timezone
from typing import Optional

from google.genai import types

logger = logging.getLogger("celery")

class GeminiCacheRegistry:
    def __init__(self, client, model: str):

        self._client = client
        self._model = model
        self._registry: dict[str, str] = {}
        self._load_existing_caches()

    def _load_existing_caches(self) -> None:
        try:
            now = datetime.now(timezone.utc)
            loaded = 0
            for cache in self._client.caches.list():
                display_name = getattr(cache, "display_name", None)
                expire_time = getattr(cache, "expire_time", None)

                if not display_name or not cache.name:
                    continue

                # Skip already-expired caches
                if expire_time and expire_time <= now:
                    logger.info(f"[CacheRegistry] Skipping expired cache: {display_name}")
                    continue

                self._registry[display_name] = cache.name
                loaded += 1
                logger.info(
                    f"[CacheRegistry] Loaded existing cache: "
                    f"display_name={display_name}, name={cache.name}, expires={expire_time}"
                )

            logger.info(f"[CacheRegistry] Hydrated {loaded} cache(s) from Gemini servers.")

        except Exception as e:
            logger.warning(f"[CacheRegistry] Failed to load existing caches: {e}")

    def _create_cache(
        self,
        display_name: str,
        system_instruction: str,
        ttl: str = DEFAULT_CACHE_TTL,
    ) -> Optional[str]:

        try:
            cache = self._client.caches.create(
                model=self._model,
                config=types.CreateCachedContentConfig(
                    system_instruction=system_instruction,
                    display_name=display_name,
                    ttl=ttl,
                ),
            )
            self._registry[display_name] = cache.name
            logger.info(
                f"[CacheRegistry] Created new cache: "
                f"display_name={display_name}, name={cache.name}, ttl={ttl}"
            )
            return cache.name

        except Exception as e:
            logger.error(f"[CacheRegistry] Failed to create cache for '{display_name}': {e}")
            return None

    def get_or_create(
        self,
        display_name: str,
        system_instruction: str,
        ttl: str = DEFAULT_CACHE_TTL,
    ) -> Optional[str]:

        if display_name in self._registry:
            logger.debug(f"[CacheRegistry] Cache hit for '{display_name}'")
            return self._registry[display_name]

        logger.info(f"[CacheRegistry] Cache miss for '{display_name}' — creating.")
        return self._create_cache(display_name, system_instruction, ttl)

    def invalidate(self, display_name: str) -> None:

        cache_name = self._registry.pop(display_name, None)
        if not cache_name:
            logger.warning(f"[CacheRegistry] invalidate() called for unknown key: '{display_name}'")
            return

        try:
            self._client.caches.delete(name=cache_name)
            logger.info(f"[CacheRegistry] Deleted cache: display_name={display_name}, name={cache_name}")
        except Exception as e:
            logger.error(f"[CacheRegistry] Failed to delete cache '{cache_name}': {e}")

    def refresh_ttl(self, display_name: str, ttl: str = DEFAULT_CACHE_TTL) -> None:

        cache_name = self._registry.get(display_name)
        if not cache_name:
            logger.warning(f"[CacheRegistry] refresh_ttl() called for unknown key: '{display_name}'")
            return

        try:
            self._client.caches.update(
                name=cache_name,
                config=types.UpdateCachedContentConfig(ttl=ttl),
            )
            logger.info(f"[CacheRegistry] Refreshed TTL for '{display_name}' to {ttl}")
        except Exception as e:
            logger.error(f"[CacheRegistry] Failed to refresh TTL for '{cache_name}': {e}")

    def list_cached(self) -> dict[str, str]:

        return dict(self._registry)

if __name__ == "__main__":
    GeminiCacheRegistry()