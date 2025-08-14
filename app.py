from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Load Firebase credentials (downloaded from Firebase)
cred = credentials.Certificate(r"C:\\Users\\Vinitha\\Desktop\\final\\expiry-aef7c-firebase-adminsdk-fbsvc-edf775aa42.json")

firebase_admin.initialize_app(cred)

# Initialize Firestore database
db = firestore.client()

@app.route('/')
def home():
    return jsonify({"message": "Firebase Flask API is running!"})

if __name__ == "__main__":
    app.run(debug=True)
