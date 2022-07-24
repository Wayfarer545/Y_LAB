import os
from dotenv import load_dotenv
from pathlib import Path


VERSION: str = "1.0.0"

load_dotenv()

# JWT SETTINGS
JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
JWT_EXPIRE_TIME: int = 30

# Название проекта. Используется в Swagger-документации
PROJECT_NAME: str = os.getenv("PROJECT_NAME")

# Настройки Redis
REDIS_HOST: str = os.getenv("REDIS_HOST")
REDIS_PORT: int = int(os.getenv("REDIS_PORT"))
CACHE_EXPIRE_IN_SECONDS: int = 60 * 5  # 5 минут

# Настройки Postgres
POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT"))
POSTGRES_DB: str = os.getenv("POSTGRES_DB")
POSTGRES_USER: str = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")

DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent
