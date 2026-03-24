import json
from chat.models import LawSection

def load_data():
    with open("chat/data/ipc_sections.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        LawSection.objects.update_or_create(
            code=item["code"],
            defaults={
                "title": item["title"],
                "description": item["description"],
                "punishment": item["punishment"],
                "bailable": item["bailable"]
            }
        )

    print("✅ IPC Sections Loaded Successfully!")