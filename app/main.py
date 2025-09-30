from fastapi import FastAPI
from app.api.routes import router
from app.config import Config
import uvicorn

app = FastAPI(title="Skill-360-skill Recommendation")

# Include API routes
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)