import uuid
import json

# Generate dictionary with random UUIDs
keys_dict = {
    "00": str(uuid.uuid4()),
    "01": str(uuid.uuid4()),
    "10": str(uuid.uuid4()),
    "11": str(uuid.uuid4())
}

# Serialize the dictionary and write it to keys.json
with open('keys.json', 'w') as file:
    json.dump(keys_dict, file, indent=4)

print("[INFO] UUID dictionary generated and saved to keys.json")
