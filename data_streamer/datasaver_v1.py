import tkinter
import tkinter.filedialog
import tkinter.ttk

DIRECTORY_WHERE_DATA_IS_SAVED = "."


def switch_button_to_record(button: tkinter.Button):
    button.config(text="Record")
    button.config(bg="green")

def switch_button_to_stop(button: tkinter.Button):
    button.config(text="Pause")
    button.config(bg="red")
    
def start_recording(button : tkinter.Button):
    
    button_text = button['text']
    
    if button_text == "Record":
        switch_button_to_stop(button)
    elif button_text == "Pause":
        switch_button_to_record(button)

def select_folder(label : tkinter.Label):
    DIRECTORY_WHERE_DATA_IS_SAVED = tkinter.filedialog.askdirectory()
    label.config(text=DIRECTORY_WHERE_DATA_IS_SAVED)
    

def start_recording_application():
    m = tkinter.Tk()
    m.title("Dataset recording")
    m.geometry("800x600")
    w = tkinter.Label(m, text="EEG recording interface")
    w.pack()
    w.config(font= ("Arial", 20, "bold"))
    

    select_folder_label = tkinter.Label(m, width=50,  text="Select folder label")
    select_folder_label.config(text=DIRECTORY_WHERE_DATA_IS_SAVED, background="grey")
    select_folder_label.pack()
    button_select_folder = tkinter.Button(m, text="Select folder",command=lambda: select_folder(select_folder_label))
    button_select_folder.pack()
    input_filename = tkinter.Entry(m)
    input_filename.pack()
    
    separator = tkinter.ttk.Separator(m, orient="horizontal")
    separator.pack()
    
    button = tkinter.Button(m, text="Record", width=30   ,command=lambda : start_recording(button))
    button.config(bg="green")
    button.pack()
    m.mainloop()