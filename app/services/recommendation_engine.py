from app.core.job_normalizer import JobNormalizer
from app.services.rag_service import RAGService
from app.services.llm_service import LLMService
from app.api.models import SkillRecommendationResponse, Skill, FrameworkSkills
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecommendationEngine:
    def __init__(self):
        self.normalizer = JobNormalizer()
        self.rag_service = RAGService()
        self.llm_service = LLMService()

    def get_recommendations(self, role: str, domain: str, industry: str): # type: ignore
        """Generate skill recommendations using O*NET and ESCO, with LLM-assigned per-skill proficiencies."""
        frameworks = ["O*NET", "ESCO"]
        framework_skills = []
        
        # Map domain to country for framework selection
        domain_to_country = {
            "USA": "USA",
            "US": "USA",
            "United States": "USA",
            "EU": "EU",
            "Europe": "EU",
            "European Union": "EU",
            "India": "India",
            "Singapore": "Singapore",
            "Australia": "Australia",
            "Canada": "Canada",
            "UK": "UK",
            "United Kingdom": "UK"
        }
        country = domain_to_country.get(domain, domain)
        logger.info(f"Processing recommendations for role: {role}, domain: {domain}, industry: {industry}")
        
        # Generate job description based on role, domain, and industry
        job_description_prompt = (
            f"Provide a detailed and professional job description for a {role} position in the {industry} industry, "
            f"specifically for the {domain} region/market. Include key responsibilities, typical work environment, "
            f"and what makes this role important in the {industry} sector. Keep it concise (3-4 sentences)."
        )
        job_description = self.llm_service.generate(job_description_prompt)
        logger.info(f"Generated job description for {role} in {industry}")

        for framework in frameworks:
            # Normalize job title
            normalized_title = self.normalizer.normalize(role, framework)
            logger.info(f"Normalized job title for {framework}: {role} -> {normalized_title}")

            # Get candidate skills from RAG
            query = f"Skills for {normalized_title} {role} role in {industry} industry in {framework}"
            rag_results = self.rag_service.query(query, framework, n_results=12)
            candidate_skills = [meta.get("skill", meta.get("name", "")) for meta in rag_results if "skill" in meta or "name" in meta]
            logger.info(f"RAG candidates for {framework}: {len(candidate_skills)} skills")

            # If insufficient RAG results, supplement with LLM-generated candidates
            if len(candidate_skills) < 6:
                logger.info(f"Supplementing RAG with LLM for {framework}")
                base_prompt = (
                    f"List 8-10 candidate skills for a {role} role in {industry} industry using {framework}. "
                    "Focus on core hard and soft skills. Output comma-separated names only."
                )
                llm_candidates_str = self.llm_service.generate(base_prompt)
                llm_candidates = self._parse_llm_skills(llm_candidates_str)
                candidate_skills.extend(llm_candidates)
                candidate_skills = list(set(candidate_skills))[:12]  # Dedupe and limit

            # LLM prompt for categorization and per-skill proficiency assignment
            skills_list_str = ", ".join(candidate_skills) # type: ignore
            llm_prompt = (
                f"For a {role} role in {industry} industry, take these {framework} candidate skills: {skills_list_str}. "
                "Categorize into hard (technical) and soft (interpersonal) skills. "
                "Assign realistic proficiency levels (Beginner, Intermediate, Advanced, Expert) per skill based on typical role requirements in the industry. "
                f"Consider the specific demands of {industry} industry for this {role} position. "
                "Limit to 8-10 hard and 2-4 soft. Output ONLY valid JSON: "
                "{{\"hard_skills\": [{\"name\": \"Skill Name\", \"proficiency\": \"Level\"}, ...], "
                "\"soft_skills\": [{\"name\": \"Skill Name\", \"proficiency\": \"Level\"}, ...]}}"
            )
            llm_response = self.llm_service.generate(llm_prompt)
            
            # Parse JSON from LLM response
            try:
                parsed = json.loads(llm_response.strip())
                hard_skills_data = parsed.get("hard_skills", [])
                soft_skills_data = parsed.get("soft_skills", [])
                logger.info(f"Parsed {len(hard_skills_data)} hard and {len(soft_skills_data)} soft skills for {framework}")
            except json.JSONDecodeError:
                logger.warning(f"JSON parse failed for {framework}, using fallback")
                # Fallback: simple list without category/proficiency (rare)
                fallback_skills = [{"name": skill, "proficiency": "Intermediate"} for skill in candidate_skills[:8]]
                hard_skills_data = fallback_skills[:6]  # Assume first as hard
                soft_skills_data = fallback_skills[6:] if len(fallback_skills) > 6 else []

            # Convert to Pydantic models with category
            hard_skills_models = [
                Skill(name=skill["name"], category="Hard", proficiency=skill.get("proficiency", "Intermediate"))
                for skill in hard_skills_data
            ]
            soft_skills_models = [
                Skill(name=skill["name"], category="Soft", proficiency=skill.get("proficiency", "Intermediate"))
                for skill in soft_skills_data
            ]

            framework_skills.append(FrameworkSkills(
                framework=framework,
                hard_skills=hard_skills_models,
                soft_skills=soft_skills_models
            ))

        return SkillRecommendationResponse(
            role=role,
            domain=domain,
            industry=industry,
            country=country,
            job_description=job_description,
            skills=framework_skills
        )

    def _parse_llm_skills(self, response: str) -> list:
        """Parse comma-separated skills from LLM."""
        import re
        response = re.sub(r'[^\w\s,]', '', response).strip()
        return [skill.strip() for skill in response.split(",") if skill.strip() and len(skill.strip()) > 2][:10]

    def get_job_description(self, job_title: str) -> str:
        """Generate job description using LLM."""
        prompt = f"Provide a detailed job description for a {job_title}."
        return self.llm_service.generate(prompt)


# from app.core.job_normalizer import JobNormalizer
# from app.core.skill_categorizer import SkillCategorizer
# from app.core.proficiency_mapper import ProficiencyMapper
# from app.services.rag_service import RAGService
# from app.services.llm_service import LLMService
# from app.api.models import SkillRecommendationResponse, Skill, FrameworkSkills
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class RecommendationEngine:
#     def __init__(self):
#         self.normalizer = JobNormalizer()
#         self.categorizer = SkillCategorizer()
#         self.proficiency_mapper = ProficiencyMapper()
#         self.rag_service = RAGService()
#         self.llm_service = LLMService()

#     def get_recommendations(self, job_title: str, country: str = None, proficiency: str = None):  # type: ignore
#         """Generate skill recommendations for a job title using O*NET and ESCO."""
#         frameworks = ["O*NET", "ESCO"]
#         framework_skills = []

#         for framework in frameworks:
#             # Normalize job title
#             normalized_title = self.normalizer.normalize(job_title, framework)
#             logger.info(f"Normalized job title for {framework}: {job_title} -> {normalized_title}")

#             # Query RAG for skills
#             query = f"Skills required for {normalized_title} in {framework}"
#             rag_results = self.rag_service.query(query, framework, n_results=15)
#             logger.info(f"RAG returned {len(rag_results)} skills for {framework}")

#             # Extract skills with descriptions
#             skills = [
#                 {"name": meta["skill"], "description": meta.get("description", meta["skill"])}
#                 for meta in rag_results if "skill" in meta
#             ]

#             # If no skills from RAG, fallback to LLM
#             if not skills:
#                 logger.warning(f"No skills from RAG for {framework}, falling back to LLM")
#                 proficiency_str = f" at {proficiency} level" if proficiency else ""
#                 prompt = (
#                     f"List 10 skills required for a {job_title} using {framework} framework{proficiency_str}. "
#                     "Focus on core hard skills and some soft skills related to {job_title} at the {proficiency or 'intermediate'} level. "
#                     "Format as a comma-separated list of skill names only (e.g., Python, Communication, SQL)."
#                 )
#                 llm_response = self.llm_service.generate(prompt)
#                 llm_skills = self._parse_llm_skills(llm_response)
#                 skills = [{"name": skill, "description": skill} for skill in llm_skills]

#             # Remove duplicates while preserving order
#             seen = set()
#             unique_skills = []
#             for skill in skills:
#                 if skill["name"] not in seen:
#                     seen.add(skill["name"])
#                     unique_skills.append(skill)
#             skills = unique_skills
#             logger.info(f"Total unique skills for {framework}: {len(skills)}")

#             # Categorize skills using LLM
#             hard_skills, soft_skills = self.categorizer.categorize(skills)

#             # Map proficiency, passing the overall proficiency
#             hard_skills = [self.proficiency_mapper.map_proficiency(skill, proficiency) for skill in hard_skills]
#             soft_skills = [self.proficiency_mapper.map_proficiency(skill, proficiency) for skill in soft_skills]

#             # Convert to Pydantic models
#             hard_skills = [Skill(**skill) for skill in hard_skills]
#             soft_skills = [Skill(**skill) for skill in soft_skills]

#             framework_skills.append(FrameworkSkills(
#                 framework=framework,
#                 hard_skills=hard_skills,
#                 soft_skills=soft_skills
#             ))

#         return SkillRecommendationResponse(
#             job_title=job_title,
#             country=country,
#             skills=framework_skills
#         )

#     def _parse_llm_skills(self, response: str) -> list:
#         """Parse LLM response to extract clean skill names."""
#         import re
#         response = re.sub(r'\*\*.*?\*\*|\n|\d+\.\s', '', response)
#         skills = [skill.strip() for skill in response.split(",") if skill.strip()]
#         return skills

#     def get_job_description(self, job_title: str) -> str:
#         """Generate job description using LLM."""
#         prompt = f"Provide a detailed job description for a {job_title}."
#         return self.llm_service.generate(prompt)
