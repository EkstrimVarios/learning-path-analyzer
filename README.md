# Learning Path Analyzer
![Tests](https://github.com/EkstrimVarios/learning-path-analyzer/workflows/Tests%20and%20Code%20Quality/badge.svg)
![Weekly Report](https://github.com/EkstrimVarios/learning-path-analyzer/workflows/Weekly%20Learning%20Report/badge.svg)

## Description
Система анализа пути обучения студента на основе логов LMS (Moodle, Canvas и др.).  
Определяет, какие типы активностей (входы, сдача заданий, форумы, тесты) **наиболее сильно коррелируют с высокой успеваемостью**, и даёт персонализированные рекомендации.

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup
```bash
git clone https://github.com/EkstrimVarios/learning-path-analyzer
cd learning-path-analyzer
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt