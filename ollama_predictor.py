import ollama
from pathlib import Path
from config import OLLAMA_MODEL

class TrendPredictor:
    def __init__(self):
        self.system_prompt = Path("prompts/fashion_trends.txt").read_text()
    
    def predict(self, trend_data):
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Trend data:\n{trend_data}"}
            ],
            options={"temperature": 0.7, "num_predict": 256}
        )
        return response['message']['content']
