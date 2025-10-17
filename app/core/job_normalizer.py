class JobNormalizer:
    def __init__(self):
        # Placeholder for ISCO or framework mappings
        self.mappings = {
            "data scientist": {"O*NET": "15-2051.00", "ESCO": "252901"},
            "software engineer": {"O*NET": "15-1252.00", "ESCO": "251202"},
            # Add more mappings as needed
        }

    def normalize(self, job_title: str, framework: str) -> str:
        """Normalize job title to a framework-specific occupation code."""
        job_title = job_title.lower().strip()
        return self.mappings.get(job_title, {}).get(framework, job_title)