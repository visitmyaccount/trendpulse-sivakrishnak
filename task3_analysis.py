import pandas as pd
import numpy as np 
import os 
from dotenv import load_dotenv
import glob


load_dotenv() 

DATA_DIR = os.getenv("DATA_DIR")


def analyze_data(file_path): 
    
    try: 
        df = pd.read_csv(file_path)
    except Exception as e: 
        print(f'Failed to load {file_path}')
        return
        
    print(f"Loaded data: {df.shape}")
    print(f"\nFirst 5 rows:")
    print(df.head())
    
    score_mean=df['score'].mean()
    num_comments_mean = df['num_comments'].mean()
    
    print(f"\nAverage score    : {score_mean:,.2f}")
    print(f"Average comments : {num_comments_mean:,.2f}")
        
    print("\n--- NumPy Stats ---")
    
    scores = df['score'].to_numpy()
    
    print(f"Mean score    : {np.mean(scores):,.2f}")
    print(f"Median score  : {np.median(scores):,.2f}")
    print(f"Std deviation : {np.std(scores):,.2f}")
    print(f"Max score     : {np.max(scores):,}")
    print(f"Min score     : {np.min(scores):,}")
    
    
    top_category = df['category'].value_counts().idxmax()
    top_count = df['category'].value_counts().max()
    print(f"Most stories in: {top_category} ({top_count} stories)")
    
    
    idx_most_comments = df['num_comments'].idxmax()
    most_commented_title = df.loc[idx_most_comments, 'title']
    most_commented_count = df.loc[idx_most_comments, 'num_comments']
    print(f"Most commented story: \"{most_commented_title}\" — {most_commented_count:,} comments")

    
    df['engagement'] = df['num_comments'] / (df['score'] + 1)
    
    df['is_popular'] = df['score'] > score_mean
    
    return df


def save_as_csv(df, file_path):
    # Create cleaned file with same name
    out_file = file_path.replace("clean", "analysed")
    
    df.to_csv(out_file, index=False)
    
    print(f"Saved to {out_file}")

if __name__ == "__main__":
    path_str = f'{DATA_DIR}/clean_*.csv'
    print(path_str)
    json_files = glob.glob(path_str)
    
    if not json_files : 
        print(f'CSV file not found in directory : {DATA_DIR}')
        
    latest = sorted(json_files)[-1]
    
    df = analyze_data(latest)
    
    save_as_csv(df, latest)
    
