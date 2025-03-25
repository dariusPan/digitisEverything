from flask import Flask, request, render_template_string, session, send_file
import pytesseract
from PIL import Image, ImageOps, ImageFilter
import numpy as np
import io

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB upload limit
app.secret_key = "replace_with_a_random_secret_key"  # Replace with a secure key

HTML_TEMPLATE = '''
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>OCR Text Extraction</title>
  </head>
  <body>
    <h1>Upload an Image for OCR Extraction</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="image" accept="image/*" required>
      <input type="submit" value="Extract Text">
    </form>
    {% if text %}
      <h2>Extracted Text:</h2>
      <pre>{{ text }}</pre>
      <form action="/download" method="get">
        <button type="submit">Download Text</button>
      </form>
    {% endif %}
  </body>
</html>
'''

def allowed_file(filename):
    allowed_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
    return filename.lower().endswith(allowed_extensions)

def auto_invert(image):
    """
    Inverts the image if the average brightness is below a threshold.
    This helps to handle images with white text on dark backgrounds.
    """
    # Ensure image is in grayscale ('L') mode
    if image.mode != 'L':
        image = image.convert('L')
    arr = np.array(image)
    if arr.mean() < 128:
        image = ImageOps.invert(image)
    return image

def preprocess_image(image):
    """
    Apply a series of filters to improve OCR accuracy.
    Steps:
    1. Convert to grayscale.
    2. Apply autocontrast to enhance differences.
    3. Optionally invert colors based on brightness.
    4. Reduce noise with a median filter.
    5. Apply thresholding to binarize the image.
    """
    # Convert to grayscale and enhance contrast
    gray = ImageOps.grayscale(image)
    gray = ImageOps.autocontrast(gray)
    
    # Auto-invert if necessary (handles white text on dark background)
    gray = auto_invert(gray)
    
    # Reduce noise with a median filter
    gray = gray.filter(ImageFilter.MedianFilter(size=3))
    
    # Apply thresholding to obtain a binary image
    threshold_value = 128
    binary = gray.point(lambda x: 0 if x < threshold_value else 255, '1')
    
    return binary

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = None
    if request.method == 'POST':
        image_file = request.files.get('image')
        if not image_file or image_file.filename == "":
            extracted_text = "No image selected for uploading."
        elif not allowed_file(image_file.filename):
            extracted_text = "Unsupported file type."
        else:
            try:
                # Open and preprocess the image
                image = Image.open(image_file.stream)
                processed_image = preprocess_image(image)
                # Use Tesseract OCR with a specific page segmentation mode
                extracted_text_raw = pytesseract.image_to_string(image, config='--psm 6')
                extracted_text = pytesseract.image_to_string(processed_image, config='--psm 6')
                # Store extracted text in session for download
                session['extracted_text_raw'] = extracted_text_raw
                session['extracted_text'] = extracted_text
            except Exception as e:
                extracted_text = f"Error processing image: {e}"
    return render_template_string(HTML_TEMPLATE, text=extracted_text)

@app.route('/download', methods=['GET'])
def download():
    extracted_text_raw = session.get('extracted_text_raw', '')
    extracted_text = session.get('extracted_text', '')
    if not extracted_text:
        return "No text available for download.", 400
    file_object = io.BytesIO()
    file_object.write(extracted_text_raw.encode('utf-8'))
    file_object.write(extracted_text.encode('utf-8'))
    file_object.seek(0)
    # Use `download_name` if using Flask 2.x or later
    return send_file(file_object, as_attachment=True, download_name='extracted_text.txt', mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)