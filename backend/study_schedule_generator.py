"""
Weekly Study Schedule & Pomodoro Distribution Engine
Generates balanced weekly study blocks respecting user time commitments.
"""
from typing import List, Dict, Any

class StudyScheduleGenerator:
    DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    @staticmethod
    def generate_schedule(topics: List[Dict[str, Any]], available_hours_per_day: Dict[str, float]) -> Dict[str, Any]:
        schedule = {d: [] for d in StudyScheduleGenerator.DAYS}
        topic_idx = 0

        for day in StudyScheduleGenerator.DAYS:
            avail_hours = available_hours_per_day.get(day, 0.0)
            pomodoro_slots = int(avail_hours * 2) # 25 min pomodoros per hour approx 2

            for _ in range(pomodoro_slots):
                if not topics:
                    break
                topic = topics[topic_idx % len(topics)]
                schedule[day].append({
                    "topic": topic["name"],
                    "duration_minutes": 25,
                    "break_minutes": 5
                })
                topic_idx += 1

        total_sessions = sum(len(sessions) for sessions in schedule.values())
        return {
            "total_pomodoro_sessions": total_sessions,
            "total_study_hours": round(total_sessions * 0.5, 1),
            "weekly_schedule": schedule
        }
