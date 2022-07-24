import alembic
import redis
import uvicorn
from fastapi import FastAPI

from src.api.v1.resources import posts, users
from src.core import config
from src.db import cache, redis_cache


app = FastAPI(
    title=config.PROJECT_NAME,
    version=config.VERSION,
    docs_url="/api/openapi",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    )



@app.get("/")
def root():
    return {"service": config.PROJECT_NAME, "version": config.VERSION}


@app.on_event("startup")
def startup():
    """Подключаемся к базам при старте сервера"""
    cache.active_tokens = redis_cache.UserCache(
        cache_instance=redis.Redis(
            db=2,
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            max_connections=10
        )
    )
    cache.blocked_tokens = redis_cache.UserCache(
        cache_instance=redis.Redis(
            db=1,
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            max_connections=10
        )
    )
    cache.posts_cache = redis_cache.PostCache(
        cache_instance=redis.Redis(
            db=0,
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            max_connections=10,
        )
    )

@app.on_event("shutdown")
def shutdown():
    """Отключаемся от баз при выключении сервера"""
    cache.posts_cache.close()
    cache.active_tokens.close()
    cache.blocked_tokens.close()


# Подключаем роутеры
app.include_router(router=posts.router, prefix="/api/v1/posts")
app.include_router(router=users.router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
