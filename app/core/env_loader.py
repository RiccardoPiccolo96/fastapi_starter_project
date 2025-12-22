from pathlib import Path
import os
from dotenv import load_dotenv

def load_env():
    env = os.getenv("ENV", "dev")
    env_file = Path(f".env.{env.lower()}")
    
    if not env_file.exists():
        env_file = Path(".env")
    
    if env_file.exists():
        load_dotenv(env_file)
    
    return env