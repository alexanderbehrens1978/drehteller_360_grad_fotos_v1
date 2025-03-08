Stand vom 08.03.2025

360-drehteller/
├── app.py                  # Hauptanwendung, startet den Webserver
├── config/
│   ├── __init__.py
│   └── settings.py         # Globale Einstellungen und Konfigurationsklasse
├── controllers/
│   ├── __init__.py
│   ├── arduino_controller.py  # Arduino-Steuerungslogik
│   ├── camera_controller.py   # Kamerasteuerung (gphoto2 und Webcam)
│   └── turntable_controller.py # Drehteller-Steuerungslogik
├── models/
│   ├── __init__.py
│   ├── project.py          # Datenmodell für Projekte
│   └── photo_session.py    # Datenmodell für Fotosessions
├── static/
│   ├── css/
│   │   ├── main.css        # Hauptstil
│   │   └── viewer.css      # Stile für den 360°-Viewer
│   ├── js/
│   │   ├── main.js         # Haupt-JavaScript
│   │   ├── settings.js     # Einstellungsseiten-Logik
│   │   ├── project.js      # Projektverwaltungslogik
│   │   └── viewer.js       # 360°-Viewer-Implementierung
│   └── img/
│       └── placeholder.jpg # Platzhalter-Bild
├── templates/
│   ├── base.html           # Basis-Template
│   ├── index.html          # Hauptseite
│   ├── project.html        # Projektverwaltungsseite
│   ├── settings.html       # Einstellungsseite
│   └── viewer.html         # 360°-Viewer-Seite
├── utils/
│   ├── __init__.py
│   ├── arduino_finder.py   # Arduino-Erkennungsutility
│   ├── camera_finder.py    # Kamera-Erkennungsutility
│   ├── image_processor.py  # Bildverarbeitungsutility
│   └── path_manager.py     # Pfad- und Dateimanagement
├── arduino/
│   └── turntable_controller.ino  # Arduino-Sketch
├── requirements.txt        # Python-Abhängigkeiten
└── README.md               # Projektdokumentation
