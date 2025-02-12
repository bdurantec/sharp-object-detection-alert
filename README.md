# Sharp Object Detection Alert

## Project Overview

The **Sharp Object Detection Alert** is a cutting-edge tool designed to detect sharp objects in videos. It processes
videos provided via Google Drive links, analyzes frames using the YOLOv8 model (`yolov8n.pt`), sends the frames to Azure
Computer Vision for object detection, and then utilizes an OpenAI-powered assistant to evaluate the results. Based on
the analysis, the system sends alert, result, or error notifications via Gmail SMTP.

## Features

- Video frame extraction and analysis using Python-OpenCV and YOLOv8 model.
- Integration with Azure Computer Vision for object detection.
- OpenAI Assistant for interpreting the results from Computer Vision.
- Email notifications sent using Gmail SMTP:
    - **Alert email**: When a sharp object is detected.
    - **Result notification**: When no sharp object is detected.
    - **Error notification**: When an error occurs during processing.

## Services Integrated

### 1. **YOLOv8 Model (`yolov8n.pt`)**

- The **YOLOv8 model** is used for detecting objects in each video frame. It helps identify potential sharp objects
  based on the features trained into the model.

### 2. **Azure Computer Vision**

- Once frames are extracted, they are sent to **Azure Computer Vision** for object content and object detection. It
  analyzes the image and provides a detailed result (objects detected, confidence score, etc.).

### 3. **OpenAI Assistant**

- The **OpenAI assistant** evaluates the JSON response from Azure Computer Vision, interpreting whether a sharp object
  is present, what object it is, and providing additional details about the object detected.

### 4. **Gmail SMTP Service**

- The system sends **emails** via Gmail SMTP, using the results from the analysis. There are three types of emails:
    - **Alert Email**: If a sharp object is detected in the video.
    - **Result Notification**: If no sharp object is detected.
    - **Error Notification**: If any error occurs during the video processing.

## Getting Started

### Prerequisites

Make sure you have the following installed on your machine:

- **Python 3.12**: Ensure you have Python installed by running:
  ```bash
  python --version
- Google Drive link for the video to be analyzed following the pattern
  `https://drive.google.com/uc?id=ID_GOOGLE_DRIVE_VIDEO`.
- Email account for sending emails via SMTP.

## Installation Steps

### Clone the repository:

```bash
git clone https://github.com/yourusername/sharp-object-detection-alert.git
cd sharp-object-detection-alert
```

### Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Set up your .env file:

```env
GOOGLE_DRIVE_VIDEO_LINK = "https://drive.google.com/uc?id=ID_GOOGLE_DRIVE_VIDEO"
ALERT_CONTACT_EMAIL = ""
```

**_The project has mandatory variables not mentioned here in the README for security reasons!_**

## Running the Project

To start processing a video and analyze for sharp objects, follow these steps:

### Run the main script in the root folder:

```bash
python app.py
```

The script will:

- Download the video from the provided Google Drive link.
- Process the video frame by frame using YOLOv8.
- Send each frame to Azure Computer Vision for analysis.
- Use the OpenAI assistant to interpret the results.
- Send an email alert (if a sharp object is detected), notification (if no sharp object is found), or an error
  notification (if something goes wrong).

### Check your email inbox and spam (junk mail):

You will receive an email `from: brunodurantec@gmail.com` based on the result of the analysis.

- Alert email: When a sharp object is detected in the video.
- Result notification: When no sharp object is detected.
- Error notification: When an error occurs during the processing.

### Tips

- Do you want to vary the model, number of frames and the confidence for selection? Access the file `src\infra\yolo_frame_selection.py` and update the variables on the top!

---

## Contact

If you have any questions or need support, feel free to reach out:

- LinkedIn: https://www.linkedin.com/in/brunodurante/
- Email: brunodurantec@gmail.com

