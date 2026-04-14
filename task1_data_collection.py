import time
import os 
from datetime import  datetime
from dotenv import load_dotenv
import requests
import json

load_dotenv()

def fetch_articles(retires=3, delay=2):
    payload={
        "query" : {            "$query": {
                "$and": [
                {
                    "keyword": "AI \"Artificial intelligence\" \"machine learning\" \"deep learning\" chatgpt \"generative AI\"",
                    "keywordSearchMode": "simple"
                },
                {
                    "categoryUri": "news/Technology"
                }
                ]
            },
            "$filter": {
                "forceMaxDataTimeWindow": "31"
            }
        }, 
        "resultType" : "articles", 
        "articleSortBy" : "date", 
        "articleCount" : os.getenv("MAX_ARTICLES"), 
        "apiKey" :  os.getenv("NEWS_API_KEY")
    }
    
    for attempt in range(retires): 
        try: 
            print(os.getenv("BASE_URL"))
            response =  requests.post(os.getenv("BASE_URL"), json=payload, timeout=10)
            response.raise_for_status() 
            return response.json()
        except Exception as e: 
            print(f"[Retry {attempt+1}] Error: {e}")
            time.sleep(delay)

    raise Exception("Failed to fetch data after retries")



def normalize_articles(raw_json):
    articles = raw_json.get("articles", {}).get("results", [])
    
    normalized=[]
    for a in articles: 
        normalized.append({
            "id" : a.get("uri"), 
            "title" : a.get("title"), 
            "body" : a.get("body"), 
            "source" : a.get("source", {}).get("title"), 
            "date" : a.get("date"), 
            "sentiment" : a.get("sentiment"), 
            "url" : a.get("url"), 
            "lang" : a.get("lang")
        })
        
    return normalized


def save_raw(data):
    DATA_DIR = os.getenv("DATA_DIR")
    print(f"DATA_DIR:{DATA_DIR}")
    os.makedirs(DATA_DIR, exist_ok=True)
    filename = f"{DATA_DIR}/raw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
        
    print(f"[INFO] Raw data saved: {filename}")
    
    return filename


if __name__ == "__main__": 
    raw = fetch_articles()
    normalized = normalize_articles(raw)
    print(normalized)
    abc= {
        "key" : "value"
    }
    save_raw(normalized)