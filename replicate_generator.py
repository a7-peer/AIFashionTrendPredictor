import replicate
from config import REPLICATE_API_TOKEN
from pathlib import Path

class FashionImageGenerator:
    def __init__(self):
        self.prompt_template = Path("prompts/image_prompts.txt").read_text()
        self.client = replicate.Client(api_token=REPLICATE_API_TOKEN)
    
    def generate(self, trend_description):
        prompt = self.prompt_template.format(trend=trend_description)
        output = self.client.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={
                "prompt": prompt,
                "negative_prompt": "western clothing, low quality, blurry",
                "width": 768,
                "height": 1024
            }
        )
        return output[0] if output else None
