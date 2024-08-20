import json
from ClassManager import ClassManager


# Recursively associate tag with ID
def associate_tag_with_id(node, class_manager, tagset_id, category):
    if "tag_id" in node:
        tag_id, is_new = class_manager.get_or_create_tag_id(node["tag_id"], category)
        if is_new:
            tag = {"id": tag_id, "value": node["tag_id"]}
            class_manager.add_tag_to_tagset(tagset_id, tag)
        node["tag_id"] = tag_id

    if "child_nodes" in node:
        for child_node in node["child_nodes"]:
            associate_tag_with_id(child_node, class_manager, tagset_id, category)


def build_hierarchiy(class_manager, hierarchy):
    # Associate the correct tagset_id for the hierarchy
    hierarchy_name = hierarchy["name"]
    tagset_id = class_manager.get_or_create_tagset_id(hierarchy_name, 1)
    hierarchy["tagset_id"] = tagset_id
    # Start recursive function to match the value with the correct id
    associate_tag_with_id(hierarchy["rootnode"], class_manager, tagset_id, hierarchy_name)
    # Add the hierarchy to the ClassManager
    class_manager.add_hierarchy(hierarchy_name, hierarchy)


def build_hierarchies(class_manager, path):
    with open(path, "r") as f:
        hierarchies = json.load(f)

    for hierarchy in hierarchies:
        build_hierarchiy(class_manager, hierarchy)
    
