from fastapi import APIRouter, HTTPException
from app.api.models import JobRequest, SkillRecommendationResponse, JobDescriptionResponse
from app.services.recommendation_engine import RecommendationEngine

router = APIRouter()

@router.post("/recommend-skills", response_model=SkillRecommendationResponse)
async def recommend_skills(request: JobRequest):
    try:
        engine = RecommendationEngine()
        recommendation = engine.get_recommendations(
            role=request.role,
            domain=request.domain,
            industry=request.industry
        )
        return recommendation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/job-description/{job_title}", response_model=JobDescriptionResponse)
async def get_job_description(job_title: str):
    try:
        engine = RecommendationEngine()
        description = engine.get_job_description(job_title)
        return JobDescriptionResponse(job_title=job_title, description=description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# from fastapi import APIRouter, HTTPException
# from app.api.models import JobRequest, SkillRecommendationResponse, JobDescriptionResponse
# from app.services.recommendation_engine import RecommendationEngine

# router = APIRouter()

# @router.post("/recommend-skills", response_model=SkillRecommendationResponse)
# async def recommend_skills(request: JobRequest):
#     try:
#         engine = RecommendationEngine()
#         recommendation = engine.get_recommendations(
#             job_title=request.job_title,
#             country=request.country, # type: ignore
#             proficiency=request.proficiency if request.proficiency is not None else ""
#         )
#         return recommendation
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/job-description/{job_title}", response_model=JobDescriptionResponse)
# async def get_job_description(job_title: str):
#     try:
#         engine = RecommendationEngine()
#         description = engine.get_job_description(job_title)
#         return JobDescriptionResponse(job_title=job_title, description=description)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
