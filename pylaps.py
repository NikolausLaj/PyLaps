import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import cv2
import os

# Initialize customtkinter settings
ctk.set_appearance_mode("System")  # Options: "System" (default), "Light", "Dark"
ctk.set_default_color_theme("blue")  # Options: "blue" (default), "dark-blue", "green"

class TimeLapseApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.title("Time-Lapse Creator")
        self.geometry("500x400")

        # Variables
        self.image_files = []
        self.display_time = ctk.StringVar(value="1")  # Default display time 1 second
        
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
        
        # Ask where to save the video
        save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        if not save_path:
            return
        
        # Create video
        self.generate_video(save_path, display_time)

    def generate_video(self, save_path, display_time):
        """Generates a time-lapse video from the images."""
        # Get the size of the first image to define the video size
        first_image = cv2.imread(self.image_files[0])
        height, width, layers = first_image.shape

        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(save_path, fourcc, 1 / display_time, (width, height))

        for image_file in self.image_files:
            img = cv2.imread(image_file)
            video.write(img)

        video.release()
        messagebox.showinfo("Success", f"Time-lapse video saved as {save_path}")

# Run the application
if __name__ == "__main__":
    app = TimeLapseApp()
    app.mainloop()
