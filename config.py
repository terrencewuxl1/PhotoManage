import os, json

CONFIG_DIR = os.getcwd()
CONFIG_PATH = os.path.join(CONFIG_DIR, "settings.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config(cfg):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)

def get_db_path():
    cfg = load_config()
    db_path = cfg.get("db_path", "").strip()

    # default path if empty
    if not db_path:
        db_path = os.path.join(CONFIG_DIR, "media.db")

    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return db_path
