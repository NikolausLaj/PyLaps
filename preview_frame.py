import customtkinter as ctk
from PIL import Image

class PreviewFrame(ctk.CTkFrame):
    def __init__(self, parent, show_timelapse_callback):
        super().__init__(parent, corner_radius=0)

        self.show_timelapse_callback = show_timelapse_callback  # Reference to go back to Timelapse Frame

        self.image_label = ctk.CTkLabel(self, text="")
        self.image_label.pack(expand=True)

        # Create a frame to hold the buttons on the same row
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=20)

        # Back to Timelapse, Start, and Stop buttons aligned in the same frame
        self.back_button = ctk.CTkButton(self.button_frame, text="Back to Timelapse", command=self.show_timelapse_callback)
        self.back_button.pack(side="left", padx=10)

        self.start_button = ctk.CTkButton(self.button_frame, text="Start", command=self.start_preview)
        self.start_button.pack(side="left", padx=10)

        self.stop_button = ctk.CTkButton(self.button_frame, text="Stop", command=self.stop_preview)
        self.stop_button.pack(side="left", padx=10)

        self.images = []
        self.image_index = 0
        self.is_previewing = False

    def start_preview(self, images=None):
        """ Start the timelapse preview with a list of image file paths """
        if images:
            self.images = images  # Only set new images if provided

        if self.images and not self.is_previewing:
            self.image_index = 0
            self.is_previewing = True
            self.display_next_image()

    def stop_preview(self):
        """ Stop the timelapse preview """
        self.is_previewing = False

    def display_next_image(self):
        if self.image_index < len(self.images) and self.is_previewing:
            image_path = self.images[self.image_index]
            img = Image.open(image_path)

            # Maintain aspect ratio while fitting the image into a 600x400 box
            img = self.resize_image_to_fit(img, (600, 400))

            # Use CTkImage for high-DPI scaling and customtkinter compatibility
            ctk_image = ctk.CTkImage(img, size=(img.width, img.height))

            self.image_label.configure(image=ctk_image)
            self.image_label.image = ctk_image  # Keep a reference to avoid garbage collection

            self.image_index += 1

            # Display the next image after 1 second (1000 ms)
            self.after(1000, self.display_next_image)
        else:
            self.is_previewing = False  # Stop previewing after all images are displayed

    def resize_image_to_fit(self, img, max_size):
        """ Resize the image to fit within max_size, maintaining aspect ratio """
        original_width, original_height = img.size
        max_width, max_height = max_size

        # Calculate the aspect ratio
        aspect_ratio = original_width / original_height

        # Determine new dimensions based on the aspect ratio
        if original_width > original_height:
            # Landscape orientation: fit width
            new_width = min(original_width, max_width)
            new_height = int(new_width / aspect_ratio)
        else:
            # Portrait orientation: fit height
            new_height = min(original_height, max_height)
            new_width = int(new_height * aspect_ratio)

        # Ensure the image fits within the bounding box
        if new_width > max_width:
            new_width = max_width
            new_height = int(new_width / aspect_ratio)
        if new_height > max_height:
            new_height = max_height
            new_width = int(new_height * aspect_ratio)

        return img.resize((new_width, new_height), Image.LANCZOS)
