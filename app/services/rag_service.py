import chromadb
from sentence_transformers import SentenceTransformer
from app.config import Config

class RAGService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=Config.CHROMA_DB_PATH)
        self.collection = self.client.get_or_create_collection(name="skills")
        self.encoder = SentenceTransformer("all-MiniLM-L6-v2")

    def query(self, query_text: str, framework: str, n_results: int = 5):
        """Query the vector database for relevant skills."""
        query_embedding = self.encoder.encode(query_text).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where={"framework": framework}
        )
        return results["metadatas"][0] if results["metadatas"] else []

    def add_documents(self, documents: list, metadatas: list):
        """Add documents to the vector database."""
        embeddings = self.encoder.encode([doc["text"] for doc in documents]).tolist()
        self.collection.add(
            documents=[doc["text"] for doc in documents],
            embeddings=embeddings,
            metadatas=metadatas,
            ids=[f"doc_{i}" for i in range(len(documents))]
        )