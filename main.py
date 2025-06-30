from pytrends.request import TrendReq
from pytrends.exceptions import TooManyRequestsError
import pandas as pd
import time

def get_trend_data(save_path="fashion_trends.csv"):
    pytrends = TrendReq(hl='en-US', tz=360)
    keywords = ['kurti', 'lawn suits', 'bridal lehenga', 'abaya', 'winter shawls']

    retries = 3
    for attempt in range(retries):
        try:
            pytrends.build_payload(keywords, geo='PK', timeframe='today 12-m')
            data = pytrends.interest_over_time()
            if data.empty:
                raise ValueError("No trend data returned.")
            
            data_cleaned = data.drop(columns='isPartial', errors='ignore')
            
            # Save to CSV
            data_cleaned.to_csv(save_path)
            print(f"Trend data saved to {save_path}")

            return data_cleaned
        
        except TooManyRequestsError:
            print(f"[Attempt {attempt + 1}] Rate limit hit. Retrying in 60 seconds...")
            time.sleep(60)
        
        except Exception as e:
            print(f"[Attempt {attempt + 1}] Error fetching trend data: {e}")
            time.sleep(10)

    raise RuntimeError("Failed to fetch Google Trends data after multiple attempts.")
df = get_trend_data("trend_output.csv")
print(df.head())
