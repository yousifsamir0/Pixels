import tkinter as tk
import threading
import pickle
import time
import Recorder 
import Player






        



class RecorderApp:
    def __init__(self, root):
        self.root = root
        self.recorder = Recorder.Recorder()
        self.recording = False
        # self.recorder.start()
        # Start recording button
        self.create_widgets()
    def create_widgets(self):
        # Start recording button
        self.start_btn = tk.Button(self.root, text="Start Recording", command=self.start_recording)
        self.start_btn.grid(row=0, column=0, padx=5, pady=5)

        # Stop recording button
        self.stop_btn = tk.Button(self.root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=5, pady=5)

        # Run or save recording buttons (initially disabled)
        self.run_save_frame = tk.Frame(self.root)
        self.run_save_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        self.run_btn = tk.Button(self.run_save_frame, text="Run Recording", command=self.run_recording, state=tk.DISABLED)
        self.run_btn.pack(side=tk.LEFT, padx=2)
        
        self.run_reverse_btn = tk.Button(self.run_save_frame, text="Run Recording in Reverse", command=self.run_recording_in_reverse, state=tk.DISABLED)
        self.run_reverse_btn.pack(side=tk.LEFT, padx=2)
        
        self.save_btn = tk.Button(self.run_save_frame, text="Save Recording", command=self.save_recording, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=2)
        
        self.load_btn = tk.Button(self.run_save_frame, text="Load Recording", command=self.load_recording)
        self.load_btn.pack(side=tk.LEFT, padx=2)

        # Entry field for file name
        self.file_name_entry = tk.Entry(self.root, width=30)
        self.file_name_entry.grid(row=2, column=0, columnspan=2, padx=5, pady=5)


    def start_recording(self):
        self.recording = True
        self.recorder.clear_records()
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.run_btn.config(state=tk.DISABLED)
        self.run_reverse_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        self.file_name_entry.config(state=tk.DISABLED)
        Player.check_and_activate_window()
        self.recorder.start_recording()


    def stop_recording(self):
        self.recording = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.recorder.stop_recording()
        if not self.recorder.is_empty():
            self.run_btn.config(state=tk.NORMAL)
            self.run_reverse_btn.config(state=tk.NORMAL)
            self.save_btn.config(state=tk.NORMAL)
            self.file_name_entry.config(state=tk.NORMAL)

    # def stop_recording_key(self, event:keyboard.KeyboardEvent):
    #     if self.recording and event.name=='p':
    #         print('[GUI_stopKey]')

    def run_recording(self):
        Player.check_and_activate_window()
        self.recorder.play()
        
        # self.recorder.join()
    def run_recording_in_reverse(self):
        Player.check_and_activate_window()
        self.recorder.play(reverse=True)
        

    def save_recording(self):
        file_name = self.file_name_entry.get()
        if file_name:
            with open(file_name + '.pkl', 'wb') as f:
                pickle.dump(self.recorder.records, f)
            self.recorder.clear_records()
            self.run_btn.config(state=tk.DISABLED)
            self.run_reverse_btn.config(state=tk.DISABLED)
            self.save_btn.config(state=tk.DISABLED)
    def load_recording(self):
        file_name = self.file_name_entry.get()
        if file_name:
            loaded_events = load_events_from_file(file_name + '.pkl')
            if loaded_events:
                self.recorder.records = loaded_events
                self.run_btn.config(state=tk.NORMAL)
                self.run_reverse_btn.config(state=tk.NORMAL)
                self.save_btn.config(state=tk.NORMAL)
                self.start_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.DISABLED)


def load_events_from_file(filename):
    try:
        with open(filename, 'rb') as f:
            events_list = pickle.load(f)
        return events_list
    except FileNotFoundError:
        print("File not found.")
        return []
    


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Keyboard Event Recorder")
    app = RecorderApp(root)
    root.mainloop()


    # keyboard.play(a)
