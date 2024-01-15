from bson import ObjectId

def convert_object_id(data):
    if isinstance(data, list):
        for item in data:
            convert_object_id(item)
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
            convert_object_id(value)
    return data
