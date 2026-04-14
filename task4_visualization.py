import os
import glob
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt

# Load environment variables
load_dotenv()
DATA_DIR = os.getenv("DATA_DIR")


def get_short_title(title):
    title = str(title)
    return title[:47] + "..." if len(title) > 50 else title


def run_visualization_task(latest):
    try:
        df = pd.read_csv(latest)
    except Exception as e:
        print(f"Failed to load {latest}: {e}")
        return

    

    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    ax0, ax1, ax2, ax3 = axes.flatten()

    # --- CHART 1: Top 10 Stories ---
    top_10 = df.sort_values(by='score', ascending=False).head(10)
    short_titles = [get_short_title(t) for t in top_10['title']]

    ax0.barh(short_titles, top_10['score'])
    ax0.set_title('Top 10 Stories by Score')
    ax0.invert_yaxis()
    ax0.set_xlabel('Score')

    # --- CHART 2: Category Count ---
    cat_counts = df['category'].value_counts()

    ax1.bar(cat_counts.index, cat_counts.values)
    ax1.set_title('Stories per Category')
    ax1.set_ylabel('Count')
    ax1.tick_params(axis='x', rotation=30)

    # --- CHART 3: Scatter Plot ---
    pop = df[df['is_popular'] == True]
    not_pop = df[df['is_popular'] == False]

    ax2.scatter(pop['score'], pop['num_comments'], label='Popular')
    ax2.scatter(not_pop['score'], not_pop['num_comments'], alpha=0.5, label='Normal')
    ax2.set_title('Score vs Comments')
    ax2.set_xlabel('Score')
    ax2.set_ylabel('Comments')
    ax2.legend()

    # --- CHART 4: Summary ---
    ax3.axis('off')

    summary_text = (
        f"Data Summary\n\n"
        f"Total Stories: {len(df)}\n"
        f"Average Score: {df['score'].mean():.1f}\n"
        f"Top Category: {cat_counts.index[0]}"
    )

    ax3.text(0.1, 0.5, summary_text, fontsize=14, fontweight='bold')

    
    plt.suptitle('TrendPulse HackerNews Dashboard', fontsize=20)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Save output
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "dashboard.png")
    plt.savefig(output_path)

    print(f"Dashboard saved to {output_path}")


if __name__ == "__main__":
    

    path_str = f"{DATA_DIR}/analysed_*.csv"
    csv_files = glob.glob(path_str)

    if not csv_files:
        print(f"CSV files found in directory: {DATA_DIR}")
    else:
        latest = sorted(csv_files)[-1]
        print(f"Using file: {latest}")
        run_visualization_task(latest)