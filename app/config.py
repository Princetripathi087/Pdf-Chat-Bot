from pydantic import BaseSettings
#from pydantic_settings import BaseSettings #change here
import dotenv

dotenv.load_dotenv('./local.env')

class Settings(BaseSettings):
    DATABASE_URL: str
    MONGO_INITDB_DATABASE: str
    MONGO_INITDB_VEC_DATABASE: str
    DATABASE_URL_VECTOR: str

    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    REFRESH_TOKEN_EXPIRES_IN: int
    ACCESS_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    CLIENT_ORIGIN: str
    API_KEY: str

    class Config:
        extra = "allow"
        env_file = './local.env'


settings = Settings()

