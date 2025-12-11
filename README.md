# 🏭 Project 3: Automated OCR Data Logging for Industrial Monitoring

This project demonstrates advanced **Computer Vision** and **Optical Character Recognition (OCR)** techniques to automate the extraction of critical time-series data from visual displays, such as digital meters, gauges, or production counters. This solution eliminates the errors and time consumption associated with manual data logging.

### 🎯 Business Value & Problem Solved

**Problem:** In industrial, utility, and manufacturing environments, recording readings from digital meters is often done manually, leading to human error, missed readings, and delays in operational reporting.

**Solution:** This tool provides a reliable, automated, and real-time method to capture and log numerical readings directly from video feeds or images, ensuring data integrity for monitoring and analytics.

---

### ⚙️ Technology Stack

* **Primary Tool:** Tesseract OCR (Integrated via Python)
* **Image Processing:** OpenCV (cv2)
* **Data Handling:** Pandas (for time-series logging)
* **Core Skill:** Real-Time Data Extraction and Automation

### 📸 Technical Breakdown: The Automation Pipeline

The system works by processing visual input through a series of steps to isolate and read the target numerical value: 

1.  **Input Acquisition:** The system takes sequential screenshots or frames from a video stream (e.g., from a security camera monitoring a gauge).
2.  **Image Pre-processing (OpenCV):** This is the most critical step. Techniques are applied to ensure the numbers are perfectly clean for OCR:
    * **Grayscaling & Thresholding:** Converts the image to black and white to maximize contrast.
    * **Region of Interest (ROI) Masking:** Precisely crops the image to focus only on the digital display area (e.g., coordinates for the multiplier area). This drastically improves OCR accuracy.
3.  **Optical Character Recognition (Tesseract):** The cleaned image segment is passed to Tesseract, which extracts the text. Configuration is optimized to recognize only numerical characters (0-9 and decimal points).
4.  **Data Logging:** The extracted number is paired with a timestamp and logged into a CSV file, creating a clean time-series record of the meter readings.

### 📊 Output Data Example (`meter_readings.csv`)

| Timestamp | Reading | Confidence |
| :--- | :--- | :--- |
| 2025-12-11 14:30:00 | 1.05 | 98.7% |
| 2025-12-11 14:30:05 | 2.51 | 95.2% |
| 2025-12-11 14:30:10 | 3.99 | 97.5% |

### 📁 Key Files

* `ocr_logger.py`: The main script handling the image processing pipeline, Tesseract integration, and data logging.
* `test_images/`: Directory containing static screenshots used to test the OCR accuracy (e.g., `meter_01.png`, `meter_02.png`).
* `meter_readings.csv`: The final time-series data output file.

---

### 💻 Setup and Running the Project

1.  **Dependencies:** Ensure Tesseract OCR is installed on your system, and the path is correctly configured.
2.  **Python Libraries:**
    ```bash
    pip install opencv-python pytesseract pandas
    ```
3.  **Execution:**
    ```bash
    python ocr_logger.py
    ```
