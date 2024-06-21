import json
from ClassManager import ClassManager

genre_hierarchy = {
    "name": "genre_1",
    "tagset_id": None,  # Vous devrez définir le tagset_id pour les genres
    "rootnode": {
        "tag_id": "popular",  # Root genre
        "child_nodes": [
            {
                "tag_id": "rock",
                "child_nodes": [
                    {   "tag_id": "alternativerock", 
                        "child_nodes": [
                            {   "tag_id": "dreampop", 
                                "child_nodes": [
                                    {"tag_id": "shoegaze", "child_nodes": []},
                                ]},
                            {"tag_id": "grunge", "child_nodes": []},
                            {"tag_id": "indierock", "child_nodes": []},
                    ]},
                    {   "tag_id": "experimentalrock", 
                        "child_nodes": [
                            {"tag_id": "postrock", "child_nodes": []},
                            {"tag_id": "artrock", "child_nodes": []},
                        ]},
                    {   "tag_id": "progressiverock", 
                        "child_nodes": [
                            {"tag_id": "symphonicrock", "child_nodes": []},
                        ]},
                    {"tag_id": "hardrock", "child_nodes": []},
                    {"tag_id": "psychedelicrock", "child_nodes": []},
                    {"tag_id": "southernrock", "child_nodes": []},
                    {"tag_id": "classicrock", "child_nodes": []},
                    {"tag_id": "christianrock", "child_nodes": []},
                    {"tag_id": "stonerrock", "child_nodes": []},

                ]
            },
            {
                "tag_id": "pop",
                "child_nodes": [
                    {   "tag_id": "jpop", 
                        "child_nodes": [
                            {"tag_id": "anime", "child_nodes": []},
                        ]},
                    {   "tag_id": "poprock", 
                        "child_nodes": [
                            {"tag_id": "poppunk", "child_nodes": []},
                        ]},
                    {"tag_id": "electropop", "child_nodes": []},
                    {"tag_id": "indiepop", "child_nodes": []},
                    {"tag_id": "kpop", "child_nodes": []},
                ]
            },
            {
                "tag_id": "hiphop",
                "child_nodes": [
                    {"tag_id": "trap", "child_nodes": []},
                    {"tag_id": "comedy", "child_nodes": []},
                    {"tag_id": "undergroundhiphop", "child_nodes": []},
                ]
            },
            {
                "tag_id": "folk",
                "child_nodes": [
                    {"tag_id": "folkrock", "child_nodes": []},
                    {"tag_id": "singersongwriter", "child_nodes": []},
                ]
            },
            {
                "tag_id": "blues",
                "child_nodes": [
                    {"tag_id": "bluesrock", "child_nodes": []},
                ]
            },
            {
                "tag_id": "jazz",
                "child_nodes": [
                    {"tag_id": "nujazz", "child_nodes": []},
                    {"tag_id": "smoothjazz", "child_nodes": []},
                ]
            },
            {
                "tag_id": "punk",
                "child_nodes": [
                    {   "tag_id": "hardcorepunk",
                        "child_nodes": [
                            {"tag_id": "emo", "child_nodes": []},
                        ]},
                    {"tag_id": "grindcore", "child_nodes": []},
                    {"tag_id": "posthardcore", "child_nodes": []},
                    {"tag_id": "postpunk", "child_nodes": []},
                    {"tag_id": "skatepunk", "child_nodes": []},
                ]
            },
            {
                "tag_id": "metal",
                "child_nodes": [
                    {   "tag_id": "deathmetal",
                        "child_nodes": [
                            {"tag_id": "melodicdeathmetal", "child_nodes": []},
                        ]},
                    {   "tag_id": "metalcore",
                        "child_nodes": [
                            {"tag_id": "deathcore", "child_nodes": []},
                        ]},
                    {   "tag_id": "alternativemetal", 
                        "child_nodes": [
                            {"tag_id": "numetal", "child_nodes": []},
                        ]},
                    {"tag_id": "folkmetal", "child_nodes": []},
                    {"tag_id": "trashmetal", "child_nodes": []},
                    {"tag_id": "doommetal", "child_nodes": []},
                    {"tag_id": "symphonicmetal", "child_nodes": []},
                    {"tag_id": "powermetal", "child_nodes": []},
                    {"tag_id": "blackmetal", "child_nodes": []},
                    {"tag_id": "progressivemetal", "child_nodes": []},
                    {"tag_id": "gothicmetal", "child_nodes": []},
                ]
            },
            {
                "tag_id": "country",
                "child_nodes": [
                    {"tag_id": "countryrock", "child_nodes": []},
                    {"tag_id": "alternativecountry", "child_nodes": []},
                ]
            },
            {
                "tag_id": "electronic",
                "child_nodes": [
                    {   "tag_id": "electronicrock", 
                        "child_nodes": [
                            {   "tag_id": "newwave", 
                                "child_nodes": [
                                    {   "tag_id": "synthpop", 
                                        "child_nodes": [
                                            {   "tag_id": "electroclash", 
                                                "child_nodes": [
                                                    {"tag_id": "electropop", "child_nodes": []},
                                            ]},
                                        ]},
                                    {"tag_id": "darkwave", "child_nodes": []},
                                ]},
                        ]},
                    {   "tag_id": "ambient", 
                        "child_nodes": [
                            {"tag_id": "darkambient", "child_nodes": []},
                            {"tag_id": "newage", "child_nodes": []},
                        ]},
                    {   "tag_id": "industrial", 
                        "child_nodes": [
                            {"tag_id": "ebm", "child_nodes": []},
                            {"tag_id": "industrialmetal", "child_nodes": []},
                        ]},
                    {   "tag_id": "ukgarage", 
                        "child_nodes": [
                            {"tag_id": "grime", "child_nodes": []},
                            {"tag_id": "dubstep", "child_nodes": []},
                        ]},
                    {   "tag_id": "house", 
                        "child_nodes": [
                            {"tag_id": "deephouse", "child_nodes": []},
                            {"tag_id": "futurehouse", "child_nodes": []},
                            {"tag_id": "electrohouse", "child_nodes": []},
                            {"tag_id": "progressivehouse", "child_nodes": []},
                            {"tag_id": "techhouse", "child_nodes": []},
                        ]},
                    {   "tag_id": "chillout", 
                        "child_nodes": [
                            {"tag_id": "downtempo", "child_nodes": []},
                            {"tag_id": "lounge", "child_nodes": []},
                            {"tag_id": "triphop", "child_nodes": []},
                        ]},
                    {   "tag_id": "hauntology", 
                        "child_nodes": [
                            {"tag_id": "chillwave", "child_nodes": []},
                            {"tag_id": "vaporwave", "child_nodes": []},
                            {"tag_id": "synthwave", "child_nodes": []},
                        ]},
                    {   "tag_id": "trance", 
                        "child_nodes": [
                            {"tag_id": "progressivetrance", "child_nodes": []},
                            {"tag_id": "psychedelictrance", "child_nodes": []},
                        ]},
                    {"tag_id": "techno", "child_nodes": []},
                    {"tag_id": "drumandbass", "child_nodes": []},
                    {"tag_id": "hardcore", "child_nodes": []},
                    {"tag_id": "electro", "child_nodes": []},
                    {"tag_id": "electronica", "child_nodes": []},
                ]
            },
            {
                "tag_id": "soundtrack",
                "child_nodes": [
                    {"tag_id": "videogamemusic", "child_nodes": []},
                ]
            },
            {
                "tag_id": "rnbandsoul",
                "child_nodes": [
                    {"tag_id": "disco", "child_nodes": []},
                    {"tag_id": "soul", "child_nodes": []},
                    {"tag_id": "funk", "child_nodes": []},                ]
            },
            {
                "tag_id": "experimental",
                "child_nodes": [
                    {"tag_id": "noise", "child_nodes": []},
                    {"tag_id": "lofi", "child_nodes": []},
                ]
            },
            {
                "tag_id": "reggae",
                "child_nodes": [
                    {"tag_id": "dub", "child_nodes": []},
                    {"tag_id": "ska", "child_nodes": []},
                ]
            },
            {
                "tag_id": "latin",
                "child_nodes": [
                    {"tag_id": "salsa", "child_nodes": []},
                    {"tag_id": "reggaeton", "child_nodes": []},
                ]
            },
            {
                "tag_id": "rap",
                "child_nodes": [
                    {"tag_id": "raprock", "child_nodes": []},
                ]
            }
        ]
    }
}

def associate_tag_with_id(node, class_manager, tagset_id, category):
    # Associate the tag with the id
    if "tag_id" in node:
        tag_id, new_id = class_manager.get_or_create_tag_id(node["tag_id"], category)
        # And add the tag to the tagset if it is new
        if new_id:
            tag = {"id": tag_id, "value": node["tag_id"]}
            class_manager.add_tag_to_tagset(tagset_id, tag)
        node["tag_id"] = tag_id
    # Recurse on the children
    if "child_nodes" in node:
        for child_node in node["child_nodes"]:
            associate_tag_with_id(child_node, class_manager, tagset_id, category)

def build_hierarchy_json(hierarchy, class_manager):
    # Get tagset for genre
    tagset_id = class_manager.get_or_create_tagset_id(hierarchy["name"], 1)
    hierarchy["tagset_id"] = tagset_id

    associate_tag_with_id(hierarchy["rootnode"], class_manager, tagset_id, hierarchy["name"])
    # Save hierarchy in ClassManager
    class_manager.add_hierarchy(hierarchy["name"],hierarchy)

    # Build the alphanumerical hierarchy
    build_alphanumerical_hierarchy(class_manager)

# Build the alphanumerical hierarchy
def build_alphanumerical_hierarchy(class_manager):
    # Create tagset for genre
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    hierarchy = {
        "name": "alphanumerical",
        "tagset_id": None,
        "rootnode": {
            "tag_id": "all",
            "child_nodes": []
        }
    }
    for letter in alphabet:
        hierarchy["rootnode"]["child_nodes"].append({
            "tag_id": letter,
            "child_nodes": []
        })
    # Create tagset for alphanumerical
    tagset_id = class_manager.get_or_create_tagset_id(hierarchy["name"], 1)
    hierarchy["tagset_id"] = tagset_id
    associate_tag_with_id(hierarchy["rootnode"], class_manager, tagset_id, hierarchy["name"])

    # Save hierarchy in ClassManager
    class_manager.add_hierarchy(hierarchy["name"],hierarchy)
    
