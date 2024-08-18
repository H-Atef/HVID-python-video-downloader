# HVID Downloader

HVID Downloader is a Python desktop application aimed at providing users with a fast and easy-to-use video downloader. The project enables users to download videos from various websites by simply providing the URL of the desired video. Additionally, it offers the functionality to download videos in audio format by automatically converting them.

## Features

- Download videos from different websites by entering the video URL.
- Convert videos to audio format (.mp3) automatically.
- Built with Kivy for a user-friendly interface.
- Utilizes Pytubefix, wget, and Selenium for downloading videos from YouTube and other websites in formats like .mp4 and .mp3.

## Future Enhancements

The project can be expanded and maintained to work on smartphones, providing accessibility to a wider audience. Potential future features include:

- Integration of more video download websites and techniques.

- Addition of text summarizer for effectively summarizing video content using AI.

## Technologies Used

- **Kivy**: Used for building the application interface.
- **Pytubefix, wget, Selenium**: Employed for downloading videos from various websites.
  
## How to Use

1. Enter the URL of the video you want to download and specify a path.
2. Select the desired format for the downloaded video.
3. Click the download button to save the video to your device.

## Instructions

- **Install Packages**: Run the following command to install required packages:

```python
pip install -r requirements.txt
```

- **Run Main File**: Execute the following command to run the main file:

```python
python -m video_main.py
```

---
