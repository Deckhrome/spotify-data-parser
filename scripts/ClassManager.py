class ClassManager:
    """
    This class manages the creation of hierarchies, tagsets, tags, and medias.

    Attributes:
    ----------------
    hierarchies: A dictionary that stores hierarchies.
    tagsets: A dictionary that stores tagsets.
    tags: A dictionary that stores tags categorized by type.
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
        self.hierarchies = {}
        self.tagsets = {}
        self.tags = {
            "uri": {},
            "track_name": {},
            "track_duration": {},
            "track_popularity": {},
            "album_name": {},
            "artist_infos": {},
            "happiness_percentage": {},
            "sadness_percentage": {},
            "anger_percentage": {},
            "fear_percentage": {},
            "genre": {},
            "alphanumerical": {},
            "emotion": {},
            "Timestamp UTC": {},
        }
        self.medias = []
        self.next_tag_id = 1
        self.next_tagset_id = 1

    def get_or_create_tag_id(self, value, category, verify=True):
        """
        Returns the tag ID if it exists, otherwise creates it.

        Args:
            value (str): The value of the tag.
            category (str): The category of the tag.
            verify (bool): A boolean that specifies whether to verify the tag.

        Returns:
            tuple: The tag ID and a boolean indicating if a new tag was created.
        """
        category = self._normalize_category(category)
        if category not in self.tags:
            raise ValueError(f"Unknown category: {category}")

        if value in self.tags[category] and verify:
            return self.tags[category][value], False

        tag_id = self.next_tag_id
        self.tags[category][value] = tag_id
        self.next_tag_id += 1
        return tag_id, True

    def get_or_create_tagset_id(self, name, tagset_type):
        """
        Returns the tagset ID if it exists, otherwise creates it.

        Args:
            name (str): The name of the tagset.
            tagset_type (int): The type of the tagset.

        Returns:
            int: The tagset ID.
        """
        name = self._normalize_tagset_name(name)
        if name in self.tagsets:
            return self.tagsets[name]["id"]

        tagset_id = self.next_tagset_id
        self.tagsets[name] = {
            "id": tagset_id,
            "name": name,
            "type": tagset_type,
            "tags": [],
        }
        self.next_tagset_id += 1
        return tagset_id

    def add_tag_to_tagset(self, tagset_id, tag):
        """
        Adds a tag to a tagset.

        Args:
            tagset_id (int): The ID of the tagset.
            tag (objet with id and value): The tag to add.
        """
        for tagset in self.tagsets.values():
            if tagset["id"] == tagset_id:
                tagset["tags"].append(tag)
                return
        raise ValueError(f"Tagset with id {tagset_id} not found")

    def add_media(self, path, thumbnail, list_of_tags):
        """
        Adds a media to the list of medias.

        Args:
            path (str): The path of the media.
            thumbnail (str): The path of the thumbnail.
            list_of_tags (list): The list of tags associated with the media.
        """
        self.medias.append({"path": path, "thumbnail": thumbnail, "tags": list_of_tags})

    def to_dict(self):
        """
        Converts the tag manager to a dictionary.

        Returns:
            dict: A dictionary representation of the tag manager.
        """
        return {
            "hierarchies": list(self.hierarchies.values()),
            "tagsets": list(self.tagsets.values()),
            "medias": self.medias,
        }

    def add_hierarchy(self, name, hierarchy):
        """Adds a hierarchy to the dictionary of hierarchies."""
        self.hierarchies[name] = hierarchy

    def _normalize_category(self, category):
        """Normalizes the category name."""
        if category in ["genre_2", "genre_3"]:
            return "genre"
        return category

    def _normalize_tagset_name(self, name):
        """Normalizes the tagset name."""
        if name in ["genre_2", "genre_3"]:
            return "genre"
        return name
