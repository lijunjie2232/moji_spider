# handle_keys.py
import json
from pathlib import Path
from tqdm import tqdm


class Key:
    def __init__(self, name: str):
        self.name = name
        self.optional = False


def calculate_keys(json_file: Path):

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        key_set = {}
        collection_list = data.get("result", {}).get("result", [])
        # gather keys of collection
        for collection in tqdm(collection_list):
            key_list = collection.keys()
            for k in key_list:
                key_set[k] = key_set.get(k, Key(k))
            for k in key_set.keys():
                if k not in key_list or collection.get(k) is None:
                    key_set[k].optional = True
            pass
        for i in key_set.values():
            print(f"{i.name}: {'optional' if i.optional else 'required'}")


if __name__ == "__main__":

    root = Path(__file__).parent.resolve()

    json_files = [
        root / "fetchSharedFoldersWithType_6_3000.json",
        root / "fetchSharedFoldersWithType_4_3000.json",
        root / "fetchSharedFoldersWithType_1_3000.json",
    ]

    for json_file in json_files:
        print("----------------------------------------")
        print(f"Processing file: {json_file}")
        calculate_keys(json_file)
        print("----------------------------------------")
        print("\n")
