import os 
import glob 
from dotenv import load_dotenv
import pandas as pd


load_dotenv()

DATA_DIR = os.getenv("DATA_DIR")

def clean_data(file_path):
    df = pd.read_json(file_path)
    
     
    print(f"Loaded {len(df)}  stories from {file_path} ")
    
    
    # Drop duplicates : ideally, won't exist.
    df = df.drop_duplicates(subset=['post_id'])
    
    print(f'After removing duplicates: {len(df)} ')
    # Drop data missing rows.
    df = df.dropna(subset=['post_id', 'title', 'score'])
    
    print(f'After removing nulls: {len(df)}')
    
    # Remove spaces in title 
    df['title'] = df['title'].str.strip()
    
    #Remove score < 5
    df = df[df['score'] >= 5]
    
    print(f'After removing low scores: {len(df)}')
    
    # score should be int
    df['score'] = df['score'].astype(int)
    
    #Fill zeros if missing and converting it as int
    df['num_comments'] = df['num_comments'].fillna(0).astype(int)
    
    print(f"Rows remaining after cleaning: {len(df)}")
    
    return df
    
    
def save_as_csv(df, file_path):
    # Create cleaned file with same name
    out_file = file_path.replace("trends", "clean").replace(".json", ".csv")
    
    df.to_csv(out_file, index=False)
    
    print(f'Saved {len(df)} rows to {out_file}')
    print(f"Total rows saved: {len(df)}")
    
    print("\nStories per Category:")
    print(df['category'].value_counts())
    
    
    
if __name__ == "__main__":
    path_str = f'{DATA_DIR}/trends_*.json'
    json_files = glob.glob(path_str)
    
    if not json_files : 
        print(f'Json file not found in directory : {DATA_DIR}')
        
    latest = sorted(json_files)[-1]
    df = clean_data(latest)
    save_as_csv (df, latest)