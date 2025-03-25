# digitisEverything
This app provides digitization across data types

# Setup
## 1. System Requirements

- **Operating System:** Linux, macOS, or Windows
- **Python:** Version 3.6 or later
- **Memory:** At least 512 MB free RAM (1 GB recommended)
- **Disk Space:** Approximately 100 MB for dependencies and logs
- **Additional Software:** Tesseract OCR engine installed on your system

## 2. Installation

### 2.1. Install Python and Pip

Ensure that Python 3.6 or above and pip are installed. Verify with:
```bash
python --version
pip --version
```

# First Function
# OCR Text Extraction Webapp – User Manual

## 1. Overview

The OCR Text Extraction webapp is a lightweight, Flask-based application designed to extract text from images using Tesseract OCR. It utilizes open source libraries (Flask, Pillow, and pytesseract) and runs entirely locally without any external API calls. The app includes built-in validation for image uploads and basic image pre‑processing to boost OCR accuracy.

## 2. How to Use the Webapp
### 2.1. Uploading an Image

- Select Image: Click the file selection button and choose an image file from your computer. Accepted file types include PNG, JPG, JPEG, GIF, BMP, and TIFF.
- Submit: Click the "Extract Text" button to upload the image.

### 2.2. Viewing the Extracted Text

- Once the image is processed, the page refreshes to display the extracted text below the upload form.
- If any issues occur (e.g., unsupported file type or processing error), an appropriate error message is displayed.

## 3. Code Details and Customization
### 3.1. Image Pre-processing

- Grayscale Conversion: The image is converted to grayscale using ImageOps.grayscale(), enhancing OCR accuracy.
- Optional Thresholding: Uncomment and adjust the thresholding code if further processing is needed:
```python
image = image.point(lambda x: 0 if x < 128 else 255, '1')
```
### 3.2. Tesseract Configuration
- Page Segmentation Mode (PSM): The OCR process uses --psm 6 to assume a uniform block of text. Modify this setting in the pytesseract.image_to_string function if required.

### 3.3. File Validation
- The helper function allowed_file() restricts uploads to common image formats, ensuring only supported file types are processed.

### 3.4. Maximum File Size
- The setting app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024 limits file uploads to 16 MB, maintaining performance and preventing server overload.

## 4. Troubleshooting
### 4.1. Tesseract Not Found
- **Issue:** Error indicating Tesseract is not found.
- **Solution:** Ensure Tesseract is installed and added to your system's PATH. Alternatively, specify the Tesseract path in your code:
```python
pytesseract.pytesseract.tesseract_cmd = r'/path/to/tesseract'
```
### 4.2. Image Processing Errors
- **Issue:** Errors during image processing may occur if the file is corrupted or incompatible.
- **Solution:** Verify the integrity of the image and ensure it is in one of the allowed formats.

### 4.3. Large File Uploads
- **Issue:** Large images can slow down processing.
- **Solution:** Reduce image size before upload or adjust MAX_CONTENT_LENGTH if system resources allow.

## 5. Frequently Asked Questions (FAQs)
**Q1: What types of images can I upload?**
A: Accepted image formats include PNG, JPG, JPEG, GIF, BMP, and TIFF.

**Q2: Can this app process handwritten text?**
A: Tesseract is optimized for printed text. For handwritten text, consider alternative open source OCR models like EasyOCR.

**Q3: How do I adjust the OCR configuration?**
A: Modify the Tesseract configuration options in the pytesseract.image_to_string function call.

**Q4: How can I improve OCR accuracy further?**
A: Experiment with additional image pre-processing steps such as noise reduction, thresholding, or resizing. Integrating OpenCV can also provide advanced image processing options.

## 7. Additional Resources
[Tesseract OCR Documentation](https://tesseract-ocr.github.io/tessdoc/)

[Flask Documentation](https://flask.palletsprojects.com/en/stable/)

[Pillow Documentation](https://pillow.readthedocs.io/en/stable/)

[pytesseract GitHub Repository](https://github.com/madmaze/pytesseract)

[EasyOCR (for handwritten text)](https://github.com/JaidedAI/EasyOCR)