import sqlite3
from datetime import datetime, timedelta
from plyer import notification

def check_expiry():
    """Checks for items expiring tomorrow and sends notifications."""
    conn = sqlite3.connect("expiry_tracker.db")
    cursor = conn.cursor()
    
    # Get today's date and tomorrow's date
    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)
    
    # Fetch items expiring tomorrow
    cursor.execute("SELECT name, expiry_date FROM items")
    items = cursor.fetchall()
    conn.close()

    for name, expiry_date in items:
        try:
            exp_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()
            if exp_date == tomorrow:
                send_notification(name, expiry_date)
        except ValueError:
            pass  # Ignore invalid date formats

def send_notification(name, expiry_date):
    """Sends a desktop/mobile notification."""
    notification.notify(
        title="Expiry Reminder",
        message=f"{name} expires on {expiry_date}. Please use it soon!",
        timeout=10
    )

if __name__ == "__main__":
    check_expiry()

