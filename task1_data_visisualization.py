import json
import matplotlib.pyplot as plt
import os 
import glob
from dotenv import load_dotenv

load_dotenv()

def visualize(file_path):
    with open(file_path) as f:
        data = json.load(f)

    keywords = data["top_keywords"]
    words = [k[0] for k in keywords]
    counts = [k[1] for k in keywords]

    plt.figure()
    plt.bar(words, counts)
    plt.xticks(rotation=45)
    plt.title("Top Trending Keywords")
    plt.tight_layout()
    plt.show()

    print("\n Top Articles:")
    for art in data["top_articles"]:
        print(f"{art['trend_score']} → {art['title']}")


if __name__ == "__main__":
    
    DATA_DIR = os.getenv("DATA_DIR")
    files = glob.glob(f"{DATA_DIR}/analysis_*.json")
    latest = sorted(files)[-1]
    visualize(latest)