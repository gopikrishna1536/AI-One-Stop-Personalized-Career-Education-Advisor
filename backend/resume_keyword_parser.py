"""
Resume Keyword Density & ATS Compliance Parser
Evaluates resume text against target job description for keyword match rate and ATS optimization.
"""
import re
from typing import Dict, List, Set, Any

class ResumeKeywordParser:
    STOPWORDS = {"and", "the", "in", "to", "of", "with", "for", "a", "an", "on", "at", "by", "is", "as", "our", "we"}

    def extract_keywords(self, text: str) -> List[str]:
        tokens = re.findall(r"[a-zA-Z0-9_\+#\.-]+", text.lower())
        return [t for t in tokens if len(t) > 1 and t not in self.STOPWORDS]

    def score_resume(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        resume_tokens = self.extract_keywords(resume_text)
        jd_tokens = self.extract_keywords(job_description)

        resume_set: Set[str] = set(resume_tokens)
        jd_freq: Dict[str, int] = {}
        for t in jd_tokens:
            jd_freq[t] = jd_freq.get(t, 0) + 1

        top_jd_keywords = sorted(jd_freq.items(), key=lambda x: x[1], reverse=True)[:20]
        top_keys = [k for k, _ in top_jd_keywords]

        matched = [k for k in top_keys if k in resume_set]
        missing = [k for k in top_keys if k not in resume_set]

        match_score = (len(matched) / len(top_keys) * 100.0) if top_keys else 100.0

        return {
            "ats_match_percentage": round(match_score, 1),
            "matched_keywords": matched,
            "missing_keywords": missing,
            "total_resume_words": len(resume_tokens),
            "is_ats_friendly": match_score >= 65.0
        }
