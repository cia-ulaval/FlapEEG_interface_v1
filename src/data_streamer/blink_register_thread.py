import threading
import src.data_set_acquisition.blink_register_app as blink_register_app

class BlinkRegisterThread(threading.Thread):
    
    def __init__(self, output_path, multithread_blink_value):
        threading.Thread.__init__(self, daemon=True)
        self.blink_register_app = blink_register_app.BlinkRegisterApp(output_path, multithread_blink_value)
        
    def run(self):
        self.blink_register_app.start()
        
    def stop(self):
        self.blink_register_app.stop()
        