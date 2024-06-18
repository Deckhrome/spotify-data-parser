# This tagset is used to classify the first letter of the track name and the first two letters of the track name
def build_alphanumerical_tagset(class_manager):
    # Create the alphanumerical tagset
    tagset_id = class_manager.get_or_create_tagset_id("alphanumerical", 1)
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    n = len(alphabet)
    for i in range(n):
        tag_value = alphabet[i]
        tag_id = class_manager.get_or_create_tag_id(tag_value, "alphanumerical")
        tag = {"id": tag_id, "value": tag_value}
        class_manager.add_tag_to_tagset(tagset_id, tag)

def build_tagset(class_manager):
    # Create all different tagsets
    build_alphanumerical_tagset(class_manager)
