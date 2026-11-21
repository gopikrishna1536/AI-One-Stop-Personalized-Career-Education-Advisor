"""
Gale-Shapley Mentorship Matching Engine
Computes stable matches between student career mentees and industry mentors.
"""
from typing import Dict, List, Any

class MentorshipMatcher:
    @staticmethod
    def stable_match(mentees_prefs: Dict[str, List[str]], mentors_prefs: Dict[str, List[str]]) -> Dict[str, str]:
        """
        Gale-Shapley deferred acceptance algorithm (mentee-proposing).
        Returns a dict of mentee -> matched mentor.
        """
        free_mentees = list(mentees_prefs.keys())
        mentor_matches: Dict[str, str] = {} # mentor -> mentee
        proposals_made: Dict[str, int] = {m: 0 for m in free_mentees}

        # Precompute mentor ranking lookup for O(1) comparison
        mentor_ranks = {}
        for mentor, prefs in mentors_prefs.items():
            mentor_ranks[mentor] = {mentee: rank for rank, mentee in enumerate(prefs)}

        while free_mentees:
            mentee = free_mentees[0]
            mentee_pref_list = mentees_prefs[mentee]

            if proposals_made[mentee] >= len(mentee_pref_list):
                free_mentees.pop(0)
                continue

            preferred_mentor = mentee_pref_list[proposals_made[mentee]]
            proposals_made[mentee] += 1

            if preferred_mentor not in mentor_matches:
                mentor_matches[preferred_mentor] = mentee
                free_mentees.pop(0)
            else:
                current_match = mentor_matches[preferred_mentor]
                ranks = mentor_ranks.get(preferred_mentor, {})
                if ranks.get(mentee, 999) < ranks.get(current_match, 999):
                    mentor_matches[preferred_mentor] = mentee
                    free_mentees.pop(0)
                    free_mentees.append(current_match)

        # Invert to mentee -> mentor
        return {mentee: mentor for mentor, mentee in mentor_matches.items()}
