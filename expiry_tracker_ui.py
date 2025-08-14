import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, scrolledtext
import cv2
import pytesseract
import speech_recognition as sr
import threading
from datetime import datetime, timedelta
from database import add_item, get_items
# Configure Tesseract path (Windows users)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Initialize main Tkinter window
root = ttk.Window(themename="superhero")  
root.title("Expiry Date Tracker")
root.geometry("700x500")
# Function to switch between screens
def show_frame(frame):
    frame.tkraise()
# Function to scan an image using OCR
def scan_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return
    image = cv2.imread(file_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    # Extract product name and expiry date
    lines = text.split("\n")
    product_name = lines[0] if lines else "Unknown Product"
    expiry_date = "Not Found"
    for line in lines:
        if any(keyword in line.lower() for keyword in ["exp", "expiry", "use by", "best before"]):
            expiry_date = line.strip()
            break
    add_item(product_name, expiry_date)
    messagebox.showinfo("Item Added", f"Product: {product_name}\nExpiry Date: {expiry_date}")
# Function to load items from database
def load_items():
    items = get_items()
    items_text = "\n".join([f"{name} - {expiry}" for name, expiry in items]) if items else "No items yet."
    items_display.config(state="normal")
    items_display.delete("1.0", "end")
    items_display.insert("1.0", items_text)
    items_display.config(state="disabled")
# Function to check and display expiry alerts
def check_expiry_alerts():
    items = get_items()
    alert_items = []
    today = datetime.today()
    # Check if items are nearing expiry (e.g., 7 days before expiry)
    for name, expiry in items:
        try:
            expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
            if expiry_date - today <= timedelta(days=7):  # Expiry within 7 days
                alert_items.append(f"{name} - Expiry: {expiry}")
        except ValueError:
            continue  # Skip items with invalid expiry date format
    return alert_items
# Function to update the expiry alerts on the expiry alerts screen
def update_expiry_alerts():
    alert_items = check_expiry_alerts()
    if alert_items:
        alerts_text = "\n".join(alert_items)
    else:
        alerts_text = "No items are nearing expiry."
    expiry_alerts_display.config(state="normal")
    expiry_alerts_display.delete("1.0", "end")
    expiry_alerts_display.insert("1.0", alerts_text)
    expiry_alerts_display.config(state="disabled")
# Create container frame
container = ttk.Frame(root)
container.pack(fill="both", expand=True)
# Define frames for each page
frames = {}
for screen in ("home", "add_item", "view_items", "chatbot", "expiry_alerts"):
    frame = ttk.Frame(container)
    frames[screen] = frame
    frame.grid(row=0, column=0, sticky="nsew")
# ------------ Home Screen ------------
home_frame = frames["home"]
ttk.Label(home_frame, text="Expiry Date Tracker", font=("Arial", 24, "bold"), bootstyle=PRIMARY).pack(pady=10)
# Buttons for home screen
ttk.Button(home_frame, text="📷 Scan Item", bootstyle=SUCCESS, command=lambda: show_frame(frames["add_item"])).pack(pady=5)
ttk.Button(home_frame, text="📜 View Items", bootstyle=INFO, command=lambda: [show_frame(frames["view_items"]), load_items()]).pack(pady=5)
ttk.Button(home_frame, text="🤖 Chatbot", bootstyle=WARNING, command=lambda: show_frame(frames["chatbot"])).pack(pady=5)
ttk.Button(home_frame, text="🔔 Check Expiry Alerts", bootstyle=INFO, command=lambda: [show_frame(frames["expiry_alerts"]), update_expiry_alerts()]).pack(pady=5)
ttk.Button(home_frame, text="❌ Exit", bootstyle=DANGER, command=root.quit).pack(pady=5)
# ------------ Add Item Screen ------------
add_item_frame = frames["add_item"]
ttk.Label(add_item_frame, text="📷 Add New Item", font=("Arial", 20, "bold")).pack(pady=10)
ttk.Button(add_item_frame, text="🔍 Scan Image", bootstyle=SUCCESS, command=scan_image).pack(pady=10)
ttk.Button(add_item_frame, text="⬅ Go Back", bootstyle=SECONDARY, command=lambda: show_frame(frames["home"])).pack(pady=10)
# ------------ View Items Screen ------------
view_items_frame = frames["view_items"]
ttk.Label(view_items_frame, text="📜 Stored Items", font=("Arial", 20, "bold")).pack(pady=10)
items_display = scrolledtext.ScrolledText(view_items_frame, width=60, height=10, state="disabled", font=("Arial", 12))
items_display.pack(pady=5)
ttk.Button(view_items_frame, text="⬅ Go Back", bootstyle=SECONDARY, command=lambda: show_frame(frames["home"])).pack(pady=10)
# ------------ Chatbot Screen ------------
chatbot_frame = frames["chatbot"]
ttk.Label(chatbot_frame, text="🤖 Chatbot (Voice & Text)", font=("Arial", 20, "bold")).pack(pady=10)
chat_input = ttk.Entry(chatbot_frame, width=50)
chat_input.pack(pady=5)
# Chat history display
chat_history = scrolledtext.ScrolledText(chatbot_frame, width=60, height=10, state="disabled", font=("Arial", 12))
chat_history.pack(pady=5)
def chatbot_reply(user_message):
    """Generate a chatbot response based on simple rules."""
    user_message = user_message.lower()
    if "hello" in user_message:
        return "Hi! How can I assist you today?"
    elif "expiry" in user_message:
        return "You can scan an item to check its expiry date!"
    elif "thank you" in user_message:
        return "You're welcome! 😊"
    else:
        return "I'm still learning. Ask me about expiry tracking!"
def send_message():
    """Process user text input."""
    user_message = chat_input.get().strip()
    if user_message:
        response = chatbot_reply(user_message)
        display_message(f"You: {user_message}\nBot: {response}\n")
        chat_input.delete(0, "end")
def display_message(message):
    """Display chatbot messages in chat history."""
    chat_history.config(state="normal")
    chat_history.insert("end", message + "\n")
    chat_history.config(state="disabled")
    chat_history.yview("end")
def recognize_voice():
    """Use voice recognition to capture user input."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        display_message("🎙️ Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            user_message = recognizer.recognize_google(audio)
            display_message(f"You (Voice): {user_message}")
            response = chatbot_reply(user_message)
            display_message(f"Bot: {response}")
        except sr.UnknownValueError:
            display_message("Bot: Sorry, I couldn't understand that.")
        except sr.RequestError:
            display_message("Bot: Voice service is unavailable.")
# Buttons for chatbot actions
ttk.Button(chatbot_frame, text="💬 Send", bootstyle=PRIMARY, command=send_message).pack(pady=5)
ttk.Button(chatbot_frame, text="🎤 Voice Input", bootstyle=WARNING, command=lambda: threading.Thread(target=recognize_voice, daemon=True).start()).pack(pady=5)
ttk.Button(chatbot_frame, text="⬅ Go Back", bootstyle=SECONDARY, command=lambda: show_frame(frames["home"])).pack(pady=10)
# ------------ Expiry Alerts Screen ------------
expiry_alerts_frame = frames["expiry_alerts"]
ttk.Label(expiry_alerts_frame, text="🔔 Expiry Alerts", font=("Arial", 20, "bold")).pack(pady=10)
# Expiry alerts display
expiry_alerts_display = scrolledtext.ScrolledText(expiry_alerts_frame, width=60, height=10, state="disabled", font=("Arial", 12))
expiry_alerts_display.pack(pady=10)
ttk.Button(expiry_alerts_frame, text="⬅ Go Back", bootstyle=SECONDARY, command=lambda: show_frame(frames["home"])).pack(pady=10)
# Show home screen initially
show_frame(frames["home"])
# Start Tkinter main loop
root.mainloop()