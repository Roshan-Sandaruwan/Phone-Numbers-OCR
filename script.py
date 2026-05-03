import cv2
import pytesseract
import re
import os
import csv

# Path to your image folder
folder_path = "images"

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

all_numbers = []

for filename in os.listdir(folder_path):
    if filename.endswith((".png", ".jpg", ".jpeg")):
        img_path = os.path.join(folder_path, filename)
        
        print(f"\nProcessing: {filename}")

        # Read image
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # OCR
        text = pytesseract.image_to_string(gray)

        # Extract phone numbers
        numbers = re.findall(r'\+?\d[\d\s\-]{8,15}\d', text)

        print("Found:", numbers)

        for num in numbers:
            cleaned = re.sub(r"[^\d+]", "", num)  # clean number
            all_numbers.append([filename, cleaned])  # store with image name

# Remove duplicates
unique_numbers = list({tuple(row) for row in all_numbers})

# Save to CSV
with open("phone_numbers.csv", "w", newline="") as file:
    writer = csv.writer(file)
    
    # Header
    writer.writerow(["Image Name", "Phone Number"])
    
    # Data
    writer.writerows(unique_numbers)

print("\n✅ CSV file saved as phone_numbers.csv")