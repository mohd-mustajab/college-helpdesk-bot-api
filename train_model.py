import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Load intents
with open("data/intents.json", "r") as f:
    data = json.load(f)

corpus, labels = [], []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        corpus.append(pattern.lower())
        labels.append(intent["tag"])

# Vectorize
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)
y = np.array(labels)

# Train model
model = LogisticRegression()
model.fit(X, y)

# Save model
joblib.dump(vectorizer, "models/vectorizer.joblib")
joblib.dump(model, "models/classifier.joblib")

print("✅ Model training complete! Files saved in models/")
