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

@app.route('/api/project/<project_id>/sessions')
def api_project_sessions(project_id):
    """API-Endpunkt zum Abrufen der Sessions eines Projekts"""
    project = project_manager.get_project(project_id)
    if not project:
        return jsonify({'error': 'Projekt nicht gefunden'}), 404
    
    sessions = [session.to_dict() for session in project.sessions]
    return jsonify(sessions)

@app.route('/api/turntable/move', methods=['POST'])
def api_move_turntable():
    """API-Endpunkt zum Bewegen des Drehtellers"""
    global arduino_controller, turntable_controller
    
    if not arduino_controller:
        arduino_controller = ArduinoController(settings.arduino_port, settings.arduino_baudrate)
    
    if not turntable_controller:
        turntable_controller = TurntableController(arduino_controller, 5)
    
    degrees = int(request.form.get('degrees', 5))
    success = turntable_controller.move_degrees(degrees)
    
    return jsonify({'success': success})

@app.route('/api/camera/capture', methods=['POST'])
def api_capture_photo():
    """API-Endpunkt zum Aufnehmen eines Fotos"""
    global camera_controller
    
    if not camera_controller:
        camera_controller = CameraController(settings.camera_type, settings.camera_device)
    
    project_id = request.form.get('project_id')
    session_id = request.form.get('session_id')
    angle = int(request.form.get('angle', 0))
    
    photo_path = path_manager.get_photo_path(project_id, session_id, angle)
    success = camera_controller.capture_photo(photo_path)
    
    return jsonify({'success': success, 'path': photo_path if success else None})

@app.route('/api/background/remove', methods=['POST'])
def api_remove_background():
    """API-Endpunkt zur Hintergrundentfernung für ein einzelnes Bild"""
    image_path = request.form.get('image_path')
    reference_path = request.form.get('reference_path', None)
    use_ai = request.form.get('use_ai', 'true').lower() == 'true'
    
    if not image_path or not os.path.exists(image_path):
        return jsonify({'error': 'Ungültiger Bildpfad'}), 400
    
    output_path = os.path.splitext(image_path)[0] + '_transparent.png'
    
    if reference_path and os.path.exists(reference_path):
        success = background_remover.remove_background_with_reference(image_path, reference_path, output_path)
    elif use_ai:
        success = background_remover.remove_background_with_ai(image_path, output_path)
    else:
        return jsonify({'error': 'Keine gültige Methode zur Hintergrundentfernung angegeben'}), 400
    
    return jsonify({
        'success': success,
        'image_path': image_path,
        'output_path': output_path if success else None
    })

@app.route('/api/project/<project_id>/session/<session_id>/background/remove', methods=['POST'])
def api_remove_project_backgrounds(project_id, session_id):
    """API-Endpunkt zur Hintergrundentfernung für alle Bilder einer Session"""
    project = project_manager.get_project(project_id)
    if not project:
        return jsonify({'error': 'Projekt nicht gefunden'}), 404
    
    session = project.get_session(session_id)
    if not session:
        return jsonify({'error': 'Session nicht gefunden'}), 404
    
    reference_path = request.form.get('reference_path', None)
    use_ai = request.form.get('use_ai', 'true').lower() == 'true'
    
    result = background_remover.process_project_images(project, session, reference_path, use_ai)
    
    return jsonify(result)
