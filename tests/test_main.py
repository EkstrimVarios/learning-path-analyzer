import pandas as pd
import pytest
import tempfile
import os
from src.main import LearningPathAnalyzer

def test_preprocessing():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("student_id,event_type,timestamp,grade\n")
        f.write("1,login,2025-01-01,85\n")
        f.write("1,submit,2025-01-02,85\n")
        temp_path = f.name

    try:
        analyzer = LearningPathAnalyzer(temp_path)
        assert "activity" in analyzer.df.columns
        assert analyzer.df["activity"].iloc[0] == "login"
        assert analyzer.df["activity"].iloc[1] == "assignment"
    finally:
        os.unlink(temp_path)

def test_summary_output():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("student_id,event_type,timestamp,grade\n")
        f.write("1,submit,2025-01-01,90\n")
        f.write("2,post,2025-01-02,80\n")
        temp_path = f.name

    try:
        analyzer = LearningPathAnalyzer(temp_path)
        summary = analyzer.summary()
        assert "assignment" in summary.index or "forum" in summary.index
        assert "mean" in summary.columns
        assert "count" in summary.columns
    finally:
        os.unlink(temp_path)

def test_correlation_with_grades():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("student_id,event_type,timestamp,grade\n")
        f.write("1,submit,2025-01-01,100\n")
        f.write("1,post,2025-01-02,100\n")
        f.write("2,login,2025-01-01,50\n")
        temp_path = f.name

    try:
        analyzer = LearningPathAnalyzer(temp_path)
        corr = analyzer.correlation_with_grades()
        assert isinstance(corr, pd.Series)
        assert len(corr) >= 1
        # "login" должен быть в данных, даже если корреляция низкая
        assert "login" in corr.index or "assignment" in corr.index
    finally:
        os.unlink(temp_path)

def test_empty_file_raises_error():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        # Ничего не пишем → файл пустой
        temp_path = f.name

    try:
        with pytest.raises(pd.errors.EmptyDataError):
            LearningPathAnalyzer(temp_path)
    finally:
        os.unlink(temp_path)

def test_invalid_event_type():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("student_id,event_type,timestamp,grade\n")
        f.write("1,unknown_event,2025-01-01,75\n")
        temp_path = f.name

    try:
        analyzer = LearningPathAnalyzer(temp_path)
        assert analyzer.df["activity"].iloc[0] == "other"
    finally:
        os.unlink(temp_path)