from app.services.llm_service import LLMService

class SkillCategorizer:
    def __init__(self):
        self.llm_service = LLMService()

    def categorize(self, skills: list) -> tuple:
        """Categorize skills into hard and soft skills using LLM."""
        hard_skills = []
        soft_skills = []
        for skill in skills:
            skill_name = skill.get("name", "")
            skill_desc = skill.get("description", skill_name)
            if not skill_name:
                continue
            # Clean skill name
            skill_name_clean = self._clean_skill_name(skill_name)
            if not skill_name_clean:
                continue
            # Use LLM to determine category
            category = self._determine_category(skill_name_clean, skill_desc)
            proficiency = self._assign_proficiency(skill_name_clean)
            skill_obj = {"name": skill_name_clean, "category": category, "proficiency": proficiency}
            if category == "Hard":
                hard_skills.append(skill_obj)
            else:
                soft_skills.append(skill_obj)
        return hard_skills, soft_skills

    def _clean_skill_name(self, skill: str) -> str:
        """Clean skill name by removing unwanted prefixes and suffixes."""
        unwanted_prefixes = ["such as ", "to ", "and ", "or "]
        for prefix in unwanted_prefixes:
            if skill.lower().startswith(prefix):
                skill = skill[len(prefix):]
        skill = skill.split(",")[0].split(":")[0].strip()
        if len(skill.split()) > 5:
            return ""
        return skill

    def _determine_category(self, skill_name: str, skill_desc: str) -> str:
        """Use LLM to determine if a skill is hard or soft."""
        prompt = (
            f"Given the skill '{skill_name}' with description: '{skill_desc}', "
            "determine if it is a hard skill (technical, job-specific) or a soft skill "
            "(interpersonal, behavioral). Respond with only 'Hard' or 'Soft'."
        )
        response = self.llm_service.generate(prompt)
        return response.strip() if response.strip() in ["Hard", "Soft"] else "Soft"  # Default to Soft if unclear

    def _assign_proficiency(self, skill: str) -> str:
        """Assign proficiency level (placeholder logic)."""
        # Replace with framework-specific proficiency data if available
        if any(kw in skill.lower() for kw in ["machine learning", "python", "sql"]):
            return "Advanced"
        elif any(kw in skill.lower() for kw in ["basic", "beginner"]):
            return "Beginner"
        return "Intermediate"