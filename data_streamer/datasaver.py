import tkinter
import tkinter.filedialog
import tkinter.ttk
import typing
import threading
import os
from enum import Enum
import data_streamer.streamer as streamer

class Datasaver:
    class STATE(Enum):
        IDLE=1
        STREAMING=2
        
        
    def __init__(self):
        self.DIRECTORY_WHERE_DATA_IS_SAVED = ""
        self.FILE_WHERE_DATA_IS_SAVED = "test.csv"
        self.state : Datasaver.STATE = self.STATE.IDLE
        self.root = tkinter.Tk()
        self.setup_layout()
    
    def log_info(self, message:str):
        print(f"INFO : {message}")
    def log_warning(self, message:str):
        print(f"WARNING : {message}")
    def log_error(self, message:str):
        print(f"ERROR : {message}")
    
    def start_main_loop(self):
        self.root.mainloop()
        
    def start_thread(self):
        self.thread: threading.ThreadError = streamer.StreamerThread(output_path=self.create_full_file_name())
        self.thread.start()
    
    def stop_thread(self):
        self.thread.stop()
        self.thread.join()

    def create_full_file_name(self):
        return os.path.join(self.DIRECTORY_WHERE_DATA_IS_SAVED, 
                            self.FILE_WHERE_DATA_IS_SAVED)

    def setup_layout(self):
        self.root.title("Dataset recording")
        self.root.geometry("800x600")
        w = tkinter.Label(self.root, text="EEG recording interface")
        w.pack()
        w.config(font= ("Arial", 20, "bold"))
        
        def switch_button_to_record(button: tkinter.Button):
            self.state = self.STATE.IDLE
            self.stop_thread()
            button.config(text="Record")
            button.config(bg="green")

        def switch_button_to_stop(button: tkinter.Button):
            self.state = self.STATE.STREAMING
            button.config(text="Pause")
            button.config(bg="red")
            self.start_thread()
            
        def start_recording(button : tkinter.Button):
            button_text = button['text']
            if button_text == "Record":
                switch_button_to_stop(button)
            elif button_text == "Pause":
                switch_button_to_record(button)

        def file_name_modified(*args):
            if input_var.get():
                self.FILE_WHERE_DATA_IS_SAVED = input_var.get()
                self.log_info(f"New file name {self.FILE_WHERE_DATA_IS_SAVED}" )
            else :
                self.log_warning("The name is empty, using previous name {self.FILE_WHERE_DATA_IS_SAVED}")

        def select_folder(label : tkinter.Label):
            self.DIRECTORY_WHERE_DATA_IS_SAVED = tkinter.filedialog.askdirectory()
            self.log_info(f"New folder {self.DIRECTORY_WHERE_DATA_IS_SAVED}" )
            label.config(text=self.DIRECTORY_WHERE_DATA_IS_SAVED)

        select_folder_label = tkinter.Label(self.root, width=50,  text="Select folder label")
        select_folder_label.config(text=self.DIRECTORY_WHERE_DATA_IS_SAVED, background="grey")
        select_folder_label.pack()
        button_select_folder = tkinter.Button(self.root, text="Select folder",command=lambda: select_folder(select_folder_label))
        button_select_folder.pack()
        
        input_var = tkinter.StringVar()
        input_var.trace_add("write", file_name_modified)
        input_filename = tkinter.Entry(self.root, textvariable=input_var)
        input_filename.pack()
        
        
        separator = tkinter.ttk.Separator(self.root, orient="horizontal")
        separator.pack()
        
        button = tkinter.Button(self.root, text="Record", width=30   ,command=lambda : start_recording(button))
        button.config(bg="green")
        button.pack()
    