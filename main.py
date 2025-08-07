import logging
from watcher import start_watching

def main():
    logging.basicConfig(
        level   = logging.INFO,
        format  = "[%(asctime)s] %(levelname)s: %(message)s"
    )
    start_watching()

if __name__ == "__main__":
    main()