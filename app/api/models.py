from pydantic import BaseModel
from typing import Optional, List

class Skill(BaseModel):
    name: str
    category: str  # Hard or Soft
    proficiency: str  # Beginner, Intermediate, Advanced, Expert (or as requested, e.g., Begginer)

class FrameworkSkills(BaseModel):
    framework: str
    hard_skills: List[Skill]
    soft_skills: List[Skill]

class JobRequest(BaseModel):
    role: str
    domain: str
    industry: str

class SkillRecommendationResponse(BaseModel):
    role: str
    domain: str
    industry: str
    country: str
    job_description: str
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

# class FrameworkSkills(BaseModel):
#     framework: str
#     hard_skills: List[Skill]
#     soft_skills: List[Skill]

# class JobRequest(BaseModel):
#     job_title: str
#     country: Optional[str] = None
#     proficiency: Optional[str] = None  # New field for overall proficiency level

# class SkillRecommendationResponse(BaseModel):
#     job_title: str
#     country: Optional[str]
#     skills: List[FrameworkSkills]

# class JobDescriptionResponse(BaseModel):
#     job_title: str
#     description: str