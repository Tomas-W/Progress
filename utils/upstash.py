import os

from typing import Final
from upstash_redis import Redis

from utils.logger import logger


USERS_PREFIX: Final = "users_"
WEIGHTS_PREFIX: Final = "weights_"
WEIGHT_GUESSES_PREFIX: Final = "guess_weight_"


class Upstash:
    """Handles all data storage operations."""
    def __init__(self):
        self.redis: Redis | None = None
        self.users_memory: dict[str, str] = {}           # username: password
        self.weights_memory: dict[str, float] = {}       # date: weight
        self.weight_guesses_memory: dict[str, str] = {}  # username: date|weight
        self._init_redis()
        if self.redis is None:
            self._add_user_to_memory(os.getenv("LOCAL_USERNAME"), os.getenv("LOCAL_PASSWORD"))

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
        """Adds user to Redis or memory fallback."""
        if self.redis:
            return self._add_user_to_redis(username, password)
        else:
            self._add_user_to_memory(username, password)
            return False
    
    def _add_user_to_redis(self, username: str, password: str) -> None:
        """Adds user to Redis."""
        try:
            self.redis.set(f"{USERS_PREFIX}{username}", password)
            return True
        
        except Exception as e:
            logger.error(f"Error adding user to Redis: {e}")
            self._add_user_to_memory(username, password)
            return False
    
    def get_user(self, username: str) -> tuple[str, str] | tuple[None, None]:
        """Gets user from Redis or memory fallback."""
        if self.redis:
            return self._get_user_from_redis(username)
        else:
            return self._get_user_from_memory(username)
    
    def _get_user_from_redis(self, username: str) -> str | None:
        """Gets user from Redis."""
        try:
            result = self.redis.get(f"{USERS_PREFIX}{username}")
            return result
        
        except Exception as e:
            logger.error(f"Error fetching user from Redis: {e}")
            return self._get_user_from_memory(username)
    
    def add_weight(self, weight: float, date: str) -> None:
        """Adds weight to Redis or memory fallback."""
        if self.redis:
            self._add_weight_to_redis(weight, date)
        else:
            self._add_weight_to_memory(weight, date)
    
    def _add_weight_to_redis(self, weight: float, date: str) -> None:
        """Adds weight to Redis."""
        try:
            self.redis.set(f"{WEIGHTS_PREFIX}{date}", weight)
        
        except Exception as e:
            logger.error(f"Error adding weight to Redis: {e}")
            self._add_weight_to_memory(weight, date)

    def get_weight(self, date: str) -> float | None:
        """Gets weight from Redis or memory fallback."""
        if self.redis:
            return self._get_weight_from_redis(date)
        else:
            return self._get_weight_from_memory(date)
    
    def _get_weight_from_redis(self, date: str) -> float | None:
        """Gets weight from Redis."""
        try:
            result = self.redis.get(f"{WEIGHTS_PREFIX}{date}")
            return result
        
        except Exception as e:
            logger.error(f"Error fetching weight from Redis: {e}")
            return self._get_weight_from_memory(date)
    
    def add_weight_guess(self, username: str, date: str, weight: float) -> None:
        """Adds weight guess to Redis or memory fallback."""
        if self.redis:
            self._add_weight_guess_to_redis(username, date, weight)
        else:
            self._add_weight_guess_to_memory(username, date, weight)
    
    def _add_weight_guess_to_redis(self, username: str, date: str, weight: float) -> None:
        """Adds weight guess to Redis."""
        try:
            data = f"{date}|{weight}"
            self.redis.set(f"{WEIGHT_GUESSES_PREFIX}{username}", data)
        except Exception as e:
            logger.error(f"Error adding weight guess to Redis: {e}")
            self._add_weight_guess_to_memory(username, date, weight)
    
    def get_weight_guess(self, username: str) -> tuple[str | None, float | None]:
        """Gets weight guess from Redis or memory fallback. Returns tuple of (date, weight)"""
        if self.redis:
            return self._get_weight_guess_from_redis(username)
        else:
            return self._get_weight_guess_from_memory(username)
    
    def _get_weight_guess_from_redis(self, username: str) -> tuple[str | None, float | None]:
        """Gets weight guess from Redis"""
        try:
            result = self.redis.get(f"{WEIGHT_GUESSES_PREFIX}{username}")
            if result is None:
                return None, None
            
            date_str, weight_str = result.split("|")
            return date_str, float(weight_str)
        
        except Exception as e:
            logger.error(f"Error fetching weight guess from Redis: {e}")
            return None, None
    
    def _get_user_from_memory(self, username: str) -> str | None:
        """Gets users from memory storage"""
        try:
            return self.users_memory[username]
        
        except Exception as e:
            logger.error(f"Error fetching user from memory: {e}")
            return None
    
    def _add_user_to_memory(self, username: str, password: str) -> None:
        """Adds user to memory storage"""
        self.users_memory[username] = password
    
    def _get_weight_from_memory(self, date: str) -> float | None:
        """Gets weight from memory storage"""
        try:
            return self.weights_memory[date]
        
        except Exception as e:
            logger.error(f"Error fetching weight from memory: {e}")
            return None
    
    def _add_weight_to_memory(self, weight: float, date: str) -> None:
        """Adds weight to memory storage"""
        self.weights_memory[date] = weight
    
    def _add_weight_guess_to_memory(self, username: str, date: str, weight: float) -> None:
        """Adds weight guess to memory storage"""
        self.weight_guesses_memory[username] = f"{date}|{weight}"
    
    def _get_weight_guess_from_memory(self, username: str) -> tuple[str | None, float | None]:
        """Gets weight guess from memory storage"""
        try:
            result = self.weight_guesses_memory.get(username)
            if result is None:
                return None, None
            
            date_str, weight_str = result.split("|")
            return date_str, float(weight_str)
        
        except Exception as e:
            logger.error(f"Error fetching weight guess from memory: {e}")
            return None, None


upstash = Upstash()
