# This tagset is used to classify the first letter of the track name and the first two letters of the track name

alphabet = "abcdefghijklmnopqrstuvwxyz"

def build_alphanumerical_tagset(class_manager):
    # Create the alphanumerical tagset
    tagset_id = class_manager.get_or_create_tagset_id("alphanumerical", 1)
    for letter in alphabet:
        tag_value = letter
        tag_id = class_manager.get_or_create_tag_id(tag_value, "alphanumerical")
        tag = {"id": tag_id, "value": tag_value}
        class_manager.add_tag_to_tagset(tagset_id, tag)

def build_track_name_tagset(class_manager):
    # Create the track name tagset
    tagset_id = class_manager.get_or_create_tagset_id("track_name", 1)
    for letter in alphabet:
        tag_value = f"track_name_{letter}"
        tag_id = class_manager.get_or_create_tag_id(tag_value, "track_name")
        tag = {"id": tag_id, "value": tag_value}
        class_manager.add_tag_to_tagset(tagset_id, tag)

def build_tagset(class_manager):
    # Create all different tagsets
    build_alphanumerical_tagset(class_manager)
