
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
   ```

2. **tkinterdnd2**: Enables drag-and-drop functionality for the GUI.
   ```bash
   pip install tkinterdnd2
   ```

3. **OpenCV**: Handles image processing and video generation.
   ```bash
   pip install opencv-python
   ```

4. **FFmpeg**: Needed for encoding videos in MP4 format with H.264 codec. On Ubuntu, you can install it using:
   ```bash
   sudo apt install ffmpeg
   ```

5. **NumPy**: Used for image manipulation.
   ```bash
   pip install numpy
   ```

### Virtual Environment (Optional)
It is recommended to use a virtual environment to manage dependencies. You can create and activate a virtual environment with the following commands:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Usage

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <project-folder>
   ```

2. **Install Required Libraries**: Install the required Python libraries by running:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Program**: Run the Python script to start the GUI:
   ```bash
   python pylaps.py
   ```

4. **Using the Program**:
    - **Drag and Drop**: Drag and drop the images into the designated area in the GUI.
    - **Set Display Time**: Specify how long each image should be shown (in seconds).
    - **Select Tracking Mode**: Choose between "No Tracking" or "Eye Tracking". If you select "Eye Tracking", the program will attempt to align the eyes of the person across all images.
    - **Create Video**: Click the "Create" button to generate the time-lapse video.

5. **Output**: The final time-lapse video will be saved as an MP4 file in the selected location.

## Functionality

### Main Components:
- **Drag-and-Drop Interface**: Users can drag and drop image files into the interface to add them to the time-lapse.
- **Time-lapse Creation**: The user can define the display time for each image, and the program will combine them into a single video.
- **Eye Tracking Stabilization**:
   When this option is selected, the program uses OpenCV's `CascadeClassifier` to detect and align the eyes across multiple images, ensuring the person's eyes remain in the same position, creating a more stabilized time-lapse effect.
- **Video Export**:
   The final video is encoded using FFmpeg to ensure cross-platform compatibility (MP4 format with H.264 codec).

## Known Issues
- The eye stabilization feature depends on the quality and clarity of the images. For best results, ensure the images are well-lit and have a clear view of the person's face and eyes.
- Eye detection using OpenCV’s `CascadeClassifier` may not work well for all images (particularly if the face is not facing forward or the eyes are partially covered).

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue if you encounter any problems or have suggestions for improvements.