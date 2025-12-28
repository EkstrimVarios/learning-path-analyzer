import pandas as pd
import numpy as np
from .utils import parse_lms_event

class LearningPathAnalyzer:
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)
        self._preprocess()

    def _preprocess(self):
        # Пример: колонки: student_id, event_type, timestamp, grade
        self.df["activity"] = self.df["event_type"].apply(parse_lms_event)
        self.df["timestamp"] = pd.to_datetime(self.df["timestamp"])

    def summary(self):
        # Простой анализ: средняя оценка по типу активности
        by_activity = self.df.groupby("activity")["grade"].agg(["mean", "count"])
        return by_activity

    def correlation_with_grades(self):
        # Псевдо-корреляция по количеству событий
        activity_counts = self.df.groupby(["student_id", "activity"]).size().unstack(fill_value=0)
        grades = self.df.groupby("student_id")["grade"].mean()
        merged = activity_counts.join(grades)
        return merged.corr()["grade"].drop("grade")