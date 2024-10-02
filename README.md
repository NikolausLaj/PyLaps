# Time-Lapse Creator with Eye Stabilization

## Overview
This project is a Python-based application that allows users to create time-lapse videos from a set of images. The program includes a drag-and-drop interface for adding images, an option to set the display duration for each image, and an eye stabilization feature that ensures a person's eyes remain in the same position across all frames.

## Features
- **Drag and Drop Interface**: Easily add images to create the time-lapse.
- **Custom Display Time**: Set how long each image should be displayed in the video.
- **Eye Tracking Stabilization**: Aligns the eyes of a person in the images, ensuring a smooth time-lapse transition.
- **Video Export**: The final video is saved in a cross-platform MP4 format with H.264 encoding for maximum compatibility.

## Requirements

### Libraries
To run this project, you will need to install the following libraries:
1. **customtkinter**: A modern GUI library.
   ```bash
   pip install customtkinter
   pip install tkinterdnd2
   pip install opencv-python
   pip install numpy
