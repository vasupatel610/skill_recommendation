from pydantic import BaseModel
from typing import Optional, List, Dict

class Skill(BaseModel):
    name: str
    category: str  # Hard or Soft
    proficiency: str  # Beginner, Intermediate, Advanced, Expert

class FrameworkSkills(BaseModel):
    framework: str
    hard_skills: List[Skill]
    soft_skills: List[Skill]

class JobRequest(BaseModel):
    job_title: str
    country: Optional[str] = None

class SkillRecommendationResponse(BaseModel):
    job_title: str
    country: Optional[str]
    skills: List[FrameworkSkills]

class JobDescriptionResponse(BaseModel):
    job_title: str
    description: str


# from pydantic import BaseModel
# from typing import Optional, List, Dict

# class Skill(BaseModel):
#     name: str
#     category: str  # Hard or Soft
#     proficiency: str  # Beginner, Intermediate, Advanced, Expert

# class JobRequest(BaseModel):
#     job_title: str
#     country: Optional[str] = None
#     framework: Optional[str] = "O*NET"  # Default to O*NET

# class SkillRecommendationResponse(BaseModel):
#     job_title: str
#     country: Optional[str]
#     framework: str
#     hard_skills: List[Skill]
#     soft_skills: List[Skill]

# class JobDescriptionResponse(BaseModel):
#     job_title: str
#     description: str