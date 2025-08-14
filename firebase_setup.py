import firebase_admin
from firebase_admin import credentials, auth

# Load Firebase credentials
cred = credentials.Certificate(r"C:\Users\Vinitha\Desktop\final\expiry-aef7c-firebase-adminsdk-fbsvc-edf775aa42.json")  # Replace with actual JSON filename
firebase_admin.initialize_app(cred)

print("🔥 Firebase connected successfully!")
