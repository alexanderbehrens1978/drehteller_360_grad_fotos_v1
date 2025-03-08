#!/usr/bin/env python3
# Datei: app.py
# Hauptanwendungsmodul für die 360° Drehteller Anwendung

import os
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for
from config.settings import Settings
from controllers.arduino_controller import ArduinoController
from controllers.camera_controller import CameraController
from controllers.turntable_controller import TurntableController
from models.project import Project, ProjectManager
from utils.arduino_finder import ArduinoFinder
from utils.camera_finder import CameraFinder
from utils.path_manager import PathManager
from utils.image_processor import ImageProcessor
from utils.background_remover import BackgroundRemover

# Logger konfigurieren
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Flask-App initialisieren
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Pfadmanager initialisieren
path_manager = PathManager()
path_manager.ensure_directories()

# Einstellungen laden
settings = Settings()

# Controller initialisieren
arduino_finder = ArduinoFinder()
camera_finder = CameraFinder()
arduino_controller = None
camera_controller = None
turntable_controller = None

# Projektverwaltung initialisieren
project_manager = ProjectManager(path_manager.projects_dir)

# Bildverarbeitung initialisieren
image_processor = ImageProcessor(path_manager)
background_remover = BackgroundRemover()
