Skill-360-Recommendation
A skill recommendation engine that suggests hard and soft skills for job roles using O*NET and ESCO frameworks, powered by Groq's LLM and FastAPI.
Setup

Clone the repository:
git clone <repo-url>
cd skill-360-recommendation


Install dependencies:
pip install -r requirements.txt


Set up environment variables:

Copy .env.example to .env and add your Groq API key:cp .env.example .env


Edit .env to include your GROQ_API_KEY.


Download framework datasets:

Run the script to download O*NET and ESCO datasets:python scripts/download_frameworks.py




Initialize vector database:

Set up ChromaDB with the framework data:python scripts/setup_database.py




Run the FastAPI application:
uvicorn app.main:app --reload


Access the API:

API documentation is available at http://localhost:8000/docs.



Folder Structure

app/: FastAPI application, core logic, and services.
data/: Framework datasets and vector database storage.
scripts/: Utility scripts for setup and testing.
tests/: Unit tests for API and recommendation logic.

API Endpoints

POST /recommend-skills: Get skill recommendations for a job title and optional country.
GET /job-description/{job_title}: Get a job description for a given job title.

Dependencies

Python 3.9+
FastAPI, Groq, ChromaDB, Sentence Transformers, etc. (see requirements.txt)

Notes

Ensure O*NET and ESCO datasets are downloaded and placed in data/frameworks/.
The project uses Groq's free API for LLM-based recommendations.
ChromaDB is used for the RAG vector store.
