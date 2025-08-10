import asyncio
import random
import httpx

API_URL = "http://localhost:8000/readings"

async def main():
    async with httpx.AsyncClient() as client:
        while True:
            value = round(random.uniform(6.8, 7.2), 2)
            if random.random() < 0.1:
                value = round(random.uniform(5.0, 9.0), 2)
            payload = {"parameter": "pH", "value": value}
            try:
                await client.post(API_URL, json=payload)
            except Exception as exc:
                print(f"Failed to post reading: {exc}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
