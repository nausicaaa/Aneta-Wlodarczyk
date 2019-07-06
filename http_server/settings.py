from sanic_envconfig import EnvConfig


class Settings(EnvConfig):
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8080
    DB_URL: str = 'postgresql://postgres:postgres@localhost/postgres:8000'
    REQUEST_MAX_SIZE = 1000000
