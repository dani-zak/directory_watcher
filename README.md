# Telegram Directory Monitor

Uno script Python che monitora la creazione di nuove cartelle in una directory (anche tramite symlink) e invia notifiche su Telegram. Se non vengono create nuove cartelle per più di 2 giorni, invia un avviso di inattività.

## Struttura del progetto

├── config.py # Parametri di configurazione (token, chat, directory, soglie)
├── notifier.py # Funzione per inviare messaggi Telegram
├── watcher.py # Watchdog + thread di controllo di inattività
└── main.py # Entry-point dell’applicazione


---

## Prerequisiti

- Python 3.7+
- Librerie Python:
  ```bash

  pip install watchdog requests

---

## Installazione e avvio (Linux)

 ```bash
git clone git@github.com:dani-zak/directory_watcher.git
cd directory_watcher
python3 -m venv venv
source venv/bin/activate
pip install watchdog requests
python main.py