import customtkinter as ctk
from tkinter import StringVar

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=0)

        self.theme_label = ctk.CTkLabel(self, text="Select Theme:")
        self.theme_label.pack(pady=20)

        # Variable to store selected theme
        self.theme_var = StringVar(value="System")

        # Radio buttons for selecting theme
        self.theme_light = ctk.CTkRadioButton(self, text="Light Mode", variable=self.theme_var, value="Light", command=self.change_theme)
        self.theme_light.pack(pady=10)

        self.theme_dark = ctk.CTkRadioButton(self, text="Dark Mode", variable=self.theme_var, value="Dark", command=self.change_theme)
        self.theme_dark.pack(pady=10)

        self.theme_system = ctk.CTkRadioButton(self, text="System Mode", variable=self.theme_var, value="System", command=self.change_theme)
        self.theme_system.pack(pady=10)

    def change_theme(self):
        # Change the theme of the app
        selected_theme = self.theme_var.get()  # Get the selected theme from the radio buttons
        ctk.set_appearance_mode(selected_theme)
