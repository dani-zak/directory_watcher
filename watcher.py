import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from notifier import send_telegram_message
from config import MONITOR_DIR

class NewDirectoryHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            dir_name  = event.src_path.rstrip("/").split("/")[-1]
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            message   = (
                f"📂 *Nuova cartella*: `{dir_name}`\n"
                f"📁 `{event.src_path}`\n"
                f"🕒 {timestamp}"
            )
            logging.info(f"Detected new dir: {event.src_path}")
            send_telegram_message(message)

def start_watching():
    handler  = NewDirectoryHandler()
    observer = Observer()
    observer.schedule(handler, MONITOR_DIR, recursive=False)
    observer.start()
    logging.info(f"Started watching directory: {MONITOR_DIR}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Stopping observer...")
        observer.stop()
    observer.join()
