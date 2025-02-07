import tkinter
import tkinter.filedialog
import tkinter.ttk
import typing
import threading

class Datasaver:
    def __init__(self):
        self.DIRECTORY_WHERE_DATA_IS_SAVED = ""
        self.root = tkinter.Tk()
        self.setup_layout()
    
    def set_thread_function(self, callback:callable):
        self.thread = threading.Thread(target=callback, daemon=False)
        
    def start_main_loop(self):
        self.thread.start()
        self.root.mainloop()

    def setup_layout(self):
        self.root.title("Dataset recording")
        self.root.geometry("800x600")
        w = tkinter.Label(self.root, text="EEG recording interface")
        w.pack()
        w.config(font= ("Arial", 20, "bold"))
        
        def switch_button_to_record(button: tkinter.Button):
            button.config(text="Record")
            button.config(bg="green")
            self.resume_thread()

        def switch_button_to_stop(button: tkinter.Button):
            button.config(text="Pause")
            button.config(bg="red")
            self.pause_thread()
            
        def start_recording(button : tkinter.Button):
            button_text = button['text']
            if button_text == "Record":
                switch_button_to_stop(button)
            elif button_text == "Pause":
                switch_button_to_record(button)

        def select_folder(label : tkinter.Label):
            DIRECTORY_WHERE_DATA_IS_SAVED = tkinter.filedialog.askdirectory()
            label.config(text=DIRECTORY_WHERE_DATA_IS_SAVED)

        select_folder_label = tkinter.Label(self.root, width=50,  text="Select folder label")
        select_folder_label.config(text=self.DIRECTORY_WHERE_DATA_IS_SAVED, background="grey")
        select_folder_label.pack()
        button_select_folder = tkinter.Button(self.root, text="Select folder",command=lambda: select_folder(select_folder_label))
        button_select_folder.pack()
        input_filename = tkinter.Entry(self.root)
        input_filename.pack()
        
        separator = tkinter.ttk.Separator(self.root, orient="horizontal")
        separator.pack()
        
        button = tkinter.Button(self.root, text="Record", width=30   ,command=lambda : start_recording(button))
        button.config(bg="green")
        button.pack()
    