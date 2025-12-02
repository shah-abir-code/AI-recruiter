# ui/streamlit_app.py
import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hr.add_job import hr_add_job
from candidate.apply_job import apply_for_job
from backend.database.db_handler import load_jobs, load_apps

st.title("AI RecruitMatch")

tab1, tab2 = st.tabs(["Candidate", "HR"])

with tab1:
    st.header("Candidate")
    jobs = load_jobs()
    if jobs:
        options = {str(j['job_id']): f"{j['title']} (ID:{j['job_id']})" for j in jobs}
        selected = st.selectbox("Select Job", options=list(options.keys()), format_func=lambda x: options[x])
    else:
        st.info("No jobs yet.")

    uploaded = st.file_uploader("Upload resume", type=["pdf","docx","txt"])
    pasted = st.text_area("Or paste resume")
    name = st.text_input("Name (optional)")

    if st.button("Apply"):
        if not jobs:
            st.warning("No jobs to apply.")
        else:
            job_id = int(selected)
            res = apply_for_job(uploaded, pasted, job_id, applicant_name=name)
            if res.get("ok"):
                st.success(f"Applied. Score: {res['result']['score_final']}")
            else:
                st.error(res.get("msg"))

with tab2:
    st.header("HR")
    title = st.text_input("Title")
    desc = st.text_area("Description")
    if st.button("Add Job"):
        out = hr_add_job(title, desc)
        if out.get("ok"):
            st.success(f"Job added: {out['job_id']}")
    st.subheader("Jobs")
    for j in load_jobs():
        st.write(f"ID: {j['job_id']} | {j['title']}")
    st.subheader("Applications")
    for a in load_apps():
        st.write(a)
