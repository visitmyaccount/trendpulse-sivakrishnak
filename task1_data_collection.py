import requests
import os 
from dotenv import load_dotenv
import json 
import time
from datetime import datetime
import traceback

load_dotenv()

# Fetch story ids via static json link.
def fetch_story_ids():
    print('trying to get story ids.')
    story_ids = []
    try: 
        TOP_STORIES_JSON_URL = os.getenv("TOP_STORY_LINK")
        response = requests.get(TOP_STORIES_JSON_URL)
        response.raise_for_status()
        story_ids = response.json()
        print(f'response:{story_ids}')
    except Exception as e: 
        print(e)
        
    return story_ids
    
def get_story_details(story_id):
    print(f'fetching story details:{story_id}')
    
    try: 
        STORY_LINK = os.getenv("STORY_LINK")
        STORY_LINK = STORY_LINK.replace("{id}", str(story_id))
        headers = {"User-Agent": "TrendPulse/1.0"}
        response = requests.get(STORY_LINK, headers= headers)
        response.raise_for_status()
        return response.json()
    except Exception as e: 
        print(e)
    
    raise Exception(f"Failed to fetch data for story:{story_id}")


def get_category_by_title(story_title):
    
    if story_title:        
        story_title = story_title.lower()
        categories = get_category_words()
        for ci in categories: 
            for keyword in ci['keywords']: 
                if keyword in story_title: 
                    return ci['category']
            
    return None
    # return "default-category"
    
def normalize_story(story_details):
    return {
        "post_id" : story_details.get("id", ""), 
        "title" : story_details.get("title", ""), 
        "category": get_category_by_title(story_details.get("title", "")), 
        "score" : story_details.get("score", 0), 
        "num_comments" : story_details.get("descendants", 0), 
        "author" : story_details.get("by", ""), 
        "collected_at": datetime.now().isoformat()
    }
    
    
def get_category_words(): 
    category_map_array = [
        {
            "category" : "technology", 
            "keywords" : ["AI","software","tech","code","computer","data","cloud","API","GPU","LLM"]
        },
        {
            "category" : "worldnews", 
            "keywords" : ["war","government","country","president","election","climate","attack","global"]
        }, 
        {
            "category" : "sports", 
            "keywords" : ["NFL","NBA","FIFA","sport","game","team","player","league","championship"]
        },
        {
            "category" : "science", 
            "keywords" : ["research","study","space","physics","biology","discovery","NASA","genome", "care?", "concert"]
        }, 
         {
            "category" : "entertainment", 
            "keywords" : ["movie","film","music","Netflix","game","book","show","award","streaming"]
        }, 
    ]
    
    return category_map_array
    
if __name__ == "__main__": 
    #Max stories per category
    max_stories_per_category=25
    #All story ids
    story_ids = fetch_story_ids()
    
    # key, list of records
    category_normalized_data_list = {}
    
    
    for category_data in get_category_words():
        category = category_data['category']
        for item_id in story_ids[:]:  
            try: 
                # fetch only once.
                story_ids.remove(item_id)
                
                item_details = get_story_details(item_id)
                
                # Filter if type story
                if not item_details or item_details['type'] != 'story':
                    continue
                
                #Normaize 
                standard_story= normalize_story(item_details)
                
                #If category is not found in given list then leave it. 
                if not standard_story['category']:
                    continue
                
                # Check for max allowed stories per category.
                if len(category_normalized_data_list.get(standard_story.get('category', ""), "")) < max_stories_per_category:
                    category_normalized_data_list.setdefault(standard_story['category'], []).append(standard_story)  
                
                
                if len(category_normalized_data_list.get(category, "")) >= max_stories_per_category:
                    break
            except Exception as e: 
                print(f"faile to fetch data for {item_id}. continue for next story")
                traceback.print_exc() 
            
        print("Sleep 2 seconds between category loop")
        time.sleep(2)

    
    final_list = []
    # keep all stories in single to list . For saving
    for list_cate in category_normalized_data_list.keys(): 
        final_list.extend(category_normalized_data_list[list_cate])
        
    # Fetching directory from .env
    DATA_DIR = os.getenv("DATA_DIR")

    # Create directory if not exist
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    # file name with date string.
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{date_str}.json"
    
    with open(filename, 'w') as f:
        json.dump(final_list, f, indent=4)
        
    print(f"Collected {len(final_list)} stories. Saved to {filename}") 