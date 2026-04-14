import json 
import re 
import glob
import os 
from dotenv import load_dotenv

load_dotenv()

def clean_text(text): 
    if not text: 
        return ""
    
    text = text.lower() 
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def process_file(file_path): 
    with open(file_path) as f:
        data = json.load(f)
        
    seen = set()
    processed = []
    
    for item in data: 
        if item["id"] in seen: 
            continue
        seen.add(item["id"])
        
        processed.append({
            **item, 
            "clean_title" : clean_text(item["title"]),
            "clean_body" : clean_text(item["body"])
        })
        
    out_file = file_path.replace("raw", "processed")
    
    with open(out_file, "w") as f: 
        json.dump(processed, f, indent=4)
        
    print(f"[INFO] processed saved: {out_file}")
    return out_file


if __name__ == "__main__": 
    DATA_DIR = os.getenv("DATA_DIR")
    files = glob.glob(f"{DATA_DIR}/raw_*.json")
    latest = sorted(files)[-1]
    process_file(latest)