#!/usr/bin/env python3
"""
Weekly Learning Path Report Generator

This script:
- Loads latest LMS log data (assumed to be in data/latest_logs.csv)
- Runs analysis using the LearningPathAnalyzer
- Saves a visual report (PNG + text summary) into reports/
- Optionally prepares artifacts for GitHub Actions
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
from datetime import datetime
from src.main import LearningPathAnalyzer

# Ensure output directory exists
os.makedirs("reports", exist_ok=True)

def load_latest_data():
    """Load the latest LMS log data."""
    # In real use, this could fetch from an LMS API or S3
    # For this project, we assume data/latest_logs.csv exists
    try:
        return pd.read_csv("data/latest_logs.csv")
    except FileNotFoundError:
        # Fallback to sample data for demo/CI
        print("latest_logs.csv not found. Using sample.csv for report.")
        return pd.read_csv("data/sample.csv")

def generate_static_plot(correlation_series, output_path):
    """Generate a matplotlib bar plot."""
    correlation_series.sort_values().plot(kind='barh', figsize=(8, 5))
    plt.title("Correlation of Activity Types with Final Grade")
    plt.xlabel("Correlation Coefficient")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def generate_interactive_plot(correlation_series, output_path):
    """Generate a Plotly interactive HTML report."""
    fig = px.bar(
        x=correlation_series.values,
        y=correlation_series.index,
        orientation='h',
        title="Activity Impact on Student Performance",
        labels={"x": "Correlation with Grade", "y": "Activity Type"}
    )
    fig.write_html(output_path)

def main():
    print("📊 Generating weekly learning path report...")
    
    # Load data
    df = load_latest_data()
    df.to_csv("data/latest_logs.csv", index=False)  # Ensure it exists for consistency

    # Run analysis
    analyzer = LearningPathAnalyzer("data/latest_logs.csv")
    corr = analyzer.correlation_with_grades()

    # Save text summary
    summary_text = f"""
Learning Path Report — Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}
=============================================================================

Top 3 most impactful activities (by correlation with grade):
{corr.sort_values(ascending=False).head(3).to_string()}

Recommendation:
- Students should prioritize activities with high positive correlation.
- Avoid over-reliance on low-impact actions (e.g., passive logins).

Full correlation breakdown:
{corr.to_string()}
    """.strip()

    with open("reports/summary.txt", "w", encoding="utf-8") as f:
        f.write(summary_text)

    # Generate plots
    generate_static_plot(corr, "reports/activity_correlation.png")
    generate_interactive_plot(corr, "reports/activity_correlation.html")

    print("✅ Report saved to reports/summary.txt, .png, and .html")

if __name__ == "__main__":
    main()