import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from record_moves import RecorderApp

class FarmGUI:
    def __init__(self, master):
        self.master = master
        master.title("Farming GUI")

        # Variables to store user inputs
        self.image_path = tk.StringVar()
        self.seed_number = tk.IntVar()
        self.grow_time = tk.IntVar()
        self.energy_drink_image_path = tk.StringVar()
        self.energy_drink_number = tk.IntVar()
        self.energy_drink_energy = tk.DoubleVar()

        self.create_widgets()

    def create_widgets(self):
        # Seed group
        seed_frame = tk.LabelFrame(self.master, text="Seed Details")
        seed_frame.grid(row=0, column=0, padx=10, pady=10)

        # Energy drink group
        energy_drink_frame = tk.LabelFrame(self.master, text="Energy Drink Details")
        energy_drink_frame.grid(row=1, column=0, padx=10, pady=10)

        # Seed details
        self.seed_image_label = tk.Label(seed_frame)
        self.seed_image_label.grid(row=0, column=0, rowspan=3)
        tk.Label(seed_frame, text="Select Seed Image:").grid(row=0, column=1)
        tk.Label(seed_frame, text="Seed Number:").grid(row=1, column=1)
        tk.Label(seed_frame, text="Grow Time (minuts):").grid(row=2, column=1)

        # Energy drink details
        self.energy_drink_image_label = tk.Label(energy_drink_frame)
        self.energy_drink_image_label.grid(row=0, column=0, rowspan=3)
        tk.Label(energy_drink_frame, text="Select Energy Drink Image:").grid(row=0, column=1)
        tk.Label(energy_drink_frame, text="Energy Drink Number:").grid(row=1, column=1)
        tk.Label(energy_drink_frame, text="Energy Drink Energy:").grid(row=2, column=1)

        # Entry fields
        self.seed_image_entry = tk.Entry(seed_frame, textvariable=self.image_path, bd=0)
        self.seed_image_entry.grid(row=0, column=2)
        tk.Entry(seed_frame, textvariable=self.seed_number).grid(row=1, column=2)
        tk.Entry(seed_frame, textvariable=self.grow_time).grid(row=2, column=2)
        self.energy_drink_image_entry = tk.Entry(energy_drink_frame, textvariable=self.energy_drink_image_path, bd=0)
        self.energy_drink_image_entry.grid(row=0, column=2)
        tk.Entry(energy_drink_frame, textvariable=self.energy_drink_number).grid(row=1, column=2)
        tk.Entry(energy_drink_frame, textvariable=self.energy_drink_energy).grid(row=2, column=2)

        # Buttons
        tk.Button(seed_frame, text="Select Image", command=self.select_seed_image).grid(row=0, column=3)
        tk.Button(energy_drink_frame, text="Select Image", command=self.select_energy_drink_image).grid(row=0, column=3)

        # Button frame
        button_frame = tk.Frame(self.master)
        button_frame.grid(row=2, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Start Farming", command=self.start_farming).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Open Recorder", command=self.open_old_gui).pack(side=tk.LEFT)

    def select_seed_image(self):
        self.image_path.set(filedialog.askopenfilename())
        if self.image_path.get() != "":
            self.seed_image_entry.config(bd=1)
            image = Image.open(self.image_path.get())
            image = image.resize((50, 50), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            self.seed_image_label.config(image=photo)
            self.seed_image_label.image = photo
        else:
            self.seed_image_entry.config(bd=0)

    def select_energy_drink_image(self):
        self.energy_drink_image_path.set(filedialog.askopenfilename())
        if self.energy_drink_image_path.get() != "":
            self.energy_drink_image_entry.config(bd=1)
            image = Image.open(self.energy_drink_image_path.get())
            image = image.resize((50, 50), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            self.energy_drink_image_label.config(image=photo)
            self.energy_drink_image_label.image = photo
        else:
            self.energy_drink_image_entry.config(bd=0)

    def start_farming(self):
        # Implement farming process based on user inputs
        pass

    def open_old_gui(self):
        # Implement opening the old GUI
        old_root = tk.Toplevel(self.master)
        old_app = RecorderApp(old_root)

def main():
    root = tk.Tk()
    app = FarmGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
