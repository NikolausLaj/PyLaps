import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import cv2
import os
import subprocess
import numpy as np

class TimeLapseApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.title("Time-Lapse Creator")
        self.geometry("500x450")

        # Variables
        self.image_files = []
        self.display_time = ctk.StringVar(value="1")  # Default display time 1 second
        self.tracking_option = ctk.StringVar(value="No Tracking")  # Default is No Tracking
        
        # Create Drag and Drop area
        self.drop_area = ctk.CTkLabel(self, text="Drag and Drop Images Here", width=400, height=150, fg_color="gray75", corner_radius=10)
        self.drop_area.pack(pady=20)
        
        # Enable Drag and Drop
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.add_files)

        # Time entry field
        self.time_label = ctk.CTkLabel(self, text="Time per image (seconds):", font=("Arial", 12))
        self.time_label.pack()
        self.time_entry = ctk.CTkEntry(self, textvariable=self.display_time, width=100)
        self.time_entry.pack(pady=5)
        
        # Add tracking option dropdown
        self.tracking_label = ctk.CTkLabel(self, text="Select Tracking Mode:", font=("Arial", 12))
        self.tracking_label.pack(pady=5)
        self.tracking_dropdown = ctk.CTkOptionMenu(self, values=["No Tracking", "Eye Tracking"], variable=self.tracking_option)
        self.tracking_dropdown.pack(pady=10)
        
        # Create Button
        self.create_button = ctk.CTkButton(self, text="Create", command=self.create_timelapse)
        self.create_button.pack(pady=20)

    def add_files(self, event):
        """Handles adding files through drag-and-drop."""
        files = self.tk.splitlist(event.data)
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                self.image_files.append(file)
        self.drop_area.configure(text=f"{len(self.image_files)} images added")
    
    def create_timelapse(self):
        """Creates a time-lapse video from the added images."""
        if not self.image_files:
            messagebox.showwarning("No images", "Please drag and drop images to create a time-lapse.")
            return
        
        try:
            display_time = float(self.display_time.get())
        except ValueError:
            messagebox.showwarning("Invalid Time", "Please enter a valid time duration for each image.")
            return
        
        # Ask where to save the video (temporary uncompressed output)
        save_path = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI files", "*.avi")])
        if not save_path:
            return
        
        # Create uncompressed video using OpenCV
        uncompressed_path = os.path.splitext(save_path)[0] + "_uncompressed.avi"
        self.generate_video(uncompressed_path, display_time)
        
        # Now use FFmpeg to re-encode the video in MP4 with H.264
        final_output = save_path.replace(".avi", ".mp4")
        self.encode_with_ffmpeg(uncompressed_path, final_output)
        
        # Remove uncompressed video
        os.remove(uncompressed_path)
        
        messagebox.showinfo("Success", f"Time-lapse video saved as {final_output}")

    def generate_video(self, save_path, display_time):
        """Generates a time-lapse video with optional eye stabilization."""
        first_image = cv2.imread(self.image_files[0])
        height, width, _ = first_image.shape

        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        video = cv2.VideoWriter(save_path, fourcc, 1 / display_time, (width, height))

        # Load the Haar Cascade for eye detection
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        # Initialize reference eye center for alignment
        reference_eye_center = None

        for idx, image_file in enumerate(self.image_files):
            img = cv2.imread(image_file)
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Detect eyes in the current image
            eyes = eye_cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=5)

            if len(eyes) > 0:
                # Take the first detected eye (or the largest one)
                eyes = sorted(eyes, key=lambda x: x[2] * x[3], reverse=True)  # Sort by size
                (ex, ey, ew, eh) = eyes[0]
                current_eye_center = (ex + ew // 2, ey + eh // 2)  # Center of the detected eye

                if reference_eye_center is None:
                    # Set the reference eye center from the first image
                    reference_eye_center = current_eye_center

                # Calculate the translation needed to align the eyes
                dx = reference_eye_center[0] - current_eye_center[0]
                dy = reference_eye_center[1] - current_eye_center[1]

                # Apply the translation to align the image
                translation_matrix = np.float32([[1, 0, dx], [0, 1, dy]])
                img_aligned = cv2.warpAffine(img, translation_matrix, (width, height))
            else:
                # If no eyes are detected, just use the original image (no translation)
                img_aligned = img

            # Write the aligned (or unaligned) image to the video
            video.write(img_aligned)

        video.release()

    def encode_with_ffmpeg(self, input_path, output_path):
        """Uses FFmpeg to encode the uncompressed video into MP4 (H.264)."""
        ffmpeg_command = [
            'ffmpeg', '-y', '-i', input_path,
            '-c:v', 'libx264', '-crf', '23',  # CRF controls video quality (lower is better)
            '-preset', 'medium',               # Controls encoding speed vs compression ratio
            '-movflags', 'faststart',          # Helps with web streaming
            output_path
        ]
        subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Run the application
if __name__ == "__main__":
    app = TimeLapseApp()
    app.mainloop()
