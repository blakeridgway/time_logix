# timelogix/ui/components.py
import customtkinter as ctk


def create_label(parent, text, font_family, font_size):
    return ctk.CTkLabel(parent, text=text, font=(font_family, font_size))


def create_entry(parent, width):
    return ctk.CTkEntry(parent, width=width)


def create_button(parent, text, command):
    return ctk.CTkButton(parent, text=text, command=command, corner_radius=8)


def create_combo(parent, values, width):
    return ctk.CTkComboBox(parent, values=values, width=width)


def create_text_box(parent, width, height, font):
    return ctk.CTkTextbox(parent, width=width, height=height, font=font)
