import os
import time
import logging
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from notifier import send_telegram_message
from config import MONITOR_DIR, INACTIVITY_THRESHOLD, CHECK_INTERVAL

WATCH_DIR = os.path.realpath(MONITOR_DIR)

last_created_time = time.time()
has_sent_inactivity_alert = False

class NewDirectoryHandler(FileSystemEventHandler):
    def on_created(self, event):
        global last_created_time, has_sent_inactivity_alert
        if event.is_directory:
            last_created_time = time.time()
            has_sent_inactivity_alert = False

            dir_name  = os.path.basename(event.src_path.rstrip("/"))
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            message   = (
                f"📂 *Nuova cartella*: `{dir_name}`\n"
                f"📁 `{event.src_path}`\n"
                f"🕒 {timestamp}"
            )
            logging.info(f"Detected new dir: {event.src_path}")
            send_telegram_message(message)


def inactivity_checker():
    global last_created_time, has_sent_inactivity_alert
    while True:
        time.sleep(CHECK_INTERVAL)
        elapsed = time.time() - last_created_time
        if elapsed >= INACTIVITY_THRESHOLD and not has_sent_inactivity_alert:
            since = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_created_time))
            message = (
                f"⚠️ *Nessuna nuova cartella* creata da più di 2 giorni.\n"
                f"Ultima creazione: {since}\n"
                f"Controlla lo stato della directory: `{WATCH_DIR}`"
            )
            logging.warning("No new directories for over threshold, sending alert...")
            send_telegram_message(message)
            has_sent_inactivity_alert = True


def start_watching():
    checker_thread = threading.Thread(target=inactivity_checker, daemon=True)
    checker_thread.start()

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