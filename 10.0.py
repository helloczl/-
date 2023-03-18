import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import os

class Clock(tk.Tk):
    def __init__(self,*args, **kwargs):
        tk.Tk.__init__(self,*args, **kwargs)
        self.overrideredirect(True)
        self.attributes("-topmost", 1)
        self.wm_attributes("-alpha", 0.5)
        #self.geometry("+800+400")

        self.clock_frame = tk.Frame(self, bg="black")
        self.clock_frame.pack(expand=True, fill="both")
        self.clock_label = tk.Label(self.clock_frame, font=("Arial", 30), bg="black", fg="white")
        self.clock_label.pack(pady=10)

        self.clock_frame.bind("<Button-1>", self.start_move)
        self.clock_frame.bind("<B1-Motion>", self.on_move)
        self.clock_frame.bind("<ButtonRelease-1>", self.end_move)

        self.bind("<Button-3>", self.open_settings)
        self.update_clock()

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.after(1000, self.update_clock)

    def open_settings(self, event):
        settings = Settings(self.clock_frame, self.clock_label)
        settings.attributes("-topmost", 1)
        settings.wait_window()
        if settings.topmost_var.get():
            self.attributes("-topmost", 1)
        else:
            self.attributes("-topmost", 0)

    def start_move(self, event):
        self._x = event.x
        self._y = event.y

    def on_move(self, event):
        deltax = event.x - self._x
        deltay = event.y - self._y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry("+{}+{}".format(x, y))

    def end_move(self, event):
        pass

class Settings(tk.Toplevel):
    def __init__(self, master=None, clock_label=None, clock_frame=None, *args, **kwargs):
        tk.Toplevel.__init__(self, master=master, *args, **kwargs)
        self.geometry("300x300")
        self.clock_label = clock_label
        self.clock_frame = clock_frame
        self.settings_frame = ttk.Frame(self)
        self.settings_frame.pack(expand=True, fill="both")
        self.settings_frame.pack_propagate(False)

        # Font settings
        font_frame = ttk.LabelFrame(self.settings_frame, text="Font")
        font_frame.pack(padx=10, pady=10)

        current_font = clock_label.cget("font").split()
        current_font_family = current_font[0]
        current_font_size = int(current_font[1])

        self.font_var = tk.StringVar(value=current_font_family)
        font_label = ttk.Label(font_frame, text="Font")
        font_label.pack(side="left", padx=5)
        font_menu = tk.OptionMenu(font_frame, self.font_var, "Arial", "Calibri", "Times New Roman", "System", command=self.update_font)
        font_menu.pack(side="left", padx=5)

        self.size_var = tk.IntVar(value=current_font_size)
        size_label = ttk.Label(font_frame, text="Size")
        size_label.pack(side="left", padx=5)
        size_scale = tk.Scale(font_frame, from_=10, to=150, orient="horizontal", variable=self.size_var, command=self.update_font)
        size_scale.pack(side="left", padx=5)

        self.color_var = tk.StringVar(value="white")
        color_label = ttk.Label(font_frame, text="Color")
        color_label.pack(side="left", padx=5)
        color_menu = tk.OptionMenu(font_frame, self.color_var, "white", "black", "red", "green", "blue", "yellow", command=self.update_font)
        color_menu.pack(side="left", padx=5)

        # Topmost settings
        topmost_frame = ttk.LabelFrame(self.settings_frame, text="Topmost")
        topmost_frame.pack(padx=10, pady=10)

        self.topmost_var = tk.BooleanVar(value=False)
        topmost_checkbutton = ttk.Checkbutton(topmost_frame, text="Topmost", variable=self.topmost_var)
        topmost_checkbutton.pack(side="left", padx=5)

        # Position settings
        position_frame = ttk.LabelFrame(self.settings_frame, text="Position")
        position_frame.pack(padx=10, pady=10)

        self.x_var = tk.StringVar()
        x_label = ttk.Label(position_frame, text="X")
        x_label.pack(side="left", padx=5)
        x_entry = ttk.Entry(position_frame, textvariable=self.x_var, width=5)
        x_entry.pack(side="left", padx=5)

        self.y_var = tk.StringVar()
        y_label = ttk.Label(position_frame, text="Y")
        y_label.pack(side="left", padx=5)
        y_entry = ttk.Entry(position_frame, textvariable=self.y_var, width=5)
        y_entry.pack(side="left", padx=5)

        # Save and cancel buttons
        button_frame = ttk.Frame(self.settings_frame)
        button_frame.pack(pady=10)

        save_button = ttk.Button(button_frame, text="Save", command=self.save_settings)
        save_button.pack(side="left", padx=5)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.destroy_settings)
        cancel_button.pack(side="left", padx=5)

        # Exit button
        exit_button = ttk.Button(button_frame, text="Exit", command=self.destroy)
        exit_button.pack(side="left", padx=5)

        # Read settings from file
        self.read_settings()

    def update_font(self, *args):
        font_family = self.font_var.get()
        if font_family == "System":
            font_family = ""
        font_size = self.size_var.get()
        font_color = self.color_var.get()
        self.clock_label.config(font=(font_family, font_size), fg=font_color)

    def save_settings(self):
        font = self.clock_label.cget("font")
        font_color = self.color_var.get()
        topmost = self.topmost_var.get()
        x = self.x_var.get()
        y = self.y_var.get()
        file_path = "C:/clock/settings.txt"
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        with open(file_path, "w") as f:
            f.write(f"font={font}\nfont_color={font_color}\ntopmost={topmost}\nx={x}\ny={y}")
        if self.topmost_var.get():
            self.attributes("-topmost", 1)
        else:
            self.attributes("-topmost", 0)
        self.clock_frame.wm_geometry(f"+{x}+{y}")  # 更新一级窗口的位置
        messagebox.showinfo("Settings", "Settings saved successfully!")
        self.destroy()

    def destroy_settings(self):
        self.settings_frame.destroy()
        self.destroy()

    def read_settings(self):
        file_path = "C:/clock/settings.txt"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                for line in f:
                    setting, value = line.strip().split("=")
                    if setting == "font":
                        font_family, font_size = value.split()
                        font_size = int(font_size)
                        self.font_var.set(font_family)
                        self.size_var.set(font_size)
                        self.clock_label.config(font=(font_family, font_size))
                    elif setting == "font_color":
                        self.color_var.set(value)
                        self.clock_label.config(fg=value)
                    elif setting == "topmost":
                        self.topmost_var.set(value == "True")
                    elif setting == "x":
                        self.x_var.set(value)
                    elif setting == "y":
                        self.y_var.set(value)

        # Update x and y entries with current position of clock frame
        x, y = self.clock_frame.winfo_x(), self.clock_frame.winfo_y()
        self.x_var.set(str(x))
        self.y_var.set(str(y))
    def update_font(self, *args):
        font_family = self.font_var.get()
        if font_family == "System":
            font_family = ""
        font_size = self.size_var.get()
        font_color = self.color_var.get()
        self.clock_label.config(font=(font_family, font_size), fg=font_color)

    def save_settings(self):
        font = self.clock_label.cget("font")
        font_color = self.color_var.get()
        topmost = self.topmost_var.get()
        file_path = "C:/clock/settings.txt"
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        with open(file_path, "w") as f:
            f.write(f"font={font}\nfont_color={font_color}\ntopmost={topmost}")
        if self.topmost_var.get():
            self.attributes("-topmost", 1)
        else:
            self.attributes("-topmost", 0)
        messagebox.showinfo("Settings", "Settings saved successfully!")
        self.destroy()

    def destroy_settings(self):
        self.settings_frame.destroy()
        self.destroy()

    def read_settings(self):
        file_path = "C:/clock/settings.txt"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                for line in f:
                    setting, value = line.strip().split("=")
                    if setting == "font":
                        font_family, font_size = value.split()
                        font_size = int(font_size)
                        self.font_var.set(font_family)
                        self.size_var.set(font_size)
                        self.clock_label.config(font=(font_family, font_size))
                    elif setting == "font_color":
                        self.color_var.set(value)
                        self.clock_label.config(fg=value)
                    elif setting == "topmost":
                        self.topmost_var.set(value == "True")

if __name__ == "__main__":
    app = Clock()
    app.mainloop()