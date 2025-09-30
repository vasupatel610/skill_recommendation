from app.core.job_normalizer import JobNormalizer
from app.core.skill_categorizer import SkillCategorizer
from app.core.proficiency_mapper import ProficiencyMapper
from app.services.rag_service import RAGService
from app.services.llm_service import LLMService
from app.api.models import SkillRecommendationResponse, Skill, FrameworkSkills
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecommendationEngine:
    def __init__(self):
        self.normalizer = JobNormalizer()
        self.categorizer = SkillCategorizer()
        self.proficiency_mapper = ProficiencyMapper()
        self.rag_service = RAGService()
        self.llm_service = LLMService()

    def get_recommendations(self, job_title: str, country: str = None): # type: ignore
        """Generate skill recommendations for a job title using O*NET and ESCO."""
        frameworks = ["O*NET", "ESCO"]
        framework_skills = []

        for framework in frameworks:
            # Normalize job title
            normalized_title = self.normalizer.normalize(job_title, framework)
            logger.info(f"Normalized job title for {framework}: {job_title} -> {normalized_title}")

            # Query RAG for skills
            query = f"Skills required for {normalized_title} in {framework}"
            rag_results = self.rag_service.query(query, framework, n_results=15)
            logger.info(f"RAG returned {len(rag_results)} skills for {framework}")

            # Extract skills with descriptions
            skills = [
                {"name": meta["skill"], "description": meta.get("description", meta["skill"])}
                for meta in rag_results if "skill" in meta
            ]

            # If no skills from RAG, fallback to LLM
            if not skills:
                logger.warning(f"No skills from RAG for {framework}, falling back to LLM")
                prompt = (
                    f"List 10 skills required for a {job_title} using {framework} framework. skills has to be core skills and aome soft skills related to {job_title}. "
                    "Format as a comma-separated list of skill names only (e.g., Python, Communication, SQL)."
                )
                llm_response = self.llm_service.generate(prompt)
                llm_skills = self._parse_llm_skills(llm_response)
                skills = [{"name": skill, "description": skill} for skill in llm_skills]

            # Remove duplicates while preserving order
            seen = set()
            unique_skills = []
            for skill in skills:
                if skill["name"] not in seen:
                    seen.add(skill["name"])
                    unique_skills.append(skill)
            skills = unique_skills
            logger.info(f"Total unique skills for {framework}: {len(skills)}")

            # Categorize skills using LLM
            hard_skills, soft_skills = self.categorizer.categorize(skills)

            # Map proficiency
            hard_skills = [self.proficiency_mapper.map_proficiency(skill) for skill in hard_skills]
            soft_skills = [self.proficiency_mapper.map_proficiency(skill) for skill in soft_skills]

            # Convert to Pydantic models
            hard_skills = [Skill(**skill) for skill in hard_skills]
            soft_skills = [Skill(**skill) for skill in soft_skills]

            framework_skills.append(FrameworkSkills(
                framework=framework,
                hard_skills=hard_skills,
                soft_skills=soft_skills
            ))

        return SkillRecommendationResponse(
            job_title=job_title,
            country=country,
            skills=framework_skills
        )

    def _parse_llm_skills(self, response: str) -> list:
        """Parse LLM response to extract clean skill names."""
        import re
        response = re.sub(r'\*\*.*?\*\*|\n|\d+\.\s', '', response)
        skills = [skill.strip() for skill in response.split(",") if skill.strip()]
        return skills

    def get_job_description(self, job_title: str) -> str:
        """Generate job description using LLM."""
        prompt = f"Provide a detailed job description for a {job_title}."
        return self.llm_service.generate(prompt)


# from app.core.job_normalizer import JobNormalizer
# from app.core.skill_categorizer import SkillCategorizer
# from app.core.proficiency_mapper import ProficiencyMapper
# from app.services.rag_service import RAGService
# from app.services.llm_service import LLMService
# from app.api.models import SkillRecommendationResponse, Skill
# import re

# class RecommendationEngine:
#     def __init__(self):
#         self.normalizer = JobNormalizer()
#         self.categorizer = SkillCategorizer()
#         self.proficiency_mapper = ProficiencyMapper()
#         self.rag_service = RAGService()
#         self.llm_service = LLMService()

#     def get_recommendations(self, job_title: str, country: str = None, framework: str = "O*NET"): # type: ignore
#         """Generate skill recommendations for a job title."""
#         # Normalize job title
#         normalized_title = self.normalizer.normalize(job_title, framework)

#         # Query RAG for skills
#         query = f"Skills required for {normalized_title} in {framework}"
#         rag_results = self.rag_service.query(query, framework, n_results=15)

#         # Extract skills with descriptions
#         skills = [
#             {"name": meta["skill"], "description": meta.get("description", meta["skill"])}
#             for meta in rag_results if "skill" in meta
#         ]

#         # If insufficient skills, fallback to LLM
#         if len(skills) < 5:
#             prompt = (
#                 f"List 10 skills required for a {job_title} using {framework} framework. "
#                 "Format as a comma-separated list of skill names only (e.g., Python, Communication, SQL)."
#             )
#             llm_response = self.llm_service.generate(prompt)
#             llm_skills = self._parse_llm_skills(llm_response)
#             # Add LLM skills with generic descriptions
#             skills.extend([
#                 {"name": skill, "description": skill} for skill in llm_skills
#                 if skill not in [s["name"] for s in skills]
#             ])

#         # Remove duplicates while preserving order
#         seen = set()
#         unique_skills = []
#         for skill in skills:
#             if skill["name"] not in seen:
#                 seen.add(skill["name"])
#                 unique_skills.append(skill)
#         skills = unique_skills

#         # Categorize skills using LLM
#         hard_skills, soft_skills = self.categorizer.categorize(skills)

#         # Map proficiency
#         hard_skills = [self.proficiency_mapper.map_proficiency(skill) for skill in hard_skills]
#         soft_skills = [self.proficiency_mapper.map_proficiency(skill) for skill in soft_skills]

#         # Convert to Pydantic models
#         hard_skills = [Skill(**skill) for skill in hard_skills]
#         soft_skills = [Skill(**skill) for skill in soft_skills]

#         return SkillRecommendationResponse(
#             job_title=job_title,
#             country=country,
#             framework=framework,
#             hard_skills=hard_skills,
#             soft_skills=soft_skills
#         )

#     def _parse_llm_skills(self, response: str) -> list:
#         """Parse LLM response to extract clean skill names."""
#         response = re.sub(r'\*\*.*?\*\*|\n|\d+\.\s', '', response)
#         skills = [skill.strip() for skill in response.split(",") if skill.strip()]
#         return skills

#     def get_job_description(self, job_title: str) -> str:
#         """Generate job description using LLM."""
#         prompt = f"Provide a list of required hard and soft skills for a {job_title}."
#         return self.llm_service.generate(prompt)


