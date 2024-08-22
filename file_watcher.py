import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class FileHandler(FileSystemEventHandler):
    def __init__(self, script_path):
        self.script_path = script_path

    def on_created(self, event):
        if not event.is_directory:
            print(f"New file detected: {event.src_path}")
            # Run the vocab_report.py script
            subprocess.run(["python", self.script_path])

def monitor_folder(folder_path, script_path):
    event_handler = FileHandler(script_path)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)
    observer.start()
    print(f"Monitoring folder: {folder_path}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    folder_to_watch = "./blogs"  # Path to the blogs folder
    script_to_run = "./vocab_report.py"  # Path to your vocab_report.py script
    monitor_folder(folder_to_watch, script_to_run)
