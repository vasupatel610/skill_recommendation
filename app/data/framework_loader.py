import os
import pandas as pd
from app.config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FrameworkLoader:
    def __init__(self):
        self.onet_path = Config.ONET_DATA_PATH
        self.esco_path = Config.ESCO_DATA_PATH

    def load_onet(self):
        """Load O*NET skills data."""
        skills_file = os.path.join(self.onet_path, "Skills.txt")
        if not os.path.exists(skills_file):
            logger.error(f"Skills file not found at {skills_file}")
            return pd.DataFrame()

        try:
            # Load Skills.txt (tab-separated)
            skills_df = pd.read_csv(skills_file, sep="\t", encoding="utf-8")
            logger.info(f"Loaded {len(skills_df)} skills from {skills_file}")
            logger.debug(f"Columns in Skills.txt: {list(skills_df.columns)}")

            # Check for required columns
            required_columns = ["O*NET-SOC Code", "Element Name", "Element ID"]
            if not all(col in skills_df.columns for col in required_columns):
                logger.error(f"Missing required columns in Skills.txt. Found: {list(skills_df.columns)}")
                return pd.DataFrame()

            # Load Content Model Reference for descriptions
            content_file = os.path.join(self.onet_path, "Content Model Reference.txt")
            if os.path.exists(content_file):
                content_df = pd.read_csv(content_file, sep="\t", encoding="utf-8")
                skills_df = skills_df.merge(
                    content_df[["Element ID", "Description"]],
                    on="Element ID",
                    how="left"
                )
                logger.info("Merged Content Model Reference for skill descriptions")
            else:
                logger.warning(f"Content Model Reference not found at {content_file}")
                skills_df["Description"] = skills_df["Element Name"]  # Fallback to Element Name

            # Filter out rows with missing critical fields
            skills_df = skills_df[skills_df["O*NET-SOC Code"].notna() & skills_df["Element Name"].notna()]
            logger.info(f"Filtered to {len(skills_df)} valid skills")
            return skills_df
        except Exception as e:
            logger.error(f"Error loading O*NET data: {str(e)}")
            return pd.DataFrame()

    def load_esco(self):
        """Load ESCO skills data from CSV."""
        skills_file = os.path.join(self.esco_path, "skills_en.csv")
        if not os.path.exists(skills_file):
            logger.warning(f"ESCO skills file not found at {skills_file}")
            return pd.DataFrame()

        try:
            esco_df = pd.read_csv(skills_file, encoding="utf-8")
            logger.info(f"Loaded {len(esco_df)} skills from {skills_file}")
            return esco_df.rename(columns={
                "preferredLabel": "Element Name",
                "description": "Description",
                "conceptUri": "Element ID"
            })
        except Exception as e:
            logger.error(f"Error loading ESCO data: {str(e)}")
            return pd.DataFrame()

    def load_mappings(self):
        """Load framework mappings."""
        return {
            "O*NET": {
                "data scientist": "15-2051.00",
                "data sciencetist": "15-2051.00",
                "software engineer": "15-1252.00",
                "software developer": "15-1252.00"
            },
            "ESCO": {
                "data scientist": "252901",
                "data sciencetist": "252901",
                "software engineer": "251202",
                "software developer": "251202"
            }
        }

# import os
# import pandas as pd
# from app.config import Config
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class FrameworkLoader:
#     def __init__(self):
#         self.onet_path = Config.ONET_DATA_PATH
#         self.esco_path = Config.ESCO_DATA_PATH

#     def load_onet(self):
#         """Load O*NET skills data."""
#         skills_file = os.path.join(self.onet_path, "Skills.txt")
#         if not os.path.exists(skills_file):
#             logger.error(f"Skills file not found at {skills_file}")
#             return pd.DataFrame()

#         try:
#             # Load Skills.txt (tab-separated)
#             skills_df = pd.read_csv(skills_file, sep="\t")
#             logger.info(f"Loaded {len(skills_df)} skills from {skills_file}")

#             # Load Content Model Reference for descriptions (if available)
#             content_file = os.path.join(self.onet_path, "Content Model Reference.txt")
#             if os.path.exists(content_file):
#                 content_df = pd.read_csv(content_file, sep="\t")
#                 # Merge to get descriptions (assuming Element ID links them)
#                 skills_df = skills_df.merge(
#                     content_df[["Element ID", "Description"]],
#                     on="Element ID",
#                     how="left"
#                 )
#                 logger.info("Merged Content Model Reference for skill descriptions")
#             else:
#                 logger.warning(f"Content Model Reference not found at {content_file}")
#                 skills_df["Description"] = skills_df["Element Name"]  # Fallback

#             return skills_df
#         except Exception as e:
#             logger.error(f"Error loading O*NET data: {str(e)}")
#             return pd.DataFrame()

#     def load_esco(self):
#         """Load ESCO dataset (placeholder)."""
#         skills_file = os.path.join(self.esco_path, "skills.json")
#         if os.path.exists(skills_file):
#             try:
#                 esco_df = pd.read_json(skills_file)
#                 logger.info(f"Loaded {len(esco_df)} skills from {skills_file}")
#                 return esco_df
#             except Exception as e:
#                 logger.error(f"Error loading ESCO data: {str(e)}")
#         logger.warning(f"ESCO skills file not found at {skills_file}")
#         return pd.DataFrame()

#     def load_mappings(self):
#         """Load framework mappings."""
#         return {
#             "O*NET": {
#                 "data scientist": "15-2051.00",
#                 "data sciencetist": "15-2051.00",
#                 "software engineer": "15-1252.00"
#             },
#             "ESCO": {
#                 "data scientist": "252901",
#                 "data sciencetist": "252901",
#                 "software engineer": "251202"
#             }
#         }