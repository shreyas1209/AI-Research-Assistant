import asyncio
from functools import wraps
from typing import Tuple, TypeVar, Callable, Any
from backend.utils.logger import get_logger

logger = get_logger(__name__)

# Type variable for the decorated function's return type
T = TypeVar('T')

def async_retry(
    retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Exception, ...] = (Exception,)
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator for async retry logic.
    
    Args:
        retries: Number of retries before giving up
        delay: Initial delay between retries in seconds
        backoff: Multiplier applied to delay between retries
        exceptions: Tuple of exceptions to catch and retry on
        
    Returns:
        Decorated async function with retry logic
        
    Example:
        @async_retry(retries=3, delay=1.0, backoff=2.0)
        async def my_function():
            # Your async code here
            pass
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None
            current_delay = delay
            
            for attempt in range(retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == retries:
                        logger.error(f"Failed after {retries} retries: {str(e)}")
                        raise
                    
                    logger.warning(
                        f"Attempt {attempt + 1}/{retries} failed: {str(e)}. "
                        f"Retrying in {current_delay:.1f} seconds..."
                    )
                    
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff
            
            raise last_exception
        return wrapper
    return decorator
