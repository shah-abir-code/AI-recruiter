from sentence_transformers import SentenceTransformer, util

# lazy load model
_model = None
def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def semantic_score(resume_text, job_text):
    model = get_model()
    emb_r = model.encode(resume_text, convert_to_tensor=True)
    emb_j = model.encode(job_text, convert_to_tensor=True)
    sim = util.cos_sim(emb_r, emb_j).item()
    sim = (sim + 1)/2.0
    return round(sim, 3)
