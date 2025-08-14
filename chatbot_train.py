import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Sample training data: user messages and their intent labels
training_data = [
    ("hello", "greeting"),
    ("hi", "greeting"),
    ("hey", "greeting"),
    ("how are you", "greeting"),
    ("how do I scan a product", "scan_help"),
    ("how to scan", "scan_help"),
    ("where do I upload image", "scan_help"),
    ("show me the items", "view_items"),
    ("what items are stored", "view_items"),
    ("list products", "view_items"),
    ("what is expiring", "expiry_check"),
    ("check expiry", "expiry_check"),
    ("what's about expiry alert", "expiry_check"),
    ("thank you", "thanks"),
    ("thanks", "thanks"),
    ("bye", "farewell"),
    ("goodbye", "farewell")
]

# Split data
texts, labels = zip(*training_data)

# Create a pipeline: TF-IDF + Logistic Regression
model = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LogisticRegression())
])

# Train the model
model.fit(texts, labels)

# Save the model
joblib.dump(model, "chatbot_model.pkl")
print("✅ Model trained and saved as chatbot_model.pkl")
