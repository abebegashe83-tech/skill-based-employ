import os
import re
import string
import sys
import traceback

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from apps.jobs.models import Job

# ── Domain Definitions ─────────────────────────────────────────────────────
TECH_DOMAIN = [
    "react", "nodejs", "python", "javascript", "django", "java", "spring", "angular",
    "vue", "typescript", "golang", "rust", "kubernetes", "docker", "aws", "azure",
    "sql", "nosql", "mongodb", "postgresql", "mysql", "redis", "elasticsearch",
    "graphql", "rest", "api", "microservices", "devops", "ci/cd", "git", "linux",
    "agile", "scrum", "machine learning", "data science", "deep learning", "nlp", "ai"
]

HEALTH_DOMAIN = [
    "nurse", "doctor", "medical", "clinic", "patient", "healthcare", "hospital",
    "surgery", "pharmacy", "medicine", "diagnosis", "treatment", "clinical",
    "physician", "surgeon", "dentist", "pharmacist", "radiology", "pathology",
    "oncology", "cardiology", "neurology", "pediatrics", "emergency", "triage",
    "vitals", "cpr", "epidemiology", "public health"
]

BUSINESS_DOMAIN = [
    "sales", "marketing", "finance", "accounting", "management", "hr", "recruiting",
    "consulting", "strategy", "operations", "logistics", "supply chain", "procurement",
    "customer service", "business development", "partnerships", "revenue", "profit",
    "budgeting", "forecasting", "financial planning", "investment", "banking",
    "insurance", "real estate", "compliance", "auditing", "risk management"
]

# ── Multi-Domain Skill Relationship Map ─────────────────────────────────────────────────────
SKILL_MAP = {
    # HEALTHCARE
    'nursing': ['patient care', 'clinical skills', 'vital signs', 'healthcare', 'medical'],
    'patient care': ['nursing', 'caregiving', 'clinical support', 'healthcare'],
    'clinical skills': ['nursing', 'medical procedures', 'healthcare'],
    'medical assistant': ['patient care', 'clinical support', 'healthcare'],
    'pharmacy': ['medication', 'pharmacology', 'healthcare'],
    'pharmacology': ['pharmacy', 'medication', 'healthcare'],
    'doctor': ['diagnosis', 'treatment', 'medical', 'healthcare'],
    'diagnosis': ['doctor', 'clinical analysis', 'medical'],
    'laboratory': ['lab technician', 'medical testing', 'healthcare'],
    'lab technician': ['laboratory', 'testing', 'medical'],
    'public health': ['epidemiology', 'healthcare', 'medical'],
    'epidemiology': ['public health', 'data analysis', 'healthcare'],
    'caregiver': ['patient care', 'nursing', 'healthcare'],
    'radiology': ['medical imaging', 'x-ray', 'diagnostics'],
    'x-ray': ['radiology', 'medical imaging', 'diagnostics'],
    'medical imaging': ['radiology', 'x-ray', 'diagnostics', 'medical'],
    'diagnostics': ['radiology', 'medical imaging', 'x-ray', 'doctor', 'medical'],
    'vital signs': ['nursing', 'patient care', 'healthcare'],
    'medical procedures': ['clinical skills', 'nursing', 'healthcare'],
    'clinical support': ['medical assistant', 'patient care', 'healthcare'],
    'medication': ['pharmacy', 'pharmacology', 'healthcare'],
    'medical': ['doctor', 'nursing', 'healthcare', 'diagnosis'],
    'testing': ['laboratory', 'lab technician', 'medical'],
    'healthcare': ['nursing', 'doctor', 'medical assistant', 'pharmacy'],

    # ENGINEERING
    'civil engineering': ['construction', 'structural design', 'engineering'],
    'mechanical engineering': ['machines', 'design', 'engineering'],
    'electrical engineering': ['circuits', 'electronics', 'engineering'],
    'software engineering': ['programming', 'development', 'engineering'],
    'construction': ['civil engineering', 'project management', 'engineering'],
    'structural design': ['civil engineering', 'engineering'],
    'cad': ['design', 'engineering', 'autocad'],
    'autocad': ['cad', 'design', 'engineering'],
    'machines': ['mechanical engineering', 'engineering'],
    'design': ['cad', 'autocad', 'mechanical engineering', 'engineering'],
    'circuits': ['electrical engineering', 'engineering'],
    'electronics': ['electrical engineering', 'engineering'],
    'programming': ['software engineering', 'development'],
    'development': ['software engineering', 'programming'],
    'engineering': ['civil engineering', 'mechanical engineering', 'electrical engineering', 'software engineering'],
    'project management': ['construction', 'engineering', 'management'],

    # BUSINESS / MANAGEMENT
    'management': ['leadership', 'operations', 'business'],
    'project management': ['planning', 'coordination', 'management'],
    'marketing': ['branding', 'advertising', 'business'],
    'sales': ['negotiation', 'customer service', 'business'],
    'finance': ['accounting', 'budgeting', 'business'],
    'accounting': ['finance', 'bookkeeping', 'business'],
    'human resources': ['recruitment', 'employee relations', 'hr'],
    'recruitment': ['hr', 'hiring', 'human resources'],
    'customer service': ['communication', 'support', 'business'],
    'leadership': ['management', 'business'],
    'operations': ['management', 'business'],
    'planning': ['project management', 'management'],
    'coordination': ['project management', 'management'],
    'branding': ['marketing', 'business'],
    'advertising': ['marketing', 'business'],
    'negotiation': ['sales', 'business'],
    'budgeting': ['finance', 'business'],
    'bookkeeping': ['accounting', 'finance'],
    'employee relations': ['human resources', 'hr'],
    'hiring': ['recruitment', 'human resources'],
    'communication': ['customer service', 'business'],
    'support': ['customer service', 'business'],
    'hr': ['human resources', 'recruitment'],
    'business': ['management', 'marketing', 'sales', 'finance', 'accounting'],

    # EDUCATION
    'teaching': ['education', 'classroom management', 'tutoring'],
    'education': ['teaching', 'training', 'learning'],
    'classroom management': ['teaching', 'education'],
    'training': ['education', 'coaching', 'teaching'],
    'tutoring': ['teaching', 'education'],
    'learning': ['education', 'training'],
    'coaching': ['training', 'education', 'teaching'],

    # TECH
    'python': ['django', 'flask', 'fastapi', 'backend', 'data science'],
    'django': ['python', 'backend', 'rest api', 'drf'],
    'flask': ['python', 'backend', 'rest'],
    'fastapi': ['python', 'api', 'async'],
    'react': ['javascript', 'frontend', 'next.js', 'redux', 'jsx'],
    'next.js': ['react', 'frontend', 'ssr'],
    'node': ['express', 'backend', 'node.js'],
    'node.js': ['express', 'nestjs', 'javascript', 'backend', 'rest api', 'nodejs'],
    'express': ['node.js', 'backend', 'api', 'javascript', 'express.js'],
    'sql': ['database', 'postgresql', 'mysql'],
    'database': ['sql', 'postgresql', 'mysql', 'mongodb'],
    'postgresql': ['sql', 'database', 'postgres'],
    'mysql': ['sql', 'database'],
    'mongodb': ['nosql', 'database', 'mongo'],
    'javascript': ['react', 'node.js', 'express', 'frontend', 'backend'],
    'backend': ['python', 'django', 'flask', 'node.js', 'express', 'fastapi'],
    'frontend': ['react', 'javascript', 'next.js', 'vue', 'angular'],
    'data science': ['python', 'pandas', 'numpy', 'machine learning'],
    'machine learning': ['python', 'tensorflow', 'pytorch', 'data science'],
    'tensorflow': ['python', 'machine learning', 'deep learning'],
    'pytorch': ['python', 'machine learning', 'deep learning'],
    'pandas': ['python', 'data science', 'numpy'],
    'numpy': ['python', 'data science', 'pandas'],
    'rest api': ['backend', 'api', 'django', 'express'],
    'api': ['rest api', 'backend', 'graphql'],
    'graphql': ['api', 'backend', 'javascript'],
    'docker': ['devops', 'container', 'kubernetes'],
    'kubernetes': ['docker', 'devops', 'k8s'],
    'devops': ['docker', 'kubernetes', 'ci/cd'],
    'ci/cd': ['devops', 'docker'],
    'aws': ['cloud', 'devops'],
    'cloud': ['aws', 'azure', 'gcp', 'devops'],
    'java': ['spring', 'spring boot', 'backend'],
    'spring': ['java', 'spring boot', 'backend'],
    'spring boot': ['java', 'spring', 'backend'],
    'typescript': ['angular', 'react', 'frontend'],
    'angular': ['typescript', 'frontend'],
    'vue': ['javascript', 'frontend'],
    'nest.js': ['node.js', 'typescript', 'backend'],
    'rest': ['rest api', 'backend', 'api'],
    'drf': ['django', 'python', 'backend'],
    'async': ['fastapi', 'python', 'backend'],
    'ssr': ['next.js', 'react', 'frontend'],
    'redux': ['react', 'javascript', 'frontend'],
    'jsx': ['react', 'javascript', 'frontend'],
    'nodejs': ['node.js', 'express', 'javascript', 'backend'],
    'express.js': ['express', 'node.js', 'javascript', 'backend'],
    'nosql': ['mongodb', 'database'],
    'mongo': ['mongodb', 'nosql', 'database'],
    'postgres': ['postgresql', 'sql', 'database'],
    'k8s': ['kubernetes', 'devops', 'docker'],
    'deep learning': ['tensorflow', 'pytorch', 'machine learning', 'python'],
}


def _normalize_skill(skill):
    """Normalize skill names to canonical forms."""
    if not skill:
        return skill
    
    skill_lower = skill.lower().strip()
    skill_lower = skill_lower.translate(str.maketrans('', '', string.punctuation))
    
    normalizations = {
        'nodejs': 'node.js',
        'js': 'javascript',
        'ts': 'typescript',
        'reactjs': 'react',
        'vuejs': 'vue',
        'angularjs': 'angular',
        'postgres': 'postgresql',
        'mongo': 'mongodb',
        'k8s': 'kubernetes',
        'express.js': 'express',
        'nextjs': 'next.js',
        'nest.js': 'nestjs',
        'drf': 'django rest framework',
    }
    return normalizations.get(skill_lower, skill_lower)


def _normalize_skills(skills):
    if not skills:
        return []
    return [_normalize_skill(s) for s in skills if s]


def _build_taxonomy():
    taxonomy = {}
    for skill, related in SKILL_MAP.items():
        key = skill.lower()
        normalized_related = [_normalize_skill(r) for r in related]
        taxonomy.setdefault(key, set()).update(normalized_related)
        for r in normalized_related:
            rkey = _normalize_skill(r)
            taxonomy.setdefault(rkey, set()).add(key)
    return taxonomy

_TAXONOMY = _build_taxonomy()


def _detect_domain(skills):
    if not skills:
        return "other"
    
    skills_lower = [skill.lower() for skill in skills]
    
    tech_count = sum(1 for skill in skills_lower if any(tech in skill for tech in TECH_DOMAIN))
    health_count = sum(1 for skill in skills_lower if any(health in skill for health in HEALTH_DOMAIN))
    business_count = sum(1 for skill in skills_lower if any(biz in skill for biz in BUSINESS_DOMAIN))
    
    if tech_count >= 1:
        return "tech"
    elif health_count >= 2:
        return "health"
    elif business_count >= 2:
        return "business"
    else:
        return "other"


def _skill_overlap_score(profile_skills, job_required_skills):
    if not profile_skills or not job_required_skills:
        return 0.0

    profile_norm = _normalize_skills(profile_skills)
    job_norm = _normalize_skills(job_required_skills)

    profile_set = {s for s in profile_norm if s}
    job_set = {s for s in job_norm if s}

    if not profile_set or not job_set:
        return 0.0

    weighted_hits = 0.0
    for js in job_set:
        if js in profile_set:
            weighted_hits += 1.0
        else:
            related = _TAXONOMY.get(js, set())
            if related & profile_set:
                weighted_hits += 0.6

    return min(1.0, weighted_hits / len(job_set))


def _is_direct_or_related(u, j):
    if u == j:
        return True
    if j in SKILL_MAP.get(u, []):
        return True
    if u in SKILL_MAP.get(j, []):
        return True
    return False


def _has_any_match(user_skills, job_skills):
    if not user_skills or not job_skills:
        return False
    
    user_norm = _normalize_skills(user_skills)
    job_norm = _normalize_skills(job_skills)
    
    user_set = {s for s in user_norm if s}
    job_set = {s for s in job_norm if s}
    
    if not user_set or not job_set:
        return False
    
    for u in user_set:
        for j in job_set:
            if _is_direct_or_related(u, j):
                return True
    return False


def _is_related(u, j):
    if j in SKILL_MAP.get(u, []):
        return True
    for mid in SKILL_MAP.get(u, []):
        if j in SKILL_MAP.get(mid, []):
            return True
    return False


def _related_score(user_skills, job_skills):
    if not user_skills or not job_skills:
        return 0.0, [], [], False
    
    user_norm = _normalize_skills(user_skills)
    job_norm = _normalize_skills(job_skills)
    
    user_set = {s for s in user_norm if s}
    job_set = {s for s in job_norm if s}
    
    if not user_set or not job_set:
        return 0.0, [], [], False
    
    exact_match = any(u == j for u in user_set for j in job_set)
    score = 0.0
    direct_matches = []
    related_matches = []
    
    for u in user_set:
        for j in job_set:
            if u == j:
                score += 1.0
                if u not in direct_matches:
                    direct_matches.append(u)
            elif _is_related(u, j):
                score += 0.7
                if (u, j) not in related_matches:
                    related_matches.append((u, j))
    
    if score == 0.0:
        return 0.0, [], [], False
    
    normalized_score = score / max(len(job_set), 1)
    return min(1.0, normalized_score), direct_matches, related_matches, exact_match


def _semantic_skill_match(user_skills, job_skills):
    if not user_skills or not job_skills:
        return 0.0
    
    try:
        import numpy as np
        import torch
        import torch.nn.functional as F
        from .embedding_service import get_sentence_model

        model = get_sentence_model()
        if model is None:
            return 0.0
        
        user_norm = _normalize_skills(user_skills)
        job_norm = _normalize_skills(job_skills)
        
        user_skill_embeddings = model.encode(user_norm)
        job_skill_embeddings = model.encode(job_norm)
        
        user_skill_tensor = torch.FloatTensor(user_skill_embeddings)
        job_skill_tensor = torch.FloatTensor(job_skill_embeddings)
        
        job_coverage_scores = []
        for job_emb in job_skill_tensor:
            similarities = F.cosine_similarity(
                job_emb.unsqueeze(0), 
                user_skill_tensor, 
                dim=1
            )
            max_sim = float(torch.max(similarities))
            normalized_sim = (max_sim + 1) / 2
            job_coverage_scores.append(normalized_sim)
        
        return float(np.mean(job_coverage_scores))
    except Exception as e:
        print(f"[RECO] Semantic skill match warning: {e}")
        return 0.0


def _boost_related_skills(user_skills, job_skills, semantic_score):
    if not user_skills or not job_skills:
        return semantic_score, ""
    
    user_norm = _normalize_skills(user_skills)
    job_norm = _normalize_skills(job_skills)
    
    user_set = {s for s in user_norm if s}
    job_set = {s for s in job_norm if s}
    
    boost = 0.0
    reason = ""
    
    if 'express' in user_set and ('node' in job_set or 'node.js' in job_set):
        boost += 0.3
        reason = "Node.js and Express.js are strongly related backend technologies"
    elif ('node' in user_set or 'node.js' in user_set) and 'javascript' in job_set:
        boost += 0.2
        reason = "Node.js and JavaScript are strongly related"
    elif 'python' in user_set and 'django' in job_set:
        boost += 0.3
        reason = "Python and Django are strongly related"
    elif 'react' in user_set and 'javascript' in job_set:
        boost += 0.2
        reason = "React and JavaScript are strongly related"
    
    boosted_score = min(1.0, semantic_score + boost)
    return boosted_score, reason


def experience_score(user_exp, job_exp_required):
    if not job_exp_required:
        return 1.0
    if not user_exp:
        return 0.0
    if isinstance(user_exp, str):
        try:
            m = re.search(r'(\d+)', user_exp)
            user_exp = int(m.group(1)) if m else 0
        except Exception:
            user_exp = 0
            
    if isinstance(job_exp_required, str):
        try:
            m = re.search(r'(\d+)', job_exp_required)
            job_exp_required = int(m.group(1)) if m else 0
        except Exception:
            return 1.0

    if job_exp_required == 0:
        return 1.0
    
    if user_exp >= job_exp_required:
        return 1.0
    else:
        return user_exp / float(job_exp_required)


def _hybrid_score(skill_overlap, related_score, embedding_score, exp_score=1.0, domain_penalty=1.0, exact_match=False):
    embedding_score = min(max(embedding_score, 0), 1)
    overlap_score = min(max(skill_overlap, 0), 1)
    related_score = min(max(related_score, 0), 1)
    
    if not exact_match and related_score > 0.8:
        related_score = 0.8
    
    final_score = (
        0.45 * embedding_score +
        0.30 * overlap_score +
        0.25 * related_score
    )
    final_score = final_score * domain_penalty
    final_score = max(0, min(final_score, 1))
    
    if not exact_match:
        final_score = min(final_score, 0.85)
    
    final_score = min(final_score, 0.99)
    if exact_match:
        final_score = min(final_score, 1.0)
    
    final_score = round(final_score, 2)
    percentage = int(final_score * 100)
    
    return percentage, exact_match


def _get_profile_skills(profile):
    if not profile or not hasattr(profile, 'skills') or not profile.skills:
        return []
    raw = profile.skills
    if isinstance(raw, list):
        return [s.strip().lower() for s in raw if s and s.strip()]
    if isinstance(raw, str):
        return [s.strip().lower() for s in raw.split(',') if s and s.strip()]
    return []


def calculate_match_score(job, profile):
    if not job or not profile:
        return {"job": job, "score": 0, "skill_score": 0, "experience_score": 0, "source": "none"}

    cv_skills = []
    user_exp = getattr(profile, 'experience', 0)
    
    cv_file = getattr(profile, 'cv', None)
    if cv_file and hasattr(cv_file, 'path'):
        try:
            from ai_service.services.cv_parser import parse_cv
            parsed = parse_cv(cv_file.path)
            cv_skills = parsed.get("skills", [])
            user_exp = parsed.get("experience", user_exp)
        except Exception as e:
            print(f"[RECO] Error parsing CV: {e}")

    profile_skills = cv_skills if cv_skills else _get_profile_skills(profile)
    
    if not profile_skills or len(profile_skills) == 0 or (len(profile_skills) == 1 and not profile_skills[0]):
        return {"job": job, "score": 0, "skill_score": 0, "experience_score": 0, "source": "cv" if cv_skills else "profile"}

    job_skills = job.required_skills or []
    user_skills_norm = [s.strip().lower() for s in profile_skills if s and s.strip()]
    job_skills_norm = [s.strip().lower() for s in job_skills if s and s.strip()]
    
    if not _has_any_match(user_skills_norm, job_skills_norm):
        return {
            "job": job,
            "score": 0,
            "direct_matches": [],
            "related_matches": [],
            "skill_score": 0,
            "related_score": 0,
            "experience_score": 0,
            "reason": "no_relation",
            "exact_match": False,
            "embedding": 0,
            "overlap": 0,
            "related": 0,
            "source": "cv" if cv_skills else "profile"
        }
    
    intersection = set(user_skills_norm) & set(job_skills_norm)
    has_taxonomy_match = False
    for js in job_skills_norm:
        related = _TAXONOMY.get(js, set())
        if related & set(user_skills_norm):
            has_taxonomy_match = True
            break
    
    if len(intersection) == 0 and not has_taxonomy_match:
        user_domain = _detect_domain(profile_skills)
        job_domain = _detect_domain(job_skills)
        
        job_title_lower = job.title.lower() if job.title else ""
        user_skills_lower = [s.lower() for s in profile_skills]
        
        if user_domain != 'tech' or job_domain != 'tech':
            if 'architect' in job_title_lower:
                architect_keywords = ['architecture', 'design', 'system design', 'technical design']
                if not any(kw in ' '.join(user_skills_lower) for kw in architect_keywords):
                    return {"job": job, "score": 0, "skill_score": 0, "experience_score": 0, "source": "cv" if cv_skills else "profile"}
            
            if 'engineering' in job_title_lower:
                if not any(kw in ' '.join(user_skills_lower) for kw in ['engineering', 'engineer']):
                    return {"job": job, "score": 0, "skill_score": 0, "experience_score": 0, "source": "cv" if cv_skills else "profile"}
        
        if user_domain != 'other' and job_domain != 'other' and user_domain != job_domain:
            return {"job": job, "score": 0, "skill_score": 0, "experience_score": 0, "source": "cv" if cv_skills else "profile"}

        if not job_skills_norm or not user_skills_norm:
            return {"job": job, "score": 0, "skill_score": 0, "experience_score": 0, "source": "cv" if cv_skills else "profile"}

        try:
            import torch
            import torch.nn.functional as F
            from .embedding_service import get_sentence_model

            model = get_sentence_model()
            if model is None:
                return {"job": job, "score": 0, "skill_score": 0, "experience_score": 0, "source": "cv" if cv_skills else "profile"}

            user_embs = model.encode(user_skills_norm)
            job_embs = model.encode(job_skills_norm)
            user_tensor_skills = torch.FloatTensor(user_embs)
            job_tensor_skills = torch.FloatTensor(job_embs)

            best_per_job_skill = []
            for j_emb in job_tensor_skills:
                sims = F.cosine_similarity(j_emb.unsqueeze(0), user_tensor_skills, dim=1)
                best_per_job_skill.append(float(torch.max(sims)))
            max_semantic = max(((s + 1) / 2 for s in best_per_job_skill), default=0)

            threshold = 0.3
            if max_semantic < threshold:
                return {"job": job, "score": 0, "skill_score": 0, "experience_score": 0, "source": "cv" if cv_skills else "profile"}
        except Exception as e:
            print(f"[RECO] Embedding evaluation warning: {e}")
            return {"job": job, "score": 0, "skill_score": 0, "experience_score": 0, "source": "cv" if cv_skills else "profile"}

    user_domain = _detect_domain(profile_skills)
    job_domain = _detect_domain(job_skills)
    domain_penalty = 0.5 if (user_domain != job_domain and user_domain != 'other' and job_domain != 'other') else 1.0

    try:
        skills_score = _skill_overlap_score(profile_skills, job_skills)
        embedding_score = _semantic_skill_match(profile_skills, job_skills)
        related_score_val, direct_matches, related_matches, exact_match = _related_score(profile_skills, job_skills)
        boosted_embedding_score, reason = _boost_related_skills(profile_skills, job_skills, embedding_score)

        job_exp_map = {'ENTRY': 1, 'MID': 3, 'SENIOR': 5, 'EXECUTIVE': 10}
        job_exp_req = job_exp_map.get(job.experience_level, 2)
        exp_score_val = experience_score(user_exp, job_exp_req)

        final_score, exact_match = _hybrid_score(
            skill_overlap=skills_score,
            related_score=related_score_val,
            embedding_score=boosted_embedding_score,
            exp_score=exp_score_val,
            domain_penalty=domain_penalty,
            exact_match=exact_match
        )

        return {
            "job": job,
            "score": final_score,
            "direct_matches": direct_matches,
            "related_matches": related_matches,
            "skill_score": int(skills_score * 100),
            "related_score": int(related_score_val * 100),
            "experience_score": int(exp_score_val * 100),
            "reason": reason if reason else "matched",
            "exact_match": exact_match,
            "embedding": int(boosted_embedding_score * 100),
            "overlap": int(skills_score * 100),
            "related": int(related_score_val * 100),
            "source": "cv" if cv_skills else "profile"
        }
    except Exception as e:
        traceback.print_exc()
        return {"job": job, "score": 0, "skill_score": 0, "experience_score": 0, "source": "error"}


def get_job_recommendations(profile, top_n=5):
    jobs = list(Job.objects.filter(is_active=True))
    if not jobs:
        return []

    profile_skills = _get_profile_skills(profile)
    if not profile_skills or len(profile_skills) == 0:
        return [{
            "job": job,
            "score": 0,
            "skill_score": 0,
            "experience_score": 0,
            "source": "profile"
        } for job in jobs][:top_n]

    job_scores = []
    for job in jobs:
        try:
            score_data = calculate_match_score(job, profile)
            job_scores.append(score_data)
        except Exception as e:
            job_scores.append({
                "job": job,
                "score": 0,
                "skill_score": 0,
                "experience_score": 0,
                "source": "error"
            })

    job_scores.sort(key=lambda x: x['score'], reverse=True)
    filtered_scores = [js for js in job_scores if js['score'] >= 0.3]
    return filtered_scores[:top_n]
