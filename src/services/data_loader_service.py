import json

from pathlib import Path
from typing import Dict


class DataLoaderService:
    def __init__(self):
        pass
    
    async def load_singular_json(self, path: str) -> Dict:
        """Load singular JSON file."""
        config_path = Path(__file__).parent.parent / path

        with open(config_path) as f:
            config = json.load(f)

        return config
