import cv2
import pytesseract

# Update this with your Tesseract installation path (Windows users)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image_path):
    """Extract text from an image using OCR."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    text = pytesseract.image_to_string(gray)

    # Extract product name & expiry date (basic filtering)
    lines = text.split("\n")
    product_name = lines[0] if lines else "Unknown Product"
    expiry_date = "Not Found"
    
    for line in lines:
        if any(keyword in line.lower() for keyword in ["exp", "expiry", "use by", "best before","best by"]):
            expiry_date = line.strip()
            break
    
    return product_name, expiry_date

# Test the function
if __name__ == "__main__":
    product, expiry = extract_text("sample_image.jpg")
    print(f"Product: {product}\nExpiry Date: {expiry}")
