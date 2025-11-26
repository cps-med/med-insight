# med-ml

AI and Machine learning layer

## Overview

**med-ml** is the artificial intelligence and machine learning engine of the Med-Insight application. It is responsible for transforming cleaned and structured clinical data into predictive models, risk assessments, and data-driven insights.  

This subsystem is implemented using a Python-based AI/ML stack consistent with the rest of the Med-Insight architecture. It uses widely adopted tools and libraries such as Pandas, NumPy, scikit-learn, XGBoost, PyTorch, and MLflow for experiment tracking and model lifecycle management.

As the intelligence layer of the platform, med-ml transforms raw data into actionable predictions and recommendations. Its models and scored outputs are consumed by downstream components, such as the **med-view** dashboard and reporting tool.