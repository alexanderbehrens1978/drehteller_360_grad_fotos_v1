drehteller_360_grad_fotos/
├── app/
│   ├── __init__.py               # App-Initialisierung
│   ├── routes/
│   │   ├── __init__.py           # Router-Initialisierung
│   │   ├── main_routes.py        # Hauptrouten (/, /settings)
│   │   ├── api_routes.py         # API-Routen für Konfiguration
│   │   ├── device_routes.py      # Routen für Geräte und Hardware
│   │   ├── photo_routes.py       # Routen für Fotos und Drehungen
│   │   └── diagnostic_routes.py  # Diagnose-Routen
│   ├── services/
│   │   ├── __init__.py           # Service-Initialisierung
│   │   ├── arduino_service.py    # Arduino-Funktionalität
│   │   ├── camera_service.py     # Kamera-Funktionalität
│   │   └── config_manager.py     # Konfigurationsmanager
│   ├── utils/
│   │   ├── __init__.py
│   │   └── device_detector.py    # Geräte-Erkennung
│   └── static/
│       ├── photos/               # Gespeicherte Fotos
│       ├── js/
│       └── css/
├── templates/
│   ├── index.html
│   ├── settings.html
│   └── diagnostics.html
├── config.json                  # Konfigurationsdatei
└── web.py                       # Haupt-Skript (sehr schlank)
