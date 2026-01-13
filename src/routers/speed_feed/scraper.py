import asyncio

from typing import Dict

from ...services import DataLoaderService, TempLLM


class SpeedFeedScraper:
    def __init__(self):
        self.llm = TempLLM()
        self.data_loader = DataLoaderService()

    async def scrape(self, path: str) -> Dict:
        data = await self.data_loader.load_singular_json(path)
        
        return data


if __name__ == "__main__":
    path = "data/speed_feed/haas/raw/temp.json"
    scraper = SpeedFeedScraper()

    data = asyncio.run(scraper.scrape(path))

    print(data)
    