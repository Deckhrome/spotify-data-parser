import json

def check_duplicates(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    tagset_ids = set()
    tags = set()

    tagsets = data['tagsets']
    medias = data['medias']

    for item in tagsets:
        tagset_id = item['id']
        if tagset_id in tagset_ids:
            return f"Duplicate tagset ID: {tagset_id}"
        tagset_ids.add(tagset_id)
    
    for item in medias:
        tags = set()
        for tag in item['tags']:
            if tag in tags:
                return f"Duplicate tag ID: {tag} in media: {item['path']}"
            tags.add(tag)
        
    
    return "No duplicates found"

# Usage
json_file = '../build/full_data.json'
result = check_duplicates(json_file)
print(result)