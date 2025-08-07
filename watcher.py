import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from notifier import send_telegram_message
from config import MONITOR_DIR

WATCH_DIR = os.path.realpath(MONITOR_DIR)

class NewDirectoryHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            dir_name  = os.path.basename(event.src_path.rstrip("/"))
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
    observer.schedule(handler, WATCH_DIR, recursive=False)
    logging.info(f"Started watching directory (link: {MONITOR_DIR}) -> real: {WATCH_DIR}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Stopping observer...")
        observer.stop()
    observer.join()