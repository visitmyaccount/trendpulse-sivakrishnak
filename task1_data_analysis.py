import json 
import math 
from collections import Counter
import os 
import glob
from dotenv import load_dotenv

load_dotenv()


def compute_trend_score(article): 
    sentiment = article.get("sentiment") or 0
    length_factor = len(article.get("clean_title", "").split())
    
    return round((sentiment * 2) + math.log1p(length_factor), 3)

def extract_keywords(articles):
    words = []
    
    for a in articles: 
        words.extend(a["clean_title"].split())
        
    
    counter = Counter(words)
    return counter.most_common(20)


def analyze(file_path): 
    with open(file_path, "r") as f: 
        data = json.load(f)
        
    for a in data: 
        a["trend_score"] = compute_trend_score(a)
        
    keywords = extract_keywords(data)
    output = {
        "top_keywords" : keywords, 
        "top_articles" : sorted(data, key=lambda x: x["trend_score"], reverse=True)[:10]
    }
    
    out_file = file_path.replace("processed", "analysis")
    
    with open(out_file, "w") as f: 
        json.dump(output, f, indent=4)
        
    print(f"[INFO] Analysis saved: {out_file}")
    return out_file

if __name__ == "__main__": 
    DATA_DIR = os.getenv("DATA_DIR")
    files = glob.glob(f"{DATA_DIR}/processed_*.json")
    latest = sorted(files)[-1]
    analyze(latest)
    