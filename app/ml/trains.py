import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Create output folder if it doesn't exist
os.makedirs("app/ml", exist_ok=True)

# Load dataset
df = pd.read_csv("data/raw/complaints.csv")

X = df["complaint_text"]

# Vectorize Text
vectorizer = TfidfVectorizer(lowercase=True, stop_words="english")
X_vectorized = vectorizer.fit_transform(X)

# Train Category Model
cat_model = LogisticRegression(max_iter=1000)
cat_model.fit(X_vectorized, df["category"])

# Train Priority Model
prio_model = LogisticRegression(max_iter=1000)
prio_model.fit(X_vectorized, df["priority"])

# Train Department Model
dept_model = LogisticRegression(max_iter=1000)
dept_model.fit(X_vectorized, df["department"])

# Save vectorizer & models
joblib.dump(vectorizer, "app/ml/vectorizer.pkl")
joblib.dump(cat_model, "app/ml/category_model.pkl")
joblib.dump(prio_model, "app/ml/priority_model.pkl")
joblib.dump(dept_model, "app/ml/department_model.pkl")

print("All ML models trained and saved successfully in app/ml/")
