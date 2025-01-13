from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config: SettingsConfigDict(env_file=".env", encoding="utf-8")
    kafka_broker_address: str
    kafka_topic: str


config = Config()
