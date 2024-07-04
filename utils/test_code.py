import json
from collections import defaultdict

def check_unique_ids(data):
    # Initialize containers for the ids
    tagset_ids = set()
    tag_ids = set()
    
    # Check tagset IDs
    for tagset in data['tagsets']:
        if tagset['id'] in tagset_ids:
            return f"Duplicate tagset ID found: {tagset['id']}"
        tagset_ids.add(tagset['id'])
        
        # Check tag IDs within each tagset
        for tag in tagset['tags']:
            if tag['id'] in tag_ids:
                return f"Duplicate tag ID found: {tag['id']}"
            tag_ids.add(tag['id'])

    # Check media tag IDs
    for media in data['medias']:
        media_tag_ids = set()
        for tag_id in media['tags']:
            if tag_id not in tag_ids:
                return f"Media tag ID {tag_id} does not match any tag IDs"
            if tag_id in media_tag_ids:
                return f"Duplicate media tag ID found: {tag_id}"
            media_tag_ids.add(tag_id)
    
    return "All IDs are unique and valid."

def main():
    # Load the JSON file
    with open('../build/full_data.json') as f:
        data = json.load(f)
        
    # Run the ID checks
    result = check_unique_ids(data)
    print(result)

if __name__ == "__main__":
    main()
