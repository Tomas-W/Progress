import os

from datetime import datetime
from typing import Any, Final
from upstash_redis import Redis

from utils.logger import logger


KEEP_LAST_N_ENTRIES: Final = 200
USERS_PREFIX: Final = "users_"
WEIGHTS_PREFIX: Final = "weights_"
REQUESTS_PREFIX: Final = "requests_"
WEIGHT_GUESSES_PREFIX: Final = "guess_weight_"


class Upstash:
    """Handles all data storage operations."""
    def __init__(self):
        self.redis: Redis = None
        self.users_memory: dict[str, str] = {}
        self.weights_memory: dict[str, float] = {}
        self.weight_guesses_memory: dict[str, tuple[str, float]] = {}
        self._init_redis()
        if self.redis is None:
            self.users_memory = {"test": "test", "test2": "test2"}
    
    def _init_redis(self) -> None:
        """Initializes Redis client if environment variables are available."""
        redis_url = os.getenv("UPSTASH_REDIS_REST_URL")
        redis_token = os.getenv("UPSTASH_REDIS_REST_TOKEN")
        
        if redis_url and redis_token:
            try:
                self.redis = Redis(url=redis_url, token=redis_token)
                logger.info("Connected to Upstash Redis")
            
            except Exception as e:
                logger.error(f"Failed to connect to Upstash Redis: {e}")
                self.redis = None
        else:
            logger.info("No Redis credentials found, using in-memory storage")
    
    def add_user(self, username: str, password: str) -> None:
        """Adds user to Redis or memory fallback"""
        if self.redis:
            self._add_user_to_redis(username, password)
        else:
            self._add_user_to_memory(username, password)
    
    def get_user(self, username: str) -> tuple[str, str] | tuple[None, None]:
        """Gets user from Redis or memory fallback"""
        if self.redis:
            return self._get_user_from_redis(username)
        else:
            return self._get_user_from_memory(username)
    
    def _get_user_from_redis(self, username: str) -> str | None:
        """Gets user from Redis"""
        try:
            result = self.redis.get(f"{USERS_PREFIX}{username}")
            return result
        
        except Exception as e:
            logger.error(f"Error fetching user from Redis: {e}")
            return self._get_user_from_memory(username)
    
    def _get_user_from_memory(self, username: str) -> str | None:
        """Gets users from memory storage"""
        try:
            return self.users_memory[username]
        
        except Exception as e:
            logger.error(f"Error fetching user from memory: {e}")
            return None
    
    def _add_user_to_redis(self, username: str, password: str) -> None:
        """Adds user to Redis"""
        try:
            self.redis.set(f"{USERS_PREFIX}{username}", password)
        
        except Exception as e:
            logger.error(f"Error adding user to Redis: {e}")
            self._add_user_to_memory(username, password)
    
    def _add_user_to_memory(self, username: str, password: str) -> None:
        """Adds user to memory storage"""
        self.users_memory[username] = password
    
    def add_weight(self, weight: float, date: str) -> None:
        """Adds weight guess to Redis"""
        if self.redis:
            self._add_weight_to_redis(weight, date)
        else:
            self._add_weight_to_memory(weight, date)
    
    def _add_weight_to_redis(self, weight: float, date: str) -> None:
        """Adds weight to Redis"""
        try:
            self.redis.set(f"{WEIGHTS_PREFIX}{date}", weight)
        
        except Exception as e:
            logger.error(f"Error adding weight to Redis: {e}")
    
    def _add_weight_to_memory(self, weight: float, date: str) -> None:
        """Adds weight to memory storage"""
        self.weights_memory[date] = weight
    
    def get_weight(self, date: str) -> float | None:
        """Gets weight from Redis or memory fallback"""
        if self.redis:
            return self._get_weight_from_redis(date)
        else:
            return self._get_weight_from_memory(date)
    
    def _get_weight_from_redis(self, date: str) -> float | None:
        """Gets weight from Redis"""
        try:
            result = self.redis.get(f"{WEIGHTS_PREFIX}{date}")
            return result
        
        except Exception as e:
            logger.error(f"Error fetching weight from Redis: {e}")
            return self._get_weight_from_memory(date)
    
    def _get_weight_from_memory(self, date: str) -> float | None:
        """Gets weight from memory storage"""
        try:
            return self.weights_memory[date]
        
        except Exception as e:
            logger.error(f"Error fetching weight from memory: {e}")
            return None
    
    def add_weight_guess(self, username: str, date: str, weight: float) -> None:
        """Adds weight guess to Redis"""
        if self.redis:
            self._add_weight_guess_to_redis(username, date, weight)
        else:
            self._add_weight_guess_to_memory(username, date, weight)
    
    def _add_weight_guess_to_redis(self, username: str, date: str, weight: float) -> None:
        """Adds weight guess to Redis"""
        try:
            self.redis.set(f"{WEIGHT_GUESSES_PREFIX}{username}", [date, weight])
        
        except Exception as e:
            logger.error(f"Error adding weight guess to Redis: {e}")
    
    def _add_weight_guess_to_memory(self, username: str, date: str, weight: float) -> None:
        """Adds weight guess to memory storage"""
        self.weight_guesses_memory[f"{username}"] = [date, weight]
    
    def get_weight_guess(self, username: str) -> tuple[str, float] | None:
        """Gets weight guess from Redis or memory fallback"""
        if self.redis:
            return self._get_weight_guess_from_redis(username)
        else:
            return self._get_weight_guess_from_memory(username)
    
    def _get_weight_guess_from_redis(self, username: str) -> float | None:
        """Gets weight guess from Redis"""
        try:
            result = self.redis.get(f"{WEIGHT_GUESSES_PREFIX}{username}")
            return result
        
        except Exception as e:
            logger.error(f"Error fetching weight guess from Redis: {e}")
            return None, None
        
    def _get_weight_guess_from_memory(self, username: str) -> tuple[str, float] | None:
        """Gets weight guess from memory storage"""
        try:
            return self.weight_guesses_memory[f"{username}"]
        
        except Exception as e:
            logger.error(f"Error fetching weight guess from memory: {e}")
            return None, None
    
    def _cleanup_old_redis_entries(self, key_prefix: str) -> None:
        """Cleans up old Redis entries"""
        try:
            keys = self.redis.keys(f"{key_prefix}*")
            if len(keys) > KEEP_LAST_N_ENTRIES:
                sorted_keys = sorted(keys)
                keys_to_delete = sorted_keys[:-KEEP_LAST_N_ENTRIES//2]
                removed_keys = self.redis.delete(*keys_to_delete)
                logger.info(f"Cleaned up {removed_keys} old Redis entries")
        
        except Exception as e:
            logger.error(f"Error during Redis cleanup: {e}")
    
    def get_connection_status(self) -> dict[str, Any]:
        """Gets current storage connection status"""
        return {
            "redis_connected": self.redis is not None,
            "memory_entries": len(self.requests_memory),
            "storage_type": "redis" if self.redis else "memory"
        }


upstash = Upstash()
