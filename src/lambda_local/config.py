import os

from dataclasses import dataclass

from dotenv import load_dotenv

class ConfigError(Exception):
    pass


@dataclass(init=False)
class Config:
    functions_path_prefix: str

    def __new__(cls):
        load_dotenv()
        return super().__new__(cls)

    def __getattr__(self, __name: str) -> str:
      try:
        return os.environ[__name.upper()]
      except KeyError:
        raise ConfigError(f"Environment variable {__name.upper()} is not set") from None

_config = Config()

def get_config():
    return _config

