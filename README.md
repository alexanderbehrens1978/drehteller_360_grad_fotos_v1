# 360° Drehteller Fotografie-System

## Projektbeschreibung
Dieses Projekt ist ein komplettes System zur Erstellung interaktiver 360°-Produktansichten mit einem Computer, Arduino und einer Kamera. Der Arduino steuert einen Drehteller über ein Relais, während die Kamera automatisch Fotos aufnimmt. Die Web-Oberfläche ermöglicht die Steuerung, Konfiguration und Anzeige der 360°-Ansichten.

## Voraussetzungen

### Hardware
- Computer mit Linux Mint (oder anderer Linux-Distribution)
- Arduino Uno
- Relais-Modul (für 220V/30W Drehmotor)
- Webcam oder DSLR-Kamera mit USB-Anschluss
- Drehteller mit Schneckengetriebe (0,8° CW Drehgeschwindigkeit, 30W, 220V)

### Software
- Python 3.8 oder höher
- pip (Python-Paketmanager)
- Arduino IDE (für die Programmierung des Arduino)
- git (optional, für Versionskontrolle)

## Installation

### 1. Repository klonen
```bash
git clone https://github.com/username/360-drehteller.git
cd 360-drehteller
```

### 2. Python-Umgebung einrichten
Es wird empfohlen, eine virtuelle Python-Umgebung zu verwenden:

```bash
# Virtuelle Umgebung erstellen
python3 -m venv venv

# Virtuelle Umgebung aktivieren
source venv/bin/activate  # Unter Linux/macOS
# oder
venv\Scripts\activate     # Unter Windows
```

### 3. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### 4. Arduino-Sketch hochladen
1. Öffnen Sie die Arduino IDE
2. Öffnen Sie die Datei `arduino/turntable_controller.ino`
3. Wählen Sie das richtige Board (Arduino Uno) und den richtigen Port
4. Klicken Sie auf "Hochladen"

## Schnellstart

### Anwendung starten
```bash
# Stellen Sie sicher, dass die virtuelle Umgebung aktiviert ist
python app.py
```

Die Webanwendung ist nun unter http://localhost:5000 erreichbar.

### Erste Schritte
1. Öffnen Sie die Einstellungsseite und konfigurieren Sie den Arduino-Port und die Kamera
2. Erstellen Sie ein neues Projekt und legen Sie die gewünschten Winkelschritte fest
3. Starten Sie eine neue Aufnahmesession, um 360°-Aufnahmen zu machen
4. Verwenden Sie den 360°-Viewer, um Ihre Aufnahmen zu betrachten

## Projektstruktur

```
360-drehteller/
├── app.py                  # Hauptanwendung, startet den Webserver
├── config/                 # Konfiguration
│   ├── __init__.py
│   └── settings.py         # Einstellungsmodul
├── controllers/            # Controller für Hardware-Steuerung
│   ├── __init__.py
│   ├── arduino_controller.py
│   ├── camera_controller.py
│   └── turntable_controller.py
├── models/                 # Datenmodelle
│   ├── __init__.py
│   ├── project.py
│   └── photo_session.py
├── static/                 # Statische Dateien (CSS, JS, Bilder)
│   ├── css/
│   ├── js/
│   └── img/
├── templates/              # HTML-Templates
├── utils/                  # Hilfsfunktionen
│   ├── __init__.py
│   ├── arduino_finder.py
│   ├── camera_finder.py
│   ├── image_processor.py
│   └── path_manager.py
├── arduino/                # Arduino-Sketches
│   └── turntable_controller.ino
├── requirements.txt        # Python-Abhängigkeiten
└── README.md               # Diese Datei
```

## Funktionen

### Hauptfunktionen
- Responsive Webanwendung: Funktioniert auf PC, Tablet und Smartphone
- Projektverwaltung: Organisieren verschiedener 360°-Aufnahmen
- Automatische Kamera- und Arduino-Erkennung
- Interaktiver 360°-Viewer: Ähnlich professionellen Produktansichten im E-Commerce
- Exportfunktion für eigenständige HTML-Viewer

### Einstellungsmöglichkeiten
- Kameraauswahl (Webcam oder DSLR via gphoto2)
- Kameraauflösung
- Arduino-Port und Baudrate
- Winkelpräzision (5°, 10°, 15°, etc.)

## Fehlerbehebung

### Arduino wird nicht erkannt
- Überprüfen Sie die Verbindung des Arduino mit dem Computer
- Stellen Sie sicher, dass der richtige Arduino-Sketch hochgeladen wurde
- Prüfen Sie in den Einstellungen, ob der richtige Port ausgewählt ist

### Kamera funktioniert nicht
- Bei Webcams: Überprüfen Sie mit `v4l2-ctl --list-devices`
- Bei DSLR-Kameras: Überprüfen Sie mit `gphoto2 --auto-detect`
- Stellen Sie sicher, dass die Kamera nicht von anderen Anwendungen verwendet wird

### Relais/Motor schaltet nicht
- Überprüfen Sie die Verkabelung zwischen Arduino und Relais
- Stellen Sie sicher, dass der Motor korrekt angeschlossen ist
- Testen Sie das Relais mit dem Arduino-Sketch direkt

## Lizenz
Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die LICENSE-Datei für Details.
