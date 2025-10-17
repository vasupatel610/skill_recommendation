class ProficiencyMapper:
    def map_proficiency(self, skill: dict, overall_proficiency: str = None) -> dict: # type: ignore
        """Deprecated: LLM now assigns per-skill proficiencies directly."""
        # No-op; return as-is
        return skill


# class ProficiencyMapper:
#     def map_proficiency(self, skill: dict, overall_proficiency: str = None) -> dict: # type: ignore
#         """Map proficiency levels to skills."""
#         # Use framework-specific proficiency data if available, otherwise set to overall_proficiency or default
#         skill["proficiency"] = overall_proficiency or skill.get("proficiency", "Intermediate")
#         return skill
