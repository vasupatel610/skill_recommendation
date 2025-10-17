import httpx

async def test_recommend_skills():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/recommend-skills",
            json={"job_title": "Data Scientist", "country": "US", "framework": "O*NET"}
        )
        print(response.json())

async def test_job_description():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/job-description/Data%20Scientist")
        print(response.json())

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_recommend_skills())
    asyncio.run(test_job_description())