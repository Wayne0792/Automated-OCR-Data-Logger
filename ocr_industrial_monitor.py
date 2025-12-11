import cv2
import numpy as np
import pyautogui
import pytesseract
import time
import pandas as pd
import os
from datetime import datetime
import re

# --- CONFIGURATION FOR INDUSTRIAL MONITORING ---

# Set your Tesseract path here (if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# NEW: ROI for the Digital Gauge/Meter Display (x, y, w, h)
# You MUST update these coordinates to point to the number display area on your screen
GAUGE_DISPLAY_ROI = (650, 560, 700, 120) 

# Output CSV file name for the logged data
OUTPUT_LOG_FILE = 'industrial_meter_readings.csv'
MIN_CONFIDENCE_THRESHOLD = 75 # Only log readings if Tesseract is this confident or higher
LOGGING_INTERVAL = 1.0 # Check the display every 1.0 seconds

# --- Utility Functions ---

def initialize_log_file(filename: str):
    """Initializes the CSV log file with headers if it doesn't exist."""
    if not os.path.exists(filename):
        df = pd.DataFrame(columns=['Timestamp', 'Reading', 'Confidence', 'Source_Image'])
        df.to_csv(filename, index=False)
        print(f"Initialized new log file: {filename}")

def log_reading(timestamp, reading, confidence, image_name, log_filename):
    """Appends a new reading to the CSV log."""
    new_entry = pd.DataFrame([{'Timestamp': timestamp, 
                               'Reading': reading, 
                               'Confidence': confidence, 
                               'Source_Image': image_name}])
    new_entry.to_csv(log_filename, mode='a', header=False, index=False)
    print(f"[{timestamp}] ✅ Logged: {reading} (Conf: {confidence}%)")

def monitor_and_log_gauge(roi: tuple, log_filename: str):
    """
    Continuously monitors the defined ROI, extracts numerical data, and logs 
    valid readings to a CSV file.
    """
    last_logged_reading = ""
    
    print("\n--- Starting Industrial Gauge Monitor (Press Ctrl+C to stop) ---")

    try:
        while True:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # 1. Capture ROI (using pyautogui to grab screen area)
            screenshot_gauge = pyautogui.screenshot(region=roi)
            frame_gauge = np.array(screenshot_gauge)
            
            # 2. Image Pre-processing (Optimized for digital numbers)
            gray_gauge = cv2.cvtColor(frame_gauge, cv2.COLOR_RGB2GRAY)
            # Use Otsu's thresholding for adaptive binarization
            _, thresh_gauge = cv2.threshold(
                gray_gauge, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
            )
            
            # 3. Tesseract OCR with Confidence Tracking
            # Configure Tesseract to look for only digits and decimals
            ocr_config = r'--psm 7 -c tessedit_char_whitelist=0123456789.' 
            
            data = pytesseract.image_to_data(thresh_gauge, config=ocr_config, output_type=pytesseract.Output.DICT)
            
            # Extract highest confidence reading
            text_data = [t.strip() for t in data['text'] if t.strip()]
            confidences = [int(c) for c in data['conf'] if int(c) >= 0]
            
            current_reading = "N/A"
            avg_confidence = 0

            if text_data:
                # Use regex to find the most likely number (digits with one decimal)
                raw_text = "".join(text_data) # Combine recognized text chunks
                
                # Regex looks for digits, an optional decimal, and more digits
                match = re.search(r'\d+\.?\d+', raw_text) 
                
                if match:
                    current_reading = match.group(0)
                    avg_confidence = np.mean(confidences) if confidences else 0
                else:
                    current_reading = raw_text # Fallback to raw text if regex fails
                    avg_confidence = np.mean(confidences) if confidences else 0

            # 4. Logging Logic (Log only if confidence is high AND the reading has changed)
            if current_reading != last_logged_reading and avg_confidence >= MIN_CONFIDENCE_THRESHOLD:
                # Save the image for debugging and proof
                image_name = f"debug/{current_time.replace(':', '_').replace(' ', '_')}.png"
                cv2.imwrite(image_name, frame_gauge)
                
                log_reading(current_time, current_reading, int(avg_confidence), image_name, log_filename)
                last_logged_reading = current_reading
            elif avg_confidence < MIN_CONFIDENCE_THRESHOLD:
                 print(f"[{current_time}] 🚷 Reading too low confidence ({int(avg_confidence)}%). Skipped logging.")
            else:
                 # Reading is the same as last logged value
                 pass 

            time.sleep(LOGGING_INTERVAL)

    except KeyboardInterrupt:
        print("\n--- Script stopped by user. Final data saved to CSV. ---")
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    # Create debug folder
    os.makedirs("debug", exist_ok=True)
    initialize_log_file(OUTPUT_LOG_FILE)
    monitor_and_log_gauge(GAUGE_DISPLAY_ROI, OUTPUT_LOG_FILE)