import os
from dotenv import load_dotenv
import json

class Config:
    _instance = None 

    def __new__(cls, env=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialize(env)
        return cls._instance

    def initialize(self, env=None):
        self.env = env 
        self.load_env_file()
        self.load_config_variables()

    def load_env_file(self):
        env_files = {
            "dev": ".env.dev",
            "prod": ".env.prod",
        }
        env_file = env_files.get(self.env)

        if not env_file:
            raise ValueError(f"Invalid environment '{self.env}'. Choose from {list(env_files.keys())}")

        if not os.path.exists(env_file):
            raise FileNotFoundError(f"Environment file '{env_file}' not found!")

        load_dotenv(env_file)

    def load_config_variables(self):
        self.variables = {
            "S3_HOST": os.getenv("S3_HOST"),
            "S3_ACCESS_KEY": os.getenv("S3_ACCESS_KEY"),
            "S3_SECRET_KEY": os.getenv("S3_SECRET_KEY"),
            "S3_BUCKET_DOCUMENTS": os.getenv("S3_BUCKET_DOCUMENTS"),
            "S3_BUCKET_CHUNKS": os.getenv("S3_BUCKET_CHUNKS"),
            "SECURE_S3_CONNECTION": json.loads(os.getenv("SECURE_S3_CONNECTION").lower()),
        }

    def get(self, key, default=None):
        return self.variables.get(key, default)

    def get_env(self):
        return self.env

config = Config(env="dev") 


