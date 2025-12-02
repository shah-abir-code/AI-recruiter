import os, json
ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, "..", "data")  # or adjust path
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
JOBS_FILE = os.path.join(DATA_DIR, "jobs.json")
APPS_FILE = os.path.join(DATA_DIR, "applications.json")

def load_json(path):
    # File exists or not
    if not os.path.exists(path):
        return []

    # File empty?
    if os.path.getsize(path) == 0:
        return []

    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # corrupt file reset it
        return []



def save_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def load_jobs():
    return load_json(JOBS_FILE)

def save_jobs(jobs):
    save_json(JOBS_FILE, jobs)

def load_apps():
    return load_json(APPS_FILE)

def save_apps(apps):
    save_json(APPS_FILE, apps)
