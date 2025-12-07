from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Tuple
from datetime import datetime, timedelta
import asyncio
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class RateLimiter(BaseHTTPMiddleware):
    """
    Rate limiting middleware to prevent API abuse
    
    Implements a simple token bucket algorithm with sliding window
    """
    
    def __init__(
        self,
        app,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
        cleanup_interval: int = 300  # 5 minutes
    ):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        
        # Storage: {client_id: [(timestamp, count), ...]}
        self.minute_requests: Dict[str, list] = defaultdict(list)
        self.hour_requests: Dict[str, list] = defaultdict(list)
        
        # Start cleanup task
        self.cleanup_interval = cleanup_interval
        asyncio.create_task(self._cleanup_old_requests())
    
    def _get_client_id(self, request: Request) -> str:
        """
        Get unique client identifier
        
        Uses user_id if authenticated, otherwise IP address
        """
        # Try to get user ID from request state (set by auth middleware)
        if hasattr(request.state, "user") and request.state.user:
            return f"user_{request.state.user.id}"
        
        # Fall back to IP address
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        client_host = request.client.host if request.client else "unknown"
        return f"ip_{client_host}"
    
    def _check_rate_limit(
        self,
        client_id: str,
        requests_dict: Dict[str, list],
        limit: int,
        window: timedelta
    ) -> Tuple[bool, int]:
        """
        Check if rate limit is exceeded
        
        Returns:
            Tuple of (is_allowed, remaining_requests)
        """
        now = datetime.utcnow()
        cutoff_time = now - window
        
        # Get client's request history
        requests = requests_dict[client_id]
        
        # Remove old requests outside the window
        requests_dict[client_id] = [
            req_time for req_time in requests
            if req_time > cutoff_time
        ]
        
        current_count = len(requests_dict[client_id])
        
        # Check if limit exceeded
        if current_count >= limit:
            return False, 0
        
        # Add current request
        requests_dict[client_id].append(now)
        
        remaining = limit - current_count - 1
        return True, remaining
    
    async def dispatch(self, request: Request, call_next):
        """Process request through rate limiter"""
        
        # Skip rate limiting for health check and docs
        if request.url.path in ["/health", "/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)
        
        client_id = self._get_client_id(request)
        
        # Check minute limit
        minute_allowed, minute_remaining = self._check_rate_limit(
            client_id,
            self.minute_requests,
            self.requests_per_minute,
            timedelta(minutes=1)
        )
        
        if not minute_allowed:
            logger.warning(
                f"Rate limit exceeded (minute): {client_id} "
                f"| Path: {request.url.path}"
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded: Maximum {self.requests_per_minute} requests per minute",
                headers={"Retry-After": "60"}
            )
        
        # Check hour limit
        hour_allowed, hour_remaining = self._check_rate_limit(
            client_id,
            self.hour_requests,
            self.requests_per_hour,
            timedelta(hours=1)
        )
        
        if not hour_allowed:
            logger.warning(
                f"Rate limit exceeded (hour): {client_id} "
                f"| Path: {request.url.path}"
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded: Maximum {self.requests_per_hour} requests per hour",
                headers={"Retry-After": "3600"}
            )
        
        # Add rate limit headers to response
        response = await call_next(request)
        response.headers["X-RateLimit-Limit-Minute"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining-Minute"] = str(minute_remaining)
        response.headers["X-RateLimit-Limit-Hour"] = str(self.requests_per_hour)
        response.headers["X-RateLimit-Remaining-Hour"] = str(hour_remaining)
        
        return response
    
    async def _cleanup_old_requests(self):
        """Periodic cleanup of old request records"""
        while True:
            await asyncio.sleep(self.cleanup_interval)
            
            try:
                now = datetime.utcnow()
                cutoff_minute = now - timedelta(minutes=2)  # Keep 2 minutes of history
                cutoff_hour = now - timedelta(hours=2)  # Keep 2 hours of history
                
                # Cleanup minute requests
                for client_id in list(self.minute_requests.keys()):
                    self.minute_requests[client_id] = [
                        req_time for req_time in self.minute_requests[client_id]
                        if req_time > cutoff_minute
                    ]
                    if not self.minute_requests[client_id]:
                        del self.minute_requests[client_id]
                
                # Cleanup hour requests
                for client_id in list(self.hour_requests.keys()):
                    self.hour_requests[client_id] = [
                        req_time for req_time in self.hour_requests[client_id]
                        if req_time > cutoff_hour
                    ]
                    if not self.hour_requests[client_id]:
                        del self.hour_requests[client_id]
                
                logger.debug(
                    f"Rate limiter cleanup completed. "
                    f"Active clients: {len(self.minute_requests)}"
                )
                
            except Exception as e:
                logger.error(f"Error in rate limiter cleanup: {str(e)}")