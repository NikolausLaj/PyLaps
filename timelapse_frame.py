import customtkinter as ctk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES
from PIL import Image, ImageTk
import numpy as np
import os
import cv2  # OpenCV for face and eye detection

class TimelapseFrame(ctk.CTkFrame):
    def __init__(self, parent, show_preview_callback):
        super().__init__(parent, corner_radius=0)

        self.show_preview_callback = show_preview_callback  # Reference to switch to Preview Frame

        # Load the OpenCV face and eye classifiers
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        # Store the uploaded file paths and thumbnails
        self.uploaded_files = []
        self.thumbnail_size = (100, 100)
        self.image_frame = None

        # Create a container for drag-and-drop and images
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(expand=True, fill="both", pady=10)

        # Create a drag-and-drop area for uploading images
        self.drop_area = ctk.CTkLabel(self.content_frame, text="Drag and Drop Images Here", width=400, height=150, fg_color="gray75", corner_radius=10)
        self.drop_area.pack(expand=True, padx=20, pady=20)

        # Bind the drag-and-drop functionality
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.on_file_drop)

        # Add stabilization type selection (dropdown)
        self.stabilization_label = ctk.CTkLabel(self, text="Select Stabilization Mode:")
        self.stabilization_label.pack(side="bottom", pady=10)

        self.stabilization_options = ["None", "Eye Tracking", "Horizon"]
        self.stabilization_combobox = ctk.CTkComboBox(self, values=self.stabilization_options)
        self.stabilization_combobox.pack(side="bottom", pady=10)

        # Add a Preview button (initially hidden until images are uploaded)
        self.preview_button = ctk.CTkButton(self, text="Preview", command=self.show_preview)
        self.preview_button.pack(side="bottom", pady=20)
        self.preview_button.pack_forget()  # Hide until images are uploaded

    def on_file_drop(self, event):
        """ Handle the dropped files """
        file_paths = self.split_filenames(event.data)
        file_names = [os.path.basename(path) for path in file_paths]  # Extract just the filenames

        self.uploaded_files = file_paths  # Store the full paths for later preview
        self.display_uploaded_images(file_paths)  # Display thumbnails

        messagebox.showinfo("Files Dropped", "\n".join(file_names))

        # Show the preview button after images are uploaded
        self.preview_button.pack(side="bottom")

    def display_uploaded_images(self, file_paths):
        """ Replace the drag-and-drop area with thumbnails of the uploaded images """
        # Remove the drag-and-drop area
        self.drop_area.pack_forget()

        # Create a frame to hold the thumbnails
        if self.image_frame:
            self.image_frame.destroy()  # Remove the previous image frame if it exists

        self.image_frame = ctk.CTkFrame(self.content_frame)
        self.image_frame.pack(pady=20, expand=True, fill="both")

        # If "Eye Tracking" is selected, align images based on eyes
        if self.stabilization_combobox.get() == "Eye Tracking":
            aligned_images = self.align_images_based_on_eyes(file_paths)
            file_paths = aligned_images  # Update the file paths with aligned images

        # Add the thumbnails of the uploaded images
        for i, file_path in enumerate(file_paths):
            img = Image.open(file_path)
            img.thumbnail(self.thumbnail_size)  # Create thumbnail with the specified size
            img_tk = ImageTk.PhotoImage(img)

            label = ctk.CTkLabel(self.image_frame, image=img_tk, text="")
            label.image = img_tk  # Keep a reference to avoid garbage collection
            label.grid(row=i // 4, column=i % 4, padx=10, pady=10)  # Arrange in a grid (4 columns)

    def align_images_based_on_eyes(self, file_paths):
        """ Align images based on eye detection using OpenCV """
        aligned_images = []
        eye_positions = []

        for file_path in file_paths:
            # Load image in grayscale for eye detection
            img = cv2.imread(file_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Detect faces in the image
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) == 0:
                aligned_images.append(file_path)
                continue  # Skip alignment if no face is detected

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]

                # Detect eyes within the face region
                eyes = self.eye_cascade.detectMultiScale(roi_gray)
                if len(eyes) >= 2:  # We need at least two eyes to align
                    # Calculate the center of the eyes
                    eye1, eye2 = eyes[0], eyes[1]
                    eye1_center = (eye1[0] + eye1[2] // 2, eye1[1] + eye1[3] // 2)
                    eye2_center = (eye2[0] + eye2[2] // 2, eye2[1] + eye2[3] // 2)

                    # Calculate midpoint of the two eyes
                    eye_midpoint = ((eye1_center[0] + eye2_center[0]) // 2, (eye1_center[1] + eye2_center[1]) // 2)
                    eye_positions.append(eye_midpoint)

                    aligned_images.append(file_path)

        if len(eye_positions) < 2:
            return file_paths  # Not enough eyes detected to align

        # Align images based on the first image's eye position
        reference_eye_position = eye_positions[0]

        for i, file_path in enumerate(aligned_images):
            if i == 0:
                continue  # No need to align the first image

            # Calculate the shift needed to align the eyes
            dx = reference_eye_position[0] - eye_positions[i][0]
            dy = reference_eye_position[1] - eye_positions[i][1]

            img = cv2.imread(file_path)
            aligned_img = self.shift_image(img, dx, dy)

            # Save the aligned image
            aligned_file_path = f"aligned_{i}.jpg"
            cv2.imwrite(aligned_file_path, aligned_img)
            aligned_images[i] = aligned_file_path

        return aligned_images

    def shift_image(self, img, dx, dy):
        """ Shift an image by dx and dy """
        rows, cols, _ = img.shape
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        shifted_img = cv2.warpAffine(img, M, (cols, rows))
        return shifted_img

    def show_preview(self):
        """ Switch to the preview frame if images are uploaded """
        if not self.uploaded_files:
            messagebox.showwarning("No Images", "Please upload images before previewing.")
        else:
            selected_stabilization = self.stabilization_combobox.get()  # Get the selected stabilization mode
            print(f"Selected stabilization: {selected_stabilization}")  # This can be used later in the preview logic

            # Switch to the preview frame and pass the uploaded images
            self.show_preview_callback(self.uploaded_files)

    @staticmethod
    def split_filenames(filenames):
        """ Helper method to split filenames from the drag-and-drop event """
        return filenames.strip().split()  # Handles space-separated filesimport customtkinter as ctk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES
from PIL import Image, ImageTk
import os
import cv2  # OpenCV for face and eye detection
import numpy as np

class TimelapseFrame(ctk.CTkFrame):
    def __init__(self, parent, show_preview_callback):
        super().__init__(parent, corner_radius=0)

        self.show_preview_callback = show_preview_callback  # Reference to switch to Preview Frame

        # Load the OpenCV face and eye classifiers
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        # Store the uploaded file paths and thumbnails
        self.uploaded_files = []
        self.thumbnail_size = (100, 100)
        self.image_frame = None
        self.aligned_files = []  # Store aligned images for preview

        # Create a container for drag-and-drop and images
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(expand=True, fill="both", pady=10)

        # Create a drag-and-drop area for uploading images
        self.drop_area = ctk.CTkLabel(self.content_frame, text="Drag and Drop Images Here", width=400, height=150, fg_color="gray75", corner_radius=10)
        self.drop_area.pack(expand=True, padx=20, pady=20)

        # Bind the drag-and-drop functionality
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.on_file_drop)

        # Add stabilization type selection (dropdown)
        self.stabilization_label = ctk.CTkLabel(self, text="Select Stabilization Mode:")
        self.stabilization_label.pack(side="bottom", pady=10)

        self.stabilization_options = ["None", "Eye Tracking", "Horizon"]
        self.stabilization_combobox = ctk.CTkComboBox(self, values=self.stabilization_options)
        self.stabilization_combobox.pack(side="bottom", pady=10)

        # Add a Preview button (initially hidden until images are uploaded)
        self.preview_button = ctk.CTkButton(self, text="Preview", command=self.show_preview)
        self.preview_button.pack(side="bottom", pady=20)
        self.preview_button.pack_forget()  # Hide until images are uploaded

    def on_file_drop(self, event):
        """ Handle the dropped files """
        file_paths = self.split_filenames(event.data)
        file_names = [os.path.basename(path) for path in file_paths]  # Extract just the filenames

        self.uploaded_files = file_paths  # Store the full paths for later preview
        self.display_uploaded_images(file_paths)  # Display thumbnails

        messagebox.showinfo("Files Dropped", "\n".join(file_names))

        # Show the preview button after images are uploaded
        self.preview_button.pack(side="bottom")

    def display_uploaded_images(self, file_paths):
        """ Replace the drag-and-drop area with thumbnails of the uploaded images """
        # Remove the drag-and-drop area
        self.drop_area.pack_forget()

        # Create a frame to hold the thumbnails
        if self.image_frame:
            self.image_frame.destroy()  # Remove the previous image frame if it exists

        self.image_frame = ctk.CTkFrame(self.content_frame)
        self.image_frame.pack(pady=20, expand=True, fill="both")

        # Add the thumbnails of the uploaded images
        for i, file_path in enumerate(file_paths):
            img = Image.open(file_path)
            img.thumbnail(self.thumbnail_size)  # Create thumbnail with the specified size
            img_tk = ImageTk.PhotoImage(img)

            label = ctk.CTkLabel(self.image_frame, image=img_tk, text="")
            label.image = img_tk  # Keep a reference to avoid garbage collection
            label.grid(row=i // 4, column=i % 4, padx=10, pady=10)  # Arrange in a grid (4 columns)

    def align_images_based_on_eyes(self, file_paths):
        """ Align images based on eye detection using OpenCV """
        aligned_images = []
        eye_positions = []

        for file_path in file_paths:
            # Load image in grayscale for eye detection
            img = cv2.imread(file_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Detect faces in the image
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) == 0:
                aligned_images.append(file_path)
                continue  # Skip alignment if no face is detected

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]

                # Detect eyes within the face region
                eyes = self.eye_cascade.detectMultiScale(roi_gray)
                if len(eyes) >= 2:  # We need at least two eyes to align
                    # Calculate the center of the eyes
                    eye1, eye2 = eyes[0], eyes[1]
                    eye1_center = (eye1[0] + eye1[2] // 2, eye1[1] + eye1[3] // 2)
                    eye2_center = (eye2[0] + eye2[2] // 2, eye2[1] + eye2[3] // 2)

                    # Calculate midpoint of the two eyes
                    eye_midpoint = ((eye1_center[0] + eye2_center[0]) // 2, (eye1_center[1] + eye2_center[1]) // 2)
                    eye_positions.append(eye_midpoint)

                    aligned_images.append(file_path)

        if len(eye_positions) < 2:
            return file_paths  # Not enough eyes detected to align

        # Align images based on the first image's eye position
        reference_eye_position = eye_positions[0]

        for i, file_path in enumerate(aligned_images):
            if i == 0:
                continue  # No need to align the first image

            # Calculate the shift needed to align the eyes
            dx = reference_eye_position[0] - eye_positions[i][0]
            dy = reference_eye_position[1] - eye_positions[i][1]

            img = cv2.imread(file_path)
            aligned_img = self.shift_image(img, dx, dy)

            # Save the aligned image
            aligned_file_path = f"aligned_{i}.jpg"
            cv2.imwrite(aligned_file_path, aligned_img)
            aligned_images[i] = aligned_file_path

        return aligned_images

    def shift_image(self, img, dx, dy):
        """ Shift an image by dx and dy """
        rows, cols, _ = img.shape
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        shifted_img = cv2.warpAffine(img, M, (cols, rows))
        return shifted_img

    def show_preview(self):
        """ Switch to the preview frame if images are uploaded """
        if not self.uploaded_files:
            messagebox.showwarning("No Images", "Please upload images before previewing.")
        else:
            selected_stabilization = self.stabilization_combobox.get()  # Get the selected stabilization mode

            # If Eye Tracking is selected, align the images
            if selected_stabilization == "Eye Tracking":
                self.aligned_files = self.align_images_based_on_eyes(self.uploaded_files)
                print(f"Eye Tracking stabilization applied, aligned images: {self.aligned_files}")
                self.show_preview_callback(self.aligned_files)  # Pass aligned images to the preview

            # If no stabilization is selected, show the original images
            else:
                print(f"Stabilization: {selected_stabilization}, showing original images.")
                self.show_preview_callback(self.uploaded_files)  # Pass original images for preview

    @staticmethod
    def split_filenames(filenames):
        """ Helper method to split filenames from the drag-and-drop event """
        return filenames.strip().split()  # Handles space-separated files

