# from app.data.vector_store import VectorStore

# def main():
#     vector_store = VectorStore()
#     vector_store.initialize()
#     print("Vector database initialized successfully.")

# if __name__ == "__main__":
#     main()
import sys
import os
import logging

# Add project root to PYTHONPATH
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

try:
    from app.data.vector_store import VectorStore
except ImportError as e:
    print(f"Error importing VectorStore: {e}")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        vector_store = VectorStore()
        vector_store.initialize()
        logger.info("Vector database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize vector database: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()