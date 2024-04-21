from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    GCP_PROJECT: str
    GCP_TOPIC: str
    GCP_SUB: str

    PUBLISHER_CRED_LOCATION: str = ""
    SUBSCRIBER_CRED_LOCATION: str = ""
    


class DevSettings(Settings):
    model_config = SettingsConfigDict(env_file="config/dev.env", extra="ignore")


class ProdSettings(Settings):
    # it reads from envvar!
    ...


def get_config() -> Settings:
    if os.getenv("ENV"):  # there is DOMAIN name provided
        config = ProdSettings()
    else:
        config = DevSettings()

    return config


if __name__ == "__main__":
    configurations = get_config()
    print(configurations)


