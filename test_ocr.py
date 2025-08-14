from scanner import extract_text

image_path = "C:/Users/Vinitha/Desktop/image.jpg"  # Update this path
product, expiry = extract_text(image_path)
print(f"Product: {product}")
print(f"Expiry Date: {expiry}")
