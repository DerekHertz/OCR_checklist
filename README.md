
# Decoding Checklist App

This Streamlit app streamlines the decoding checklist process, ensuring accuracy and consistency.

Key Features:

Image Upload and Chip Number Extraction: Users upload a photo of decoding chips, and the app automatically extracts chip numbers using EasyOCR.
Manual Chip List Validation: Users paste a list of assigned chips from Slack for cross-validation.
Chip Number Matching and Discrepancy Alerting: The app checks for matches between extracted and pasted chip numbers, highlighting any discrepancies.
Decoder Information and Signature Capture: Decoders provide their name, initials, and a signature (or drawing) for accountability.
Microscope Selection: Users select the microscope used for decoding.
Data Collection and Output: The app gathers decoder information, microscope details, chip match status, and a canvas drawing for recording and review.
Dependencies:

Streamlit
EasyOCR
OpenCV
pandas
numpy
PIL (Pillow)
streamlit-drawable-canvas
Usage:

Run the app: streamlit run app.py
Enter your name and select a microscope.
Upload a photo of decoding chips.
Paste the assigned chip list from Slack.
Verify chip number matches and provide secondary validation.
Enter your initials and create a signature or drawing.
The app will display captured data and collected information.
Additional Notes:

The app highlights text boxes in uploaded images for visual clarity.
It encourages secondary validation for enhanced accuracy.
It includes a fun drawing feature for decoder engagement.
