import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, scrolledtext
import cv2
import pytesseract
import speech_recognition as sr
import threading
import sqlite3
import datetime
import time

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

# Function to check for expiry notifications
def check_expiry():
    conn = sqlite3.connect("expiry_tracker.db")
    cursor = conn.cursor()

    today = datetime.date.today()
    three_days_later = today + datetime.timedelta(days=3)

    cursor.execute("SELECT name, expiry_date FROM items")
    items = cursor.fetchall()

    expiring_soon = []
    for name, expiry in items:
        try:
            expiry_date = datetime.datetime.strptime(expiry, "%Y-%m-%d").date()
            if today <= expiry_date <= three_days_later:
                expiring_soon.append(f"{name} - {expiry}")
        except ValueError:
            continue

    conn.close()

    if expiring_soon:
        reminder_text = "⚠ Expiring Soon:\n" + "\n".join(expiring_soon)
        messagebox.showwarning("Expiry Reminder", reminder_text)

# Background thread to check expiry every 10 minutes
def start_expiry_checker():
    def expiry_thread():
        while True:
            check_expiry()
            time.sleep(600)  # 10 minutes

    threading.Thread(target=expiry_thread, daemon=True).start()

# Create container frame
container = ttk.Frame(root)
container.pack(fill="both", expand=True)

# Define frames for each page
frames = {}
for screen in ("home", "add_item", "view_items", "chatbot"):
    frame = ttk.Frame(container)
    frames[screen] = frame
    frame.grid(row=0, column=0, sticky="nsew")

# ------------ Home Screen ------------
home_frame = frames["home"]
ttk.Label(home_frame, text="Expiry Date Tracker", font=("Arial", 24, "bold"), bootstyle=PRIMARY).pack(pady=10)

# Expiry alert section
expiry_alert = ttk.Label(home_frame, text="Checking for expiry alerts...", font=("Arial", 12), bootstyle=WARNING)
expiry_alert.pack(pady=5)

def update_expiry_alert():
    conn = sqlite3.connect("expiry_tracker.db")
    cursor = conn.cursor()
    
    today = datetime.date.today()
    three_days_later = today + datetime.timedelta(days=3)

    cursor.execute("SELECT name, expiry_date FROM items")
    items = cursor.fetchall()
    
    expiring_soon = []
    for name, expiry in items:
        try:
            expiry_date = datetime.datetime.strptime(expiry, "%Y-%m-%d").date()
            if today <= expiry_date <= three_days_later:
                expiring_soon.append(f"{name} - {expiry}")
        except ValueError:
            continue

    conn.close()

    if expiring_soon:
        expiry_alert.config(text="⚠ Expiring Soon:\n" + "\n".join(expiring_soon))
    else:
        expiry_alert.config(text="✅ No upcoming expiries")

ttk.Button(home_frame, text="📷 Scan Item", bootstyle=SUCCESS, command=lambda: show_frame(frames["add_item"])).pack(pady=5)
ttk.Button(home_frame, text="📜 View Items", bootstyle=INFO, command=lambda: [show_frame(frames["view_items"]), load_items()]).pack(pady=5)
ttk.Button(home_frame, text="🤖 Chatbot", bootstyle=WARNING, command=lambda: show_frame(frames["chatbot"])).pack(pady=5)
ttk.Button(home_frame, text="🔔 Check Expiry Alerts", bootstyle=PRIMARY, command=update_expiry_alert).pack(pady=5)
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

# ------------ Start Background Task ------------
start_expiry_checker()

# Show home screen initially
show_frame(frames["home"])

# Start Tkinter main loop
root.mainloop()
