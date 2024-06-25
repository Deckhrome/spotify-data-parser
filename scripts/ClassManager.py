class ClassManager:
    """
    Description: This class manages the creation of hierarchies, tagsets, tags, and medias.

    Attributes:
    ----------------
    hierarchies: A dictionary that stores hierarchies.
    tagsets: A dictionary that stores tagsets.
    tags: A dictionary that stores tags.
    medias: A list that stores medias.
    next_tag_id: An integer that stores the next tag ID.
    next_tagset_id: An integer that stores the next tagset ID.

    Methods:
    ----------------
    get_or_create_tag_id: Returns the tag ID if it exists, otherwise creates it.
    get_or_create_tagset_id: Returns the tagset ID if it exists, otherwise creates it.
    add_tag_to_tagset: Adds a tag to a tagset.
    add_media: Adds a media to the list of medias.
    to_dict: Converts the tag manager to a dictionary.
    add_hierarchy: Adds a hierarchy to the dictionary of hierarchies.

    """
    def __init__(self):
        self.hierarchies = {}  # Dictionary for hierarchies
        self.tagsets = {}  # Dictionary for tagsets
        self.tags = {
            'track_name': {},
            'track_duration': {},
            'track_popularity': {},
            'album_name': {},
            'artist_infos': {},
            'happiness_percentage': {},
            'sadness_percentage': {},
            'anger_percentage': {},
            'fear_percentage': {},
            'genre': {},
            'alphanumerical': {},
            'emotion': {},
        }  # Separate dictionaries for tag categories
        self.medias = []  # List for medias
        self.next_tag_id = 1
        self.next_tagset_id = 1

    def get_or_create_tag_id(self, value, category, verify=True):
        """
        Description: This function returns the tag ID if it exists, otherwise creates it.

        Arguments:
        ----------------
        value: The value of the tag.
        category: The category of the tag.
        verify: A boolean that specifies whether to verify the tag.

        Returns:
        ----------------
        tag_id: The tag ID.
        """
        # Ensure the category exists
        if category == "genre_2" or category == "genre_3":
            category = "genre"
        if category not in self.tags:
            raise ValueError(f"Unknown category: {category}")
        
        # Search for the tag in the appropriate category dictionary
        if value in self.tags[category] and verify:
            return self.tags[category][value], False

        # If the tag is not found, create it
        tag_id = self.next_tag_id
        self.tags[category][value] = tag_id
        self.next_tag_id += 1
        return tag_id, True

    def get_or_create_tagset_id(self, name, tagset_type):
        """
        Description: This function returns the tagset ID if it exists, otherwise creates it.

        Arguments:
        ----------------
        name: The name of the tagset.
        tagset_type: The type of the tagset.

        Returns:
        ----------------
        tagset_id: The tagset ID.
        """
        # If name is genre_2 or genre_3, return the id of genre_1
        if name == "genre_2" or name == "genre_3":
            return self.tagsets["genre"]['id']
        # Search for the tagset in the dictionary
        if name in self.tagsets:
            return self.tagsets[name]['id']
        # If the tagset is not found, create it
        tagset_id = self.next_tagset_id
        self.tagsets[name] = {'id': tagset_id, 'name': name, 'type': tagset_type, 'tags': []}
        self.next_tagset_id += 1
        return tagset_id

    def add_tag_to_tagset(self, tagset_id, tag):
        # Search for the tagset in the dictionary
        for tagset in self.tagsets.values():
            if tagset['id'] == tagset_id:
                # if tag not in tagset['tags']:  # Ensure the tag is unique
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
