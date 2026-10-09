"""
Natural Language Skill Extraction Service

This service allows employers to describe job requirements in natural language
(e.g., "I want backend developer") and automatically extracts relevant skills
using semantic similarity with a predefined skill taxonomy.
"""

import numpy as np
from typing import List, Dict, Tuple
import re

# Import the lazy model getter from embedding_service
from .embedding_service import get_sentence_model

# Comprehensive skill taxonomy for extraction
SKILL_TAXONOMY = {
    # Backend Development
    'backend developer': ['python', 'django', 'flask', 'fastapi', 'node.js', 'express', 'java', 'spring', 'spring boot', 'ruby', 'rails', 'php', 'laravel', 'go', 'golang', 'c#', '.net', 'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'api', 'rest api', 'graphql', 'microservices'],
    'backend': ['python', 'django', 'flask', 'fastapi', 'node.js', 'express', 'java', 'spring', 'spring boot', 'ruby', 'rails', 'php', 'laravel', 'go', 'golang', 'c#', '.net', 'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'api', 'rest api', 'graphql', 'microservices'],
    
    # Frontend Development
    'frontend developer': ['javascript', 'react', 'vue', 'angular', 'typescript', 'html', 'css', 'next.js', 'nuxt.js', 'redux', 'webpack', 'tailwind', 'sass', 'jquery'],
    'frontend': ['javascript', 'react', 'vue', 'angular', 'typescript', 'html', 'css', 'next.js', 'nuxt.js', 'redux', 'webpack', 'tailwind', 'sass', 'jquery'],
    
    # Full Stack
    'full stack developer': ['javascript', 'react', 'vue', 'angular', 'typescript', 'python', 'django', 'flask', 'node.js', 'express', 'sql', 'postgresql', 'mysql', 'mongodb', 'git', 'docker', 'aws', 'rest api', 'graphql'],
    'full stack': ['javascript', 'react', 'vue', 'angular', 'typescript', 'python', 'django', 'flask', 'node.js', 'express', 'sql', 'postgresql', 'mysql', 'mongodb', 'git', 'docker', 'aws', 'rest api', 'graphql'],
    
    # Mobile Development
    'mobile developer': ['react native', 'flutter', 'swift', 'kotlin', 'android', 'ios', 'mobile', 'xamarin', 'ionic', 'cordova'],
    'android developer': ['android', 'kotlin', 'java', 'android studio', 'gradle', 'sdk'],
    'ios developer': ['ios', 'swift', 'objective-c', 'xcode', 'cocoa touch', 'swiftui'],
    
    # DevOps & Cloud
    'devops engineer': ['docker', 'kubernetes', 'aws', 'azure', 'gcp', 'ci/cd', 'jenkins', 'gitlab', 'terraform', 'ansible', 'linux', 'bash', 'python', 'monitoring', 'logging'],
    'cloud engineer': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'ansible', 'linux', 'networking', 'security'],
    'sre': ['docker', 'kubernetes', 'aws', 'azure', 'gcp', 'monitoring', 'logging', 'linux', 'python', 'go', 'incident management'],
    
    # Data Science & ML
    'data scientist': ['python', 'pandas', 'numpy', 'machine learning', 'tensorflow', 'pytorch', 'scikit-learn', 'statistics', 'sql', 'data visualization', 'jupyter', 'r'],
    'machine learning engineer': ['python', 'tensorflow', 'pytorch', 'scikit-learn', 'mlops', 'docker', 'kubernetes', 'aws', 'deep learning', 'nlp', 'computer vision'],
    'data engineer': ['python', 'sql', 'etl', 'data pipeline', 'apache spark', 'hadoop', 'airflow', 'kafka', 'aws', 'azure', 'gcp', 'postgresql', 'mongodb'],
    
    # Web Development (General)
    'web developer': ['javascript', 'html', 'css', 'react', 'vue', 'angular', 'node.js', 'python', 'django', 'php', 'sql', 'git', 'rest api'],
    
    # Database
    'database administrator': ['sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'oracle', 'database administration', 'backup', 'replication', 'performance tuning'],
    
    # Security
    'security engineer': ['cybersecurity', 'network security', 'penetration testing', 'security analysis', 'python', 'linux', 'aws', 'azure', 'gcp', 'incident response'],
    
    # QA & Testing
    'qa engineer': ['testing', 'selenium', 'junit', 'test automation', 'quality assurance', 'python', 'java', 'javascript', 'ci/cd'],
    
    # Project Management
    'project manager': ['agile', 'scrum', 'project management', 'jira', 'confluence', 'leadership', 'communication', 'planning'],
    
    # UI/UX Design
    'ui designer': ['figma', 'sketch', 'adobe xd', 'ui design', 'user interface', 'prototyping', 'design systems'],
    'ux designer': ['user research', 'wireframing', 'prototyping', 'user testing', 'figma', 'sketch', 'ux design', 'user experience'],
    
    # Specific Technologies
    'python developer': ['python', 'django', 'flask', 'fastapi', 'pandas', 'numpy', 'sql', 'postgresql', 'mongodb', 'git'],
    'javascript developer': ['javascript', 'react', 'vue', 'angular', 'node.js', 'express', 'typescript', 'html', 'css'],
    'java developer': ['java', 'spring', 'spring boot', 'maven', 'gradle', 'sql', 'postgresql', 'mysql', 'git'],
    'php developer': ['php', 'laravel', 'symfony', 'composer', 'mysql', 'postgresql', 'git'],
    'react developer': ['javascript', 'react', 'redux', 'typescript', 'next.js', 'html', 'css', 'webpack'],
    'vue developer': ['javascript', 'vue', 'vuex', 'typescript', 'nuxt.js', 'html', 'css', 'vite'],
    'angular developer': ['typescript', 'angular', 'rxjs', 'html', 'css', 'javascript'],
}

# Flatten the taxonomy for easier lookup
ALL_SKILLS = set()
for skills in SKILL_TAXONOMY.values():
    ALL_SKILLS.update(skills)


def extract_skills_from_description(description: str, threshold: float = 0.6, top_k: int = 10) -> List[Dict]:
    """
    Extract relevant skills from a natural language job description.
    
    Args:
        description: Natural language description (e.g., "I want backend developer")
        threshold: Semantic similarity threshold (0-1)
        top_k: Maximum number of skills to return
    
    Returns:
        List of dicts with skill name and similarity score
    """
    if not description:
        return []
    
    # Preprocess description
    description_clean = description.lower().strip()
    
    # Check for direct keyword matches using regex boundaries
    direct_matches = []
    for role, skills in SKILL_TAXONOMY.items():
        pattern = r'\b' + re.escape(role) + r'\b'
        if re.search(pattern, description_clean):
            direct_matches.extend([(skill, 1.0) for skill in skills])
    
    # If direct matches found, deduplicate and return
    if direct_matches:
        seen = set()
        unique_matches = []
        for skill, score in direct_matches:
            if skill not in seen:
                seen.add(skill)
                unique_matches.append({'skill': skill, 'similarity': score})
        return unique_matches[:top_k]
    
    model = get_sentence_model()
    
    # Fallback to semantic similarity if model is available
    if model is None:
        return []
    
    try:
        import torch
        import torch.nn.functional as F

        # Encode description & skills
        description_embedding = model.encode([description_clean])
        description_tensor = torch.FloatTensor(description_embedding)
        
        all_skills_list = list(ALL_SKILLS)
        skill_embeddings = model.encode(all_skills_list)
        skill_tensor = torch.FloatTensor(skill_embeddings)
        
        # Calculate cosine similarity
        similarities = F.cosine_similarity(description_tensor, skill_tensor, dim=1)
        
        # Normalize scores from [-1, 1] to [0, 1]
        similarities_np = similarities.numpy()
        similarities_normalized = (similarities_np + 1) / 2
        
        # Rank matches above threshold
        top_indices = np.argsort(similarities_normalized)[::-1]
        top_matches = []
        
        for idx in top_indices:
            similarity = float(similarities_normalized[idx])
            if similarity >= threshold and len(top_matches) < top_k:
                top_matches.append({
                    'skill': all_skills_list[idx],
                    'similarity': round(similarity, 4)
                })
        
        return top_matches
    except Exception as e:
        print(f"Error during skill embedding extraction: {e}")
        return []


def suggest_skills_from_partial(partial: str, top_k: int = 5) -> List[str]:
    """
    Suggest skills based on partial input (autocomplete).
    
    Args:
        partial: Partial skill name or description
        top_k: Number of suggestions to return
    
    Returns:
        List of skill suggestions
    """
    if not partial:
        return []
    
    partial_clean = partial.lower().strip()
    
    # Direct prefix matches
    prefix_matches = [skill for skill in ALL_SKILLS if skill.startswith(partial_clean)]
    if prefix_matches:
        return prefix_matches[:top_k]
    
    model = get_sentence_model()
    
    # Fallback to semantic suggestions
    if model is None:
        return []
    
    try:
        import torch
        import torch.nn.functional as F

        partial_embedding = model.encode([partial_clean])
        partial_tensor = torch.FloatTensor(partial_embedding)
        
        all_skills_list = list(ALL_SKILLS)
        skill_embeddings = model.encode(all_skills_list)
        skill_tensor = torch.FloatTensor(skill_embeddings)
        
        similarities = F.cosine_similarity(partial_tensor, skill_tensor, dim=1)
        similarities_normalized = (similarities.numpy() + 1) / 2
        
        top_indices = np.argsort(similarities_normalized)[::-1]
        return [all_skills_list[idx] for idx in top_indices[:top_k]]
    except Exception as e:
        print(f"Error suggesting skills: {e}")
        return []


def get_role_skills(role: str) -> List[str]:
    """
    Get skills associated with a specific role.
    
    Args:
        role: Role name (e.g., "backend developer")
    
    Returns:
        List of skills for that role
    """
    if not role:
        return []

    role_clean = role.lower().strip()
    
    # Direct match
    if role_clean in SKILL_TAXONOMY:
        return SKILL_TAXONOMY[role_clean]
    
    # Partial match
    for key, skills in SKILL_TAXONOMY.items():
        if role_clean in key or key in role_clean:
            return skills
    
    return []


def enhance_job_skills(description: str, existing_skills: List[str] = None) -> List[str]:
    """
    Enhance existing skills with semantically extracted skills from description.
    
    Args:
        description: Job description
        existing_skills: List of already specified skills
    
    Returns:
        Combined list of unique skills
    """
    extracted = extract_skills_from_description(description, threshold=0.5, top_k=15)
    extracted_skills = [item['skill'] for item in extracted]
    
    if existing_skills:
        combined = list(dict.fromkeys(existing_skills + extracted_skills))
        return combined
    
    return extracted_skills
