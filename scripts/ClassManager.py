class ClassManager:
    def __init__(self):
        self.hierarchies = {} # Dictionary for hierarchies
        self.tagsets = {}  # Dictionary for tagsets
        self.tags = {}  # Dictionary for tags
        self.medias = []  # List for medias
        self.next_tag_id = 1
        self.next_tagset_id = 1

    def get_or_create_tag_id(self, value):
        # Search for the tag in the dictionary
        if value in self.tags:
            return self.tags[value]['id']
        # If the tag is not found, create it
        tag_id = self.next_tag_id
        self.tags[value] = {'id': tag_id, 'value': value}
        self.next_tag_id += 1
        return tag_id

    def get_or_create_tagset_id(self, name, tagset_type):
        # Search for the tagset in the dictionary
        if name in self.tagsets:
            return self.tagsets[name]['id']
        # If name is genre_2 or genre_3, return the id of genre_1
        if name == "genre_2" or name == "genre_3":
            return self.tagsets["genre_1"]['id']
        # If the tagset is not found, create it
        tagset_id = self.next_tagset_id
        self.tagsets[name] = {'id': tagset_id, 'name': name, 'type': tagset_type, 'tags': []}
        self.next_tagset_id += 1
        return tagset_id

    def add_tag_to_tagset(self, tagset_id, tag):
        # Search for the tagset in the dictionary
        for tagset in self.tagsets.values():
            if tagset['id'] == tagset_id:
                if tag not in tagset['tags']:  # Ensure the tag is unique
                    tagset['tags'].append(tag)
                return
        raise ValueError(f"Tagset with id {tagset_id} not found")

    def add_media(self, path, list_of_tags):
        self.medias.append({'path': path, 'tags': list_of_tags})

    def to_dict(self):
        # Convert tagsets to a list
        hierarchies_list = list(self.hierarchies.values())
        tagsets_list = list(self.tagsets.values())
        return {
            'hierarchies': hierarchies_list,
            'tagsets': tagsets_list,
            'medias': self.medias
        }
    
    def add_hierarchy(self, name, hierarchy):
        self.hierarchies[name] = hierarchy
