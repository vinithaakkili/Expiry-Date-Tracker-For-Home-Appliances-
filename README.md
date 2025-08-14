# Expiry Date Tracker for Home Appliances

A Python-based application to track the expiry dates of home appliances and household essentials.  
The app combines **OCR-based scanning**, **AI-powered expiry predictions**, **reminders**, and an **interactive chatbot** in a single user-friendly package.

---

##  Features
- **OCR-Based Scanning** (`scanner.py`, `test_ocr.py`)  
  Extracts product names and expiry dates from labels using Tesseract OCR.
- **AI Chatbot** (`chatbot_interface.py`, `chatbot_train.py`)  
  Interactive chatbot to assist users with expiry information and app guidance.
- **Reminders & Alerts** (`reminder.py`)  
  Sends notifications when items are about to expire.
- **Data Storage** (`database.py`, `expiry_tracker.db`)  
  Uses SQLite to store item details locally.
- **User Interface** (`expiry_tracker_ui.py`, `expiry_tracker.kv`)  
  Simple UI for adding, viewing, and managing items.
- **Manual Entry Option**  
  Add product details manually when OCR is not possible.

## 🛠️ Tech Stack / Tools Used
- **Language:** Python
- **UI Framework:** Tkinter & Kivy (`.kv` file for layout)
- **Database:** SQLite
- **OCR:** `pytesseract`
- **Machine Learning / AI:** Chatbot training scripts in Python
- **Notifications:** `plyer` / email via `smtplib`
- **Version Control:** Git & GitHub

