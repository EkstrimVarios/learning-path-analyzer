import pandas as pd
import pytest
from src.main import LearningPathAnalyzer

def test_preprocessing():
    df = pd.DataFrame({
        "student_id": [1, 1],
        "event_type": ["login", "submit"],
        "timestamp": ["2025-01-01", "2025-01-02"],
        "grade": [85, 90]
    })
    df.to_csv("tests/test_data.csv", index=False)
    analyzer = LearningPathAnalyzer("tests/test_data.csv")
    assert "activity" in analyzer.df.columns
    assert analyzer.df["activity"].iloc[1] == "assignment"

def test_summary():
    # аналогично — создай временный CSV
    pass

def test_correlation():
    pass

# Добавь ещё 2-3 теста → легко набирается 5