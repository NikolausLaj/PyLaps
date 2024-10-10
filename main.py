import customtkinter as ctk
from tkinterdnd2 import TkinterDnD
from timelapse_frame import TimelapseFrame
from settings_frame import SettingsFrame
from preview_frame import PreviewFrame

# Initialize custom tkinter
ctk.set_appearance_mode("System")  # Can be "System", "Dark", or "Light"
ctk.set_default_color_theme("blue")  # Default color theme

class TimelapseApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.title("Timelapse Application")
        self.geometry("800x600")

        # Create sidebar frame with buttons for navigation
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")

        self.timelapse_button = ctk.CTkButton(self.sidebar_frame, text="Timelapse", command=self.show_timelapse_frame)
        self.timelapse_button.pack(pady=20, padx=10)

        self.settings_button = ctk.CTkButton(self.sidebar_frame, text="Settings", command=self.show_settings_frame)
        self.settings_button.pack(pady=20, padx=10)

        # Create main frame where content will be shown
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(side="right", expand=True, fill="both")

        # Initialize frames
        self.timelapse_frame = TimelapseFrame(self.main_frame, self.show_preview_frame)
        self.settings_frame = SettingsFrame(self.main_frame)
        self.preview_frame = PreviewFrame(self.main_frame, self.show_timelapse_frame)

        # Show the Timelapse frame by default
        self.show_timelapse_frame()

    def show_timelapse_frame(self):
        # Clear the main frame and show the timelapse UI
        self.clear_frame()
        self.timelapse_frame.pack(expand=True, fill="both")

    def show_settings_frame(self):
        # Clear the main frame and show the settings UI
        self.clear_frame()
        self.settings_frame.pack(expand=True, fill="both")

    def show_preview_frame(self, images):
        # Clear the main frame and show the preview UI with images
        self.clear_frame()
        self.preview_frame.pack(expand=True, fill="both")
        self.preview_frame.start_preview(images)

    def clear_frame(self):
        # Destroy all widgets in the main frame before switching
        for widget in self.main_frame.winfo_children():
            widget.pack_forget()


if __name__ == "__main__":
    app = TimelapseApp()
    app.mainloop()
