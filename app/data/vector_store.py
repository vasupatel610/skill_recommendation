from app.services.rag_service import RAGService
from app.data.framework_loader import FrameworkLoader
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        self.rag_service = RAGService()
        self.loader = FrameworkLoader()

    def initialize(self):
        """Initialize vector store with framework data."""
        # Clear existing collection
        try:
            self.rag_service.client.delete_collection("skills")
            logger.info("Cleared existing 'skills' collection")
        except:
            logger.info("No existing 'skills' collection to clear")

        # Load O*NET data
        onet_data = self.loader.load_onet()
        if not onet_data.empty:
            documents = []
            metadatas = []
            for _, row in onet_data.iterrows():
                skill_name = row.get("Element Name", "")
                skill_desc = row.get("Description", skill_name)
                occupation_code = row.get("O*NET-SOC Code", "")
                element_id = row.get("Element ID", "")
                if skill_name and skill_desc and occupation_code:
                    documents.append({
                        "text": f"{skill_name}: {skill_desc}",
                        "framework": "O*NET",
                        "skill": skill_name,
                        "description": skill_desc,
                        "element_id": element_id
                    })
                    metadatas.append({
                        "framework": "O*NET",
                        "skill": skill_name,
                        "occupation_code": occupation_code,
                        "description": skill_desc,
                        "element_id": element_id
                    })
            if documents:
                self.rag_service.add_documents(documents, metadatas)
                logger.info(f"Added {len(documents)} O*NET skills to vector store")
            else:
                logger.warning("No valid O*NET documents to add")
        else:
            logger.warning("No O*NET data loaded")

        # Load ESCO data
        esco_data = self.loader.load_esco()
        if not esco_data.empty:
            documents = []
            metadatas = []
            for _, row in esco_data.iterrows():
                skill_name = row.get("Element Name", "")
                skill_desc = row.get("Description", skill_name)
                occupation_code = row.get("Element ID", "")
                if skill_name and skill_desc:
                    documents.append({
                        "text": f"{skill_name}: {skill_desc}",
                        "framework": "ESCO",
                        "skill": skill_name,
                        "description": skill_desc
                    })
                    metadatas.append({
                        "framework": "ESCO",
                        "skill": skill_name,
                        "occupation_code": occupation_code,
                        "description": skill_desc
                    })
            if documents:
                self.rag_service.add_documents(documents, metadatas)
                logger.info(f"Added {len(documents)} ESCO skills to vector store")
            else:
                logger.warning("No valid ESCO documents to add")
        else:
            logger.warning("No ESCO data loaded")

        # Verify collection size
        collection = self.rag_service.client.get_collection("skills")
        count = collection.count()
        logger.info(f"Vector store contains {count} documents")
        if count == 0:
            logger.error("Vector store is empty after initialization")


# from app.services.rag_service import RAGService
# from app.data.framework_loader import FrameworkLoader
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class VectorStore:
#     def __init__(self):
#         self.rag_service = RAGService()
#         self.loader = FrameworkLoader()

#     def initialize(self):
#         """Initialize vector store with framework data."""
#         # Load O*NET data
#         onet_data = self.loader.load_onet()
        
#         if not onet_data.empty:
#             documents = []
#             metadatas = []
#             for _, row in onet_data.iterrows():
#                 skill_name = row.get("Element Name", "")
#                 skill_desc = row.get("Description", skill_name)
#                 occupation_code = row.get("O*NET-SOC Code", "")
#                 if skill_name and skill_desc:
#                     documents.append({
#                         "text": f"{skill_name}: {skill_desc}",
#                         "framework": "O*NET",
#                         "skill": skill_name,
#                         "description": skill_desc
#                     })
#                     metadatas.append({
#                         "framework": "O*NET",
#                         "skill": skill_name,
#                         "occupation_code": occupation_code,
#                         "description": skill_desc
#                     })

#             # Add to vector store
#             self.rag_service.add_documents(documents, metadatas)
#             logger.info(f"Added {len(documents)} O*NET skills to vector store")
#         else:
#             logger.warning("No O*NET data loaded, skipping vector store population for O*NET")

#         # Load ESCO data (placeholder)
#         esco_data = self.loader.load_esco()
#         if not esco_data.empty:
#             # Add ESCO data processing logic here
#             logger.info("ESCO data loaded, but processing not implemented")
#         else:
#             logger.warning("No ESCO data loaded")