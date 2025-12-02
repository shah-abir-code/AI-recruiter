from backend.database.db_handler import load_jobs, save_jobs
from backend.skills.skill_extractor import extract_keywords_from_text
import time

def hr_add_job(title, description):
    jobs = load_jobs()
    job_id = int(time.time()*1000)
    text = f"{title}. {description}"
    keywords = extract_keywords_from_text(text, top_n=25)
    job = {
        "job_id": job_id,
        "title": title,
        "description": description,
        "text": text,
        "keywords": [k.lower() for k in keywords],
        "created_at": time.ctime()
    }
    jobs.append(job)
    save_jobs(jobs)
    return {"ok": True, "job_id": job_id}
