from backend.extractor.docx_pdf_extractor import extract_text_from_file
from backend.skills.skill_extractor import extract_skills_from_resume, extract_keywords_from_text
from backend.database.db_handler import load_jobs, load_apps, save_apps, load_jobs, save_jobs
import time, os
from backend.database.db_handler import save_json

def get_global_keywords():
    jobs = load_jobs()
    kws = []
    for j in jobs:
        kws += j.get("keywords", [])  # if keywords saved
        # else compute on the fly:
        # kws += extract_keywords_from_text(j.get("text",""), top_n=20)
    return sorted(list(set([k.lower() for k in kws])))

def save_resume_file(uploaded_file):
    from backend.database.db_handler import DATA_DIR
    resumes_dir = os.path.join(os.path.dirname(DATA_DIR), "..", "data", "resumes")
    os.makedirs(resumes_dir, exist_ok=True)
    name = getattr(uploaded_file, "name", f"resume_{int(time.time())}.txt")
    dest = os.path.join(resumes_dir, f"{int(time.time())}_{name}")
    raw = uploaded_file.read()
    with open(dest, "wb") as f:
        f.write(raw)
    return dest

def apply_for_job(uploaded_file, pasted_text, job_id, applicant_name=None):
    if uploaded_file:
        path = save_resume_file(uploaded_file)
        resume_text = extract_text_from_file(path)
    else:
        resume_text = pasted_text or ""
        path = None

    jobs = load_jobs()
    job = next((j for j in jobs if str(j.get("job_id")) == str(job_id)), None)
    if not job:
        return {"ok": False, "msg": "Job not found."}

    global_kws = get_global_keywords()
    resume_skills = extract_skills_from_resume(resume_text, global_kws)
    job_kws = job.get("keywords") or extract_keywords_from_text(job.get("text",""), top_n=20)

    # compute keyword match
    kscore = 0.0
    if job_kws:
        kscore = len(set(resume_skills) & set([k.lower() for k in job_kws])) / len(job_kws)

    # optional semantic
    try:
        from backend.matching.job_matching import semantic_score
        sscore = semantic_score(resume_text, job.get("text",""))
    except:
        sscore = None

    if sscore is None:
        final = round(kscore, 3)
    else:
        final = round(0.6 * sscore + 0.4 * kscore, 3)

    apps = load_apps()
    record = {
        "app_id": int(time.time()*1000),
        "job_id": job_id,
        "applicant_name": applicant_name or "Anonymous",
        "resume_path": path,
        "score_final": final,
        "score_keyword": round(kscore,3),
        "score_semantic": sscore,
        "resume_skills": resume_skills,
        "job_keywords": job_kws,
        "applied_at": time.ctime()
    }
    apps.append(record)
    save_apps(apps)
    return {"ok": True, "result": record}
