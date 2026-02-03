UPI QR Web App

Quick start

1. Activate your virtualenv (Windows PowerShell):

   & .\.venv\Scripts\Activate.ps1

2. Install requirements:

   python -m pip install -r requirements.txt

3. Run the app:

   python app.py

4. Open http://127.0.0.1:5000 in your browser.

Features
- Generate UPI URI and render QR image in the browser.
- Shows official links for Google Pay, Paytm and PhonePe.

Notes
- Pillow is required by the `qrcode` package to create PNG images.
