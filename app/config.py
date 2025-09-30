import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = "llama-3.3-70b-versatile"
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "/home/artisans15/projects/skill_recommendation/data/vector_db")
    ONET_DATA_PATH = os.getenv("ONET_DATA_PATH", "/home/artisans15/projects/skill_recommendation/data/framworks/onet/db_30_0_text")
    ESCO_DATA_PATH = os.getenv("ESCO_DATA_PATH", "/home/artisans15/projects/skill_recommendation/data/framworks/esco/ESCO dataset - v1.2.0 - classification - en - csv")