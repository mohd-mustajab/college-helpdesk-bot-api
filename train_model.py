import json
import random
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load intents
with open("data/intents.json", "r", encoding="utf-8") as f:
    intents = json.load(f)["intents"]

# Prepare training data
X = []
y = []

for intent in intents:
    for pattern in intent["patterns"]:
        X.append(pattern.lower())
        y.append(intent["tag"])

# Vectorize text
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# Train model
clf = LogisticRegression(max_iter=1000)
clf.fit(X_vec, y)

# Save model
joblib.dump(vectorizer, "models/vectorizer.joblib")
joblib.dump(clf, "models/classifier.joblib")

print("✅ Model trained and saved successfully!")
