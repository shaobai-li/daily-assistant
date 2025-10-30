import json

def clean_json_tags(json_str):
    return json_str.replace("```json", "").replace("```", "").strip()