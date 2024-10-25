import json
import os

def load_user_data(json_file_path):
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as f:
            return json.load(f)
    return {}

# JSON 파일에 저장하는 함수
def save_data(data, json_file_path):
    with open(json_file_path, "w") as f:
        json.dump(data, f, indent=4)