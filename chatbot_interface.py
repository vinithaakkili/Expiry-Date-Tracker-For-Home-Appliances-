import joblib

# Load the trained model
model = joblib.load("chatbot_model.pkl")

# Define fixed replies per intent
intent_responses = {
    "greeting": "Hi! I'm your expiry tracker assistant. How can I help?",
    "scan_help": "To scan a product, click the 'Scan Item' button and upload the image.",
    "view_items": "Go to 'View Items' to see all saved products with expiry dates.",
    "expiry_check": "You can check alerts by clicking 'Check Expiry Alerts'.",
    "thanks": "You're welcome! 😊",
    "farewell": "Goodbye! Stay aware of expiry dates!"
}

def chatbot_reply(user_message):
    predicted_intent = model.predict([user_message])[0]
    return intent_responses.get(predicted_intent, "Sorry, I didn't understand that. Try asking about expiry tracking.")

# Example loop
if __name__ == "__main__":
    print("🤖 Chatbot ready! (Type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            print("Bot: See you again!")
            break
        response = chatbot_reply(user_input)
        print(f"Bot: {response}")
